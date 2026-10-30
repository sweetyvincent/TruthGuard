import re
from collections import Counter

def terms(s): return re.findall(r"[a-z0-9]+", s.lower())

def retrieve(question, chunks, limit=8):
    q = Counter(terms(question))
    scored = []
    for c in chunks:
        words = Counter(terms(c.text))
        overlap = sum(min(v, words[k]) for k, v in q.items())
        # Simple transparent lexical baseline; replaceable with BM25/vector retrieval.
        score = overlap / max(1, sum(q.values()))
        if score > 0: scored.append((score, c))
    return sorted(scored, key=lambda x: x[0], reverse=True)[:limit]
