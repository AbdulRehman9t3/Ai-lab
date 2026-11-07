import json
from task2_chunks import make_chunks
from lab6_search import Retriever

with open("corpus.json", encoding="utf-8") as f:
    docs = json.load(f)
with open("task2_labels.json", encoding="utf-8") as f:
    labels = json.load(f)

queries = [
    ("Can I get more time on my coursework if I was unwell?", "handbook"),
    ("My neighbour kept my box for a week and it turned out crushed. Is it too late to complain?", "returns"),
    ("I am locked out and cannot remember my login details. Will someone call me with a fix?", "it_help"),
]

records = make_chunks(docs, "sentence")

for backend in ["tfidf", "embedding"]:
    print("Backend:", backend)
    try:
        engine = Retriever(records, backend)
    except (ImportError, OSError) as e:
        print("  not run:", type(e).__name__, "-", e)
        print()
        continue
    for query, doc_id in queries:
        print("Query:", query)
        hits = engine.search(query, k=3)
        if not hits:
            print("  no matching records")
        for rank, (r, score) in enumerate(hits, 1):
            whole = r["doc"] == doc_id and labels[doc_id] in r["text"]
            print(f"  {rank}. {r['id']} chars {r['start']}-{r['end']} score={score:.3f} full evidence: {'yes' if whole else 'no'}")
            print("     ", r["text"])
        print()
