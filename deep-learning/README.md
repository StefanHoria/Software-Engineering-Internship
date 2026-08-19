# Exerciții Deep Learning

Zece exerciții scrise după parcurgerea cărții *Deep Learning with Python* (François Chollet).
Fiecare fișier e un script independent care descarcă singur setul de date prin
`keras.datasets` și compară două variante de model, ca să se vadă efectul unei singure
decizii de arhitectură.

Notițele pe capitole sunt în [`docs/notite-deep-learning.md`](../docs/notite-deep-learning.md).

| Fișier | Set de date | Ce compară |
|---|---|---|
| [`ex01_imdb_mlp_variants.py`](ex01_imdb_mlp_variants.py) | IMDB | variante de MLP pentru clasificare binară |
| [`ex02_reuters_softmax_vs_sigmoid.py`](ex02_reuters_softmax_vs_sigmoid.py) | Reuters | softmax vs. sigmoid pe clasificare multiclasă |
| [`ex03_boston_regression_norms.py`](ex03_boston_regression_norms.py) | Boston Housing | efectul normalizării datelor în regresie |
| [`ex04_iris_mlp_vs_rf.py`](ex04_iris_mlp_vs_rf.py) | Iris | rețea neuronală vs. Random Forest |
| [`ex05_mlp_with_dropout.py`](ex05_mlp_with_dropout.py) | IMDB | dropout ca metodă de regularizare |
| [`ex06_boston_kfold_vs_split.py`](ex06_boston_kfold_vs_split.py) | Boston Housing | K-Fold vs. train/test simplu |
| [`ex07_cifar10_cnn_augmentation.py`](ex07_cifar10_cnn_augmentation.py) | CIFAR-10 | CNN cu și fără data augmentation |
| [`ex08_transfer_vgg16_cifar10.py`](ex08_transfer_vgg16_cifar10.py) | CIFAR-10 | transfer learning cu VGG16 pre-antrenat |
| [`ex09_char_lstm_text_generation.py`](ex09_char_lstm_text_generation.py) | text propriu | generare de text caracter cu caracter (LSTM) |
| [`ex10_multi_input_model.py`](ex10_multi_input_model.py) | date sintetice | model multi-input cu Keras Functional API |

## Rulare

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install tensorflow scikit-learn numpy matplotlib
python ex01_imdb_mlp_variants.py
```

`ex07` și `ex08` (CIFAR-10, VGG16) sunt cele mai lente — pe CPU durează sensibil mai mult
decât restul.
