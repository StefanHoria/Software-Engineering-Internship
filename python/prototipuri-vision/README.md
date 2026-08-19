# Desktop Computer Vision Prototypes

Before writing the Android app, the same ideas were tested quickly on a laptop, in Python with
OpenCV. The scripts here are the intermediate steps that led to
[VisionDemo](../../android/VisionDemo/) — each one adds a piece on top of the previous.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

| Script | What it tests |
|---|---|
| [`test_emotii.py`](test_emotii.py) | emotion only, with DeepFace plus a Haar cascade fallback; detection every 5th frame for speed |
| [`testd.py`](testd.py) | emotion (DeepFace) + hands (MediaPipe Hands) in the same pipeline, with an FPS readout |
| [`testd2.py`](testd2.py) | adds age and gender; downscales to 640 px for performance |
| [`testd3.py`](testd3.py) | adds Text-to-Speech (`pyttsx3`) with a 1.5 s cooldown between announcements |
| [`test2.py`](test2.py) | CSV logging of the results (`out/log_*.csv`) and smoothing over a 5-frame window |
| [`read_book_titles.py`](read_book_titles.py) | OCR on book spines with EasyOCR (ro + en), including ±90° rotations, read aloud |

The decisions validated here — periodic instead of per-frame detection, downscaling before
inference, temporal smoothing, a TTS cooldown — were then reimplemented in Kotlin.
`read_book_titles.py` was the starting point for [ScannerISBN](../../android/ScannerISBN/).

## Running

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install mediapipe pyttsx3 easyocr    # only needed for some of the scripts
python testd3.py
```

The versions in `requirements.txt` are pinned deliberately: the combination
`tensorflow 2.15 / keras 2.15 / numpy 1.26 / protobuf 3.20` was the only one that worked with
`deepface 0.0.95` without conflicts. Press `q` or `Esc` to close the camera window; in `testd3.py`,
the `v` key toggles the voice.
