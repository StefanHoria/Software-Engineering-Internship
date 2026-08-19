

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import imdb
import numpy as np


(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)


def vectorize_sequences(sequences, dimension=10000):

    results = np.zeros((len(sequences), dimension), dtype="float32")

    for i, seq in enumerate(sequences):
        results[i, seq] = 1.0
    return results


x_train = vectorize_sequences(x_train)
x_test  = vectorize_sequences(x_test)


y_train = np.asarray(y_train).astype("float32")
y_test  = np.asarray(y_test).astype("float32")


hidden_sizes = [8, 16, 64]
histories = {}

for size in hidden_sizes:

    model = keras.Sequential([
        layers.Dense(size, activation="relu", input_shape=(10000,)),
        layers.Dense(1, activation="sigmoid")
    ])

    model.compile(optimizer="rmsprop",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])

    history = model.fit(x_train, y_train,
                        epochs=8,
                        batch_size=512,
                        validation_split=0.1,
                        verbose=2)

    histories[size] = history.history


for size in hidden_sizes:
    model = keras.Sequential([
        layers.Dense(size, activation="relu", input_shape=(10000,)),
        layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="rmsprop",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])

    model.fit(x_train, y_train, epochs=8, batch_size=512, verbose=0)
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"[Hidden={size}] Test accuracy: {acc:.4f}")
