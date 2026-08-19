
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.datasets import cifar10


(x_train, y_train), (x_test, y_test) = cifar10.load_data()


x_train = tf.image.resize(x_train, (224,224)).numpy()
x_test  = tf.image.resize(x_test,  (224,224)).numpy()


x_train = preprocess_input(x_train)
x_test  = preprocess_input(x_test)



base = VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))
base.trainable = False


model_fe = keras.Sequential([
    base,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation="relu"),
    layers.Dense(10, activation="softmax")
])
model_fe.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model_fe.fit(x_train, y_train, epochs=3, batch_size=64, validation_split=0.1, verbose=2)
print("Feature extraction:", model_fe.evaluate(x_test, y_test, verbose=0))


base.trainable = True
for layer in base.layers[:-4]:
    layer.trainable = False

model_fe.compile(optimizer=keras.optimizers.Adam(1e-5),
                 loss="sparse_categorical_crossentropy",
                 metrics=["accuracy"])
model_fe.fit(x_train, y_train, epochs=2, batch_size=64, validation_split=0.1, verbose=2)
print("Fine-tuned:", model_fe.evaluate(x_test, y_test, verbose=0))
