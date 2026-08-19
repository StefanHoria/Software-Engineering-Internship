<h1 align="center">Practică de domeniu — Anul II</h1>

<p align="center">
  <b>Ștefan Horia-Eusebiu</b><br>
  Facultatea de Inginerie Electrică și Știința Calculatoarelor<br>
  Universitatea Transilvania din Brașov · 2024–2025
</p>

<p align="center">
  <img src="https://img.shields.io/badge/durata-90%20ore%20%2F%2015%20zile-blue" alt="90 de ore">
  <img src="https://img.shields.io/badge/Kotlin-Android-7F52FF?logo=kotlin&logoColor=white" alt="Kotlin">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-Lite-FF6F00?logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Git-LFS-F05032?logo=git&logoColor=white" alt="Git LFS">
</p>

<p align="center">
  🇬🇧 English version: <a href="README.md">README.md</a>
</p>

---

Repository-ul adună tot ce am construit în cele 90 de ore de practică: de la primele
comenzi de Git și exerciții de Python, până la **VisionDemo** — o aplicație Android care
recunoaște în timp real emoția, vârsta, genul și numărul de degete ridicate, din camera
telefonului.

Firul roșu al practicii a fost același lucru încercat de trei ori, tot mai aproape de un
produs real: întâi prototipuri rapide în Python cu OpenCV pe laptop, apoi aceleași idei
rescrise în Kotlin cu modele TensorFlow Lite pe telefon, și în final încă o aplicație
Android care refolosește pipeline-ul deja învățat.

<p align="center">
  <img src="docs/media/visiondemo-screenshot.jpg" alt="VisionDemo — emoție, vârstă și gen afișate live" width="300">
  <br>
  <sub><i>VisionDemo rulând pe telefon: emoția, vârsta și genul estimate live, cu TTS și lanternă.</i></sub>
</p>

## Cuprins

