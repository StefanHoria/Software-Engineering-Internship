
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


n = 2000
img = np.random.rand(n, 32, 32, 3).astype("float32")
vec = np.random.rand(n, 10).astype("float32")

y = (img.mean(axis=(1,2,3)) + vec.mean(axis=1)).astype("float32")


img_in = keras.Input(shape=(32,32,3))
x1 = layers.Conv2D(16, 3, activation="relu")(img_in)
x1 = layers.MaxPooling2D()(x1)
x1 = layers.Flatten()(x1)


vec_in = keras.Input(shape=(10,))
x2 = layers.Dense(32, activation="relu")(vec_in)


x = layers.concatenate([x1, x2])
x = layers.Dense(64, activation="relu")(x)
out = layers.Dense(1)(x)

model = keras.Model([img_in, vec_in], out)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
model.fit([img, vec], y, epochs=5, batch_size=32, validation_split=0.1, verbose=2)
