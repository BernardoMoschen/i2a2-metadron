import os
from agents.csv_cloud_agent import CSVAgent
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da página ---
st.set_page_config(
    page_title="CSV Agent Pro - Metadron", 
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
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        color: #ecf0f1;
    }
    .file-card {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        border: 1px solid #4a5f7a;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-left: 4px solid #28a745;
        transition: transform 0.2s;
        color: #ecf0f1;
    }
    .file-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .answer-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .step-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        color: #ecf0f1;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        margin: 1rem 0;
        color: #ecf0f1;
    }
    .stat-box {
        background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #4a5f7a;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        color: #ecf0f1;
    }
    /* Customização do Streamlit para dark mode */
    .stApp {
        background-color: #1e2936;
    }
    .stSidebar {
        background-color: #2c3e50;
    }
    .stMarkdown, .stText {
        color: #ecf0f1 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header principal ---
st.markdown("""
<div class="main-header">
    <h1>🤖 CSV Agent Pro - Metadron</h1>
    <p style="font-size: 1.2em;">Análise inteligente e visualização de dados CSV com IA</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎯 Dashboard de Controle")
    
    # Status do sistema
    st.markdown("#### 🟢 Status do Sistema")
    st.success("✅ Sistema Online")
    st.info("🔗 API Conectada")
    st.info("🧠 Modelo: Llama-3-8B")
    
    st.markdown("---")
    
    st.markdown("### 📊 Estatísticas da Sessão")
    if 'questions_asked' not in st.session_state:
        st.session_state.questions_asked = 0
    if 'files_processed' not in st.session_state:
        st.session_state.files_processed = 0
    
    st.metric("Perguntas Feitas", st.session_state.questions_asked)
    st.metric("Arquivos Processados", st.session_state.files_processed)
    
    st.markdown("---")
    
    st.markdown("### 💡 Dicas Avançadas")
    with st.expander("🔍 Perguntas Básicas"):
        st.markdown("""
        - "Quantas linhas e colunas tem?"
        - "Quais são os tipos de dados?"
        - "Mostre as primeiras linhas"
        - "Há valores nulos?"
        """)
    
    with st.expander("📊 Análises Estatísticas"):
        st.markdown("""
        - "Calcule a média da coluna X"
        - "Qual o valor máximo em Y?"
        - "Mostre a distribuição dos dados"
        - "Encontre outliers"
        """)
    
    with st.expander("🔗 Análise Comparativa"):
        st.markdown("""
        - "Compare arquivos A e B"
        - "Qual arquivo tem mais dados?"
        - "Encontre diferenças entre datasets"
        """)
    
    st.markdown("---")
    
    # Links úteis
    st.markdown("### 🔗 Links Úteis")
    st.markdown("[📂 GitHub](https://github.com/BernardoMoschen/i2a2-metadron)")
    st.markdown("[📚 Documentação](https://github.com/BernardoMoschen/i2a2-metadron/tree/main/entregas/desafio_03)")
    
    st.markdown("---")
    
    # Controles avançados
    st.markdown("### ⚙️ Configurações")
    sample_size = st.slider("Tamanho da Amostra", 10, 100, 50, help="Número de linhas enviadas para a IA")
    show_debug = st.checkbox("Modo Debug", help="Mostra informações técnicas")

# --- Métricas principais ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="stat-box">
        <h3 style="margin:0; color:#667eea;">🎓</h3>
        <p style="margin:0; font-weight:bold;">Curso</p>
        <p style="margin:0;">I2A2</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h3 style="margin:0; color:#28a745;">🚀</h3>
        <p style="margin:0; font-weight:bold;">Equipe</p>
        <p style="margin:0;">Metadron</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h3 style="margin:0; color:#dc3545;">🧠</h3>
        <p style="margin:0; font-weight:bold;">Modelo</p>
        <p style="margin:0;">Llama-3-8B</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <h3 style="margin:0; color:#ffc107;">📁</h3>
        <p style="margin:0; font-weight:bold;">Formato</p>
        <p style="margin:0;">CSV/ZIP</p>
    </div>
    """, unsafe_allow_html=True)

# --- Seção de Upload ---
st.markdown('<div class="step-header"><h3>📁 Passo 1: Envie seus dados</h3></div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Arraste ou clique para selecionar arquivos", 
    type=["csv", "zip"], 
    help="Formatos aceitos: .csv (individual) ou .zip (contendo múltiplos CSVs)",
    accept_multiple_files=True
)

if uploaded_files:
    data_folder = "./data"
    os.makedirs(data_folder, exist_ok=True)
    
    # Limpa arquivos antigos
    for f in os.listdir(data_folder):
        file_path = os.path.join(data_folder, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # Inicializar agente
    agent = CSVAgent(data_folder)
    
    all_processed_files = []
    
    # Processar cada arquivo enviado
    progress_bar = st.progress(0)
    for i, uploaded_file in enumerate(uploaded_files):
        with st.spinner(f"🔄 Processando {uploaded_file.name}..."):
            processed_files = agent.process_uploaded_file(uploaded_file)
            all_processed_files.extend(processed_files)
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    st.session_state.files_processed = len(all_processed_files)
    
    if all_processed_files:
        st.markdown('<div class="step-header"><h3>✅ Arquivos Processados</h3></div>', unsafe_allow_html=True)
        
        # Mostrar arquivos em grid
        cols = st.columns(min(3, len(all_processed_files)))
        for i, file in enumerate(all_processed_files):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="file-card">
                    <h4 style="margin:0; color:#28a745;">📄 {file}</h4>
                    <p style="margin:0.5rem 0 0 0; color:#bdc3c7; font-size:0.9em;">
                        Pronto para análise
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    # Carregar dados existentes
    agent.load_data()
    files = agent.list_files()
    
    if files:
        # --- Seção de Seleção de Arquivo ---
        st.markdown('<div class="step-header"><h3>🎯 Passo 2: Análise de dados</h3></div>', unsafe_allow_html=True)
        
        # Seleção de modo de análise
        analysis_mode = st.radio(
            "Escolha o modo de análise:",
            ["📊 Arquivo Individual", "🔗 Múltiplos Arquivos", "📈 Dashboard Geral"],
            horizontal=True
        )
        
        if analysis_mode == "📊 Arquivo Individual":
            selected_file = st.selectbox(
                "Escolha o arquivo CSV",
                files,
                help="Selecione qual arquivo deseja analisar"
            )
            
            if selected_file:
                df = agent.dataframes[selected_file]
                
                # Dashboard do arquivo
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Linhas", f"{len(df):,}")
                with col2:
                    st.metric("📈 Colunas", len(df.columns))
                with col3:
                    st.metric("💾 Tamanho", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                with col4:
                    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                    st.metric("❌ Dados Ausentes", f"{missing_pct:.1f}%")
                
                # Visualizações
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Dados", "📊 Informações", "🔢 Estatísticas", "📈 Gráficos"])
                
                with tab1:
                    st.dataframe(df.head(sample_size), use_container_width=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📋 Colunas:**")
                        for col in df.columns:
                            st.write(f"• **{col}** ({df[col].dtype})")
                    with col2:
                        st.markdown("**🔍 Informações Gerais:**")
                        st.write(f"• Forma: {df.shape}")
                        st.write(f"• Memória: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
                        st.write(f"• Valores únicos totais: {df.nunique().sum()}")
                
                with tab3:
                    numeric_columns = df.select_dtypes(include=['number']).columns
                    if len(numeric_columns) > 0:
                        st.dataframe(df[numeric_columns].describe(), use_container_width=True)
                        
                        # Matriz de correlação
                        if len(numeric_columns) > 1:
                            st.markdown("**🔗 Matriz de Correlação**")
                            corr_matrix = df[numeric_columns].corr()
                            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Nenhuma coluna numérica encontrada para estatísticas")
                
                with tab4:
                    if len(numeric_columns) > 0:
                        # Seletor de coluna para gráfico
                        selected_column = st.selectbox("Escolha uma coluna numérica:", numeric_columns)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            # Histograma
                            fig = px.histogram(df, x=selected_column, title=f"Distribuição de {selected_column}")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Box plot
                            fig = px.box(df, y=selected_column, title=f"Box Plot de {selected_column}")
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Nenhuma coluna numérica disponível para gráficos")
        
        elif analysis_mode == "🔗 Múltiplos Arquivos":
            selected_files = st.multiselect(
                "Escolha os arquivos para comparação:",
                files,
                help="Selecione múltiplos arquivos para análise comparativa"
            )
            
            if len(selected_files) >= 2:
                # Comparação básica
                comparison_data = []
                for file in selected_files:
                    df = agent.dataframes[file]
                    comparison_data.append({
                        'Arquivo': file,
                        'Linhas': len(df),
                        'Colunas': len(df.columns),
                        'Tamanho (KB)': df.memory_usage(deep=True).sum() / 1024
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
                
                # Gráfico de comparação
                fig = px.bar(comparison_df, x='Arquivo', y='Linhas', title="Comparação de Número de Linhas")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Selecione pelo menos 2 arquivos para comparação")
        
        else:  # Dashboard Geral
            # Estatísticas gerais
            total_rows = sum(len(agent.dataframes[f]) for f in files)
            total_columns = sum(len(agent.dataframes[f].columns) for f in files)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📁 Total de Arquivos", len(files))
            with col2:
                st.metric("📊 Total de Linhas", f"{total_rows:,}")
            with col3:
                st.metric("📈 Total de Colunas", total_columns)
            
            # Gráfico geral
            files_data = []
            for file in files:
                df = agent.dataframes[file]
                files_data.append({
                    'Arquivo': file,
                    'Linhas': len(df),
                    'Colunas': len(df.columns)
                })
            
            if files_data:
                files_df = pd.DataFrame(files_data)
                fig = px.scatter(files_df, x='Colunas', y='Linhas', text='Arquivo',
                               title="Visão Geral dos Arquivos")
                fig.update_traces(textposition="top center")
                st.plotly_chart(fig, use_container_width=True)
        
        # --- Seção de Perguntas ---
        st.markdown('<div class="step-header"><h3>💬 Passo 3: Faça sua pergunta</h3></div>', unsafe_allow_html=True)
        
        # Perguntas sugeridas mais avançadas
        st.markdown("**💡 Sugestões de perguntas avançadas:**")
        suggestion_cols = st.columns(4)
        
        suggestions = [
            ("🔍 Estrutura", "Descreva a estrutura detalhada deste dataset"),
            ("📊 Resumo", "Faça um resumo executivo dos dados"),
            ("🧮 Estatísticas", "Calcule estatísticas descritivas completas"),
            ("🔎 Qualidade", "Analise a qualidade dos dados e identifique problemas")
        ]
        
        for i, (icon, text) in enumerate(suggestions):
            with suggestion_cols[i]:
                if st.button(f"{icon}", help=text):
                    st.session_state.suggested_question = text
        
        # Campo de pergunta melhorado
        question = st.text_area(
            "💭 Digite sua pergunta ou análise desejada:",
            value=st.session_state.get('suggested_question', ''),
            height=120,
            placeholder="Ex: Compare as vendas entre janeiro e fevereiro... Quais são os principais insights dos dados?",
            help="Seja específico! A IA pode fazer análises complexas e comparações."
        )
        
        # Botões de ação
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            analyze_button = st.button("🚀 Analisar com IA", type="primary", use_container_width=True)
        
        with col2:
            if st.button("🔄 Limpar", use_container_width=True):
                if 'suggested_question' in st.session_state:
                    del st.session_state.suggested_question
                st.rerun()
        
        with col3:
            if analysis_mode == "📊 Arquivo Individual" and 'selected_file' in locals():
                export_data = agent.dataframes[selected_file].head(100).to_csv()
                st.download_button(
                    "📥 Export",
                    export_data,
                    f"{selected_file}_sample.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        # Análise da pergunta
        if analyze_button and question:
            if analysis_mode == "📊 Arquivo Individual" and 'selected_file' in locals():
                with st.spinner("🤖 IA analisando seus dados... Isso pode levar alguns segundos."):
                    answer = agent.query_data(selected_file, question)
                
                st.session_state.questions_asked += 1
                
                st.markdown("### 🎯 Resposta da IA")
                st.markdown(f"""
                <div class="answer-box">
                    <h4 style="margin-top:0; color:white;">📋 Análise Completa:</h4>
                    {answer}
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar informações de debug se habilitado
                if show_debug:
                    with st.expander("🔧 Informações de Debug"):
                        st.write(f"**Arquivo analisado:** {selected_file}")
                        st.write(f"**Linhas no sample:** {sample_size}")
                        st.write(f"**Tamanho total do dataset:** {len(agent.dataframes[selected_file])}")
                
                # Limpar sugestão após uso
                if 'suggested_question' in st.session_state:
                    del st.session_state.suggested_question
            
            elif analysis_mode == "🔗 Múltiplos Arquivos" and 'selected_files' in locals() and len(selected_files) > 0:
                st.info("🔄 Análise de múltiplos arquivos em desenvolvimento!")
            
            else:
                st.warning("⚠️ Selecione um arquivo ou modo de análise válido!")
        
        elif analyze_button:
            st.warning("⚠️ Por favor, digite uma pergunta antes de analisar!")

else:
    # Tela inicial aprimorada
    st.markdown("""
    <div class="upload-area">
        <h2 style="color:#667eea; margin-bottom:1rem;">🎯 Bem-vindo ao CSV Agent Pro!</h2>
        <p style='font-size: 1.2em; color: #ecf0f1; margin-bottom:2rem;'>
            Análise inteligente de dados com IA de última geração
        </p>
        <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
            <div style="text-align: center;">
                <h3 style="color:#28a745;">📁</h3>
                <p style="color:#bdc3c7;"><strong>Upload</strong><br>CSV ou ZIP</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color:#667eea;">🎯</h3>
                <p style="color:#bdc3c7;"><strong>Selecione</strong><br>Arquivos</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color:#dc3545;">💬</h3>
                <p style="color:#bdc3c7;"><strong>Pergunte</strong><br>à IA</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color:#ffc107;">🚀</h3>
                <p style="color:#bdc3c7;"><strong>Obtenha</strong><br>Insights</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Footer aprimorado ---
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🧹 Limpar Cache", help="Remove arquivos temporários"):
        if 'agent' in locals():
            agent.cleanup()
        # Reset session state
        for key in ['questions_asked', 'files_processed', 'suggested_question']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

with col2:
    if st.button("🔄 Reset Sessão"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col3:
    if st.button("📊 Estatísticas"):
        st.info(f"Sessão atual: {st.session_state.questions_asked} perguntas, {st.session_state.files_processed} arquivos")

with col4:
    st.markdown("""
    <div style='text-align: right; color: #667eea; font-size: 0.9em; font-weight: bold;'>
        🚀 Powered by Metadron Team
    </div>
    """, unsafe_allow_html=True)
