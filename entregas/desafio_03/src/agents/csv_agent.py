
from langchain_ollama import OllamaLLM
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import os

class CSVAgent:
    def __init__(self, data_folder="src/data"):
        self.data_folder = data_folder
        self.dataframes = {}

    def load_data(self):
        for fname in os.listdir(self.data_folder):
            if fname.endswith(".csv"):
                path = os.path.join(self.data_folder, fname)
                self.dataframes[fname] = pd.read_csv(path)

    def list_files(self):
        return list(self.dataframes.keys())

    def query_data(self, filename, question):
        df = self.dataframes.get(filename)
        if df is None:
            return f"Arquivo {filename} não encontrado."
        llm = OllamaLLM(model="llama3:8b")
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)
        try:
            question_pt = f"Responda sempre em português. {question}"
            return agent.invoke(question_pt)
        except Exception as e:
            return f"Erro ao processar a pergunta: {e}"