# from langfuse import get_client

# from src.rag.rag import RAG
# from src.rag.reranker import BGEReranker
# from src.rag.chunker import SmartChunker
# from src.rag.loader import PDFLoader
# from src.rag.embeddings import BGEEmbeddingModel
# from src.rag.vectore_store import ChromaVectorStore
# from src.rag.retriever import VectorRetriever
# from dotenv import load_dotenv
# from langfuse.api import NotFoundError

# load_dotenv()  # Load environment variables from .env file

# DATASET_NAME = "retrieval-evaluation"
# K = 5
# import json

# DATASET_PATH = "data/evaluation/retrieval_dataset_candidates.json"



# def build_rag() -> RAG:
#     embedding_model = BGEEmbeddingModel()
#     vector_store = ChromaVectorStore()
#     retriever = VectorRetriever(embedding_model, vector_store)

#     return RAG(
#         loader=PDFLoader(),
#         chunker=SmartChunker(max_chars=500),
#         embedding_model=embedding_model,
#         vector_store=vector_store,
#         retriever=retriever,
#         reranker=BGEReranker(),
#     )


# def main() -> None:
#     langfuse = get_client()
#     rag = build_rag()

#     dataset_created = False
    
#     try:
#         dataset = langfuse.get_dataset(DATASET_NAME)
#         print(f"Using existing dataset: {dataset.name}")
#     except NotFoundError:
#         dataset = langfuse.create_dataset(
#             name=DATASET_NAME,
#             description="uae legislation retrieval evaluation dataset",
#         )
#         dataset_created = True
#         print(f"Dataset created: {dataset.name}")

#     if dataset_created:
#         with open(DATASET_PATH, "r", encoding="utf-8") as file:
#             evaluation_data = json.load(file)

#         for index, example in enumerate(evaluation_data):
#             langfuse.create_dataset_item(
#                 dataset_name=DATASET_NAME,
#                 input={"question": example["question"]},
#                 expected_output={"relevant": example["relevant"]},
#                 metadata={"source": "generated", "index": index},
#             )

#         langfuse.flush()
#         dataset = langfuse.get_dataset(DATASET_NAME)
#         print(f"Uploaded {len(evaluation_data)} items")

#     def task(*, item, **kwargs):
#         question = item.input["question"]
#         relevant = set(item.expected_output["relevant"])

#         with langfuse.start_as_current_observation(
#             as_type="span",
#             name="rag-retrieval",
#         ) as span:
#             results = rag.retrieve(question, candidate_k=20, top_k=K)
#             retrieved = [result.metadata["chunk_id"] for result in results]
#             top_k = retrieved[:K]
#             hits = sum(chunk_id in relevant for chunk_id in top_k)

#             precision = hits / K
#             recall = hits / len(relevant) if relevant else 0.0
#             reciprocal_rank = next(
#                 (
#                     1.0 / rank
#                     for rank, chunk_id in enumerate(top_k, start=1)
#                     if chunk_id in relevant
#                 ),
#                 0.0,
#             )

#             output = {"retrieved_chunk_ids": retrieved}
#             span.update(input=item.input, output=output)
#             span.score_trace(
#                 name=f"precision@{K}",
#                 value=float(precision),
#                 data_type="NUMERIC",
#             )
#             span.score_trace(
#                 name=f"recall@{K}",
#                 value=float(recall),
#                 data_type="NUMERIC",
#             )
#             span.score_trace(
#                 name=f"rr@{K}",
#                 value=float(reciprocal_rank),
#                 data_type="NUMERIC",
#             )

#             return output

#     result = dataset.run_experiment(
#         name="RAG retrieval evaluation",
#         task=task,
#     )
#     print(result.format())
#     langfuse.flush()


# if __name__ == "__main__":
#     main()

import json

from dotenv import load_dotenv
from langfuse import get_client
from langfuse.api import NotFoundError

from src.rag.rag import RAG
from src.rag.embeddings import BGEEmbeddingModel
from src.rag.retriever import VectorRetriever
from src.rag.reranker import BGEReranker
from src.rag.vectore_store import ChromaVectorStore


load_dotenv()

DATASET_NAME = "retrieval-evaluation"
DATASET_PATH = "data/evaluation/retrieval_dataset_candidates.json"

K = 5
CANDIDATE_K = 20


def build_rag() -> RAG:
    embedding_model = BGEEmbeddingModel()
    vector_store = ChromaVectorStore()

    return RAG(
        embedding_model=embedding_model,
        vector_store=vector_store,
        retriever=VectorRetriever(
            embedding_model,
            vector_store,
        ),
        reranker=BGEReranker(),
    )


def get_or_create_dataset(langfuse):
    try:
        return langfuse.get_dataset(DATASET_NAME)

    except NotFoundError:
        dataset = langfuse.create_dataset(
            name=DATASET_NAME,
            description="UAE legislation retrieval evaluation dataset",
        )

        with open(DATASET_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        for index, example in enumerate(data):
            langfuse.create_dataset_item(
                dataset_name=DATASET_NAME,
                input={"question": example["question"]},
                expected_output={
                    "relevant": example["relevant"]
                },
                metadata={
                    "source": "generated",
                    "index": index,
                },
            )

        langfuse.flush()

        print(f"Created dataset with {len(data)} items")

        return langfuse.get_dataset(DATASET_NAME)


def ndcg_at_k(retrieved, relevant, k):
    import math

    dcg = 0.0

    for rank, chunk_id in enumerate(retrieved[:k], start=1):
        if chunk_id in relevant:
            dcg += 1.0 / math.log2(rank + 1)

    ideal_hits = min(len(relevant), k)

    if ideal_hits == 0:
        return 0.0

    idcg = sum(
        1.0 / math.log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    return dcg / idcg


def main():
    langfuse = get_client()
    rag = build_rag()

    dataset = get_or_create_dataset(langfuse)

    def task(*, item, **kwargs):
        question = item.input["question"]
        relevant = set(item.expected_output["relevant"])

        results = rag.retrieve(
            question,
            candidate_k=CANDIDATE_K,
            top_k=K,
        )

        retrieved = [
            result.metadata["chunk_id"]
            for result in results
        ]

        top_k = retrieved[:K]

        hits = sum(
            chunk_id in relevant
            for chunk_id in top_k
        )

        precision = hits / K

        recall = (
            hits / len(relevant)
            if relevant
            else 0.0
        )

        reciprocal_rank = next(
            (
                1.0 / rank
                for rank, chunk_id in enumerate(top_k, start=1)
                if chunk_id in relevant
            ),
            0.0,
        )

        ndcg = ndcg_at_k(
            retrieved,
            relevant,
            K,
        )

        return {
            "retrieved_chunk_ids": retrieved,
            "precision": precision,
            "recall": recall,
            "mrr": reciprocal_rank,
            "ndcg": ndcg,
        }

    result = dataset.run_experiment(
        name="RAG retrieval evaluation",
        task=task,
    )

    print(result.format())

    langfuse.flush()


if __name__ == "__main__":
    main()