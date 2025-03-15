import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

class ModelPredictor:
    def __init__(self, model_path, class_labels):
        self.model = load_model(model_path)
        self.class_labels = class_labels

    def predict(self, img_path):
        """Predicts the piece type from an image"""
        img = Image.open(img_path).convert('L').resize((64, 64))
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=(0, -1))  # Add batch & channel dimensions

        predictions = self.model.predict(img_array)
        class_index = np.argmax(predictions)
        return self.class_labels[class_index]

# Example usage
if __name__ == "__main__":
    predictor = ModelPredictor("models/best_model.h5", ["b", "k", "n", "p", "q", "r", "empty"])
    print(predictor.predict("test_image.png"))  # Replace with an actual image path
