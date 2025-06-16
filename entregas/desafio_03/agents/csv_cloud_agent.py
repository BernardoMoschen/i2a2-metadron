import requests
import pandas as pd
import os
import streamlit as st

class CSVAgent:
    def __init__(self, folder):
        self.folder = folder
        self.dataframes = {}

    def load_data(self):
        for file in os.listdir(self.folder):
            if file.endswith(".csv"):
                path = os.path.join(self.folder, file)
                df = pd.read_csv(path)
                self.dataframes[file] = df

    def list_files(self):
        return list(self.dataframes.keys())

    def query_data(self, filenameAPI_KEY, question):
        df = self.dataframes[filename]
        sample = df.head(10).to_csv(index=False)
        prompt = (
            f"You are a data analyst. Given this CSV preview:\n\n"
            f"{sample}\n\n"
            f"User question: {question}\n\n"
            f"Answer as clearly and accurately as possible."
        )

        api_key = st.secrets["API_KEY"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://your-username.streamlit.app",
            "X-Title": "csv-agent-metadron"
        }

        data = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Erro ao consultar modelo: {response.status_code} - {response.text}"
