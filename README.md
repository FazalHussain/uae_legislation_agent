# UAE Government Legislation Agent

This project is a retrieval-augmented generation (RAG) assistant for UAE legislation. It reads legal PDFs, chunks them into searchable passages, retrieves the most relevant sections for a user question, reranks them, and sends the final legal context to an LLM for an answer grounded in the underlying source material.

> The current implementation focuses on a legal question-answering workflow and includes optional retrieval-evaluation utilities. It is intended to support research and retrieval over local legislation documents, not to serve as legal advice.

## Visual flow

```mermaid
flowchart LR
    User["User question"] --> Graph["LangGraph workflow"]
    Graph --> Retrieve["retrieve_node\nVector retrieval"]
    Retrieve --> Chroma[("Chroma vector store")]
    Chroma --> Candidate["candidate chunks"]
    Candidate --> Rerank["rerank_node\nBGE reranking"]
    Rerank --> Context["build_context_node\nformat legal context"]
    Context --> Prompt["build_prompt_node\nassemble system + user prompt"]
    Prompt --> LLM["OpenAILLM\nAzure OpenAI-compatible endpoint"]
    LLM --> Answer["Final answer"]

    subgraph Indexing["Document indexing pipeline"]
        Docs["PDFs in data/"] --> Loader["PDFLoader"]
        Loader --> Chunker["SmartChunker"]
        Chunker --> Embed["BGE embeddings"]
        Embed --> Index[("Persistent Chroma index")]
    end

    subgraph Eval["Optional evaluation pipeline"]
        EvalData["Evaluation dataset"] --> Metrics["Precision@k / Recall@k / MRR"]
        Metrics --> Results["retrieval metrics"]
    end
```

## How the current application works

1. The user enters a question in `src/main.py`.
2. `src/agent.py` compiles a LangGraph workflow with the following sequence:
   - `retrieve`
   - `rerank`
   - `build_context`
   - `build_prompt`
   - `llm`
3. The retrieval stage searches the indexed legal chunks in Chroma using a multilingual embedding model.
4. The reranker narrows the candidate list to the most relevant passages.
5. Those passages are formatted into context for the system prompt.
6. `src/llm.py` calls the OpenAI client against the configured Azure OpenAI-compatible endpoint and returns the final answer.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── chroma_db/                     # local Chroma vector storage
├── data/
│   ├── *.pdf                      # source legislation PDFs
│   └── evaluation/
│       ├── retrieval_dataset.json
│       └── retrieval_dataset_candidates.json
├── src/
│   ├── agent.py                   # LangGraph orchestration
│   ├── llm.py                    # OpenAI/Azure-compatible LLM wrapper
│   ├── main.py                   # CLI entry point for user questions
│   ├── evaluation/
│   │   ├── dataset_generator.py
│   │   ├── evaluation.py
│   │   ├── langfuse_client.py
│   │   └── question_generator.py
│   ├── prompts/
│   │   ├── prompt_loader.py
│   │   └── prompts.md
│   └── rag/
│       ├── chunker.py
│       ├── embeddings.py
│       ├── loader.py
│       ├── rag.py
│       ├── reranker.py
│       ├── retriever.py
│       └── vectore_store.py
└── .env.example (if present)     # environment configuration example
```

## Core components

| Component | Responsibility |
| --- | --- |
| `src/main.py` | CLI entry point; collects the question and invokes the graph. |
| `src/agent.py` | Builds and compiles the LangGraph RAG workflow. |
| `src/llm.py` | Sends system/user prompt to the OpenAI-compatible model. |
| `src/rag/loader.py` | Extracts text from legislation PDFs. |
| `src/rag/chunker.py` | Splits the text into article- and clause-aware chunks. |
| `src/rag/embeddings.py` | Creates multilingual embeddings for legal text. |
| `src/rag/vectore_store.py` | Persists and queries chunks in Chroma. |
| `src/rag/retriever.py` | Retrieves candidate chunks using the query embedding. |
| `src/rag/reranker.py` | Reorders retrieved chunks by relevance. |
| `src/prompts/prompts.md` | System prompt and user prompt templates. |
| `src/evaluation/` | Utilities for dataset generation and retrieval metrics. |

## Setup

Use Python 3.10 or newer. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment configuration

This project reads Azure-compatible OpenAI settings from environment variables. Configure them before running the app:

```bash
export AZURE_AD_TOKEN_PROVIDER="<your-token-or-api-key>"
export AZURE_FOUNDARY_ENDPOINT="https://<your-resource>.services.ai.azure.com/models"
```

The runtime in `src/llm.py` uses these values as the OpenAI client API key and base URL. If you use a different model provider or credential flow, update the environment variables and client configuration accordingly.

## Run the app

From the repository root:

```bash
python -m src.main
```

You will be prompted to enter a legal question. The system will retrieve the relevant passages, rerank them, and answer using the legal context.

## Working with the local vector store

The project persists legal chunks under `chroma_db/`. In the current codebase, the interactive app expects a populated vector index to already exist. If you add or change source PDFs, rebuild the indexed data before running queries so the retrieval stage reflects the updated document set.

The indexing workflow is implemented in the RAG pipeline classes and can be reused when you need to re-ingest the legal corpus.

## Evaluation and dataset utilities

The repository includes utilities for building evaluation datasets and measuring retrieval quality. The evaluation modules support tasks such as:

- question generation from legal text
- label-based retrieval checks
- precision and recall metrics
- reciprocal-rank style relevance scoring

These utilities are useful when benchmarking retrieval quality, but the main end-user experience is the interactive Q&A flow shown above.

## Notes

- The project is designed for legal-document retrieval and grounded answer generation, not legal advice.
- Always verify any answer against the authoritative legislation text before relying on it for formal decisions.
- Changes in chunking logic or source filenames can affect retrieval quality and evaluation labels, so keep the indexing and evaluation data in sync when modifying the pipeline.
