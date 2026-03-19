from app.vectordb.chroma_client import get_chroma_client


def get_jd_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name="job_descriptions")


def add_jd(jd_id: str, document: str, embedding: list, metadata: dict):
    collection = get_jd_collection()
    collection.add(
        ids=[jd_id],
        documents=[document],
        embeddings=[embedding],
        metadatas=[metadata]
    )