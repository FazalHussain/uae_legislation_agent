from src.rag.chunker import SmartChunker
from src.rag.loader import PDFLoader


def main():
    documents = PDFLoader().load('data')

    chunker = SmartChunker(max_chars=500)

    chunks = chunker.split(documents)

    print(f"Total chunks: {len(chunks)}")
    print("=" * 80)

    for i, chunk in enumerate(chunks, start=1):

        print(f"CHUNK {i}")
        print("-" * 80)

        print("TEXT:")
        print(chunk.text)

        print("\nMETADATA:")
        print(chunk.metadata)

        print("\nSIZE:")
        print(len(chunk.text))

        print("=" * 80)


if __name__ == "__main__":
    main()