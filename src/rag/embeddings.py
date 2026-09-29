from sentence_transformers import SentenceTransformer


class BGEEmbeddingModel:

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3"
    ):
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()