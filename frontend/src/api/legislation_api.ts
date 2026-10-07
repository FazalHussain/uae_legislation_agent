import type { LegalSource, RagStep } from "../types";

export interface AskResponse {
    content: string;
    sources: LegalSource[];
    ragSteps: RagStep[];
}

export async function getResponse(
    query: string
): Promise<AskResponse> {
    const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            question: query,
        }),
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();

    return {
        content: data.answer,
        sources: buildSources(data.reranked_chunks),
        ragSteps: buildRagSteps(
            query,
            data.retrieved_chunks,
            data.reranked_chunks
        ),
    };
}

function buildSources(chunks: any[]): LegalSource[] {
    return chunks.map((chunk, index) => ({
        id: `source_${index}`,

        lawName: chunk.metadata?.law_name ?? "UAE Legislation",

        lawNumber: chunk.metadata?.law_number ?? "",

        year: chunk.metadata?.year ?? 0,

        articleNumber: chunk.metadata?.article_number ?? "",

        articleTitle: chunk.metadata?.article_title ?? "",

        relevantText: chunk.text ?? "",

        fullArticleText: chunk.metadata?.full_article_text ?? chunk.text ?? "",

        relevanceScore: chunk.metadata?.score ?? 0,

        category: chunk.metadata?.category ?? "",

        jurisdiction: chunk.metadata?.jurisdiction ?? "UAE",
    }));
}

function buildRagSteps(
    query: string,
    retrievedChunks: any[],
    rerankedChunks: any[]
): RagStep[] {

    return [
        {
            label: "Query Processing",
            description: "Parsing and embedding the user query",
            duration: "-",
            items: [
                {
                    id: "q1",
                    title: "Query",
                    subtitle:
                        query.length > 50
                            ? `"${query.slice(0, 50)}..."`
                            : `"${query}"`,
                    metadata: "Query submitted to RAG pipeline",
                },
            ],
        },

        {
            label: "Retrieved Documents",
            description: "Vector search across legislation corpus",
            duration: "-",
            items: retrievedChunks.map((chunk, i) => ({
                id: `ret_${i}`,
                title:
                    chunk.metadata?.law_name ?? "UAE Legislation",
                subtitle:
                    chunk.metadata?.article_number ?? "",
                metadata: `Retrieved chunk ${i + 1}`,
            })),
        },

        {
            label: "Top-K Selection",
            description: "Highest scoring chunks selected for reranking",
            duration: "-",
            items: retrievedChunks.slice(0, 20).map((chunk, i) => ({
                id: `topk_${i}`,
                title:
                    chunk.metadata?.law_name ?? "UAE Legislation",
                subtitle:
                    chunk.metadata?.article_number ?? "",
                metadata: `Rank ${i + 1}`,
            })),
        },

        {
            label: "Reranked Results",
            description: "Cross-encoder reranking for precision",
            duration: "-",
            items: rerankedChunks.map((chunk, i) => ({
                id: `rr_${i}`,
                title:
                    chunk.metadata?.law_name ?? "UAE Legislation",
                subtitle:
                    chunk.metadata?.article_number ?? "",
                score: chunk.metadata?.score,
                metadata: `Final Rank ${i + 1}`,
            })),
        },

        {
            label: "Final Context",
            description: "Context assembled for answer generation",
            duration: "-",
            items: rerankedChunks.map((chunk, i) => ({
                id: `ctx_${i}`,
                title:
                    chunk.metadata?.article_number ?? `Context ${i + 1}`,
                subtitle:
                    chunk.metadata?.law_name ?? "UAE Legislation",
                metadata: `${chunk.text.length} chars`,
            })),
        },
    ];
}