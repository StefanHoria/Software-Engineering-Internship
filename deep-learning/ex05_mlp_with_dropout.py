import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import imdb
import numpy as np


(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

def vectorize(seqs, dim=10000):
    res = np.zeros((len(seqs), dim), dtype="float32")
    for i, s in enumerate(seqs):
        res[i, s] = 1.0
    return res

x_train = vectorize(x_train)
x_test  = vectorize(x_test)


baseline = keras.Sequential([
    layers.Dense(512, activation="relu", input_shape=(10000,)),
    layers.Dense(512, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])
baseline.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


drop_model = keras.Sequential([
    layers.Dense(512, activation="relu", input_shape=(10000,)),
    layers.Dropout(0.5),
    layers.Dense(512, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(1, activation="sigmoid")
])
drop_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


baseline.fit(x_train, y_train, epochs=4, batch_size=512, validation_split=0.2, verbose=2)
drop_model.fit(x_train, y_train, epochs=4, batch_size=512, validation_split=0.2, verbose=2)

print("Baseline test:", baseline.evaluate(x_test, y_test, verbose=0))
print("Dropout  test:", drop_model.evaluate(x_test, y_test, verbose=0))
