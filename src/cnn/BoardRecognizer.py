import os

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
from src.misc import utils


class BoardRecognizer:
    def __init__(self, model_path, img_size=(64, 64)):
        self.model = load_model(model_path)
        dataset_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces"
        #class_labels = os.listdir(dataset_path)
        #self.class_labels = os.listdir(dataset_path)
        self.class_labels = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'empty', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
        self.img_size = img_size

    def extract_squares(self, image_path, save_squares=False):
        """Extracts 64 squares from a chessboard image and saves them."""
        output_dir = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\output"
        if save_squares:
            os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
        image = Image.open(image_path)
        square_size = 720 // 8  # 90 pixels per square
        squares = []
        image_mapping = []  # Store image file paths and their positions

        for row in range(8):
            row_squares = []
            for col in range(8):
                left = col * square_size
                top = row * square_size
                right = (col + 1) * square_size
                bottom = (row + 1) * square_size

                square_img = image.crop((left, top, right, bottom)).convert("RGB")
                square_img = square_img.resize(self.img_size)  # Resize for CNN
                square_array = np.array(square_img) / 255.0  # Normalize

                # Save square as an image file
                square_filename = f"{row}{col}.png"
                if save_squares:
                    square_path = os.path.join(output_dir, square_filename)
                    square_img.save(square_path)

                # Store mapping
                image_mapping.append((square_filename, (row, col)))
                row_squares.append(square_array)

            squares.append(row_squares)

        return np.array(squares), image_mapping  # Shape (8, 8, 64, 64, 3)

    def predict_board(self, image_path, save_squares=False):
        """Recognizes all pieces on the chessboard using batch prediction for speed."""
        squares, image_mapping = self.extract_squares(image_path, save_squares)  # (8, 8, 64, 64, 3)
        board_state = np.empty((8, 8), dtype=object)
        board_with_accuracy = np.empty((8, 8), dtype=object)
        prediction_mapping = []  # Store image-path-to-prediction mapping

        print("\nRecognizing Pieces...")

        # **Flatten the board for batch prediction**
        all_squares = squares.reshape(-1, 64, 64, 3)  # Shape: (64, 64, 64, 3)

        # **Perform batch prediction**
        predictions = self.model.predict(all_squares)  # Predict all 64 squares at once

        # **Process results**
        for i, (filename, (row, col)) in enumerate(image_mapping):
            predicted_class = np.argmax(predictions[i])  # Get index of highest probability
            confidence = predictions[i][predicted_class] * 100
            board_state[row, col] = self.class_labels[predicted_class]
            board_with_accuracy[row, col] = f"{self.class_labels[predicted_class]} ({confidence:.2f}%)"

            # Store mapping of image file -> prediction
            prediction_mapping.append((filename, board_state[row, col]))

        # Print image-to-prediction mapping
        if save_squares:
            print("\nImage to Prediction Mapping:")
            for img_file, predicted_piece in prediction_mapping:
                print(f"{img_file} -> {predicted_piece}")

        utils.print_board(board=board_with_accuracy, title="Predicted board with accuracy")
        utils.print_board(board=board_state, title="Predicted board")

        return board_state

if __name__ == "__main__":
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
    test_img_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\images\chessboard\board.png"
    test_img_path2 = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionBOT\resources\images\board.png"

    # Load image and convert to NumPy array
    # img = Image.open(test_img_path).convert("RGB")  # Ensure 3-channel RGB
    # img_array = np.array(img) / 255.0  # Normalize pixel values

    # Initialize recognizer and predict board
    recognizer = BoardRecognizer(model_path)
    start_time = time.time()
    board = recognizer.predict_board(test_img_path2, False)
    end_time = time.time()

    # Calculate and print the execution time
    execution_time = end_time - start_time
    print(f"Prediction took: {execution_time:.4f} seconds")

    print(utils.board_to_fen(board))