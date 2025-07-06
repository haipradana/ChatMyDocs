from llama_index.core import Settings, VectorStoreIndex
from .llm_gemini import load_llm
from .embedder import load_embedder
from llama_index.core.prompts import PromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor import SentenceTransformerRerank

def build_query_engine(docs):
    llm = load_llm()
    embed_model = load_embedder()

    Settings.llm = llm
    Settings.embed_model = embed_model

    index = VectorStoreIndex.from_documents(docs, show_progress=True)

    qa_prompt = PromptTemplate(
        """
        Context information is below.\n----------------------\n{context}\n----------------------\n
        Using the context above, answer the question below. \nIf you don't know the answer, just say that you don't know. DO NOT try to make up an answer.
        Question: {query_str}\nAnswer:
        """
    )

    retriever = VectorIndexRetriever(index=index, similarity_top_k=8)

    reranker = SentenceTransformerRerank(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_k=4,
        )
    
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=[reranker],
        response_mode="compact",
        streaming=True,
    )
    query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt})

    return query_engine