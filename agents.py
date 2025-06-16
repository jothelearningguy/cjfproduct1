import os
import json
import logging
import pandas as pd
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CSVAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "CSV Chatbot"
        }
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.system_prompt = "A:Analyze CSV data and answer questions concisely."

    def process_question(self, question: str, df: pd.DataFrame) -> str:
        try:
            # Create compact data representation
            sample_df = df.head(2)
            df_info = f"n={len(df)} c={len(df.columns)} cols={','.join(df.columns)} d={sample_df.to_string(index=False, max_colwidth=15)}"
            
            # Single API call with optimized prompt
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"q:{question} d:{df_info}"}
            ]
            
            logger.info("Making API call to OpenRouter")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "anthropic/claude-3-opus-20240229",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 100  # Reduced to minimum needed
                }
            )
            response.raise_for_status()
            logger.info("Successfully received response from OpenRouter")
            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error in OpenRouter API call: {str(e)}")
            raise 