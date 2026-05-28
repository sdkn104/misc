"""
FAISS vector store with multilingual-e5 embeddings via LangChain.
Input: pandas DataFrame with 'text' column and arbitrary metadata columns.
"""

import numpy as np
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize


def build_vectorstore(df: pd.DataFrame, text_col: str = "text") -> FAISS:
    """
    Embed texts in df[text_col] with all other columns as metadata.
    Returns a FAISS vectorstore.
    """
    # multilingual-e5-large expects "query: " / "passage: " prefixes
    docs = [
        Document(
            page_content=f"passage: {row[text_col]}",
            metadata={k: v for k, v in row.items() if k != text_col},
        )
        for _, row in df.iterrows()
    ]

    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return FAISS.from_documents(docs, embeddings)


def query_vectorstore(vs: FAISS, query: str, k: int = 5) -> list[tuple[Document, float]]:
    """Search the vectorstore with e5 query prefix. Returns (doc, score) pairs."""
    return vs.similarity_search_with_score(f"query: {query}", k=k)


def cluster_documents(vs: FAISS, n_clusters: int) -> pd.DataFrame:
    """
    K-means clustering on all vectors in the FAISS index.

    Returns a DataFrame with columns:
      - text: document page_content
      - cluster: cluster label (int)
      - <metadata keys>: all metadata fields from each document
    """
    index = vs.index
    n_docs = index.ntotal
    dim = index.d

    # extract all vectors from FAISS
    vectors = np.zeros((n_docs, dim), dtype=np.float32)
    index.reconstruct_n(0, n_docs, vectors)
    vectors = normalize(vectors)  # cosine-friendly

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(vectors)

    # retrieve documents in index order
    docs_and_ids = vs.docstore._dict  # {doc_id: Document}
    ordered_ids = [vs.index_to_docstore_id[i] for i in range(n_docs)]
    ordered_docs = [docs_and_ids[doc_id] for doc_id in ordered_ids]

    rows = []
    for doc, label in zip(ordered_docs, labels):
        row = {"text": doc.page_content, "cluster": int(label)}
        row.update(doc.metadata)
        rows.append(row)

    return pd.DataFrame(rows).sort_values("cluster").reset_index(drop=True)


def save_vectorstore(vs: FAISS, path: str) -> None:
    vs.save_local(path)


def load_vectorstore(path: str) -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)


# --- demo ---
if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "text": [
                "東京は日本の首都です。",
                "Paris is the capital of France.",
                "Berlin ist die Hauptstadt von Deutschland.",
                "机器学习是人工智能的一个分支。",
                "Deep learning is a subset of machine learning.",
                "自然言語処理はAIの重要な分野です。",
            ],
            "lang": ["ja", "en", "de", "zh", "en", "ja"],
            "source": ["wiki"] * 6,
        }
    )

    print("Building vectorstore...")
    vs = build_vectorstore(df)

    results = query_vectorstore(vs, "ヨーロッパの首都", k=3)
    print("\nQuery: ヨーロッパの首都")
    for doc, score in results:
        print(f"  score={score:.4f} [{doc.metadata}] {doc.page_content}")

    print("\nClustering (n=3):")
    clustered = cluster_documents(vs, n_clusters=3)
    print(clustered[["cluster", "text"]].to_string(index=False))

    save_vectorstore(vs, "tmp/faiss_index")
    print("\nSaved to tmp/faiss_index")
