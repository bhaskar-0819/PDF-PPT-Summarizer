ALLOWED_EXTENSIONS = [".pdf", ".pptx"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_file(filename: str, size: int):
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise ValueError("Invalid file type")

    if size > MAX_FILE_SIZE:
        raise ValueError("File too large")