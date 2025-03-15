import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class PieceRecognizer:
    def __init__(self, model_path, class_labels, img_size=(64, 64)):
        self.model = load_model(model_path)  # Load trained model
        self.class_labels = class_labels  # Label names (e.g., ['bB', 'bK', ...])
        self.img_size = img_size  # Model image size

    def predict(self, img_path):
        # Load image
        img = image.load_img(img_path, target_size=self.img_size)
        img_array = image.img_to_array(img)  # Convert to array
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0  # Normalize pixels

        # Predict
        predictions = self.model.predict(img_array)

        # Print all probabilities
        for i, label in enumerate(self.class_labels):
            print(f"{label}: {predictions[0][i] * 100:.2f}%")

        predicted_class = np.argmax(predictions)  # Get index of highest probability
        print(
            f"\nPredicted Chess Piece: {self.class_labels[predicted_class]} with {100 * np.max(predictions):.2f}% confidence.")


if __name__ == "__main__":
    # Set paths
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"
    test_img_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces\bP\board_12.png"

    # Class labels
    dataset_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces"
    class_labels = os.listdir(dataset_path)

    # Create recognizer and predict
    recognizer = PieceRecognizer(model_path, class_labels)
    recognizer.predict(test_img_path)
