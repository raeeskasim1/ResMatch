from sentence_transformers import SentenceTransformer

# Load model once globally to avoid repeated initialization overhead
model = SentenceTransformer("all-MiniLM-L6-v2")


class TextEmbedder:
    """
    Wrapper class for generating sentence embeddings using SentenceTransformer.

    This class provides methods to encode single text inputs and batches of texts
    into normalized vector embeddings for semantic similarity tasks.
    """

    def __init__(self):
        """
        Initialize the embedder with a preloaded SentenceTransformer model.
        """
        self.model = model

    def encode_one(self, text: str):
        """
        Generate embedding for a single text input.

        Args:
            text (str): Input text.

        Returns:
            list: Normalized embedding vector.
        """
        return self.model.encode(text, normalize_embeddings=True).tolist()

    def encode_many(self, texts: list, batch_size: int = 32):
        """
        Generate embeddings for multiple text inputs in batches.

        Args:
            texts (list): List of input texts.
            batch_size (int, optional): Batch size for encoding. Defaults to 32.

        Returns:
            list: List of normalized embedding vectors.
        """
        return self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True
        ).tolist()