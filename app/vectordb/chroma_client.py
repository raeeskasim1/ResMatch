import chromadb


def get_chroma_client(path: str = "./chroma_store"):
    return chromadb.PersistentClient(path=path)