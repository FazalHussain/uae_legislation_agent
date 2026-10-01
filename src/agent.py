"""Reserved module for legislation-agent orchestration components."""

import json

from langgraph.graph import StateGraph, START, END

from src.llm import OpenAILLM
from src.rag.rag import RAG
from src.rag.reranker import BGEReranker
from src.evaluation.dataset_generator import EvaluationDatasetGenerator
from src.rag.chunker import SmartChunker
from src.rag.loader import PDFLoader
from src.rag.embeddings import BGEEmbeddingModel
from src.rag.vectore_store import ChromaVectorStore
from src.rag.retriever import VectorRetriever
from src.evaluation.evaluation import precision_at_k, recall_at_k, reciprocal_rank
from src.evaluation.question_generator import OpenAIQuestionGenerator, QuestionGenerator
from src.prompts.prompt_loader import PromptLoader

# --------------------------------------------------
# Graph State
# --------------------------------------------------


class RAGState(dict):
    """
    State passed between LangGraph nodes.
    """

    question: str
    retrieved_chunks: list
    reranked_chunks: list
    context: str
    system_prompt: str
    user_prompt: str
    answer: str


# --------------------------------------------------
# Components
# --------------------------------------------------

prompt_loader = PromptLoader("src/prompts/prompts.md")

loader = PDFLoader()

chunker = SmartChunker(max_chars=500)

embedding_model = BGEEmbeddingModel()

vector_store = ChromaVectorStore()

retriever = VectorRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
)

reranker = BGEReranker()

rag = RAG(
    loader=loader,
    chunker=chunker,
    embedding_model=embedding_model,
    vector_store=vector_store,
    retriever=retriever,
    reranker=reranker,
)

llm = OpenAILLM()


# --------------------------------------------------
# Nodes
# --------------------------------------------------


def retrieve_node(state: RAGState):

    chunks = rag.retrieve(
        question=state["question"],
        top_k=10,
    )

    return {"retrieved_chunks": chunks}


def rerank_node(state: RAGState):

    chunks = rag.rerank(
        question=state["question"],
        chunks=state["retrieved_chunks"],
        top_k=5,
    )

    return {"reranked_chunks": chunks}


def build_context_node(state: RAGState):
    reranked_chunks = state["reranked_chunks"]
    context = rag.format_context(chunks=reranked_chunks)
    return {"context": context}


def build_prompt_node(state: RAGState):

    system_prompt = prompt_loader.load("uae_legislation_instructions")

    user_prompt = prompt_loader.load("user_question_prompt").format(
        question=state["question"],
        context=state["context"],
    )

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
    }


def llm_node(state: RAGState):

    answer = llm.generate(
        system_prompt=state["system_prompt"],
        user_prompt=state["user_prompt"],
    )

    return {"answer": answer}


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------

builder = StateGraph(RAGState)

builder.add_node(
    "retrieve",
    retrieve_node,
)

builder.add_node(
    "rerank",
    rerank_node,
)

builder.add_node(
    "build_context",
    build_context_node,
)

builder.add_node(
    "build_prompt",
    build_prompt_node,
)

builder.add_node(
    "llm",
    llm_node,
)

# --------------------------------------------------
# Edges
# --------------------------------------------------

builder.add_edge(
    START,
    "retrieve",
)

builder.add_edge(
    "retrieve",
    "rerank",
)

builder.add_edge(
    "rerank",
    "build_context",
)

builder.add_edge(
    "build_context",
    "build_prompt",
)

builder.add_edge(
    "build_prompt",
    "llm",
)

builder.add_edge(
    "llm",
    END,
)

graph = builder.compile()
