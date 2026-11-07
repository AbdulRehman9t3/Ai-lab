import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944 version 2.1",
    "",
    "یہ ایک مثال ہے",
    "کِتاب",
]

for text in samples:
    ws = text.split()
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    print("Original:  ", repr(text))
    print("Whitespace:", ws, len(ws))
    print("Word-like: ", words, len(words))
    print()

assert re.findall(r"\b\w+\b", "") == []

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2",
                                device="cpu")
except Exception as e:
    print("Model tokenizer not available:", type(e).__name__)
else:
    for text in samples[:2]:
        print("Model subwords:", text, model.tokenizer.tokenize(text))
