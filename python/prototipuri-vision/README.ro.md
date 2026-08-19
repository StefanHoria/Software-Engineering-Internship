# Prototipuri desktop de computer vision

> 🇬🇧 English version: [README.md](README.md)
Înainte de a scrie aplicația Android, aceleași idei au fost testate rapid pe laptop, în
Python cu OpenCV. Scripturile de aici sunt pașii intermediari care au dus la
[VisionDemo](../../android/VisionDemo/) — fiecare adaugă o bucată peste precedentul.

| Script | Ce testează |
|---|---|
| [`test_emotii.py`](test_emotii.py) | doar emoția, cu DeepFace + fallback pe Haar cascade; detecție la fiecare al 5-lea cadru pentru viteză |
| [`testd.py`](testd.py) | emoție (DeepFace) + mâini (MediaPipe Hands) în același pipeline, cu afișare FPS |
| [`testd2.py`](testd2.py) | adaugă vârsta și genul; downscale la 640 px pentru performanță |
| [`testd3.py`](testd3.py) | adaugă Text-to-Speech (`pyttsx3`) cu cooldown de 1,5 s între anunțuri |
| [`test2.py`](test2.py) | logare CSV a rezultatelor (`out/log_*.csv`) și smoothing pe fereastră de 5 cadre |
| [`read_book_titles.py`](read_book_titles.py) | OCR pe cotoarele cărților cu EasyOCR (ro + en), inclusiv rotiri ±90°, citit cu voce |

Deciziile validate aici — detecție periodică în loc de per-cadru, downscale înainte de
inferență, smoothing temporal, cooldown la TTS — au fost apoi reimplementate în Kotlin.
`read_book_titles.py` a fost punctul de plecare pentru [ScannerISBN](../../android/ScannerISBN/).

## Rulare

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install mediapipe pyttsx3 easyocr    # necesare doar pentru unele scripturi
python testd3.py
```

Versiunile din `requirements.txt` sunt fixate intenționat: combinația
`tensorflow 2.15 / keras 2.15 / numpy 1.26 / protobuf 3.20` a fost singura care a mers cu
`deepface 0.0.95` fără conflicte. Apasă `q` sau `Esc` pentru a închide fereastra camerei; în `testd3.py`, tasta `v` comută vocea.
