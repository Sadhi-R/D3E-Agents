import os
import json
import torch
from uuid import uuid4
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from transformers import AutoTokenizer, AutoModel

# Configuration
QDRANT_HOST = "http://localhost:6333"  # Change to http://localhost if using local Qdrant
COLLECTION_NAME = "d3e_widgets"
CORE_PATH = "/root/d3e_widgets/CORE"

# Load tokenizer and model
print("🧠 Loading embedding model...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained("intfloat/e5-base-v2")
model = AutoModel.from_pretrained("intfloat/e5-base-v2", torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32).to(device)

# Generate description from widget name
def get_embedding_text(name):
    description = []
    lname = name.lower()
    if "checkbox" in lname: description.append("checkbox input")
    if "date" in lname: description.append("date input or picker")
    if "time" in lname: description.append("time input")
    if "label" in lname: description.append("text label")
    if "toggle" in lname: description.append("toggle switch")
    if "dropdown" in lname: description.append("dropdown selector")
    if "rating" in lname: description.append("rating bar")
    if "input" in lname: description.append("text input field")
    if "button" in lname: description.append("clickable button")
    if "search" in lname: description.append("search field")
    return f"{name}: {', '.join(description) if description else 'generic UI component'}"

# Compute embedding
def get_embedding(text):
    input_text = f"passage: {text}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        output = model(**inputs)
    embedding = output.last_hidden_state[:, 0]  # CLS token
    return embedding.squeeze().cpu().tolist()

# Find JSON files in directory
def find_json_files(root):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".json"):
                yield os.path.join(dirpath, filename)

# Main upsert function
def upsert_widgets():
    print("🔗 Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_HOST)

    files = list(find_json_files(CORE_PATH))
    print(f"📁 Found {len(files)} JSON files in {CORE_PATH}")

    for file_path in tqdm(files, desc="🚀 Processing and Upserting JSON files"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            widget_name = os.path.splitext(os.path.basename(file_path))[0]
            embedding_text = get_embedding_text(widget_name)
            vector = get_embedding(embedding_text)

            print(f"📌 Upserting '{widget_name}' ➜ '{embedding_text}'")

            point = PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload={
                    "name": widget_name,
                    "description": embedding_text,
                    "filename": widget_name,
                    "json": data
                }
            )

            client.upsert(collection_name=COLLECTION_NAME, points=[point])

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    upsert_widgets()
