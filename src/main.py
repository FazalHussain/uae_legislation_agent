import json

from src.rag.chunker import SmartChunker
from src.rag.loader import PDFLoader
from src.rag.embeddings import BGEEmbeddingModel
from src.rag.vectore_store import ChromaVectorStore
from src.rag.retriever import VectorRetriever
from src.rag.evaluation import precision_at_k, recall_at_k

with open(
    "data/evaluation/retrieval_dataset.json",
    "r",
    encoding="utf-8"
) as file:
    evaluation_data = json.load(file)


def main():
    documents = PDFLoader().load("data")

    embedding_model = BGEEmbeddingModel()
    vector_store = ChromaVectorStore()

    chunker = SmartChunker(max_chars=500)
    chunks = chunker.split(documents)

    print(f"Total chunks: {len(chunks)}")

    # -------------------------
    # Index documents
    # -------------------------

    texts = [chunk.text for chunk in chunks]
    metadata = [chunk.metadata for chunk in chunks]

    embeddings = embedding_model.embed(texts)

    vector_store.add(
        texts,
        embeddings,
        metadata=metadata,
    )

    # -------------------------
    # Retriever
    # -------------------------

    retriever = VectorRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    # -------------------------
    # Evaluation
    # -------------------------

    for item in evaluation_data:

        question = item["question"]

        relevant_ids = set(item["relevant"])

        results = retriever.retrieve(
            question=question,
            top_k=5,
        )

        precision = precision_at_k(
            results,
            relevant_ids,
            k=5,
        )

        recall = recall_at_k(
            results,
            relevant_ids,
            k=5,
        )

        print("=" * 80)
        print("Question:", question)

        print("\nRetrieved:")

        for result in results:            
            # print("TEXT:", result.text[:100])
            # print("METADATA:", result.metadata)
            print("CHUNK ID:", repr(result.metadata.get("chunk_id")))
            # print("RELEVANT:", repr(relevant_ids))

        print(
            f"\nPrecision@5: {precision:.3f}"
        )

        print(
            f"Recall@5:    {recall:.3f}"
        )


if __name__ == "__main__":
    main()