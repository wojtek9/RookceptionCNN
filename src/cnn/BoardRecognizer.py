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

    def extract_squares(self, image_path):
        """Extracts 64 squares from a 720x720 chessboard image and returns them as an array."""
        image = Image.open(image_path)
        square_size = 720 // 8  # Each square is 90x90 pixels
        squares = []

        for row in range(8):
            row_squares = []
            for col in range(8):
                left = col * square_size
                top = row * square_size
                right = (col + 1) * square_size
                bottom = (row + 1) * square_size

                square_img = image.crop((left, top, right, bottom)).convert("RGB")  # Ensure 3 channels (RGB)
                square_img = square_img.resize(self.img_size)  # Resize for CNN
                square_array = np.array(square_img) / 255.0  # Normalize
                row_squares.append(square_array)

            squares.append(row_squares)

        return np.array(squares)  # Shape (8, 8, 64, 64, 3)

    def predict_board(self, image_path):
        """Recognizes all pieces on the chessboard and returns an 8x8 matrix."""
        squares = self.extract_squares(image_path)  # (8, 8, 64, 64, 3)
        board_state = np.empty((8, 8), dtype=object)

        for row in range(8):
            for col in range(8):
                square_img = np.expand_dims(squares[row][col], axis=0)  # Add batch dimension
                predictions = self.model.predict(square_img)
                predicted_class = np.argmax(predictions)  # Get index of highest probability
                board_state[row, col] = self.class_labels[predicted_class]

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