- [Proiectul principal — VisionDemo](#proiectul-principal--visiondemo)
- [Celelalte proiecte](#celelalte-proiecte)
- [Structura repository-ului](#structura-repository-ului)
- [Tehnologii folosite](#tehnologii-folosite)
- [Cum clonezi și rulezi](#cum-clonezi-și-rulezi)
- [Documentație](#documentație)
- [Ce am învățat](#ce-am-învățat)

---

## Proiectul principal — VisionDemo

> 📂 [`android/VisionDemo`](android/VisionDemo/) · [README detaliat](android/VisionDemo/README.md)

Aplicație Android care procesează în timp real cadrele de la cameră și combină patru
tehnologii diferite într-un singur pipeline:

| | Funcție | Tehnologie |
|---|---|---|
| 📷 | Preview + analiză cadru cu cadru | **CameraX** |
| 🙂 | Detecția feței (ROI) | **ML Kit** Face Detection |
| 🧠 | Emoție, vârstă, gen | 3 modele **TensorFlow Lite** (DeepFace) |
| ✋ | Numărarea degetelor ridicate | **MediaPipe** Hand Landmarker |
| 🔊 | Citirea rezultatelor cu voce | **TextToSpeech** (ro-RO) |
| 🔦 | Lanternă pentru lumină slabă | `CameraControl.enableTorch()` |

Două decizii au făcut diferența între „merge” și „e utilizabil”: **votul majoritar pe
ultimele 5 cadre** pentru starea fiecărui deget (fără el, numărătoarea pâlpâia
permanent) și citirea la runtime a shape-ului de intrare al fiecărui model `.tflite`,
astfel încât aceeași clasă `Eag` să funcționeze și pentru 48×48 grayscale, și pentru
224×224 RGB.

🎥 Demo cu Text-to-Speech: [`docs/media/visiondemo-tts-demo.mov`](docs/media/visiondemo-tts-demo.mov)

## Celelalte proiecte

| Proiect | Descriere | Tehnologii |
|---|---|---|
| 📚 [**ScannerISBN**](android/ScannerISBN/) | Aplicație Android care scanează codul de bare sau titlul de pe coperta unei cărți și caută volumul în Google Books | CameraX, ML Kit Barcode + OCR, Retrofit |
| 🔬 [**Prototipuri vision**](python/prototipuri-vision/) | Cele 6 scripturi desktop care au precedat VisionDemo — pașii intermediari, de la „doar emoția” până la pipeline complet cu TTS și logare CSV | OpenCV, DeepFace, MediaPipe, EasyOCR |
| 🧪 [**Exerciții Deep Learning**](deep-learning/) | 10 exerciții după *Deep Learning with Python* (Chollet), fiecare comparând două variante de model | Keras, TensorFlow, scikit-learn |
| 📊 [**Automatizare Excel**](python/01-automatizare-excel/) | Script care corectează prețurile dintr-un registru și generează automat graficul | openpyxl |
| 🎵 [**Machine Learning**](python/02-machine-learning/) | Recomandator de gen muzical cu arbore de decizie, salvat cu joblib | pandas, scikit-learn |
| 🌐 [**Website cu Django**](python/03-website-django/) | Magazin online minimal — modele, view-uri, template-uri, admin | Django, SQLite, Bootstrap |
| 🐍 [**Exerciții Python**](python/exercitii-python/) | ~35 de scripturi din trainingul de Python, de la variabile la OOP | Python 3.10 |

## Structura repository-ului

```
.
├── android/
│   ├── VisionDemo/            ⭐ proiectul principal — emoții, vârstă, gen, degete
│   └── ScannerISBN/              scanner de cărți cu Google Books API
├── python/
│   ├── prototipuri-vision/       prototipurile OpenCV care au precedat VisionDemo
│   ├── exercitii-python/         exercițiile din trainingul de Python
│   ├── 01-automatizare-excel/    automatizare openpyxl
│   ├── 02-machine-learning/      arbore de decizie cu scikit-learn
│   └── 03-website-django/        magazin online minimal
├── deep-learning/                10 exerciții Keras/TensorFlow
└── docs/
    ├── jurnal-activitati.md      jurnalul celor 15 zile de practică
    ├── notite-git.md             notițele de Git, inclusiv Git LFS
    ├── notite-deep-learning.md   rezumatul cărții lui Chollet
    └── media/                    capturi și clipuri demo
```

## Tehnologii folosite

**Android:** Kotlin · CameraX 1.3.3 · ML Kit (Face Detection, Barcode, Text Recognition) ·
MediaPipe Tasks 0.10.26 · TensorFlow Lite 2.14 · Retrofit + Moshi · Coroutines · Gradle (JDK 17)

**Python:** OpenCV · DeepFace · MediaPipe · EasyOCR · TensorFlow/Keras · scikit-learn ·
pandas · Django · openpyxl · pyttsx3

**Unelte:** Git și **Git LFS** (pentru modelele `.tflite` / `.task` și clipurile demo) ·
Android Studio · VS Code · medii virtuale Python

## Cum clonezi și rulezi

Repository-ul folosește **Git LFS** pentru modelele de rețea neuronală. Fără el, fișierele
`.tflite` și `.task` se clonează ca pointere text de câteva sute de octeți, iar aplicația
crapă la pornire.

```bash
git lfs install
git clone https://github.com/StefanHoria/Software-Engineering-Internship.git
cd Software-Engineering-Internship
git lfs pull
```

**Proiectele Android** se deschid direct din `android/VisionDemo` sau `android/ScannerISBN`
în Android Studio (JDK 17, `minSdk 24`) și se rulează pe un telefon fizic — au nevoie de cameră.

**Proiectele Python** au fiecare README-ul propriu, cu pachetele necesare. Recomandat, un
mediu virtual separat per proiect:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## Documentație

| Document | Conținut |
|---|---|
| [📅 Jurnal de activități](docs/jurnal-activitati.md) | Cele 15 zile, zi cu zi: ce am făcut, ce competențe am exersat, unde m-am blocat |
| [🔧 Notițe Git](docs/notite-git.md) | Comenzile învățate — de la `git init` până la `git lfs migrate import` |
| [🧠 Notițe Deep Learning](docs/notite-deep-learning.md) | Rezumat pe capitole din *Deep Learning with Python*, cu exemplele de cod |

## Ce am învățat

**Git nu e doar `add`, `commit`, `push`.** Push-ul a început să pice când am adăugat
modelele `.tflite` — GitHub refuză fișierele mari. Am învățat Git LFS, inclusiv
`git lfs migrate import`, ca să rescriu istoricul deja existent. Regulile sunt în
[`.gitattributes`](.gitattributes).

**Un model care merge pe laptop nu merge automat pe telefon.** Prototipurile din Python
rulau confortabil pe PC; pe Android a fost nevoie de downscale înainte de inferență, de
analiză la fiecare al N-lea cadru și de `KEEP_ONLY_LATEST` pe analyzer, ca să nu se adune
cadrele în coadă.

**Rezultatele brute pâlpâie.** Detecția degetelor era corectă în medie, dar sărea de la un
cadru la altul. Smoothing-ul temporal — vot majoritar pe o fereastră scurtă — a fost
diferența dintre un demo enervant și unul stabil.

**Dependențele contează la fel de mult ca algoritmul.** Combinația
`tensorflow 2.15 / keras 2.15 / numpy 1.26 / protobuf 3.20` a fost singura care a mers cu
`deepface 0.0.95`. De aici și obiceiul de a fixa versiunile în `requirements.txt`.

**Logcat și mesajele de eroare sunt prietene.** Cele mai multe ore pierdute au fost pe
erori de Gradle și JVM target. După ce am învățat să citesc stack-trace-ul până la capăt,
au devenit rezolvabile în minute, nu în ore.

---

<p align="center">
  <sub>Coordonator de practică: Cociaș Tiberiu Teodor</sub>
</p>
