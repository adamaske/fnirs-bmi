import tensorflow as tf
from keras import layers, models
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling1D, Concatenate
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt


#epoch data 
rest = np.load("data/rest_epochs.np.npy")[0:35]
right = np.load("data/right_epochs.np.npy")
left = np.load("data/left_epochs.np.npy")
print("rest : ", rest.shape)
print("right : ", right.shape)
print("left : ", left.shape)
#stack all data
data = np.vstack((right, left))
data = np.vstack((rest, data))

num_samples = len(data)
channels = len(data[0])
timesteps = len(data[0][0])
classes = ["rest", "right", "left"]

rest_labels =np.full(len(rest), 0)
right_labels =np.full(len(right), 1)
left_labels =np.full(len(left), 2)
labels = np.concatenate((rest_labels, np.concatenate((right_labels, left_labels ))))
labels = to_categorical(labels, num_classes=len(classes))

x_train, x_val, y_train, y_val = train_test_split(data, labels, test_size=0.3, random_state=23, shuffle=True,)

x_train.reshape(-1, channels, timesteps)
x_val.reshape(-1, channels, timesteps)

input_shape = (channels, timesteps)
inputs = layers.Input(shape=input_shape)
x = Conv1D(filters=128, kernel_size=3, activation='relu', padding='same')(inputs)
x = BatchNormalization()(x)

for layer in range(3):
    bottleneck1x1 = Conv1D(filters=64, kernel_size=1, padding='same', activation='relu')(x)
    lyrs = []
    for size in [10, 20, 40]:
        layers.append(layers.Conv1D(filters=64, kernel_size=size, padding='same', activation='relu')(bottleneck1x1))
    
    maxpool = layers.MaxPooling1D(pool_size=3, strides=1, padding='same')(x)
    lyrs.append(layers.Conv1D(filters=64, kernel_size=1, padding='same', activation='relu')(maxpool))
    x = layers.concatenate(lyrs, axis=-1)

x = layers.GlobalAveragePooling1D()(x)
x = layers.Dense(256, activation='relu')(x)
x = layers.Dropout(0.5)(x)

outputs = layers.Dense(len(classes), activation='softmax')(x)
model = models.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_val, y_val))

result = model.predict(x_train)

y_pred_classes = np.argmax(result, axis=1)
y_true = np.argmax(y_train, axis=1)

# Compute the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Normalize the confusion matrix by dividing by the sum of each row
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred_classes))

# Plotting the confusion matrix as a heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Reds', xticklabels=classes, yticklabels=classes)
plt.title('Normalized Confusion Matrix (Percentages)')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

save = input("Save this model? (yes/no) : ")
if save == "yes":
    model_path = input("Filepath : ")
    model.save(model_path)

