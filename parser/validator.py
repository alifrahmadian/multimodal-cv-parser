def ensure_schema(data):
    default = {
        "nama": "",
        "experience": [],
        "education": [],
        "skills": {
            "softskills": [],
            "hardskills": []
        }
    }

    if not isinstance(data, dict):
        return default

    for key in default:
        if key not in data:
            data[key] = default[key]

    return data