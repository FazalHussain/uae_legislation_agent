# system.md

## retrieval_question_generation

Generate {count} questions based only on the following legal text.

Requirements:

- Questions must be answerable directly from the provided text.
- Questions must test retrieval of the legal provision, not general document metadata.
- Focus on legal rights, obligations, prohibitions, conditions, exceptions, scope, definitions, applicability, procedures, penalties, dates, or legal effects.
- Do not ask about names, signatures, document formatting, or the identity of officials unless they are legally relevant.
- Do not ask questions that require information not present in the text.
- Do not infer or add information.
- Avoid duplicate or nearly identical questions.
- Questions should be natural questions that a user might ask a legal assistant.
- Return only a numbered list of questions.

Legal text:

{text}