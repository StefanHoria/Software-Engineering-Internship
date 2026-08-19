
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import reuters
import numpy as np


(num_words) = 10000
(x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=num_words)

def vectorize(seqs, dim=10000):
    res = np.zeros((len(seqs), dim), dtype="float32")
    for i, s in enumerate(seqs):
        res[i, s] = 1.0
    return res

x_train = vectorize(x_train, num_words)
x_test  = vectorize(x_test, num_words)


num_classes = np.max(y_train) + 1
y_train_cat = keras.utils.to_categorical(y_train, num_classes)
y_test_cat  = keras.utils.to_categorical(y_test, num_classes)


model_softmax = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(num_words,)),
    layers.Dense(64, activation="relu"),
    layers.Dense(num_classes, activation="softmax")
])
model_softmax.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])


model_sigmoid = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(num_words,)),
    layers.Dense(64, activation="relu"),
    layers.Dense(num_classes, activation="sigmoid")
])
model_sigmoid.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])


model_softmax.fit(x_train, y_train_cat, epochs=5, batch_size=512, validation_split=0.1, verbose=2)
model_sigmoid.fit(x_train, y_train_cat, epochs=5, batch_size=512, validation_split=0.1, verbose=2)


print("Softmax:", model_softmax.evaluate(x_test, y_test_cat, verbose=0))
print("Sigmoid:", model_sigmoid.evaluate(x_test, y_test_cat, verbose=0))
