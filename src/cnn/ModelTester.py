import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

class ModelTester:
    def __init__(self, model_path, test_images_path, class_labels):
        self.model = load_model(model_path)
        self.test_images_path = test_images_path
        self.class_labels = class_labels  # ["empty", "wP", "wR", ..., "bK"]

    def predict_image(self, image_path):
        """Predicts the chess piece in a given image."""
        img = Image.open(image_path).convert("RGB").resize((64, 64))  # Resize for CNN
        img_array = np.array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        predictions = self.model.predict(img_array)
        class_index = np.argmax(predictions)
        return self.class_labels[class_index]

    def test_all_images(self):
        """Tests all images in subfolders and prints accuracy."""
        total_images = 0
        correct_predictions = 0

        for piece_type in os.listdir(self.test_images_path):  # Iterate through "wP", "bK", etc.
            piece_folder = os.path.join(self.test_images_path, piece_type)

            if not os.path.isdir(piece_folder):
                continue  # Skip files, only process folders

            for img_name in os.listdir(piece_folder):
                img_path = os.path.join(piece_folder, img_name)
                predicted_label = self.predict_image(img_path)

                # Check if prediction matches the folder name
                if predicted_label == piece_type:
                    correct_predictions += 1

                total_images += 1
                print(f"{img_name} -> Predicted: {predicted_label} | Actual: {piece_type}")

        # Calculate accuracy
        accuracy = (correct_predictions / total_images) * 100 if total_images > 0 else 0
        print(f"\nModel Accuracy: {accuracy:.2f}% ({correct_predictions}/{total_images})")


if __name__ == "__main__":
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
    test_images_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces"
    class_labels = ["empty", "wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]

    tester = ModelTester(model_path, test_images_path, class_labels)
    tester.test_all_images()

