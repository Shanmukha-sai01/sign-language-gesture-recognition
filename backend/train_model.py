import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
import pickle
import json

print("Loading dataset...")
df = pd.read_csv("gesture_data.csv")
print(f"Total samples: {len(df)}")
print(f"Gestures: {df['gesture'].unique()}")

# Separate features and labels
X = df.drop("gesture", axis=1).values
y = df["gesture"].values

# Encode gesture names to numbers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
num_classes = len(encoder.classes_)
print(f"\nNumber of gesture classes: {num_classes}")

# Save the encoder so we can decode predictions later
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)
print("Label encoder saved.")

# Save gesture names as JSON for the API
gesture_names = encoder.classes_.tolist()
with open("gesture_names.json", "w") as f:
    json.dump(gesture_names, f)
print("Gesture names saved.")

# Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# Build the neural network
print("\nBuilding model...")
model = keras.Sequential([
    keras.layers.Input(shape=(63,)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# Train the model
print("\nTraining...")
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.1,
    verbose=1
)

# Evaluate on test set
print("\nEvaluating on test set...")
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Detailed report
y_pred = np.argmax(model.predict(X_test), axis=1)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

# Save the model
model.save("gesture_model.keras")
print("\nModel saved as gesture_model.keras")
print("Training complete!")
