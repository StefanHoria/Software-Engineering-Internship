
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import boston_housing
import numpy as np


(x_train, y_train), (x_test, y_test) = boston_housing.load_data()


mean = x_train.mean(axis=0)
std  = x_train.std(axis=0)
x_train_std = (x_train - mean) / std
x_test_std  = (x_test - mean) / std


minv = x_train.min(axis=0)
maxv = x_train.max(axis=0)
x_train_mm = (x_train - minv) / (maxv - minv + 1e-8)
x_test_mm  = (x_test - minv) / (maxv - minv + 1e-8)

def build_model():
    m = keras.Sequential([
        layers.Dense(64, activation="relu", input_shape=(x_train.shape[1],)),
        layers.Dense(64, activation="relu"),
        layers.Dense(1)
    ])
    m.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    return m


m_std = build_model()
m_std.fit(x_train_std, y_train, epochs=150, batch_size=16, verbose=0, validation_split=0.2)
print("Standardizare:", m_std.evaluate(x_test_std, y_test, verbose=0))


m_mm = build_model()
m_mm.fit(x_train_mm, y_train, epochs=150, batch_size=16, verbose=0, validation_split=0.2)
print("MinMax:", m_mm.evaluate(x_test_mm, y_test, verbose=0))
