import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from stockfish import Stockfish
from src.cnn.BoardRecognizer import BoardRecognizer
from src.misc import utils
import numpy as np
from pydantic import BaseModel

# Path to Stockfish executable
STOCKFISH_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\stockfish\stockfish-windows-x86-64-avx2.exe"

# Initialize FastAPI and Stockfish
app = FastAPI()
stockfish = Stockfish(STOCKFISH_PATH)
model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
recognizer = BoardRecognizer(model_path=model_path)  # Load trained model

class ImageRequest(BaseModel):
    image_path: str

@app.post("/analyze/")
async def analyze_chessboard(request: ImageRequest):
    """
    Analyzes a chessboard image from a local file path and returns the best move.
    """
    try:
        image_path = request.image_path  # Extract the path
        print(f"Received image path: {image_path}")

        # Open image from the provided path
        img = Image.open(image_path).convert("RGB")  # Load image from path

        # Convert PIL image to NumPy array
        image_array = np.array(img) / 255.0  # Normalize pixel values

        # Predict board state using CNN model
        board_state = recognizer.predict_board(image_array)

        # Convert board state to FEN notation
        fen = utils.board_to_fen(board_state)

        # Set Stockfish position
        stockfish.set_fen_position(fen)

        # Get best move from Stockfish
        best_move = stockfish.get_best_move()

        return {
            "fen": fen,
            "best_move": best_move
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/test/")
async def test_connection(message: str):
    return {"response": message}

print("ChessAPI is running and registering endpoints...")
print("Registered Endpoints:", [route.path for route in app.routes])
