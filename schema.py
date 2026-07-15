from box_sdk_gen import CreateAiExtractStructuredFields

EXTRACTION_FIELDS = [
    CreateAiExtractStructuredFields(
        key="governing_law",
        display_name="Governing law",
        type="string",
        prompt="The governing law or jurisdiction that applies to the agreement.",
    ),
    CreateAiExtractStructuredFields(
        key="term",
        display_name="Term",
        type="string",
        prompt="The overall duration of the agreement, including any renewal terms.",
    ),
    CreateAiExtractStructuredFields(
        key="termination",
        display_name="Termination",
        type="string",
        prompt="The termination conditions, including any required notice period.",
    ),
    CreateAiExtractStructuredFields(
        key="confidentiality_period",
        display_name="Confidentiality period",
        type="string",
        prompt="How long confidentiality obligations remain in effect after termination.",
    ),
    CreateAiExtractStructuredFields(
        key="liability_cap",
        display_name="Liability cap",
        type="string",
        prompt="The limitation of liability or liability cap, including any amount and currency.",
    ),
]
