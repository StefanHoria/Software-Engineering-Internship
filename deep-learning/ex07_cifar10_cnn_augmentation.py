import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import cifar10


(x_train, y_train), (x_test, y_test) = cifar10.load_data()


x_train = x_train.astype("float32")/255.0
x_test  = x_test.astype("float32")/255.0


def make_model():
    m = keras.Sequential([
        layers.Conv2D(32, 3, activation="relu", input_shape=(32,32,3)),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, activation="relu"),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation="relu"),
        layers.Dense(10, activation="softmax")
    ])
    m.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return m


model_plain = make_model()
model_plain.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1, verbose=2)


data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

augmented_model = keras.Sequential([
    data_augmentation,
    make_model()
])

augmented_model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
augmented_model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1, verbose=2)

print("Plain:", model_plain.evaluate(x_test, y_test, verbose=0))
print("Aug :", augmented_model.evaluate(x_test, y_test, verbose=0))
