<h1 align="center">Software Engineering Internship — Year II</h1>

<p align="center">
  <b>Ștefan Horia-Eusebiu</b><br>
  Faculty of Electrical Engineering and Computer Science<br>
  Transilvania University of Brașov · 2024–2025
</p>

<p align="center">
  <img src="https://img.shields.io/badge/duration-90%20hours%20%2F%2015%20days-blue" alt="90 hours">
  <img src="https://img.shields.io/badge/Kotlin-Android-7F52FF?logo=kotlin&logoColor=white" alt="Kotlin">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-Lite-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Git-LFS-F05032?logo=git&logoColor=white" alt="Git LFS">
</p>

<p align="center">
  🇷🇴 Documentul în limba română: <a href="README.ro.md">README.ro.md</a>
</p>

---

This repository collects everything built during 90 hours of internship: from the first Git
commands and Python exercises, up to **VisionDemo** — an Android app that recognises emotion, age,
gender and the number of raised fingers in real time, from the phone camera.

The thread running through the internship was the same idea attempted three times, each time closer
to a real product: first quick Python prototypes with OpenCV on a laptop, then the same ideas
rewritten in Kotlin with TensorFlow Lite models on the phone, and finally one more Android app
reusing the pipeline already learned.

<p align="center">
  <img src="docs/media/visiondemo-screenshot.jpg" alt="VisionDemo — emotion, age and gender displayed live" width="300">
  <br>
  <sub><i>VisionDemo running on a phone: emotion, age and gender estimated live, with TTS and torch.</i></sub>
</p>

## Contents

