import json


def get_all_fens(json_path: str) -> list:
    """Fetches all FEN strings from a JSON file and returns them as a list."""
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [entry["fen"] for entry in data.values() if "fen" in entry]

    except FileNotFoundError:
        print(f"Error: File not found - {json_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        return []