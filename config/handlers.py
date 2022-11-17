import json


def load_json(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }
    except json.JSONDecodeError:
        return {
            "file": "",
            "column": "",
            "data": "",
            "bins": "",
            "imgname": "histogram",
        }


def update_file(filepath: str, data: dict) -> None:
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
