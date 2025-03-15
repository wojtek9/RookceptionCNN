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


def board_to_fen(board_state, turn="w", castling_rights="-", en_passant="-", halfmove="0", fullmove="1"):
    """Convert board state (8x8 numpy array) into FEN string."""
    # Map CNN labels to chess symbols
    piece_map = {
        "bP": "p", "bN": "n", "bB": "b", "bR": "r", "bQ": "q", "bK": "k",
        "wP": "P", "wN": "N", "wB": "B", "wR": "R", "wQ": "Q", "wK": "K",
        "empty": "1"
    }
    fen_rows = []

    for row in board_state:
        fen_row = ""
        empty_count = 0

        for square in row:
            piece = piece_map[square]

            if piece == "1":  # Empty square
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += piece

        if empty_count > 0:
            fen_row += str(empty_count)

        fen_rows.append(fen_row)

    fen_board = "/".join(fen_rows)
    fen = f"{fen_board} {turn} {castling_rights} {en_passant} {halfmove} {fullmove}"
    return fen