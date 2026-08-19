# ScannerISBN — Book Scanner Using the Phone Camera

The second Android app written during the internship. Starting from the CameraX pipeline learned on
VisionDemo, the app scans a book's cover or barcode and looks the volume up in Google Books.

> 🇷🇴 Documentul în limba română: [README.ro.md](README.ro.md)

## The two scanning modes

`ScanMode.ISBN`
: ML Kit Barcode Scanning reads the EAN-13 / EAN-8 code from the back cover, normalises the string
  (stripping hyphens) and queries Google Books with `isbn:`.

`ScanMode.TITLE`
: ML Kit Text Recognition runs OCR on the cover, picks the most plausible title candidate and
  searches by title + author.

Analysis is throttled to one frame every 1.5 seconds, so the camera is not tied up with pointless
network requests.

## Code structure

```
app/src/main/java/aplicatie/isbn/
├── MainActivity.kt        # CameraX, tap-to-focus, mode switching, TTS, opening the result
├── FrameAnalyzer.kt       # ImageAnalysis.Analyzer — barcode or OCR, depending on the mode
├── BooksApi.kt            # Retrofit interface for Google Books + response models
├── BooksClient.kt         # building the Retrofit/OkHttp client
├── ScanMode.kt            # the ScanMode enum + the BookHit data class
├── OcrBarcodeResult.kt    # the raw result of one analysed frame
└── Extensions.kt          # frame conversion helpers
```

## Technologies

CameraX 1.3.3 · ML Kit Barcode Scanning 17.2.0 · ML Kit Text Recognition 16.0.0 ·
Retrofit 2.11 + Moshi · Kotlin Coroutines · Android TextToSpeech

## Build & run

Open `android/ScannerISBN` in Android Studio (JDK 17) and run it on a physical phone. The app
requires camera permission and internet access for the Google Books lookup.
