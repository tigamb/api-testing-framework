POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
    "additionalProperties": False,
}

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "phone", "website", "company"],
    "properties": {
        "id":       {"type": "integer"},
        "name":     {"type": "string"},
        "username": {"type": "string"},
        "email":    {"type": "string"},
        "address": {
            "type": "object",
            "required": ["street", "suite", "city", "zipcode", "geo"],
        },
        "phone":   {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "required": ["name", "catchPhrase", "bs"],
        },
    },
}

COMMENT_SCHEMA = {
    "type": "object",
    "required": ["id", "postId", "name", "email", "body"],
    "properties": {
        "id":     {"type": "integer"},
        "postId": {"type": "integer"},
        "name":   {"type": "string"},
        "email":  {"type": "string"},
        "body":   {"type": "string"},
    },
    "additionalProperties": False,
}
