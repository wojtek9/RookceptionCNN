import os

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class BoardRecognizer:
    def __init__(self, model_path, class_labels, img_size=(64, 64)):
        self.model = load_model(model_path)
        self.class_labels = class_labels
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
        """Recognizes all pieces on the chessboard, saves squares, and returns an 8x8 matrix."""
        squares, image_mapping = self.extract_squares(image_path, save_squares)  # (8, 8, 64, 64, 3)
        board_state = np.empty((8, 8), dtype=object)
        prediction_mapping = []  # Store image-path-to-prediction mapping

        print("\nRecognizing Pieces...")

        for i, (filename, (row, col)) in enumerate(image_mapping):
            square_img = np.expand_dims(squares[row][col], axis=0)  # Add batch dimension
            predictions = self.model.predict(square_img)
            predicted_class = np.argmax(predictions)  # Get index of highest probability
            board_state[row, col] = self.class_labels[predicted_class]

            # Store mapping of image file -> prediction
            prediction_mapping.append((filename, board_state[row, col]))

        # Print final board
        print("\nRecognized Chessboard:")
        for row in board_state:
            print(row)

        # Print image-to-prediction mapping
        if save_squares:
            print("\nImage to Prediction Mapping:")
            for img_file, predicted_piece in prediction_mapping:
                print(f"{img_file} -> {predicted_piece}")

        return board_state

if __name__ == "__main__":
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
    test_img_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\images\chessboard\board.png"

    dataset_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces"
    class_labels = os.listdir(dataset_path)

    recognizer = BoardRecognizer(model_path, class_labels)
    board = recognizer.predict_board(test_img_path)

    print("Recognized Chessboard:")
    for row in board:
        print(row)