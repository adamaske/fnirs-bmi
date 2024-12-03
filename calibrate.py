import tensorflow as tf

from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from keras._tf_keras.keras.utils import to_categorical

#handle data


# Model
model = Sequential([
    Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(100, 3)),
    MaxPooling1D(pool_size=2),
    Conv1D(filters=128, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(4, activation='softmax')  # 4 classes
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

import numpy as np

# Example data
num_samples = 1000
timesteps = 100
features = 3
num_classes = 4

# Generate random data
X = np.random.rand(num_samples, timesteps, features)
y = np.random.randint(0, num_classes, num_samples)

# One-hot encode labels
y = to_categorical(y, num_classes=num_classes)

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy}')


import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
plt.show()
