import io
import os
import sys
from datetime import datetime
import pandas as pd
from google import genai
from google.genai import types
from loguru import logger
from dotenv import load_dotenv

now = datetime.now()
load_dotenv()

logger.remove()
logger.add(sink=sys.stdout, format="<level>{level}</level>: {message}", colorize=True)
df = pd.read_excel("data/pdfs.xlsx")


def generate(text: str):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"""generate structured q/a and relevent q/a pairs that can be used to fine tune a Large Language model, keys must be (question & answer). Q/a must be informational and not redundant, it must explain something about UWC(University of the Western Cape) or be in the context of the document

                         {text}

                    """
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.4,
        thinking_config=types.ThinkingConfig(
            thinking_budget=5103,
        ),
        response_mime_type="application/json",
    )

    response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response += chunk.text
    return response


if __name__ == "__main__":
    path_to_save_to = "data/fine_tune"
    if os.path.exists(path_to_save_to):
        pass
    else:
        os.mkdir(path_to_save_to)

    for pdf in df.iterrows():
        url = pdf[1]["url"]
        text = pdf[1]["text"]
        logger.debug(f"Genertaing Questions and Answers Pairs for {url}..")
        qa_pair = generate(text=text)
        pd.read_json(io.StringIO(qa_pair)).to_csv(
            f"{path_to_save_to}/{url}.csv", index=False
        )
