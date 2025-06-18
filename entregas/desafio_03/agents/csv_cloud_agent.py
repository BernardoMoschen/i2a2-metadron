import pandas as pd
import os
import streamlit as st
from openai import OpenAI
import zipfile
import tempfile
import shutil
import re
import numpy as np

class CSVAgent:
    def __init__(self, folder):
        self.folder = folder
        self.dataframes = {}
        self.temp_dirs = []
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{st.secrets['API_KEY']}",
        )

    def load_data(self):
        for file in os.listdir(self.folder):
            if file.endswith(".csv"):
                path = os.path.join(self.folder, file)
                df = pd.read_csv(path)
                self.dataframes[file] = df

    def list_files(self):
        return list(self.dataframes.keys())

    def _extract_search_terms(self, question):
        """Extrai termos de busca e valores específicos da pergunta"""
        search_info = {
            'values': [],
            'keywords': [],
            'operators': [],
            'columns_mentioned': []
        }
        
        # Extrair números/valores específicos
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', question)
        search_info['values'] = [float(n) if '.' in n else int(n) for n in numbers]
        
        # Extrair operadores de comparação
        operators = re.findall(r'(maior|menor|igual|acima|abaixo|>|<|=|>=|<=)', question.lower())
        search_info['operators'] = operators
        
        # Palavras-chave comuns
        keywords = re.findall(r'\b(nota|valor|preço|quantidade|total|soma|média|máximo|mínimo|vendas|receita)\b', question.lower())
        search_info['keywords'] = list(set(keywords))
        
        return search_info

    def _find_relevant_columns(self, df, search_info):
        """Encontra colunas relevantes baseadas nos termos de busca"""
        relevant_cols = []
        
        # Buscar por palavras-chave nos nomes das colunas
        for keyword in search_info['keywords']:
            for col in df.columns:
                if keyword in col.lower():
                    relevant_cols.append(col)
        
        # Se há valores numéricos na pergunta, buscar colunas que contenham esses valores
        if search_info['values']:
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    for value in search_info['values']:
                        if value in df[col].values:
                            relevant_cols.append(col)
                            break
        
        # Se não encontrou colunas específicas, incluir todas as numéricas
        if not relevant_cols:
            relevant_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        
        # Sempre incluir a primeira coluna (geralmente ID ou chave)
        if len(df.columns) > 0 and df.columns[0] not in relevant_cols:
            relevant_cols.insert(0, df.columns[0])
        
        return list(set(relevant_cols))

    def _create_smart_sample(self, df, search_info, max_rows=50):
        """Cria uma amostra inteligente baseada na pergunta"""
        relevant_cols = self._find_relevant_columns(df, search_info)
        
        # Filtrar apenas colunas relevantes
        sample_df = df[relevant_cols].copy()
        
        # Se há valores específicos mencionados, priorizar linhas que os contenham
        if search_info['values']:
            relevant_rows = pd.DataFrame()
            
            for value in search_info['values']:
                for col in relevant_cols:
                    if df[col].dtype in ['int64', 'float64']:
                        # Busca exata
                        exact_matches = df[df[col] == value]
                        if not exact_matches.empty:
                            relevant_rows = pd.concat([relevant_rows, exact_matches])
                        
                        # Busca por proximidade (±10% do valor)
                        tolerance = abs(value * 0.1)
                        close_matches = df[abs(df[col] - value) <= tolerance]
                        if not close_matches.empty:
                            relevant_rows = pd.concat([relevant_rows, close_matches.head(10)])
            
            # Remover duplicatas
            if not relevant_rows.empty:
                relevant_rows = relevant_rows.drop_duplicates()
                
                # Se encontrou muitas linhas relevantes, pegar uma amostra
                if len(relevant_rows) > max_rows:
                    relevant_rows = relevant_rows.head(max_rows)
                
                sample_df = relevant_rows[relevant_cols]
            else:
                # Se não encontrou correspondências exatas, pegar uma amostra geral
                sample_df = sample_df.head(max_rows)
        else:
            # Se não há valores específicos, pegar amostra geral
            sample_df = sample_df.head(max_rows)
        
        return sample_df

    def query_data(self, filename, question):
        df = self.dataframes[filename]
        
        # Analisar a pergunta para criar amostra inteligente
        search_info = self._extract_search_terms(question)
        
        # Criar amostra baseada na pergunta
        sample_df = self._create_smart_sample(df, search_info)
        
        # Converter para CSV
        sample_csv = sample_df.to_csv(index=False)
        
        # Informações sobre a amostra
        sample_info = f"(Amostra inteligente: {len(sample_df)} linhas de {len(df)}, {len(sample_df.columns)} colunas de {len(df.columns)})"
        
        # Informações sobre a busca (para debug)
        search_details = f"Termos encontrados: valores={search_info['values']}, palavras-chave={search_info['keywords']}"
        
        prompt = (
            f"You are a data analyst. Given this CSV data sample from file '{filename}' {sample_info}:\n\n"
            f"Search context: {search_details}\n\n"
            f"{sample_csv}\n\n"
            f"User question: {question}\n\n"
            f"Answer based on this intelligently selected sample. "
            f"If the answer requires data not present in this sample, mention that limitation. "
            f"Answer always in portuguese, unless asked not to."
        )
        
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Adicionar informações de debug se necessário
            response = completion.choices[0].message.content
            
            if st.session_state.get('debug_mode', False):
                response += f"\n\n**Debug Info:**\n- Amostra: {len(sample_df)} linhas\n- Colunas relevantes: {list(sample_df.columns)}\n- Termos de busca: {search_info}"
            
            return response
            
        except Exception as e:
            return f"Erro ao consultar o modelo: {e}"

    def get_file_summary(self, filename):
        """Retorna um resumo do arquivo"""
        if filename not in self.dataframes:
            return "Arquivo não encontrado"
        
        df = self.dataframes[filename]
        summary = {
            'nome': filename,
            'linhas': len(df),
            'colunas': len(df.columns),
            'colunas_list': list(df.columns),
            'tipos': dict(df.dtypes.astype(str)),
            'tamanho_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
        }
        return summary

    # ... resto dos métodos permanecem iguais ...
    def extract_zip_files(self, zip_path):
        """Extrai arquivos CSV de um ZIP"""
        extracted_files = []
        
        try:
            # Criar diretório temporário
            temp_dir = tempfile.mkdtemp()
            self.temp_dirs.append(temp_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Listar arquivos no ZIP
                zip_files = zip_ref.namelist()
                csv_files = [f for f in zip_files if f.endswith('.csv')]
                
                if not csv_files:
                    st.warning("Nenhum arquivo CSV encontrado no ZIP.")
                    return extracted_files
                
                # Extrair apenas os CSVs
                for csv_file in csv_files:
                    # Extrair para o diretório temporário
                    zip_ref.extract(csv_file, temp_dir)
                    
                    # Caminho completo do arquivo extraído
                    extracted_path = os.path.join(temp_dir, csv_file)
                    
                    # Copiar para a pasta de dados principal
                    filename = os.path.basename(csv_file)
                    destination = os.path.join(self.folder, filename)
                    shutil.copy2(extracted_path, destination)
                    
                    extracted_files.append(filename)
                    st.success(f"✅ Extraído: {filename}")
                
        except zipfile.BadZipFile:
            st.error("Arquivo ZIP corrompido ou inválido.")
        except Exception as e:
            st.error(f"Erro ao extrair ZIP: {e}")
        
        return extracted_files

    def process_uploaded_file(self, uploaded_file):
        """Processa arquivo enviado via Streamlit"""
        file_path = os.path.join(self.folder, uploaded_file.name)
        
        # Salvar arquivo na pasta
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if uploaded_file.name.endswith(".zip"):
            st.info(f"📦 Processando ZIP enviado: {uploaded_file.name}")
            extracted_files = self.extract_zip_files(file_path)
            
            # Carregar os CSVs extraídos
            for csv_file in extracted_files:
                csv_path = os.path.join(self.folder, csv_file)
                try:
                    df = pd.read_csv(csv_path)
                    self.dataframes[csv_file] = df
                except Exception as e:
                    st.error(f"Erro ao carregar CSV extraído {csv_file}: {e}")
            
            return extracted_files
            
        elif uploaded_file.name.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                self.dataframes[uploaded_file.name] = df
                st.success(f"✅ CSV carregado: {uploaded_file.name}")
                return [uploaded_file.name]
            except Exception as e:
                st.error(f"Erro ao carregar CSV: {e}")
                return []
        else:
            st.warning("Tipo de arquivo não suportado. Use CSV ou ZIP.")
            return []

    def cleanup(self):
        """Limpa diretórios temporários"""
        for temp_dir in self.temp_dirs:
            try:
                shutil.rmtree(temp_dir)
            except:
                pass