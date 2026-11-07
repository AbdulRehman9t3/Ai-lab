import json
import re
from task2_chunks import make_chunks

with open("corpus.json", encoding="utf-8") as f:
    docs = json.load(f)
with open("task2_labels.json", encoding="utf-8") as f:
    labels = json.load(f)

for doc_id, evidence in labels.items():
    assert evidence in docs[doc_id], doc_id

strategies = [("window, overlap 0", "0"), ("window, overlap 10", "10"),
              ("sentence, budget 40", "sentence")]
original_words = sum(len(t.split()) for t in docs.values())
print("Documents:", {k: len(v.split()) for k, v in docs.items()},
      "total words:", original_words)
print()

kept = {}
print(f"{'strategy':<22}{'chunks':>7}{'min':>5}{'avg':>6}{'max':>5}{'repeated':>10}{'evidence kept':>15}")
for name, strategy in strategies:
    chunks = make_chunks(docs, strategy)
    sizes = [len(c["text"].split()) for c in chunks]
    for c in chunks:
        assert c["text"] == docs[c["doc"]][c["start"]:c["end"]]
        assert c["text"].strip() and max(sizes) > 0
    assert max(sizes) <= 40
    repeated = sum(sizes) - original_words
    whole = {}
    for doc_id, evidence in labels.items():
        s = docs[doc_id].index(evidence)
        e = s + len(evidence)
        mine = [c for c in chunks if c["doc"] == doc_id]
        inside = [c["id"] for c in mine if c["start"] <= s and e <= c["end"]]
        touching = [c["id"] for c in mine if c["start"] < e and s < c["end"]]
        whole[doc_id] = (inside, touching)
    kept[name] = whole
    ok = sum(1 for v in whole.values() if v[0])
    print(f"{name:<22}{len(chunks):>7}{min(sizes):>5}{sum(sizes)/len(sizes):>6.1f}{max(sizes):>5}{repeated:>10}{ok:>10} of {len(whole)}")

print()
print("Evidence by document")
for name, _ in strategies:
    for doc_id, (inside, touching) in kept[name].items():
        if inside:
            print(f"  {name:<22}{doc_id:<10}kept whole in {inside[0]}")
        else:
            print(f"  {name:<22}{doc_id:<10}split across {', '.join(touching)}")

print()
print("Sentence splitter on abbreviations")
abbreviations = ("Dr.", "e.g.", "sec.")
for doc_id, text in docs.items():
    for m in re.finditer(r"[.!?]\s+", text):
        before = text[:m.end()].rstrip()
        if before.endswith(abbreviations):
            print(f"  {doc_id}: ...{before[-25:]} | {text[m.end():m.end()+25]}...")

print()
chunks = make_chunks(docs, "sentence")
ends = [c["id"] for c in chunks if c["text"].endswith(abbreviations)]
print("Sentence chunks ending on an abbreviation:", ends or "none")
for doc_id, text in docs.items():
    pieces = [c for c in chunks if c["doc"] == doc_id]
    print(f"  {doc_id}: {len(pieces)} chunks, words per chunk",
          [len(c["text"].split()) for c in pieces])
