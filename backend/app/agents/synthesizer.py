def synthesize(question, evidence):
    if not evidence:
        return "I could not find relevant evidence in the uploaded documents. Please upload a relevant source or rephrase the question."
    # Evidence-first extractive response: no external model is silently simulated.
    selected = evidence[:3]
    lines = [e.text for e in selected]
    return "Based on the retrieved document passages:\n\n" + "\n\n".join(lines)