- [Main project — VisionDemo](#main-project--visiondemo)
- [The other projects](#the-other-projects)
- [Repository structure](#repository-structure)
- [Technologies used](#technologies-used)
- [Cloning and running](#cloning-and-running)
- [Documentation](#documentation)
- [What I learned](#what-i-learned)

---

## Main project — VisionDemo

> 📂 [`android/VisionDemo`](android/VisionDemo/) · [detailed README](android/VisionDemo/README.md)

An Android app that processes camera frames in real time and combines four different technologies
into a single pipeline:

| | Function | Technology |
|---|---|---|
| 📷 | Preview + frame-by-frame analysis | **CameraX** |
| 🙂 | Face detection (ROI) | **ML Kit** Face Detection |
| 🧠 | Emotion, age, gender | 3 **TensorFlow Lite** models (DeepFace) |
| ✋ | Counting raised fingers | **MediaPipe** Hand Landmarker |
| 🔊 | Reading results out loud | **TextToSpeech** (ro-RO) |
| 🔦 | Torch for low light | `CameraControl.enableTorch()` |

Two decisions made the difference between "it works" and "it is usable": **majority voting over the
last 5 frames** for each finger's state (without it, the count flickered constantly), and reading
each `.tflite` model's input shape at runtime, so that the same `Eag` class works for both 48×48
grayscale and 224×224 RGB inputs.

🎥 Text-to-Speech demo: [`docs/media/visiondemo-tts-demo.mov`](docs/media/visiondemo-tts-demo.mov)

## The other projects

| Project | Description | Technologies |
|---|---|---|
| 📚 [**ScannerISBN**](android/ScannerISBN/) | Android app that scans the barcode or the title on a book cover and looks the volume up in Google Books | CameraX, ML Kit Barcode + OCR, Retrofit |
| 🔬 [**Vision prototypes**](python/prototipuri-vision/) | The 6 desktop scripts that preceded VisionDemo — the intermediate steps, from "emotion only" to a full pipeline with TTS and CSV logging | OpenCV, DeepFace, MediaPipe, EasyOCR |
| 🧪 [**Deep Learning exercises**](deep-learning/) | 10 exercises following *Deep Learning with Python* (Chollet), each comparing two model variants | Keras, TensorFlow, scikit-learn |
| 📊 [**Excel automation**](python/01-automatizare-excel/) | Script that corrects prices in a workbook and generates the chart automatically | openpyxl |
| 🎵 [**Machine Learning**](python/02-machine-learning/) | Music-genre recommender using a decision tree, persisted with joblib | pandas, scikit-learn |
| 🌐 [**Django website**](python/03-website-django/) | Minimal online store — models, views, templates, admin | Django, SQLite, Bootstrap |
| 🐍 [**Python exercises**](python/exercitii-python/) | ~35 scripts from the Python training, from variables to OOP | Python 3.10 |

## Repository structure

```
.
├── android/
│   ├── VisionDemo/            ⭐ the main project — emotion, age, gender, fingers
│   └── ScannerISBN/              book scanner with the Google Books API
├── python/
│   ├── prototipuri-vision/       the OpenCV prototypes that preceded VisionDemo
│   ├── exercitii-python/         exercises from the Python training
│   ├── 01-automatizare-excel/    openpyxl automation
│   ├── 02-machine-learning/      decision tree with scikit-learn
│   └── 03-website-django/        minimal online store
├── deep-learning/                10 Keras/TensorFlow exercises
└── docs/
    ├── jurnal-activitati.md      journal of the 15 internship days
    ├── notite-git.md             Git notes, including Git LFS
    ├── notite-deep-learning.md   summary of Chollet's book
    └── media/                    screenshots and demo clips
```

## Technologies used

**Android:** Kotlin · CameraX 1.3.3 · ML Kit (Face Detection, Barcode, Text Recognition) ·
MediaPipe Tasks 0.10.26 · TensorFlow Lite 2.14 · Retrofit + Moshi · Coroutines · Gradle (JDK 17)

**Python:** OpenCV · DeepFace · MediaPipe · EasyOCR · TensorFlow/Keras · scikit-learn ·
pandas · Django · openpyxl · pyttsx3

**Tooling:** Git and **Git LFS** (for the `.tflite` / `.task` models and the demo clips) ·
Android Studio · VS Code · Python virtual environments

## Cloning and running

The repository uses **Git LFS** for the neural-network models. Without it, the `.tflite` and
`.task` files are cloned as text pointers of a few hundred bytes and the app crashes on startup.

```bash
git lfs install
git clone https://github.com/StefanHoria/Software-Engineering-Internship.git
cd Software-Engineering-Internship
git lfs pull
```

**The Android projects** open directly from `android/VisionDemo` or `android/ScannerISBN` in
Android Studio (JDK 17, `minSdk 24`) and run on a physical phone — they need a camera.

**The Python projects** each have their own README listing the required packages. A separate
virtual environment per project is recommended:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Documentation

The documents below are written in Romanian.

| Document | Content |
|---|---|
| [📅 Activity journal](docs/jurnal-activitati.md) | The 15 days, day by day: what I did, which skills I practised, where I got stuck |
| [🔧 Git notes](docs/notite-git.md) | The commands learned — from `git init` to `git lfs migrate import` |
| [🧠 Deep Learning notes](docs/notite-deep-learning.md) | Chapter-by-chapter summary of *Deep Learning with Python*, with the code examples |

## What I learned

**Git is not just `add`, `commit`, `push`.** Pushes started failing once I added the `.tflite`
models — GitHub rejects large files. I learned Git LFS, including `git lfs migrate import`, to
rewrite the history that already existed. The rules live in [`.gitattributes`](.gitattributes).

**A model that runs on a laptop does not automatically run on a phone.** The Python prototypes ran
comfortably on a PC; on Android it took downscaling before inference, analysing every Nth frame, and
`KEEP_ONLY_LATEST` on the analyzer to stop frames piling up in the queue.

**Raw results flicker.** Finger detection was correct on average, but jumped from one frame to the
next. Temporal smoothing — majority voting over a short window — was the difference between an
annoying demo and a stable one.

**Dependencies matter as much as the algorithm.** The combination
`tensorflow 2.15 / keras 2.15 / numpy 1.26 / protobuf 3.20` was the only one that worked with
`deepface 0.0.95`. Hence the habit of pinning versions in `requirements.txt`.

**Logcat and error messages are friends.** Most of the hours lost went to Gradle and JVM target
errors. Once I learned to read a stack trace all the way through, they became solvable in minutes
rather than hours.

---

<p align="center">
  <sub>Internship supervisor: Cociaș Tiberiu Teodor</sub>
</p>
