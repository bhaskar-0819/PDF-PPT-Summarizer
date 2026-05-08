from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from app.services.retrieval_service import hybrid_search
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

router = APIRouter()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simple in-memory chat history (per user)
chat_memory = {}

# Request model
class ChatRequest(BaseModel):
    user_id: str
    query: str


@router.post("/chat")
def chat_with_doc(request: ChatRequest):

    user_id = request.user_id
    query = request.query

    try:
        db_path = f"storage/user_{user_id}/db"

        if not os.path.exists(db_path):
            raise HTTPException(status_code=404, detail="No document found for this user")

        # 🔥 Hybrid retrieval
        docs = hybrid_search(query, user_id)

        if not docs:
            return {"answer": "Not enough information found in document."}

        # Build context
        context = "\n\n".join([doc.page_content for doc in docs])

        # 🔥 Chat memory (last 3 queries)
        history = chat_memory.get(user_id, [])
        history.append(query)
        chat_memory[user_id] = history[-3:]
        history_text = "\n".join(chat_memory[user_id])

        # 🔥 Improved prompt
        prompt = f"""
        You are an AI assistant answering questions from a document.

        Rules:
        - Answer ONLY from the provided context
        - If answer is not present, say "Not found in document"
        - Be clear, structured, and concise
        - Use bullet points if helpful
        - If question relates to charts/images, include visual insights

        Conversation History:
        {history_text}

        Context:
        {context}

        Question:
        {query}
        """

        # LLM call
        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        # 🔥 Source attribution WITH file names
        sources = []
        for doc in docs:
            sources.append({
                "content": doc.page_content[:200],
                "file": doc.metadata.get("source", "unknown")  # 🔥 KEY LINE
            })

        return {
            "answer": response.output_text,
            "sources": sources,
            "context_preview": context[:300]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))