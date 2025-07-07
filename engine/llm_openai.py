import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llama_index.llms.openai import OpenAI
from config import OPENAI_API_KEY

def load_llm():
    return OpenAI(
        model="gpt-4.1-mini",
        temperature=0.0,
        api_key=OPENAI_API_KEY,
        max_tokens=1024,
        stream=True,
    )
