# CSV AGENT - I2A2 METADRON

A modern and user-friendly application for asking questions about your CSV files using AI (LLM), with both terminal and web (Streamlit) interfaces.

## 📦 Project Structure

```
desafio_03
├── src
│   ├── main.py                   # Terminal interface entry point
│   ├── agents
│   │   └── csv_agent.py          # CSVAgent: loads CSVs, queries with LLM
│   ├── interface
│   │   ├── ui.py                 # Terminal interface
│   │   └── streamlit/
│   │       └── streamlit.ui.py   # Streamlit web interface
│   ├── utils
│   │   └── file_utils.py         # (Optional) Utility functions
│   └── data/
│       └── (your CSVs here)
├── requirements.txt
├── Makefile
└── README.md
```

## 🚀 Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd entregas/desafio_03
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install and run Ollama:**
   ```bash
   make ollama-serve
   make ollama-pull
   ```
4. **Run the application:**

- **Terminal**: `make run-terminal`
- **Web**: `make run-streamlit`

## 🗂️ How to use

- Upload a CSV or ZIP file via the web interface, or place your CSV files in src/data/.
- Select the desired file.
- Ask questions in natural language (e.g., "Which supplier received the highest amount?").
- Receive the answer from the AI agent, always in Portuguese.

## 🛠️ Makefile Commands

- `make install` - Installs Python dependencies
- `make run-terminal` — Runs terminal interface
- `make run-streamlit` — Runs web interface
- `make ollama-serve` — Starts the Ollama server
- `make ollama-pull` — Downloads the Llama3:8b model
- `make clean-data` — Cleans CSV files from the data folder

## 📝 Example questions

"What are the columns in the file?"
"Which supplier received the highest amount?"
"Which item had the largest delivered volume?"

## ⚠️ Requirements

- Python 3.8+
- Ollama installed and running locally
- Supported LLM models (e.g., llama3:8b)
