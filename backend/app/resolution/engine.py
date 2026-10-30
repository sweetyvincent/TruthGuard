def resolve(findings):
    if not findings:
        return {"status": "NO_CONFLICT_DETECTED", "decision": "No candidate contradiction was detected by the current lexical checks. This is not proof that the sources agree."}
    return {"status": "UNRESOLVED", "decision": "Potential disagreement detected. The available metadata does not establish which source takes precedence; do not choose automatically.", "reason": "No verified authority, effective-date, scope, or supersession metadata is available in this MVP."}
