import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class DatasetLoader:
    def __init__(self, dataset_path, img_size=(64, 64), test_size=0.1):
        self.dataset_path = dataset_path
        self.img_size = img_size
        self.test_size = test_size
        self.class_labels = os.listdir(dataset_path)
        self.datagen = ImageDataGenerator(
            rotation_range=30,
            width_shift_range=0.3,
            height_shift_range=0.3,
            shear_range=0.3,
            zoom_range=0.3,
            horizontal_flip=True,
            fill_mode='nearest'
        )

    def load_data(self):
        X, y = [], []

        for label in self.class_labels:
            class_dir = os.path.join(self.dataset_path, label)  # e.g., dataset/chesspieces/bB
            print(self.class_labels)
            print(f"Label '{label}' is assigned index {self.class_labels.index(label)}")

            if not os.path.isdir(class_dir):  # Ensure it's a directory
                continue

            # Loop through image files inside the class folder
            for img_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, img_name)

                # Ensure it's a valid image file
                if not os.path.isfile(img_path) or not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue

                print(f"✔ Loading: {img_path}")  # Debugging output

                try:
                    img = Image.open(img_path).convert("RGB").resize(self.img_size)
                    X.append(np.array(img) / 255.0)  # Normalize pixel values
                    y.append(self.class_labels.index(label))  # Encode label as index
                except Exception as e:
                    print(f"❌ Error loading image {img_path}: {e}")

        # Convert to NumPy arrays
        X = np.array(X)
        y = np.array(y)

        # Convert labels to one-hot encoding
        y = to_categorical(y, num_classes=len(self.class_labels))  # 🔥 One-hot encode labels

        # Split into train & test sets
        return train_test_split(X, y, test_size=self.test_size, random_state=42)
