import numpy as np
import tensorflow as tf
from keras.src.optimizers import Adam
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping

from cnn.DatasetLoader import DatasetLoader


class CNNTrainer:
    def __init__(self, dataset_path, model_path, img_size=(64, 64)):
        self.dataset_path = dataset_path
        self.img_size = img_size
        self.model_path = model_path
        self.dataset_loader = DatasetLoader(dataset_path)
        self.model = self.build_model()

    def build_model(self):
        base_model = MobileNetV2(input_shape=(64, 64, 3), include_top=False, weights='imagenet')

        # Fine-tune deeper layers instead of early ones
        for layer in base_model.layers[:80]:
            layer.trainable = False
        for layer in base_model.layers[80:]:
            layer.trainable = True

        model = models.Sequential([
            base_model,
            layers.Conv2D(64, (3, 3), activation='relu', padding="same"),  # Extra convolution for piece edges
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(len(self.dataset_loader.class_labels), activation='softmax')
        ])

        model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, epochs=20, batch_size=32):
        global early_stopping
        X_train, X_test, y_train, y_test = self.dataset_loader.load_data()

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        for train_idx, val_idx in skf.split(X_train, np.argmax(y_train, axis=1)):
            x_tr, x_val = X_train[train_idx], X_train[val_idx]
            y_tr, y_val = y_train[train_idx], y_train[val_idx]

            early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

            print(f"Training fold with {len(x_tr)} samples, validating on {len(x_val)} samples")

            self.model.fit(
                x_tr, y_tr,  # Train on split data
                epochs=50,
                batch_size=batch_size,
                validation_data=(x_val, y_val),  # Validate on split data
                callbacks=[early_stopping]
            )

        # Final training on full dataset after KFold validation
        self.model.fit(
            X_train, y_train,
            epochs=10,  # Fewer epochs to finalize training
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping]
        )

        self.model.save(self.model_path)


# Run training
if __name__ == "__main__":
    dataset_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\resources\dataset\chesspieces"
    model_path = r"C:\Users\christian\Desktop\Thefolder\Projects\RookceptionCNN\models\CNNModel.h5"

    trainer = CNNTrainer(dataset_path=dataset_path, model_path=model_path)
    trainer.train()
