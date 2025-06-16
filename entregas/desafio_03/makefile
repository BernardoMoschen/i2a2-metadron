# Roda a aplicação no terminal (modo texto)
run-terminal:
	python3 src/main.py

# Roda a interface web com Streamlit
run-streamlit:
	streamlit run ./streamlit_app.py

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
	rm -f src/data/*.csv

.PHONY: run-terminal run-streamlit ollama-serve ollama-pull install clean-data