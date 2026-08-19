# Notițe — *Deep Learning with Python* (François Chollet)

Rezumatul capitolelor parcurse în ziua 5 de practică, cu exemplele de cod rulate.
Exercițiile scrise pornind de la aceste notițe sunt în [`deep-learning/`](../deep-learning/).

---

## Capitolul 1 – Ce este Deep Learning?

- **AI → ML → DL**
  - AI = automatizarea sarcinilor intelectuale umane
  - ML = învață reguli din date (nu scrise de om)
  - DL = învață reprezentări pe straturi multiple (deep = multe nivele)

- **Cum funcționează?**
  - Date (input) → straturi → output
  - Fiecare strat are *weights* (parametri)
  - Se folosesc: **Loss function** (măsoară eroarea) + **Optimizer** (corectează eroarea prin gradient descent)

```python
from keras import models, layers

model = models.Sequential()
model.add(layers.Dense(512, activation="relu", input_shape=(784,)))
model.add(layers.Dense(10, activation="softmax"))

model.compile(optimizer="rmsprop",
              loss="categorical_crossentropy",
              metrics=["accuracy"])
```



---


## Capitolul 2 – Bazele matematice

- **Tensori**
  - 0D = scalari (ex: `x = 3`)
  - 1D = vectori (ex: `[1,2,3]`)
  - 2D = matrice (ex: `[[1,2],[3,4]]`)
  - 3D = imagini (lățime, înălțime, canale)
  - 4D = video (cadre, lățime, înălțime, canale)

```python

import numpy as np
x = np.array([[1,2,3],[4,5,6]])
print(x.shape)  # (2,3)

```
- **Operații pe tensori**
  - element-wise (`x + y`)
  - dot product (`np.dot(x,y)`)
  - reshape (`x.reshape((3,2))`)

- **Învățare = gradient descent**
  - Loss → feedback
  - Backpropagation → ajustează weights în pași mici
  - Repetat pe multe batch-uri → model antrenat




## Capitolul 3 – Primele rețele neuronale

- **Componente**
  - Straturi → calculează transformări
  - Model → lanț de straturi
  - Loss + Optimizer → antrenare

- **Keras** = librărie simplă pentru DL (rulează peste TensorFlow)

- **Exemple**
  - Binary classification (recenzii IMDB – pozitiv/negativ)
  - Multiclass classification (Reuters – categorii știri)
  - Regression (Boston Housing – predicție prețuri case)

```python
from keras.datasets import imdb
from keras import models, layers

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=10000)

model = models.Sequential()
model.add(layers.Dense(16, activation="relu", input_shape=(10000,)))
model.add(layers.Dense(1, activation="sigmoid"))

model.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])
```


---


## Capitolul 4 – Fundamente ML

- **Tipuri ML**: supervised, unsupervised, self-supervised, reinforcement
- **Evaluare**: train / validation / test split
- **Probleme**:
  - Overfitting → soluții: regularizare (L2), dropout, reducere dimensiuni
  - Underfitting → model prea simplu

- **Workflow ML**
  1. Definești problema + dataset
  2. Alegi metrică (accuracy, MSE etc.)
  3. Protocol de evaluare (validare)
  4. Preprocesare date
  5. Model simplu > baseline
  6. Crești complexitatea până apare overfitting
  7. Regularizare + tuning hiperparametri


---


## Capitolul 5 – DL pentru Computer Vision

- **CNN (Convolutional Neural Networks)**
  - Straturi speciale: convoluție + pooling
  - Foarte bune pe imagini

```python

from keras import models, layers

model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation="relu", input_shape=(150,150,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(1, activation="sigmoid"))

```

- **Probleme mici → soluții**: data augmentation (rotații, zoom, flip)
- **Transfer learning** → folosești rețele pre-antrenate (VGG, ResNet)
- **Vizualizări utile** → activări intermediare, filtre, heatmaps

---

## Capitolul 6 – DL pentru Text și Secvențe

- **Reprezentarea textului**
  - One-hot encoding
  - Word embeddings (Word2Vec, GloVe)

- **RNN / LSTM / GRU** → bune pentru secvențe lungi (text, time-series)

```python
from keras import layers, models

model = models.Sequential()
model.add(layers.Embedding(10000, 32))
model.add(layers.LSTM(32))
model.add(layers.Dense(1, activation="sigmoid"))

```

- **Tehnici avansate**
  - Dropout recurent
  - RNN stack (mai multe straturi)
  - Bidirectional RNN
- **Alternative**: 1D convnets pe secvențe (mai rapide)

---

## Capitolul 7 – Best Practices

- **Keras Functional API** → modele complexe (multi-input/output, DAG)
- **Callbacks + TensorBoard** → monitorizare și vizualizare antrenare
- **Optimizare**:
  - Arhitecturi avansate
  - Hyperparameter search
  - Model ensembling

---

## Capitolul 8 – Generative Deep Learning

- **Text generation cu LSTM**
- **DeepDream** (vizualizare/artefacte)
- **Style Transfer** (separare conținut vs stil)
- **VAE (Variational Autoencoders)** → generare imagini noi
- **GANs** → generator vs discriminator (celebre pentru imagini false realiste)

---

## Capitolul 9 – Concluzii

- DL = transformări succesive de date prin straturi
- Învățarea = gradient descent + backpropagation
- Probleme frecvente: overfitting → regularizare
- Arhitecturi importante: CNN, RNN, LSTM, GRU, GAN
- Transfer learning = foarte puternic pentru aplicații reale
- DL are limite (nu generalizează ca omul), dar viitorul promite (AutoML, lifelong learning etc.)
