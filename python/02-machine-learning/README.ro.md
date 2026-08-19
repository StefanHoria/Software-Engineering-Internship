# Proiect 2 — Machine Learning cu scikit-learn

> 🇬🇧 English version: [README.md](README.md)
Primul contact cu machine learning „clasic”, înainte de partea de deep learning:
un recomandator de gen muzical antrenat pe un set de date mic.

## Notebook-ul `HelloWorld.ipynb`

- Încarcă `music.csv` (vârstă + gen → gen muzical preferat) cu pandas.
- Antrenează un `DecisionTreeClassifier` pe caracteristicile `age` și `gender`.
- Împarte datele cu `train_test_split` și măsoară `accuracy_score`.
- Persistă modelul antrenat cu `joblib` → `music-recommender.joblib`, ca să nu fie nevoie
  de reantrenare la fiecare rulare.
- Exportă arborele de decizie cu `tree.export_graphviz` → `music-recommender.dot`.

`vgsales.csv` (vânzări de jocuri video) a fost folosit pentru exerciții de explorare a
datelor cu pandas.

## Vizualizarea arborelui

Fișierul `.dot` se deschide cu extensia *Graphviz* din VS Code sau se convertește:

```bash
dot -Tpng music-recommender.dot -o music-recommender.png
```

## Rulare

```bash
pip install pandas scikit-learn joblib jupyter
jupyter notebook HelloWorld.ipynb
```
