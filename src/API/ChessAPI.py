import os
import sys

from src.API.Engine import Engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from fastapi import FastAPI
from src.cnn.BoardRecognizer import BoardRecognizer
from pydantic import BaseModel, Field
from typing import Optional
import time

# Initialize FastAPI and Stockfish
app = FastAPI()
engine = Engine()
model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
recognizer = BoardRecognizer(model_path=model_path)  # Load trained model


class ImageRequest(BaseModel):
    image_path: Optional[str] = Field(None, description="Path to the local chessboard image")
    turn: Optional[str] = Field(None, description="Turn ('w' for white, 'b' for black')")
    castling_rights: Optional[str] = Field("-", description="Castling rights (e.g., 'KQkq' or '-')")
    en_passant: Optional[str] = Field("-", description="En passant target square (e.g., 'e3' or '-')")
    halfmove: Optional[int] = Field(0, description="Halfmove clock for the fifty-move rule")
    fullmove: Optional[int] = Field(1, description="Full move number")

    @classmethod
    def validate_request(cls, data):
        """ Ensure either image_path OR turn is provided. """
        if not data.get("image_path") and not data.get("turn"):
            raise ValueError("Either 'image_path' or 'turn' must be provided.")
        if data.get("turn") and data["turn"] not in {"w", "b"}:
            raise ValueError("'turn' must be either 'w' or 'b'.")
        return cls(**data)


@app.post("/analyze/")
async def analyze_chessboard(request: ImageRequest):
    """
    Analyzes a chess position based on an image and game state.
    Returns the best move as a string and logs execution time.
    """
    start_time = time.time()

    try:
        best_move = None
        if request.image_path and request.turn:
            # Predict board state using CNN model
            board_state = recognizer.predict_board(request.image_path)
            # Get best move
            best_move = engine.get_next_move(board_state, request.turn)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Request processed in {execution_time:.4f} seconds")

        return {"best_move": best_move, "execution_time": f"{execution_time:.4f} seconds"}

    except Exception as e:
        return {"error": f"API Exception: {str(e)}"}


@app.get("/test/")
async def test_connection(message: str):
    return {"response": message}


print("ChessAPI is running and registering endpoints...")
print("Registered Endpoints:", [route.path for route in app.routes])
