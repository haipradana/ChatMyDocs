from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def load_embedder():
    return HuggingFaceEmbedding(
        model_name="nomic-ai/modernbert-embed-base",
        trust_remote_code=True,
        cache_folder="./hf_cache",
    )