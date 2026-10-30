from types import SimpleNamespace
from app.retrieval.search import retrieve
from app.resolution.engine import resolve

def test_retrieval_finds_matching_chunk():
    d = SimpleNamespace(filename="policy.txt")
    c = SimpleNamespace(text="Employees may request annual leave after six months.", document=d, page_number=1)
    assert retrieve("annual leave six months", [c])[0][1] is c

def test_resolution_abstains_on_conflict():
    out = resolve([{"type": "possible_negation_conflict"}])
    assert out["status"] == "UNRESOLVED"
