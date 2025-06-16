import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.agents.csv_agent import CSVAgent
import streamlit as st
import pandas as pd
import zipfile

# --- Estilo customizado ---
st.set_page_config(page_title="CSV QA App", page_icon="📊", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp {
        background: linear-gradient(120deg, #e0e7ff 0%, #f5f7fa 100%);
    }
    .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2 {background: transparent !important;}
    .stButton>button {
        background-color: #6366f1;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338ca;
        color: #fff;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1.5px solid #6366f1;
        padding: 0.5em;
    }
    .stSelectbox>div>div>div>div {
        border-radius: 8px;
        border: 1.5px solid #6366f1;
    }
    .stMarkdown h2 {
        color: #4338ca;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# 📊 CSV QA App
Pergunte sobre seus arquivos CSV de forma fácil e inteligente!
""")

st.markdown("""
#### Passo 1: Faça upload de um arquivo CSV ou ZIP
""")

uploaded_file = st.file_uploader("Arraste ou selecione um arquivo CSV ou ZIP", type=["csv", "zip"])

if uploaded_file:
    data_folder = "src/data"
    os.makedirs(data_folder, exist_ok=True)
    # Limpa arquivos antigos
    for f in os.listdir(data_folder):
        os.remove(os.path.join(data_folder, f))
    # Salva e descompacta se necessário
    if uploaded_file.name.endswith(".zip"):
        zip_path = os.path.join(data_folder, uploaded_file.name)
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(data_folder)
    else:
        csv_path = os.path.join(data_folder, uploaded_file.name)
        with open(csv_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    agent = CSVAgent(data_folder)
    agent.load_data()
    files = agent.list_files()
    st.markdown("""
    #### Passo 2: Selecione o arquivo CSV para análise
    """)
    selected_file = st.selectbox("Selecione o arquivo CSV", files)
    if selected_file:
        df = agent.dataframes[selected_file]
        st.markdown("**Prévia dos dados:**")
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("""
        #### Passo 3: Faça sua pergunta sobre o arquivo selecionado
        """)
        question = st.text_input("Digite sua pergunta:")
        if question:
            with st.spinner("Pensando..."):
                answer = agent.query_data(selected_file, question)
            st.success("Resposta:")
            st.markdown(f"<div style='background:#fff;border-radius:8px;padding:1em 1.5em;border:1.5px solid #6366f1;font-size:1.1em'>{answer}</div>", unsafe_allow_html=True)