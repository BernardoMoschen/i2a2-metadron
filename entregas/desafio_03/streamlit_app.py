import os
from agents.csv_cloud_agent import CSVAgent
import streamlit as st
import pandas as pd

# --- Configuração da página ---
st.set_page_config(
    page_title="CSV Agent - Metadron", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS customizado ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    .file-card {
        background: #353739;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .answer-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .step-header {
        background: #353739;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Header principal ---
st.markdown("""
<div class="main-header">
    <h1>🤖 CSV Agent - Metadron</h1>
    <p>Análise inteligente de dados CSV com IA</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar com informações ---
with st.sidebar:
    st.markdown("### 📋 Informações do Projeto")
    st.info("""
    **Desafio 03 - I2A2**
    
    Agente inteligente para análise de arquivos CSV usando:
    - 🧠 **Modelo**: meta-llama/llama-3-8b-instruct
    - 🔧 **Framework**: Streamlit
    - 📊 **Dados**: CSV e ZIP
    """)
    
    st.markdown("### 🔗 Links Úteis")
    st.markdown("[📂 Repositório GitHub](https://github.com/BernardoMoschen/i2a2-metadron/tree/main/entregas/desafio_03)")
    
    st.markdown("### 💡 Exemplos de Perguntas")
    st.markdown("""
    - "Quais são as colunas do arquivo?"
    - "Qual o maior valor na coluna X?"
    - "Quantas linhas tem o dataset?"
    - "Mostre um resumo dos dados"
    - "Quais são os valores únicos na coluna Y?"
    """)

# --- Badges ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Curso", "I2A2", help="Agentes Autônomos com Redes Generativas")
with col2:
    st.metric("Grupo", "Metadron", help="Equipe desenvolvedora")
with col3:
    st.metric("Modelo", "Llama-3-8B", help="Meta Llama 3 8B Instruct")
with col4:
    st.metric("Formato", "CSV/ZIP", help="Formatos suportados")

# --- Seção de Upload ---
st.markdown('<div class="step-header"><h3>📁 Passo 1: Envie seus dados</h3></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Arraste ou clique para selecionar um arquivo", 
    type=["csv", "zip"], 
    help="Formatos aceitos: .csv (individual) ou .zip (contendo múltiplos CSVs)"
)

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
    with st.spinner("🔄 Processando arquivo..."):
        processed_files = agent.process_uploaded_file(uploaded_file)
    
    if processed_files:
        st.markdown('<div class="step-header"><h3>✅ Arquivos Processados</h3></div>', unsafe_allow_html=True)
        
        for file in processed_files:
            st.markdown(f"""
            <div class="file-card">
                📄 <strong>{file}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Carregar dados existentes
    agent.load_data()
    files = agent.list_files()
    
    if files:
        # --- Seção de Seleção de Arquivo ---
        st.markdown('<div class="step-header"><h3>🎯 Passo 2: Selecione o arquivo para análise</h3></div>', unsafe_allow_html=True)
        
        selected_file = st.selectbox(
            "Escolha o arquivo CSV",
            files,
            help="Selecione qual arquivo deseja analisar"
        )
        
        if selected_file:
            df = agent.dataframes[selected_file]
            
            # Informações do arquivo
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Linhas", f"{len(df):,}")
            with col2:
                st.metric("📈 Colunas", len(df.columns))
            with col3:
                st.metric("💾 Tamanho", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            with col4:
                st.metric("🗂️ Arquivo", selected_file.split('.')[0])
            
            # Prévia dos dados
            st.markdown("### 👀 Prévia dos dados")
            
            # Tabs para diferentes visualizações
            tab1, tab2, tab3 = st.tabs(["📋 Dados", "📊 Informações", "🔢 Estatísticas"])
            
            with tab1:
                st.dataframe(df.head(10), use_container_width=True)
            
            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Colunas:**")
                    for col in df.columns:
                        st.write(f"• {col}")
                with col2:
                    st.markdown("**Tipos de dados:**")
                    for col, dtype in df.dtypes.items():
                        st.write(f"• {col}: {dtype}")
            
            with tab3:
                numeric_columns = df.select_dtypes(include=['number']).columns
                if len(numeric_columns) > 0:
                    st.dataframe(df[numeric_columns].describe(), use_container_width=True)
                else:
                    st.info("Nenhuma coluna numérica encontrada para estatísticas")
            
            # --- Seção de Perguntas ---
            st.markdown('<div class="step-header"><h3>💬 Passo 3: Faça sua pergunta</h3></div>', unsafe_allow_html=True)
            
            # Sugestões de perguntas
            st.markdown("**💡 Sugestões de perguntas:**")
            suggestion_cols = st.columns(3)
            
            with suggestion_cols[0]:
                if st.button("🔍 Quais são as colunas?"):
                    st.session_state.suggested_question = "Quais são as colunas deste arquivo?"
            with suggestion_cols[1]:
                if st.button("📊 Resumo dos dados"):
                    st.session_state.suggested_question = "Faça um resumo completo deste dataset"
            with suggestion_cols[2]:
                if st.button("📈 Estatísticas básicas"):
                    st.session_state.suggested_question = "Mostre as principais estatísticas dos dados numéricos"
            
            # Campo de pergunta
            question = st.text_area(
                "Digite sua pergunta:",
                value=st.session_state.get('suggested_question', ''),
                height=100,
                placeholder="Ex: Qual o maior valor na coluna 'vendas'? Quantas linhas tem o dataset?"
            )
            
            # Botão de análise
            if st.button("🚀 Analisar", type="primary", use_container_width=True):
                if question:
                    with st.spinner("🤖 IA analisando seus dados..."):
                        answer = agent.query_data(selected_file, question)
                    
                    st.markdown("### 🎯 Resposta da IA")
                    st.markdown(f"""
                    <div class="answer-box">
                        {answer}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Limpar sugestão após uso
                    if 'suggested_question' in st.session_state:
                        del st.session_state.suggested_question
                else:
                    st.warning("⚠️ Por favor, digite uma pergunta antes de analisar!")

else:
    # Tela inicial quando não há arquivo
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h2>🎯 Como começar?</h2>
        <p style='font-size: 1.2em; color: #666;'>
            1. 📁 Faça upload de um arquivo CSV ou ZIP<br>
            2. 🎯 Selecione o arquivo para análise<br>
            3. 💬 Faça perguntas sobre seus dados<br>
            4. 🤖 Receba insights da IA
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🧹 Limpar Cache", help="Remove arquivos temporários"):
        if 'agent' in locals():
            agent.cleanup()
        st.rerun()

with col2:
    if st.button("🔄 Recarregar Página"):
        st.rerun()

with col3:
    st.markdown("""
    <div style='text-align: right; color: #666; font-size: 0.9em;'>
        Powered by Metadron Team 🚀
    </div>
    """, unsafe_allow_html=True)