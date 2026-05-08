import os
import numpy as np
from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


# -----------------------------
# GLOBAL CACHE
# -----------------------------
db_cache = {}
bm25_cache = {}
corpus_cache = {}
docs_cache = {}

# 🔥 NEW: Track DB file changes
db_timestamp_cache = {}


# -----------------------------
# HYBRID SEARCH (FAISS + BM25)
# -----------------------------
def hybrid_search(query: str, user_id: str, k: int = 5, alpha: float = 0.7):

    db_path = f"storage/user_{user_id}/db"
    index_file = os.path.join(db_path, "index.faiss")

    # -----------------------------
    # 🔥 1. AUTO-REFRESH CACHE
    # -----------------------------
    last_modified = os.path.getmtime(index_file) if os.path.exists(index_file) else None

    if (
        user_id not in db_cache
        or db_timestamp_cache.get(user_id) != last_modified
    ):
        print("🔄 Reloading vector DB...")

        db_cache[user_id] = FAISS.load_local(
            db_path,
            OpenAIEmbeddings(model="text-embedding-3-small"),
            allow_dangerous_deserialization=True
        )

        db_timestamp_cache[user_id] = last_modified

        # 🔥 Reset dependent caches
        docs_cache.pop(user_id, None)
        corpus_cache.pop(user_id, None)
        bm25_cache.pop(user_id, None)

    db = db_cache[user_id]

    # -----------------------------
    # 2. CACHE DOCS + CORPUS
    # -----------------------------
    if user_id not in docs_cache:
        print("📄 Loading documents into memory...")

        all_docs_dict = db.docstore._dict
        all_docs = list(all_docs_dict.values())
        corpus = [doc.page_content for doc in all_docs]

        docs_cache[user_id] = all_docs
        corpus_cache[user_id] = corpus
    else:
        all_docs = docs_cache[user_id]
        corpus = corpus_cache[user_id]

    # -----------------------------
    # 3. BM25 CACHE
    # -----------------------------
    if user_id not in bm25_cache:
        print("⚡ Building BM25 index...")

        tokenized_corpus = [doc.split() for doc in corpus]
        bm25_cache[user_id] = BM25Okapi(tokenized_corpus)

    bm25 = bm25_cache[user_id]
    tokenized_query = query.split()

    # -----------------------------
    # 4. GET TOP CANDIDATES
    # -----------------------------
    TOP_K = 50

    # Semantic search
    sem_results = db.similarity_search_with_score(query, k=TOP_K)

    # BM25 scores
    bm25_scores = bm25.get_scores(tokenized_query)

    top_bm25_idx = np.argsort(bm25_scores)[::-1][:TOP_K]

    # -----------------------------
    # 5. BUILD CANDIDATE SET
    # -----------------------------
    candidates = {}

    # Semantic results
    for doc, score in sem_results:
        sim_score = 1 / (1 + score)
        text = doc.page_content

        candidates[text] = {
            "doc": doc,
            "semantic": sim_score,
            "bm25": 0
        }

    # BM25 results
    for idx in top_bm25_idx:
        text = corpus[idx]

        if text not in candidates:
            candidates[text] = {
                "doc": all_docs[idx],
                "semantic": 0,
                "bm25": bm25_scores[idx]
            }
        else:
            candidates[text]["bm25"] = bm25_scores[idx]

    # -----------------------------
    # 6. NORMALIZATION
    # -----------------------------
    sem_vals = np.array([v["semantic"] for v in candidates.values()])
    bm25_vals = np.array([v["bm25"] for v in candidates.values()])

    if sem_vals.max() != sem_vals.min():
        sem_vals = (sem_vals - sem_vals.min()) / (sem_vals.max() - sem_vals.min())
    else:
        sem_vals = np.zeros_like(sem_vals)

    if bm25_vals.max() != bm25_vals.min():
        bm25_vals = (bm25_vals - bm25_vals.min()) / (bm25_vals.max() - bm25_vals.min())
    else:
        bm25_vals = np.zeros_like(bm25_vals)

    # Assign back normalized scores
    for i, key in enumerate(candidates.keys()):
        candidates[key]["semantic"] = sem_vals[i]
        candidates[key]["bm25"] = bm25_vals[i]

    # -----------------------------
    # 7. FINAL HYBRID SCORE
    # -----------------------------
    final_results = []

    for v in candidates.values():
        final_score = alpha * v["semantic"] + (1 - alpha) * v["bm25"]
        final_results.append((v["doc"], final_score))

    # -----------------------------
    # 8. SORT + RETURN
    # -----------------------------
    final_results.sort(key=lambda x: x[1], reverse=True)

    print(f"✅ Returning top {k} results")

    return [doc for doc, score in final_results[:k]]