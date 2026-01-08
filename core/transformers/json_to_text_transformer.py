import json
from core.transformers.base_transformer import Transformer


class JsonToTextTransformer(Transformer):
    """
    Converts normalized JSON data:
        {"type": "json", "data": ...}
    into normalized text:
        {"type": "text", "content": "..."}
    """

    def transform(self, data: dict) -> dict:
        if data.get("type") != "json":
            raise ValueError("JsonToTextTransformer expects data type 'json'")

        obj = data.get("data")

        # Pretty-print JSON safely
        text = json.dumps(obj, indent=2, ensure_ascii=False)

        return {"type": "text", "content": text}
