import pandas as pd
import os
import streamlit as st
from openai import OpenAI

class CSVAgent:
    def __init__(self, folder):
        self.folder = folder
        self.dataframes = {}
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{st.secrets['API_KEY']}",
        )

    def load_data(self):
        for file in os.listdir(self.folder):
            if file.endswith(".csv"):
                path = os.path.join(self.folder, file)
                df = pd.read_csv(path)
                self.dataframes[file] = df

    def list_files(self):
        return list(self.dataframes.keys())

    def query_data(self, filename, question):
        df = self.dataframes[filename]
        sample = df 
        prompt = (
            f"You are a data analyst. Given this CSV preview:\n\n"
            f"{sample}\n\n"
            f"User question: {question}\n\n"
            f"Answer as clearly and accurately as possible."
            f"Answer always in portuguese, unless asked not to."
        )
        
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.error(f"Ocorreu um erro ao consultar o modelo: {e}")
