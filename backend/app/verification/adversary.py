import re

NEGATIONS = {"not", "never", "no", "cannot", "can't", "prohibited", "禁止"}
def normalize(s): return re.sub(r"[^a-z0-9 ]", " ", s.lower())

def challenge(evidence):
    findings = []
    for i, a in enumerate(evidence):
        wa = set(normalize(a.text).split())
        for b in evidence[i+1:]:
            wb = set(normalize(b.text).split())
            common = wa & wb
            # Flag as a candidate only; lexical signals do not prove contradiction.
            if len(common) >= 4 and bool(wa & NEGATIONS) != bool(wb & NEGATIONS):
                findings.append({"type": "possible_negation_conflict", "source_a": a.document.filename,
                                 "source_b": b.document.filename, "page_a": a.page_number,
                                 "page_b": b.page_number, "explanation": "Shared terms with differing negation signals. Manual/contextual review required."})
    return findings
