# Box NDA risk summary

A minimal, runnable reference app that turns a non-disclosure agreement (NDA) stored in Box into a **Deal Risk Summary**, and writes that summary back to Box as a companion file.

It takes a reliable, repeatable approach: **extract, don't prompt.** Instead of asking a model open-ended questions, it defines a fixed extraction schema so Box AI returns the same clauses in the same shape for every document. It uses **Box AI Extract** (`POST /2.0/ai/extract_structured`) with confidence scores and source references enabled, scores each clause with a small, transparent rule set, and uploads the result as JSON and markdown next to the original.

This is the companion repository to the tutorial [Build an NDA risk summary with Box AI Extract](https://developer.box.com/tutorials/nda-risk-summary).

> The risk scoring here is illustrative and intended for triage only. It is not legal advice and does not replace review by a qualified professional.

## What it does

| Capability | How |
| --- | --- |
| Authenticate as a service account | Client Credentials Grant (CCG) via `box-sdk-gen` |
| Extract five key clauses as typed fields | `POST /2.0/ai/extract_structured` with `include_confidence_score` and `include_reference` |
| Score each clause and build a summary | Plain, editable rules in `risk.py` |
| Save the summary back to Box | `POST /2.0/files/content` (uploads JSON + markdown companion files) |

The extracted clauses are: governing law, term, termination, confidentiality period, and liability cap.

## Project layout

```
box-nda-risk-summary/
├── app.py            # Runs extraction, builds the summary, uploads companion files
├── box_client.py     # CCG service account authentication
├── schema.py         # The clause extraction schema
├── extract.py        # Calls Box AI Extract with confidence + references
├── risk.py           # Scoring rules + markdown rendering
├── nda-sample.pdf    # A sample NDA you can upload to Box for testing
├── requirements.txt
├── .env.example
└── .gitignore
```

## Prerequisites

- **Python 3.11+**
- A [Box developer account](https://account.box.com/signup/developer), which gives you access to the Box AI API.
- A **Client Credentials Grant (CCG)** Platform App with **App + Enterprise Access**, the scopes **Read and write all files and folders stored in Box** and **Manage AI**, and the app **authorized** in the Admin Console.
- An NDA uploaded to Box (you can use `nda-sample.pdf`) and a folder where the summary is written. Note the **file ID** and **folder ID** from their URLs.

Because a CCG app authenticates as a separate **service account**, that account does not automatically have access to your content. Invite the service account email (Developer Console → **General Settings**) as a collaborator with the **Editor** role on both the folder that contains your NDA and the output folder. Without access, API calls return `404 Not Found`.

## Setup

1. **Clone and enter the project**

   ```bash
   git clone https://github.com/box-community/box-nda-risk-summary.git
   cd box-nda-risk-summary
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure credentials**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in `BOX_CLIENT_ID`, `BOX_CLIENT_SECRET`, and `BOX_ENTERPRISE_ID` from the Developer Console, plus `NDA_FILE_ID` and `OUTPUT_FOLDER_ID` from the file and folder URLs.

   > **Never commit `.env`.** It is already in `.gitignore`.

## Run

```bash
python3 app.py
```

The script prints the raw extraction (clause values, confidence scores, and source references), prints the Deal Risk Summary as markdown, and uploads two companion files to your output folder: `NDA-<file_id>-risk-summary.json` and `NDA-<file_id>-risk-summary.md`.

## How it works

Structured extraction declares the fields up front, so Box AI returns a consistent, typed JSON object keyed by your fields instead of free-form text that drifts between runs. Because the output is predictable, `risk.py` can score it with plain code:

- A missing clause is treated as high risk.
- An uncapped liability clause is high risk; a governing law outside the approved list is medium.
- Any clause extracted below the confidence threshold (0.70) is never treated as better than medium risk, and is flagged for human review.

Enabling **confidence scores** and **source references** on the extraction call lets you flag clauses that need a human's eyes and trace every value back to the exact snippet and location in the document.

## Customize

- Edit the fields in `schema.py` to match the clauses you care about (the same workflow applies to an MSA or most commercial contracts).
- Adjust `APPROVED_JURISDICTIONS`, the confidence threshold, or the clause-specific checks in `risk.py` to match your organization's playbook.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `invalid_client` | Check `BOX_CLIENT_ID` / `BOX_CLIENT_SECRET` / `BOX_ENTERPRISE_ID` in `.env`. |
| `App is not yet authorized for use` | Authorize the app in the Admin Console (Developer Console → Authorization → Review and Submit). |
| `404 Not Found` | Add the service account as an **Editor** collaborator on the NDA's folder and the output folder. |
| `confidence_score` or `reference` is empty | Confirm `include_confidence_score=True` and `include_reference=True` on the extraction call, and that the extraction agent runs on a confidence-capable model. |
| `ModuleNotFoundError` | Activate the virtual environment: `source .venv/bin/activate`. |

## License

MIT
