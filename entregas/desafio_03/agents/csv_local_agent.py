
from langchain_ollama import OllamaLLM
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import os
import streamlit as st
import zipfile
import tempfile
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer

class CSVAgent:
    def __init__(self, folder):
        self.folder = folder
        self.dataframes = {}
        self.temp_dirs = []

    def load_data(self):
        for fname in os.listdir(self.folder):
            if fname.endswith(".csv"):
                path = os.path.join(self.folder, fname)
                self.dataframes[fname] = pd.read_csv(path)

    def list_files(self):
        return list(self.dataframes.keys())
    
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
            
    def query_data(self, filename, question, chunk_size=2000, chunk_overlap=200, max_tokens=3500):
        df = self.dataframes.get(filename)
        if df is None:
            return f"Arquivo {filename} não encontrado."
        
        # 1. Converter o DataFrame em uma lista de documentos (ex: cada linha é um documento)
        docs = [
            f"{row.to_dict()}" for _, row in df.iterrows()
        ]
        
        # 2. Chunking inteligente dos dados
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text("\n".join(docs))
        
        # 3. Calcular tokens e limitar contexto
        # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        selected_chunks = []
        total_tokens = 0
        for chunk in chunks:
            chunk_tokens = len(tokenizer.encode(chunk))
            if total_tokens + chunk_tokens > max_tokens:
                break
            selected_chunks.append(chunk)
            total_tokens += chunk_tokens
        
        # 4. Montar prompt com os chunks selecionados
        context = "\n---\n".join(selected_chunks)
        prompt = (
            f"Você é um analista de dados. Use apenas os dados abaixo do arquivo '{filename}' para responder.\n"
            f"DADOS:\n{context}\n\n"
            f"Pergunta do usuário: {question}\n"
            f"Responda sempre em português."
        )
        
        llm = OllamaLLM(model="llama3:8b")
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)
        try:
            return agent.invoke(prompt)
        except Exception as e:
            return f"Erro ao processar a pergunta: {e}"