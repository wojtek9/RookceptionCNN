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
            rotation_range=15,        # Small rotations
            width_shift_range=0.2,    # Small horizontal shifts
            height_shift_range=0.2,   # Small vertical shifts
            shear_range=10,           # Slight shearing
            zoom_range=0.1,           # Small zoom variations
            horizontal_flip=True,     # Flip horizontally
            fill_mode='nearest'
        )

    def load_data(self):
        X, y = [], []

        for label in self.class_labels:
            class_dir = os.path.join(self.dataset_path, label)

            if not os.path.isdir(class_dir):
                continue

            images = [os.path.join(class_dir, img) for img in os.listdir(class_dir) if img.endswith(('.png', '.jpg', '.jpeg'))]

            for img_path in images:
                img = Image.open(img_path).convert("RGB").resize(self.img_size)
                img_array = np.array(img) / 255.0
                X.append(img_array)
                y.append(self.class_labels.index(label))

                # Generate 5 augmented variations of each image
                for _ in range(5):
                    X.append(self.datagen.random_transform(img_array))
                    y.append(self.class_labels.index(label))

        X = np.array(X)
        y = np.array(y)

        # One-hot encode labels
        y = to_categorical(y, num_classes=len(self.class_labels))

        return train_test_split(X, y, test_size=self.test_size, random_state=42)
