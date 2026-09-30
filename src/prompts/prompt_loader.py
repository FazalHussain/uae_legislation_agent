"""Read named prompt sections from a Markdown file."""

from pathlib import Path


class PromptLoader:
    """Load prompt text from Markdown sections headed with level-two headings."""

    def __init__(self, path: str):
        """Configure the Markdown file used as the prompt source.

        Args:
            path: Filesystem path to a Markdown prompt file.

        Returns:
            None.
        """
        self.path = Path(path)

    def load(self, name: str) -> str:
        """Find a named section and return its body without surrounding whitespace.

        Args:
            name: Exact heading text of the prompt section to load.

        Returns:
            The stripped body text of the matching Markdown section.

        Raises:
            ValueError: No section with the requested heading exists.
        """
        content = self.path.read_text()

        sections = content.split("## ")

        for section in sections:
            lines = section.splitlines()

            if not lines:
                continue

            section_name = lines[0].strip()

            if section_name == name:
                return "\n".join(lines[1:]).strip()

        raise ValueError(f"Prompt not found: {name}")