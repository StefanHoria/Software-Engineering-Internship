import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import boston_housing
import numpy as np
from sklearn.model_selection import KFold


(x_train, y_train), (x_test, y_test) = boston_housing.load_data()


mean = x_train.mean(axis=0)
std  = x_train.std(axis=0)
x_train = (x_train - mean) / std
x_test  = (x_test - mean) / std

def build_model():
    m = keras.Sequential([
        layers.Dense(64, activation="relu", input_shape=(x_train.shape[1],)),
        layers.Dense(64, activation="relu"),
        layers.Dense(1)
    ])
    m.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    return m


kf = KFold(n_splits=4, shuffle=True, random_state=42)
mae_scores = []
for train_idx, val_idx in kf.split(x_train):
    m = build_model()
    m.fit(x_train[train_idx], y_train[train_idx], epochs=150, batch_size=16, verbose=0)
    mae = m.evaluate(x_train[val_idx], y_train[val_idx], verbose=0)[1]
    mae_scores.append(mae)
print("K-Fold MAE mediu:", np.mean(mae_scores))


m2 = build_model()
h = m2.fit(x_train, y_train, epochs=150, batch_size=16, validation_split=0.2, verbose=0)
val_mae_last = h.history["val_mae"][-1]
print("Hold-out val_MAE (ultimul epoch):", val_mae_last)
