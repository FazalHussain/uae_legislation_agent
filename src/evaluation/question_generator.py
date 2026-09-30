"""Define question-generation contracts and an OpenAI-backed implementation."""

from typing import Protocol
from openai import OpenAI
import os
from dotenv import load_dotenv

from src.prompts.prompt_loader import PromptLoader

load_dotenv()


# ---------- Abstractions ----------
class QuestionGenerator(Protocol):
    """Specify a service that generates questions from source text."""

    def generate(
        self,
        text: str,
        count: int = 2
    ) -> list[str]:
        """Generate a requested number of questions grounded in source text.

        Args:
            text: Source passage used as question-generation context.
            count: Maximum number of questions to produce.

        Returns:
            A list of generated question strings.
        """
        ...

# ---------- Implementation ----------

class OpenAIQuestionGenerator:
    """Generate retrieval questions from legal text using the OpenAI API."""

    def __init__(
        self,
        prompt_loader: PromptLoader,
        model_name: str = "gpt-4.1-mini",
        temperature: float = 0.7,
        max_tokens: int = 200,
    ):
        """Configure the prompt, model, and output limit for question generation.

        Args:
            prompt_loader: Loader for the retrieval-question prompt template.
            model_name: Model identifier passed to the OpenAI Responses API.
            temperature: Generation temperature retained as configuration; it is
                not currently passed in the API request.
            max_tokens: Maximum output tokens requested from the API.

        Returns:
            None.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.prompt_loader = prompt_loader

    def generate(
        self,
        text: str,
        count: int = 20
    ) -> list[str]:
        """Request questions for a passage and parse them from the model output.

        Args:
            text: Source passage used as question-generation context.
            count: Maximum number of questions to return.

        Returns:
            Up to ``count`` question strings parsed from the model response.
        """
        client = OpenAI(
            api_key=os.getenv("AZURE_AD_TOKEN_PROVIDER"),
            base_url=os.getenv("AZURE_FOUNDARY_ENDPOINT"),
        )

        prompt = self.prompt_loader.load("retrieval_question_generation").format(text=text, count=count)
        
        # Get a response
        input_text = "Generate questions from the provided text."
        response = client.responses.create(
                model=self.model_name,
                instructions=prompt,
                input=input_text,
                stream=False,
                max_output_tokens=self.max_tokens,
        )
        questions_text = response.output_text
        questions = [
            line.split('.', 1)[1].strip() for line in questions_text.splitlines() if line.strip()
        ]

        return questions[:count]

