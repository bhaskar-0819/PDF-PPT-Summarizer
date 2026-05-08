from fastapi import APIRouter, HTTPException
from app.services.file_service import (
    ingest_local_files,
    list_user_files,
    list_uploaded_files   # ✅ NEW
)

router = APIRouter()


# =====================================================
# 🔗 SYNC SHAREPOINT FILES
# =====================================================
@router.api_route("/sync-sharepoint", methods=["GET", "POST"])
def sync_files(user_id: str = "1"):
    try:
        files = ingest_local_files(user_id)

        return {
            "status": "success",
            "message": "Sync completed",
            "files_synced_count": len(files),
            "synced_files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 📂 GET SHAREPOINT FILES (FOR UI)
# =====================================================
@router.get("/user-files")
def get_user_files(user_id: str = "1"):
    try:
        files = list_user_files(user_id)   # ✅ now reads sharepoint_files/

        return {
            "status": "success",
            "files_count": len(files),
            "files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================================
# 📤 GET UPLOADED FILES (OPTIONAL UI)
# =====================================================
@router.get("/uploaded-files")
def get_uploaded_files(user_id: str = "1"):
    try:
        files = list_uploaded_files(user_id)

        return {
            "status": "success",
            "files_count": len(files),
            "files": files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))