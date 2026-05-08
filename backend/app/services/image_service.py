from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_image(image_path: str):
    """
    Uses GPT-4o mini to extract structured insights from image
    """

    # Convert image to base64
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Proper data URL
    image_data_url = f"data:image/png;base64,{base64_image}"

    # 🔥 Improved prompt
    prompt = """
    Analyze this image carefully and provide structured output:

    1. If this is a chart/graph:
       - Explain trends
       - Mention key numbers/values
       - Highlight insights

    2. If this is a diagram:
       - Explain the concept clearly in simple terms

    3. If this contains text:
       - Extract all readable text

    4. If it's a UI/dashboard/screenshot:
       - Describe key elements and what they represent

    Keep the answer concise but informative.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url
                    }
                ]
            }
        ]
    )

    return response.output_text