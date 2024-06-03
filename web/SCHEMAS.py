input_schema = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "options": {
            "type": "object",
            "properties": {
                "multilabel": {"type": "boolean"},
                "show_reasoning": {"type": "boolean"}
            },
            "required": ["multilabel"]
        },
        "classes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "class_id": {"type": "string"},
                    "class_name": {"type": "string"},
                    "class_description": {"type": "string"}
                },
                "required": ["class_id", "class_name", "class_description"]
            }
        }
    },
    "required": ["query", "options", "classes"]
}
