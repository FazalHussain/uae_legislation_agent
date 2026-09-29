from src.rag.chunker import SmartChunker
from src.rag.loader import PDFLoader
from src.rag.embeddings import BGEEmbeddingModel
from src.rag.vectore_store import ChromaVectorStore
from src.rag.retriever import VectorRetriever


def main():
    documents = PDFLoader().load('data')
    embedding_model = BGEEmbeddingModel()
    vector_store = ChromaVectorStore()

    chunker = SmartChunker(max_chars=500)

    chunks = chunker.split(documents)

    print(f"Total chunks: {len(chunks)}")
    print("=" * 80)

    texts = [chunk.text for chunk in chunks]
    metadata = [chunk.metadata for chunk in chunks]
    embeddings = embedding_model.embed(texts)

    # print(len(embeddings))
    # print(len(embeddings[0]))

    vector_store.add(texts, embeddings, metadata=metadata)

    query = input("Enter your question: ")

    retriever = VectorRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    results = retriever.retrieve(question=query, top_k=5)


    for result in results:
        print("-----")
        print(result)


if __name__ == "__main__":
    main()