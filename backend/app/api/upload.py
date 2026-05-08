import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List

from app.services.file_service import save_file
from app.services.process_service import process_file
from app.services.embedding_service import create_vector_store
from app.services.llm_service import summarize_text   # 🔥 NEW
from app.utils.validators import validate_file

router = APIRouter()


# ----------------------------------------------------
# ✅ SINGLE FILE UPLOAD + SHAREPOINT SUPPORT
# ----------------------------------------------------
@router.post("/upload")
async def upload_file(
    user_id: str,
    file: UploadFile = File(None),
    file_name: str = Form(None),
    detail_level: str = "Standard"   # 🔥 NEW
):

    try:
        # =====================================================
        # ✅ CASE 1: NORMAL FILE UPLOAD → uploaded_files
        # =====================================================
        if file:

            content = await file.read()

            validate_file(file.filename, len(content))

            # Save encrypted
            file_path = save_file(user_id, file.filename, content)

            # Process file (extract text)
            result = process_file(file_path)
            extracted_text = result["content"]

            # 🔥 NEW: Use updated summarizer
            summary = summarize_text(extracted_text, detail_level)

            # Create vector DB
            create_vector_store(
                [extracted_text],
                user_id,
                [file.filename]
            )

            return {
                "message": "File uploaded, vectorized & summarized",
                "summary": summary
            }

        # =====================================================
        # 🔥 CASE 2: SHAREPOINT FILE → sharepoint_files
        # =====================================================
        elif file_name:

            if not file_name.endswith(".enc"):
                file_name = file_name + ".enc"

            file_path = os.path.join(
                "storage",
                f"user_{user_id}",
                "sharepoint_files",
                file_name
            )

            print("Looking for SharePoint file:", file_path)

            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"File not found: {file_path}"
                )

            result = process_file(file_path)
            extracted_text = result["content"]

            # 🔥 NEW
            summary = summarize_text(extracted_text, detail_level)

            create_vector_store(
                [extracted_text],
                user_id,
                [file_name]
            )

            return {
                "message": "SharePoint file processed & summarized",
                "summary": summary
            }

        else:
            raise HTTPException(status_code=400, detail="No file provided")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )


# ----------------------------------------------------
# 🔥 MULTIPLE FILE UPLOAD → uploaded_files
# ----------------------------------------------------
@router.post("/upload-multiple")
async def upload_multiple(
    user_id: str,
    files: List[UploadFile] = File(...),
    detail_level: str = "Standard"  # 🔥 NEW
):

    summaries = {}
    texts = []
    file_names = []

    try:
        for file in files:

            content = await file.read()

            try:
                validate_file(file.filename, len(content))
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename}: {str(e)}"
                )

            file_path = save_file(user_id, file.filename, content)

            result = process_file(file_path)
            extracted_text = result["content"]

            # 🔥 NEW summarization
            summary = summarize_text(extracted_text, detail_level)

            texts.append(extracted_text)
            file_names.append(file.filename)

            summaries[file.filename] = summary

        create_vector_store(texts, user_id, file_names)

        return {
            "message": "All files uploaded, vectorized & summarized",
            "file_summaries": summaries
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing error: {str(e)}"
        )