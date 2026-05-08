import os
from app.utils.encryption import encrypt_data, decrypt_data

BASE_PATH = "storage"

# =====================================================
# 📤 SAVE UPLOADED FILES (SEPARATE FOLDER)
# =====================================================
def save_file(user_id: str, filename: str, data: bytes):

    user_folder = os.path.join(BASE_PATH, f"user_{user_id}", "uploaded_files")
    os.makedirs(user_folder, exist_ok=True)

    encrypted = encrypt_data(data)

    file_path = os.path.join(user_folder, filename + ".enc")

    with open(file_path, "wb") as f:
        f.write(encrypted)

    return file_path


# =====================================================
# 🔓 LOAD + DECRYPT (COMMON)
# =====================================================
def load_and_decrypt(file_path: str):
    with open(file_path, "rb") as f:
        encrypted = f.read()

    return decrypt_data(encrypted)


# =====================================================
# 🔗 SHAREPOINT SYNC (SEPARATE FOLDER)
# =====================================================
WATCH_FOLDER = r"C:\Users\BhaskarS\OneDrive - TheMathCompany Private Limited\EISAI Account - Documents\Doc Summarize"


def ingest_local_files(user_id: str):
    """
    Reads files from synced SharePoint folder
    and stores them in sharepoint_files (encrypted)
    """
    saved_files = []

    user_folder = os.path.join(BASE_PATH, f"user_{user_id}", "sharepoint_files")
    os.makedirs(user_folder, exist_ok=True)

    existing_files = os.listdir(user_folder)

    for filename in os.listdir(WATCH_FOLDER):

        if not filename.lower().endswith((".pdf", ".pptx")):
            continue

        # 🔥 Skip duplicates
        if filename + ".enc" in existing_files:
            continue

        file_path = os.path.join(WATCH_FOLDER, filename)

        try:
            with open(file_path, "rb") as f:
                data = f.read()

            encrypted = encrypt_data(data)

            saved_path = os.path.join(user_folder, filename + ".enc")

            with open(saved_path, "wb") as f:
                f.write(encrypted)

            saved_files.append({
                "original_name": filename,
                "stored_path": saved_path
            })

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    return saved_files


# =====================================================
# 📂 LIST SHAREPOINT FILES ONLY (FOR UI)
# =====================================================
def list_user_files(user_id: str):

    user_folder = os.path.join(BASE_PATH, f"user_{user_id}", "sharepoint_files")

    if not os.path.exists(user_folder):
        return []

    return os.listdir(user_folder)


# =====================================================
# 📂 (OPTIONAL) LIST UPLOADED FILES
# =====================================================
def list_uploaded_files(user_id: str):

    user_folder = os.path.join(BASE_PATH, f"user_{user_id}", "uploaded_files")

    if not os.path.exists(user_folder):
        return []

    return os.listdir(user_folder)