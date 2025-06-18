import pandas as pd
import os
import streamlit as st
from openai import OpenAI
import zipfile
import tempfile
import shutil

class CSVAgent:
    def __init__(self, folder):
        self.folder = folder
        self.dataframes = {}
        self.temp_dirs = []  # Para limpar diretórios temporários depois
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

    def query_data(self, filename, question):
        df = self.dataframes[filename]
        
        # Usar o dataset COMPLETO - SEM qualquer amostragem
        sample = df.to_csv(index=False)
        sample_info = f"(Dataset completo: {len(df)} linhas, {len(df.columns)} colunas)"
        
        prompt = (
            f"You are a data analyst. Given this CSV data from file '{filename}' {sample_info}:\n\n"
            f"{sample}\n\n"
            f"User question: {question}\n\n"
            f"Answer as clearly and accurately as possible. "
            f"You have access to the complete dataset for accurate analysis. "
            # f"Answer always in portuguese, unless asked not to."
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
            return completion.choices[0].message.content
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
