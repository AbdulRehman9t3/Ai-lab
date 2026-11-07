import sys
from guided_chatbot import build_bot
backend = sys.argv[1] if len(sys.argv) > 1 else "tfidf"
engine = build_bot(backend)
query = "assignment upload"
print("Suggested questions:")
for record, score in engine.search(query, k=3):
    if score > 0:
        print(record["question"], f"({score:.3f})")
