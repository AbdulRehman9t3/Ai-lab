# Lab 6: Tokenization, Chunking and Semantic Suggestions (Tasks 1 and 2)

Rasikh Ali, 42365. This folder covers Task 1 and Task 2 only. Task 3 files are not included.

## Setup

```
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell
source .venv/bin/activate           # macOS or Linux
python -m pip install numpy scikit-learn sentence-transformers
python -m pip freeze > requirements.txt
```

The first run of the embedding backend downloads `sentence-transformers/all-MiniLM-L6-v2`, so it needs internet once. TF-IDF needs no download. Run every command from this folder.

## Task 1

```
python task1_tokens.py
python task1_chatbot_check.py
python guided_chatbot.py
```

`task1_tokens.py` compares whitespace splitting with the word-like regex on seven inputs and then, if the model can be loaded, prints the model's subword tokens for two of them. `guided_chatbot.py` is the FAQ bot with two added FAQs (campus Wi-Fi and semester fee), each with a source file name. Type `exit` to stop it.

## Task 2

```
python task2_chunks.py
python guided_chunks.py
python task2_boundaries.py
python task2_semantic_check.py
python guided_embeddings.py
python guided_suggestions.py embedding
```

`corpus.json` holds three synthetic documents of 188 to 222 words. `task2_labels.json` holds the exact evidence text for each one. `task2_boundaries.py` compares 40-word windows (overlap 0 and 10) with sentence packing (budget 40). `task2_semantic_check.py` builds records from the sentence chunks and runs three paraphrased queries on TF-IDF and on the embedding backend. If the embedding library or model is missing it prints "not run" and carries on.

## Outputs

The `outputs` folder has the saved output of each script, including the chatbot transcript. `embedding_not_run.txt` is the real error from `guided_embeddings.py` in the environment used to produce these files, where sentence-transformers was not installed. No embedding results are included. Run the embedding commands above on a machine with the library installed and add those results to the report.

## Source and changes

Taken from the lab manual with small changes: `lab6_search.py` (unchanged), `guided_chatbot.py` (two FAQs added), `task2_chunks.py` (sentence chunks end at the last word instead of keeping trailing spaces, plus extra edge-case tests), `guided_chunks.py`, `guided_embeddings.py`, `guided_suggestions.py` (takes the backend as an optional argument), `task1_tokens.py` (extra samples, UTF-8 output, model section skipped if the model is not available).

Written for this lab: `corpus.json`, `task2_labels.json`, `task2_boundaries.py`, `task2_semantic_check.py`. All documents and FAQs are made up for the lab and are not real policies. Outputs were produced with Python 3.13.18, numpy 2.5.3 and scikit-learn 1.9.1.
