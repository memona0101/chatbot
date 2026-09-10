from sentence_transformers import SentenceTransformer

# Load the model once when the application starts
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding locally.
    No OpenAI API or API key required.
    """
    embedding = model.encode(text, normalize_embeddings=True)

    return embedding.tolist()