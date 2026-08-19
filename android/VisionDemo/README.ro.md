# VisionDemo — recunoaștere vizuală în timp real pe Android

> 🇬🇧 English version: [README.md](README.md)
Proiectul principal al practicii. Aplicația pornește camera telefonului și, pe fiecare
cadru, rulează trei lucruri în paralel: găsește fața, estimează emoția / vârsta / genul
și numără degetele ridicate. Rezultatul e afișat pe ecran și, opțional, citit cu voce tare.

<p align="center">
  <img src="../../docs/media/visiondemo-screenshot.jpg" alt="VisionDemo rulând pe telefon" width="320">
</p>

> Bara de sus arată rezultatul curent (`emoție | vârstă | gen`), iar butoanele de jos
> comută citirea vocală și lanterna.
> Clip demo cu Text-to-Speech: [`docs/media/visiondemo-tts-demo.mov`](../../docs/media/visiondemo-tts-demo.mov) *(Git LFS)*

---

## Funcționalități

| Funcție | Cum e implementată |
|---|---|
| Preview + analiză cadru cu cadru | CameraX (`Preview` + `ImageAnalysis`, backpressure `KEEP_ONLY_LATEST`) |
| Detecția feței | ML Kit Face Detection — extrage ROI-ul feței |
| Emoție / vârstă / gen | 3 modele TensorFlow Lite (DeepFace) rulate pe ROI |
| Numărare degete | MediaPipe Hand Landmarker (21 landmark-uri × 2 mâini) |
| Feedback audio | `TextToSpeech` Android, cu locale `ro-RO` și fallback pe `en-US` |
| Lanternă | `CameraControl.enableTorch()` pentru lumină slabă |

## Arhitectura codului

```
app/src/main/java/com/example/visiondemo/
├── MainActivity.kt        # permisiuni, CameraX, orchestrarea pipeline-ului, UI, TTS
├── EmotionAgeGender.kt    # clasa Eag — încarcă cele 3 modele .tflite și face inferența
├── Hands.kt               # clasa Hands — HandLandmarker + logica de numărare a degetelor
└── Extensions.kt          # utilitare (ImageProxy → Bitmap, corecție rotație, crop)

app/src/main/assets/       # modelele (urmărite prin Git LFS)
├── emotion_deepface.tflite
├── age_deepface.tflite
├── gender_deepface.tflite
└── hand_landmarker.task
```

### Detalii de implementare

**`Eag`** citește la runtime shape-ul tensorului de intrare al fiecărui model
(`interp.getInputTensor(0).shape()`), astfel încât aceeași clasă funcționează și dacă
modelul cere 48×48 grayscale (emoție) sau 224×224 RGB (vârstă/gen). Emoțiile sunt mapate
pe `angry, disgust, fear, happy, sad, surprise, neutral`.

**`Hands`** rulează landmarker-ul în `RunningMode.VIDEO` și decide dacă un deget e întins
pe baza unghiului din articulații — prag `55°` pentru index/mijlociu/inelar/mic și `50°`
pentru degetul mare. Pentru că rezultatul brut pâlpâia de la un cadru la altul, fiecare
deget trece printr-un **vot majoritar pe ultimele 5 cadre** (`historySize = 5`), ceea ce
a stabilizat numărătoarea.

## Build & rulare

Cerințe: Android Studio (Ladybug+), **JDK 17**, un telefon Android cu API ≥ 24.

```bash
git lfs install          # obligatoriu, altfel modelele rămân pointere de 130 de octeți
git clone https://github.com/StefanHoria/Proiecte.git
```

Deschide `android/VisionDemo` în Android Studio, lasă Gradle să sincronizeze, apoi Run.
La prima pornire aplicația cere permisiunea pentru cameră.

`compileSdk = 36`, `minSdk = 24`, `jvmTarget = 17`.

## Limitări cunoscute

- În lumină slabă acuratețea scade vizibil (de aici și butonul de lanternă).
- Estimarea vârstei e orientativă — modelele DeepFace sunt antrenate pe seturi generice.
- Numărarea degetelor cere mâna relativ frontală față de cameră.
