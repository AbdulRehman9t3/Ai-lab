import re

def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    result = []
    for i in range(0, len(spans), size-overlap):
        j = min(i+size, len(spans))
        result.append((offset+spans[i][0], offset+spans[j-1][1]))
        if j == len(spans):
            break
    return result

def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive")
    cuts = [0] + [m.end() for m in
                  re.finditer(r"[.!?]\s+", text)] + [len(text)]
    out, pending, count = [], None, 0
    for a, b in zip(cuts, cuts[1:]):
        b = a + len(text[a:b].rstrip())
        n = len(text[a:b].split())
        if not n:
            continue
        if n > size:
            if pending is not None:
                out.append(pending)
            out.extend(windows(text[a:b], size, 0, a))
            pending, count = None, 0
        elif pending is not None and count+n <= size:
            pending, count = (pending[0], b), count+n
        else:
            if pending is not None:
                out.append(pending)
            pending, count = (a, b), n
    if pending is not None:
        out.append(pending)
    return out

def make_chunks(docs, strategy):
    result = []
    for doc_id, text in docs.items():
        spans = (sentence_chunks(text) if strategy == "sentence"
                 else windows(text, 40, int(strategy)))
        for i, (a, b) in enumerate(spans):
            result.append(dict(id=f"{doc_id}:{i}", doc=doc_id,
                               start=a, end=b, text=text[a:b]))
    return result

if __name__ == "__main__":
    assert windows("") == []
    assert sentence_chunks("") == []
    assert windows("short text") == [(0, 10)]
    assert sentence_chunks("short text") == [(0, 10)]
    for bad in [(2, 2), (2, -1), (0, 0)]:
        try:
            windows("a b", *bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid size/overlap was accepted")
    long = " ".join(["word"]*95) + "."
    pieces = sentence_chunks(long)
    assert len(pieces) == 3
    assert all(len(long[a:b].split()) <= 40 for a, b in pieces)
    docs = {"example": "Reset your password. Keep recovery codes private."}
    for strategy in ["0", "10", "sentence"]:
        for c in make_chunks(docs, strategy):
            assert c["text"] == docs[c["doc"]][c["start"]:c["end"]]
            print(strategy, c)
    print("task2_chunks tests passed")
