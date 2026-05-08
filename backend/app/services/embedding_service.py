import os
import shutil
import gc
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


# 🔥 FAST DELETE
def safe_delete(path: str):
    if not os.path.exists(path):
        return

    print("🧹 Removing old DB...")

    try:
        gc.collect()
        shutil.rmtree(path, ignore_errors=True)
        print("✅ Old DB removed instantly")

    except Exception as e:
        print(f"⚠️ Delete issue: {e}")


# 🔥 IMPROVED HIERARCHICAL CHUNKING
def split_text_hierarchical(text: str, file_name: str):

    # Step 1: Split into logical sections
    sections = text.split("\n\n")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    docs = []

    for section in sections:
        section = section.strip()

        if not section or len(section) < 50:
            continue

        chunk_docs = splitter.create_documents(
            [section],
            metadatas=[{"source": file_name}]
        )

        docs.extend(chunk_docs)

    return docs


def create_vector_store(texts: list, user_id: str, file_names: list):

    print("🔄 Preparing documents for embedding...")

    all_docs = []

    # 🔥 Step 1: Chunk all files
    for text, file_name in zip(texts, file_names):
        docs = split_text_hierarchical(text, file_name)
        all_docs.extend(docs)

    print(f"📄 Total chunks created: {len(all_docs)}")

    # 🔥 Step 2: Initialize embeddings (only once)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    db_path = f"storage/user_{user_id}/db"

    # 🔥 Step 3: Clean old DB
    safe_delete(db_path)

    print("🆕 Creating fresh vector DB...")
    os.makedirs(db_path, exist_ok=True)

    # 🔥 Step 4: Create FAISS index
    db = FAISS.from_documents(all_docs, embeddings)

    # 🔥 Step 5: Save DB
    db.save_local(db_path)

    print("✅ Vector DB created successfully")

    return "Vector DB reset & created"