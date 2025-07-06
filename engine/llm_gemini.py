import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llama_index.llms.gemini import Gemini
from config import GEMINI_API_KEY

def load_llm():
    return Gemini(
        api_key=GEMINI_API_KEY,
        model="models/gemini-2.5-flash",
        stream=True,
    )
