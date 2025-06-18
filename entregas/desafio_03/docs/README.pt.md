# CSV AGENT - I2A2 METADRON

Uma aplicação moderna e amigável para fazer perguntas sobre seus arquivos CSV usando IA (LLM)com interface web (Streamlit).

## 🚀 Como começar

1. **Clone o repositório:**

   ```bash
   git clone <repository-url>
   cd entregas/desafio_03
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Instale e rode o Ollama:**
   ```bash
   make ollama-serve
   make ollama-pull
   ```
4. **Execute a aplicação:**

- **Local**: `make run-local`
- **Cloud**: `make run-cloud`

## 🛠️ Comandos Makefile

- `make install` - Instala dependências Python
- `make run-cloud` — Executa interface web com IA na cloud
- `make run-local` — Executa interface web com IA local (necessário ollama baicado e rodando)
- `make ollama-serve` — Inicia o servidor Ollama
- `make ollama-pull` — Baixa o modelo Llama3:8b
- `make clean-data` — Limpa arquivos CSV da pasta de dados

## ⚠️ Requisitos

- Python 3.8+

- Se rodando local:

  - Ollama instalado e rodando localmente, `make ollama-pull` | `make ollama-serve`

- Modelos LLM suportados (ex: llama3:8b)
