import json
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv(".env")

with open("data.json", "r") as f:
    data = json.load(f)

client = genai.Client()

employee_index = []

for key, emp in data.items():
    text = f"employee {emp['name']} {emp['role']} {emp['department']}"

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    embedding = np.array(
        result.embeddings[0].values,
        dtype=np.float32
    )

    employee_index.append({
        "key": key,
        "embedding": embedding
    })


np.save("employee_embeddings.npy", employee_index, allow_pickle=True)

print("Embeddings saved to employee_embeddings.npy")
