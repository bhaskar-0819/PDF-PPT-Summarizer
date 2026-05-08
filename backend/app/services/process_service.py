import os
import shutil

from app.services.file_service import load_and_decrypt
from app.services.parser_service import (
    extract_pdf_text,
    extract_ppt_text,
    extract_images_from_pdf,
    extract_images_from_ppt,
    extract_tables_from_ppt
)
from app.services.image_service import extract_text_from_image

# 🔥 ADD THIS (LLM)
from app.services.llm_service import summarize_text


TEMP_PATH = "temp"


# 🔥 Cleanup function
def cleanup_temp():
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH, ignore_errors=True)
    os.makedirs(TEMP_PATH, exist_ok=True)


def process_file(file_path: str):

    os.makedirs(TEMP_PATH, exist_ok=True)

    try:
        # 🔓 Step 1: Decrypt file
        decrypted = load_and_decrypt(file_path)

        # 📁 Step 2: Save temp file
        if file_path.endswith(".pdf.enc"):
            temp_file = os.path.join(TEMP_PATH, "temp.pdf")
        elif file_path.endswith(".pptx.enc"):
            temp_file = os.path.join(TEMP_PATH, "temp.pptx")
        else:
            raise ValueError("Unsupported file type")

        with open(temp_file, "wb") as f:
            f.write(decrypted)

        # =====================================================
        # 📄 PDF PROCESSING
        # =====================================================
        if file_path.endswith(".pdf.enc"):

            print("🔍 Processing PDF...")

            # 📝 TEXT
            text = extract_pdf_text(temp_file)
            print("✅ Text extracted length:", len(text))

            # 🖼️ IMAGES
            image_dir = os.path.join(TEMP_PATH, "pdf_images")
            image_paths = extract_images_from_pdf(temp_file, image_dir)

            print("🖼️ Total images found:", len(image_paths))

            image_texts = []

            for idx, img_path in enumerate(image_paths[:3]):  # limit for speed
                try:
                    print(f"📸 Processing image {idx+1}: {img_path}")
                    img_text = extract_text_from_image(img_path)
                    image_texts.append(img_text)

                except Exception as e:
                    print("❌ Image processing failed:", str(e))
                    continue

            # 🔗 COMBINE
            full_content = text

            if image_texts:
                full_content += "\n\n--- IMAGE INSIGHTS ---\n\n"
                full_content += "\n\n".join(image_texts)

            print("✅ Final combined content length:", len(full_content))

            # 🔥 SUMMARY
            summary = summarize_text(full_content)

            return {
                "content": full_content,
                "summary": summary
            }

        # =====================================================
        # 📊 PPT PROCESSING
        # =====================================================
        elif file_path.endswith(".pptx.enc"):

            print("📊 Processing PPT...")

            # 📝 TEXT
            text = extract_ppt_text(temp_file)
            print("✅ PPT text length:", len(text))

            # 📊 TABLES
            try:
                table_text = extract_tables_from_ppt(temp_file)
                print("📊 PPT tables length:", len(table_text))
            except Exception as e:
                print("⚠️ PPT table extraction failed:", str(e))
                table_text = ""

            # 🖼️ IMAGES
            image_dir = os.path.join(TEMP_PATH, "ppt_images")
            image_paths = extract_images_from_ppt(temp_file, image_dir)

            print("🖼️ PPT images found:", len(image_paths))

            image_texts = []

            for idx, img_path in enumerate(image_paths[:3]):
                try:
                    print(f"📸 Processing PPT image {idx+1}: {img_path}")
                    img_text = extract_text_from_image(img_path)
                    image_texts.append(img_text)

                except Exception as e:
                    print("❌ PPT image processing failed:", str(e))
                    continue

            # 🔗 COMBINE
            full_content = text

            if table_text:
                full_content += "\n\n--- TABLE DATA ---\n\n" + table_text

            if image_texts:
                full_content += "\n\n--- IMAGE INSIGHTS ---\n\n"
                full_content += "\n\n".join(image_texts)

            print("✅ Final PPT content length:", len(full_content))

            # 🔥 SUMMARY
            summary = summarize_text(full_content)

            return {
                "content": full_content,
                "summary": summary
            }

        else:
            raise ValueError("Unsupported file type")

    finally:
        # 🔥 Always clean temp
        cleanup_temp()