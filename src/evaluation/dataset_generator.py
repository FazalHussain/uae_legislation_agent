"""Build a retrieval evaluation dataset from generated questions and chunks."""

import json

from src.rag.rag import Chunk
from src.evaluation.question_generator import QuestionGenerator


class EvaluationDatasetGenerator:
    """Generate and save question-to-relevant-chunk evaluation examples."""

    def __init__(
        self,
        question_generator: QuestionGenerator,
    ):
        """Initialize the dataset generator with its question-generation service.

        Args:
            question_generator: Service that creates questions from chunk text.

        Returns:
            None.
        """
        self.question_generator = question_generator

    def generate(
        self,
        chunks: list[Chunk],
        chunk_count: int = 50,
        questions_per_chunk: int = 2,
        output_path: str = "data/evaluation/retrieval_dataset_candidates.json",
    ) -> None:
        """Generate questions for selected chunks and write them as JSON.

        Args:
            chunks: Source chunks whose text supplies question context and whose
                IDs become ground-truth relevant labels.
            chunk_count: Maximum number of leading chunks to process.
            questions_per_chunk: Number of questions requested for each chunk.
            output_path: Destination path for the JSON evaluation dataset.

        Returns:
            None. The generated examples are written to ``output_path``.
        """

        evaluation_data = []

        for chunk in chunks[:chunk_count]:

            questions = self.question_generator.generate(
                text=chunk.text,
                count=questions_per_chunk,
            )

            for question in questions:
                evaluation_data.append({
                    "question": question,
                    "relevant": [
                        chunk.metadata["chunk_id"]
                    ]
                })

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                evaluation_data,
                file,
                indent=2,
                ensure_ascii=False,
            )

        print(
            f"Generated {len(evaluation_data)} questions "
            f"from {chunk_count} chunks"
        )