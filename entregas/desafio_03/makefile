# Roda a interface web com Streamlit e IA LOCAl
run-local:
	streamlit run ./streamlit_app_local.py

# Roda a interface web com Streamlit e IA CLOUD
run-cloud:
	streamlit run ./streamlit_app_cloud.py

# Inicia o servidor Ollama (necessário para o agente LLM)
ollama-serve:
	ollama serve

# Baixa o modelo Llama3:8b para uso local
ollama-pull:
	ollama pull llama3:8b

# Instala todas as dependências do projeto
install:
	pip install -r requirements.txt

# Limpa arquivos CSV antigos da pasta de dados
clean-data:
	rm -f ./data/*.csv

.PHONY: run-terminal run-streamlit ollama-serve ollama-pull install clean-data