CLAUSES = [
    "governing_law",
    "term",
    "termination",
    "confidentiality_period",
    "liability_cap",
]

APPROVED_JURISDICTIONS = ["delaware", "new york", "california", "england"]

SEVERITY_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}

def assess_clause(key: str, value, confidence: dict):
    # A missing clause is the highest risk: it could not be located in the document.
    if not value:
        return "high", "Clause not found. Review the document manually."

    severity, note = "low", "Clause found."

    if key == "liability_cap" and any(
        term in value.lower() for term in ["unlimited", "no cap", "not limited"]
    ):
        severity, note = "high", "Liability appears to be uncapped."
    elif key == "governing_law" and not any(
        j in value.lower() for j in APPROVED_JURISDICTIONS
    ):
        severity, note = "medium", "Governing law is outside the approved list."

    # A low-confidence extraction is never treated as better than medium risk.
    score = (confidence or {}).get("score", 1)
    if score < 0.7 and SEVERITY_ORDER[severity] < SEVERITY_ORDER["medium"]:
        severity = "medium"
        note = f"{note} Low extraction confidence ({score:.2f}); verify against the source."

    return severity, note

def build_risk_summary(extraction: dict, document: str) -> dict:
    answer = extraction["answer"]
    scores = extraction["confidence_score"]
    references = extraction["reference"]

    findings = []
    for key in CLAUSES:
        value = answer.get(key)
        confidence = scores.get(key)
        severity, note = assess_clause(key, value, confidence)
        findings.append({
            "clause": key,
            "value": value,
            "severity": severity,
            "note": note,
            "confidence": confidence,
            "source": references.get(key),
        })

    overall = max(findings, key=lambda f: SEVERITY_ORDER[f["severity"]])["severity"]
    return {"document": document, "overall_risk": overall, "findings": findings}

def to_markdown(summary: dict) -> str:
    lines = [
        f"# Deal Risk Summary: {summary['document']}",
        "",
        f"**Overall risk:** {summary['overall_risk'].upper()}",
        "",
        "> Generated automatically for triage only. This is not legal advice.",
        "",
        "| Clause | Value | Risk | Confidence | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for f in summary["findings"]:
        level = f["confidence"]["level"] if f["confidence"] else "N/A"
        value = f["value"] or "_Not found_"
        clause = f["clause"].replace("_", " ").title()
        lines.append(
            f"| {clause} | {value} | {f['severity'].upper()} | {level} | {f['note']} |"
        )
    return "\n".join(lines)
