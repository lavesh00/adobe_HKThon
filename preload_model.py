# preload_model.py
from transformers import AutoTokenizer, AutoModel

print("📦 Pre-downloading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("✅ Model and tokenizer downloaded & cached.")
