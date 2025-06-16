# CSV AGENT - I2A2 METADRON

Uma aplicação moderna e amigável para fazer perguntas sobre seus arquivos CSV usando IA (LLM), com interface de terminal e web (Streamlit).

## 📦 Estrutura do Projeto

```
desafio_03
├── src
│   ├── main.py                   # Entrada da interface de terminal
│   ├── agents
│   │   └── csv_agent.py          # CSVAgent: carrega CSVs, consulta com LLM
│   ├── interface
│   │   ├── ui.py                 # Interface de ter⚠️ Requisitos
Python 3.8+
Ollama instalado e rodando localmente
Modelos LLM suportados (ex: llama3:8b)inal
│   │   └── streamlit/
│   │       └── streamlit.ui.py   # Interface web Streamlit
│   ├── utils
│   │   └── file_utils.py         # (Opcional) Funções utilitárias
│   └── data/
│       └── (seus CSVs aqui)
├── requirements.txt
├── Makefile
└── README.md
```

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

- **Terminal**: `make run-terminal`
- **Web**: make `run-streamlit`

## 🗂️ Como usar

- Faça upload de um arquivo CSV ou ZIP pela interface web, ou coloque seus arquivos CSV em src/data/.

- Escolha o arquivo desejado.

- Pergunte em linguagem natural (ex: "Qual fornecedor recebeu maior montante?").

- Receba a resposta do agente IA, **sempre em português**.

## 🛠️ Comandos Makefile

- `make install` - Instala dependências Python
- `make run-terminal` — Executa interface terminal
- `make run-streamlit` — Executa interface web
- `make ollama-serve` — Inicia o servidor Ollama
- `make ollama-pull` — Baixa o modelo Llama3:8b
- `make clean-data` — Limpa arquivos CSV da pasta de dados

## 📝 Exemplos de perguntas

"Quais são as colunas do arquivo?"
"Qual o fornecedor que recebeu maior valor?"
"Qual item teve maior volume entregue?"

## ⚠️ Requisitos

- Python 3.8+

- Ollama instalado e rodando localmente

- Modelos LLM suportados (ex: llama3:8b)
