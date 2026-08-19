# ScannerISBN — scanner de cărți cu camera telefonului

A doua aplicație Android scrisă în practică. Pornind de la pipeline-ul CameraX învățat la
VisionDemo, aplicația scanează coperta sau codul de bare al unei cărți și caută volumul
în Google Books.

## Cele două moduri de scanare

`ScanMode.ISBN`
: ML Kit Barcode Scanning citește codul EAN-13 / EAN-8 de pe coperta din spate,
  normalizează șirul (elimină cratimele) și interoghează Google Books după `isbn:`.

`ScanMode.TITLE`
: ML Kit Text Recognition face OCR pe copertă, alege cel mai plauzibil candidat de titlu
  și caută după titlu + autor.

Analiza e limitată la un cadru la 1,5 secunde (`throttle`), ca să nu blocheze camera cu
cereri de rețea inutile.

## Structura codului

```
app/src/main/java/aplicatie/isbn/
├── MainActivity.kt        # CameraX, tap-to-focus, comutare mod, TTS, deschidere rezultat
├── FrameAnalyzer.kt       # ImageAnalysis.Analyzer — barcode sau OCR, în funcție de mod
├── BooksApi.kt            # interfața Retrofit pentru Google Books + modelele de răspuns
├── BooksClient.kt         # construirea clientului Retrofit/OkHttp
├── ScanMode.kt            # enum ScanMode + data class BookHit
├── OcrBarcodeResult.kt    # rezultatul brut al unui cadru analizat
└── Extensions.kt          # utilitare de conversie a cadrelor
```

## Tehnologii

CameraX 1.3.3 · ML Kit Barcode Scanning 17.2.0 · ML Kit Text Recognition 16.0.0 ·
Retrofit 2.11 + Moshi · Kotlin Coroutines · Android TextToSpeech

## Build & rulare

Deschide `android/ScannerISBN` în Android Studio (JDK 17) și rulează pe un telefon fizic.
Aplicația cere permisiune de cameră și acces la internet pentru interogarea Google Books.
