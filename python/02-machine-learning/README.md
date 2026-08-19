# Project 2 — Machine Learning with scikit-learn

A first contact with "classical" machine learning, before the deep learning part: a music genre
recommender trained on a small dataset.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

## The `HelloWorld.ipynb` notebook

- Loads `music.csv` (age + gender → preferred music genre) with pandas.
- Trains a `DecisionTreeClassifier` on the `age` and `gender` features.
- Splits the data with `train_test_split` and measures `accuracy_score`.
- Persists the trained model with `joblib` → `music-recommender.joblib`, so it does not have to be
  retrained on every run.
- Exports the decision tree with `tree.export_graphviz` → `music-recommender.dot`.

`vgsales.csv` (video game sales) was used for data exploration exercises with pandas.

## Visualising the tree

The `.dot` file opens with the *Graphviz* extension in VS Code, or can be converted:

```bash
dot -Tpng music-recommender.dot -o music-recommender.png
```

## Running

```bash
pip install pandas scikit-learn joblib jupyter
jupyter notebook HelloWorld.ipynb
```
