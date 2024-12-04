import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from keras.utils import to_categorical
import numpy as np

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

# Example data
num_samples = 1000
channels = 102
timesteps = 100
classes = ["rest", "left", "right"]
num_classes = len(classes)

from segmentation import get_all_data


#epoch data 

# Generate random data
x = np.random.rand(num_samples, channels, timesteps)
y = np.random.randint(0, num_classes, num_samples)

# One-hot encode labels
y = to_categorical(y, num_classes=num_classes)

# Train-test split
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_val, y_val))

loss, accuracy = model.evaluate(x_val, y_val)
print(f'Test Accuracy: {accuracy}')

model_path = "models/model_01"
model.save(model_path)

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
plt.show()
