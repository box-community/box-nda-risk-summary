from box_sdk_gen import AiItemBase

from box_client import get_box_client
from schema import EXTRACTION_FIELDS

def extract_clauses(file_id: str) -> dict:
    client = get_box_client()

    response = client.ai.create_ai_extract_structured(
        items=[AiItemBase(id=file_id)],
        fields=EXTRACTION_FIELDS,
        include_confidence_score=True,
        include_reference=True,
    )

    return {
        "answer": response.answer or {},
        "confidence_score": response.confidence_score or {},
        "reference": response.reference or {},
    }
