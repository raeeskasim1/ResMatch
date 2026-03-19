from app.vectordb.chroma_client import get_chroma_client

COLLECTION_NAME = "resumes_index"


def get_resume_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_resume(resume_id: str, document: str, embedding: list, metadata: dict):
    collection = get_resume_collection()
    collection.add(
        ids=[resume_id],
        documents=[document],
        embeddings=[embedding],
        metadatas=[metadata]
    )


def query_resumes(query_embedding: list, top_k: int = 5):
    collection = get_resume_collection()
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances", "embeddings"]
    )


def clear_resume_collection():
    client = get_chroma_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    client.get_or_create_collection(name=COLLECTION_NAME)