from openai import OpenAI
import pandas as pd
from typing import List, Dict, Any

class BaseAgent:
    def __init__(self, client: OpenAI):
        self.client = client

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content

class CoordinatorAgent(BaseAgent):
    def __init__(self, client: OpenAI):
        super().__init__(client)
        self.system_prompt = """You are the Coordinator Agent. Your role is to:
        1. Understand the user's question
        2. Determine which agent(s) should handle the request
        3. Coordinate between the Information Extractor and Researcher agents
        4. Synthesize the final response
        Be concise and clear in your coordination."""

    def coordinate(self, user_question: str, df_info: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"User question: {user_question}\n\nDataset context:\n{df_info}"}
        ]
        return self.get_response(messages)

class InformationExtractorAgent(BaseAgent):
    def __init__(self, client: OpenAI):
        super().__init__(client)
        self.system_prompt = """You are the Information Extractor Agent. Your role is to:
        1. Extract relevant information from the dataset
        2. Perform data analysis and calculations
        3. Identify patterns and relationships in the data
        4. Provide factual information about the dataset
        Focus on extracting and analyzing the data accurately."""

    def extract_info(self, question: str, df: pd.DataFrame) -> str:
        df_info = f"""
        Dataset Information:
        - Number of rows: {len(df)}
        - Number of columns: {len(df.columns)}
        - Column names: {', '.join(df.columns)}
        - First few rows:
        {df.head().to_string()}
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Question: {question}\n\nData:\n{df_info}"}
        ]
        return self.get_response(messages)

class ResearcherAgent(BaseAgent):
    def __init__(self, client: OpenAI):
        super().__init__(client)
        self.system_prompt = """You are the Researcher Agent. Your role is to:
        1. Provide context and insights about the data
        2. Explain patterns and trends
        3. Make connections between different aspects of the data
        4. Offer interpretations and implications
        Focus on providing deeper understanding and insights."""

    def research(self, question: str, extracted_info: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Question: {question}\n\nExtracted Information:\n{extracted_info}"}
        ]
        return self.get_response(messages) 