from core.transformers.json_to_text_transformer import JsonToTextTransformer

# Map (from_type, to_type) -> transformer instance
_TRANSFORMERS = {
    ("json", "text"): JsonToTextTransformer(),
}


def get_transformer(from_type: str, to_type: str):
    return _TRANSFORMERS.get((from_type, to_type))
