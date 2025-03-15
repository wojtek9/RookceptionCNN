from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from stockfish import Stockfish
from cnn.BoardRecognizer import BoardRecognizer
from misc import utils

# Path to Stockfish executable
STOCKFISH_PATH = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\stockfish\stockfish-windows-x86-64-avx2.exe"

# Initialize FastAPI and Stockfish
app = FastAPI()
stockfish = Stockfish(STOCKFISH_PATH)
model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
recognizer = BoardRecognizer(model_path=model_path)  # Load trained model

@app.post("/analyze/")
async def analyze_chessboard(image: UploadFile = File(...)):
    try:
        # Convert uploaded file to PIL image
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Predict board state using CNN model
        board_state = recognizer.predict_board(img)  # Returns 8x8 board array

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

# Run API: uvicorn chess_api:app --host 0.0.0.0 --port 8000 --reload
