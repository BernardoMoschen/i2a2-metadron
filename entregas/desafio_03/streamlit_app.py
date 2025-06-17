import os
from agents.csv_cloud_agent import CSVAgent
import streamlit as st
import pandas as pd



# --- Estilo customizado ---
st.set_page_config(page_title="CSV Agent- Metadron", page_icon="📊", layout="centered")
st.title(f"CSV Agent- Metadron - Desafio 03")
col1, col2, col3  = st.columns(3)

with col1:st.badge("I2A2", color='red')
with col3: st.badge("Chatbot", color='orange')
with col2: st.badge("llama-3-8b")

st.divider()

st.write(
    "Agente do grupo Metadron para análise de arquivos CSV."
    "\n"
    "Usa o modelo `llama3:8b` para responder perguntas sobre os dados contidos em arquivos CSV."
    "Para mais informações sobre o projeto consulte o [repositório](https://github.com/BernardoMoschen/i2a2-metadron/tree/main/entregas/desafio_03)."
)

st.divider()


uploaded_file = st.file_uploader("Arraste ou selecione um arquivo CSV ou ZIP", type=["csv", "zip"], help="Formatos aceitos: .csv (individual) ou .zip (contendo vários CSVs)")

if uploaded_file:
    data_folder = "./data"
    os.makedirs(data_folder, exist_ok=True)
    
    # Limpa arquivos antigos
    for f in os.listdir(data_folder):
        file_path = os.path.join(data_folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Inicializar agente
    agent = CSVAgent(data_folder)
    
    # Processar arquivo enviado
    with st.spinner("Processando arquivo..."):
        processed_files = agent.process_uploaded_file(uploaded_file)
    
    if processed_files:
        st.success(f"Processados {len(processed_files)} arquivo(s)!")
        for file in processed_files:
            st.write(f"📄 {file}")
    
    # Carregar dados existentes
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
            st.markdown(f"<div style='background:transparent;border-radius:8px;padding:1em 1.5em;border:1.5px solid #6366f1;font-size:1.1em'>{answer}</div>", unsafe_allow_html=True)

# Botão de limpeza (opcional)
if st.button("🧹 Limpar cache e arquivos temporários"):
    if 'agent' in locals():
        agent.cleanup()
    st.rerun()