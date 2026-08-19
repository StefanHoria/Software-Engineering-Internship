

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

raw_text = """scriptfilm.txt"""


chars = sorted(list(set(raw_text)))
char_indices = {c:i for i,c in enumerate(chars)}
indices_char = {i:c for i,c in enumerate(chars)}


maxlen = 600000
step = 3
sentences = []
next_chars = []
for i in range(0, len(raw_text) - maxlen, step):
    sentences.append(raw_text[i:i+maxlen])
    next_chars.append(raw_text[i+maxlen])
x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.float32)
y = np.zeros((len(sentences), len(chars)), dtype=np.float32)
for i, sent in enumerate(sentences):
    for t, ch in enumerate(sent):
        x[i, t, char_indices[ch]] = 1.0
    y[i, char_indices[next_chars[i]]] = 1.0


model = keras.Sequential([
    layers.LSTM(128, input_shape=(maxlen, len(chars))),
    layers.Dense(len(chars), activation="softmax")
])
model.compile(optimizer="adam", loss="categorical_crossentropy")


model.fit(x, y, batch_size=128, epochs=10)

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)


seed = raw_text[:maxlen]
generated = seed
for _ in range(200):
    x_pred = np.zeros((1, maxlen, len(chars)), dtype=np.float32)
    for t, ch in enumerate(seed):
        x_pred[0, t, char_indices.get(ch, 0)] = 1.0
    preds = model.predict(x_pred, verbose=0)[0]
    next_index = sample(preds, temperature=0.8)
    next_char = indices_char[next_index]
    generated += next_char
    seed = generated[-maxlen:]
print(generated)
