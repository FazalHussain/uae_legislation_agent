"""Run legislation retrieval and report retrieval metrics for a dataset."""

import json

from src.rag.rag import RAG
from src.rag.reranker import BGEReranker
from src.evaluation.dataset_generator import EvaluationDatasetGenerator
from src.rag.chunker import SmartChunker
from src.rag.loader import PDFLoader
from src.rag.embeddings import BGEEmbeddingModel
from src.rag.vectore_store import ChromaVectorStore
from src.rag.retriever import VectorRetriever
from src.evaluation.evaluation import precision_at_k, recall_at_k
from src.evaluation.question_generator import OpenAIQuestionGenerator, QuestionGenerator
from src.prompts.prompt_loader import PromptLoader

with open(
    "data/evaluation/retrieval_dataset_candidates.json",
    "r",
    encoding="utf-8"
) as file:
    evaluation_data = json.load(file)


def main():
    """Build the retrieval pipeline and evaluate it against the loaded dataset.

    Args:
        None.

    Returns:
        None. Prints per-question and aggregate precision and recall metrics.
    """

    # ------------ Generate evaluation dataset ------------
    # prompt_loader = PromptLoader("src/prompts/system.md")
    # generator = OpenAIQuestionGenerator(prompt_loader=prompt_loader)

    # dataset_generator = EvaluationDatasetGenerator(
    #     question_generator=generator,
    # )
    # dataset_generator.generate(
    #     chunks=chunks
    # )
    

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

    # -------------------------
    # Ingest
    # -------------------------

    rag.ingest("data")
    

    # -------------------------
    # Evaluation
    # -------------------------

    precisions = []
    recalls = []

    for item in evaluation_data:

        question = item["question"]

        relevant_ids = set(item["relevant"])

        # -------------------------
        # Retrieve
        # -------------------------

        results = rag.retrieve(
            question=question,
            candidate_k=20,
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

        precisions.append(precision)
        recalls.append(recall)

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

    # -------------------------
    # Mean metrics
    # -------------------------

    mean_precision = sum(precisions) / len(precisions)
    mean_recall = sum(recalls) / len(recalls)

    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)

    print(f"Questions:       {len(evaluation_data)}")
    print(f"Mean Precision@5: {mean_precision:.3f}")
    print(f"Mean Recall@5:    {mean_recall:.3f}")


if __name__ == "__main__":
    main()