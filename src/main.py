"""Main entry point for the UAE Government Legislation Agent application.
This module provides a command-line interface for users to input questions
and receive generated responses based on the underlying RAG (Retrieval-Augmented Generation) workflow.

It orchestrates the interaction between the user, the RAG components,
and the language model to deliver relevant answers derived from legal texts.

"""

from src.agent import graph

#     # ------------ Generate evaluation dataset ------------
#     # prompt_loader = PromptLoader("src/prompts/system.md")
#     # generator = OpenAIQuestionGenerator(prompt_loader=prompt_loader)

#     # dataset_generator = EvaluationDatasetGenerator(
#     #     question_generator=generator,
#     # )
#     # dataset_generator.generate(
#     #     chunks=chunks
#     # )


# --------------------------------------------------
# Main
# --------------------------------------------------


def main():
    question = input("Enter your question: ")

    result = graph.invoke(
        {
            "question": question,
        }
    )

    # print("\nRetrieved Context:")
    # print(result.get("context", ""))

    print("\nGenerated Response:")
    print(result["answer"])


if __name__ == "__main__":
    main()
