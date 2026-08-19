# Deep Learning Exercises

Ten exercises written while working through *Deep Learning with Python* (François Chollet). Each
file is a standalone script that downloads its own dataset through `keras.datasets` and compares two
variants of a model, so that the effect of a single architectural decision becomes visible.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

The chapter notes are in [`docs/notite-deep-learning.md`](../docs/notite-deep-learning.md)
(in Romanian).

| File | Dataset | What it compares |
|---|---|---|
| [`ex01_imdb_mlp_variants.py`](ex01_imdb_mlp_variants.py) | IMDB | MLP variants for binary classification |
| [`ex02_reuters_softmax_vs_sigmoid.py`](ex02_reuters_softmax_vs_sigmoid.py) | Reuters | softmax vs. sigmoid on multi-class classification |
| [`ex03_boston_regression_norms.py`](ex03_boston_regression_norms.py) | Boston Housing | the effect of data normalisation in regression |
| [`ex04_iris_mlp_vs_rf.py`](ex04_iris_mlp_vs_rf.py) | Iris | neural network vs. Random Forest |
| [`ex05_mlp_with_dropout.py`](ex05_mlp_with_dropout.py) | IMDB | dropout as a regularisation method |
| [`ex06_boston_kfold_vs_split.py`](ex06_boston_kfold_vs_split.py) | Boston Housing | K-Fold vs. a simple train/test split |
| [`ex07_cifar10_cnn_augmentation.py`](ex07_cifar10_cnn_augmentation.py) | CIFAR-10 | CNN with and without data augmentation |
| [`ex08_transfer_vgg16_cifar10.py`](ex08_transfer_vgg16_cifar10.py) | CIFAR-10 | transfer learning with a pre-trained VGG16 |
| [`ex09_char_lstm_text_generation.py`](ex09_char_lstm_text_generation.py) | own text | character-level text generation (LSTM) |
| [`ex10_multi_input_model.py`](ex10_multi_input_model.py) | synthetic data | multi-input model with the Keras Functional API |

## Running

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install tensorflow scikit-learn numpy matplotlib
python ex01_imdb_mlp_variants.py
```

`ex07` and `ex08` (CIFAR-10, VGG16) are the slowest — on a CPU they take considerably longer than
the rest.
