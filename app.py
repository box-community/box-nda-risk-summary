import io
import json
import os

from dotenv import load_dotenv
from box_sdk_gen import UploadFileAttributes, UploadFileAttributesParentField

from box_client import get_box_client
from extract import extract_clauses
from risk import build_risk_summary, to_markdown

load_dotenv()

def upload_companion_file(client, folder_id: str, name: str, content: str) -> str:
    files = client.uploads.upload_file(
        attributes=UploadFileAttributes(
            name=name,
            parent=UploadFileAttributesParentField(id=folder_id),
        ),
        file=io.BytesIO(content.encode("utf-8")),
    )
    return files.entries[0].id

if __name__ == "__main__":
    file_id = os.getenv("NDA_FILE_ID")
    folder_id = os.getenv("OUTPUT_FOLDER_ID")

    extraction = extract_clauses(file_id)
    print("Raw extraction:")
    print(json.dumps(extraction, indent=2))

    summary = build_risk_summary(extraction, document=f"NDA-{file_id}")
    markdown = to_markdown(summary)

    print("\nDeal Risk Summary:")
    print(markdown)

    client = get_box_client()
    json_id = upload_companion_file(
        client, folder_id, f"{summary['document']}-risk-summary.json",
        json.dumps(summary, indent=2),
    )
    md_id = upload_companion_file(
        client, folder_id, f"{summary['document']}-risk-summary.md", markdown,
    )

    print(f"\nUploaded JSON summary (file ID {json_id}) and markdown summary (file ID {md_id}).")
