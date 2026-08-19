# Jurnal de activități — 15 zile / 90 de ore

Program: 09:00–15:00, online. Sinteză a fișelor de activitate zilnică din caietul de practică.

---

## Săptămâna 1 — Git și fundamentele Python

### Ziua 1 · 30.07
**Activități:** instalare Git; configurare globală (user, email, VS Code ca editor, EOL pentru Windows); inițializare repo local; primele snapshot-uri.
**Competențe:** versionare, organizarea fișierelor de proiect, lucru în linia de comandă.
**Observații:** am înțeles fluxul *working tree → staging → commit*; VS Code setat ca difftool.

### Ziua 2 · 31.07
**Activități:** jurnalizare Git (`log`, `show`), redenumire/mutare cu `git mv`, ștergere cu `git rm`, excluderi în `.gitignore`, vizualizarea diferențelor (`git diff`, `git diff --staged`).
**Competențe:** citirea istoricului, diffs, bune practici `.gitignore`.
**Observații:** am fixat greșeli comune (unstage/restore) și am notat comenzile utile → [notite-git.md](notite-git.md).

### Ziua 3 · 01.08
**Activități:** training Python — variabile, tipuri, funcții, OOP, lucru cu fișiere; exerciții practice și scripturi mici.
**Competențe:** sintaxă Python, structuri de date, debugging.
**Observații:** Python mi s-a părut mult mai simplu decât alte limbaje încercate până acum; la început uitam de indentare.

### Ziua 4 · 02.08
**Activități:** medii virtuale — creare/activare, instalare pachete, separarea dependențelor; `pip freeze` / `requirements.txt`.
**Competențe:** management de dependențe, reproducerea mediului de lucru.
**Observații:** la început nu înțelegeam de ce e nevoie de `venv`, dar după ce am văzut că îmi separă dependențele am realizat cât e de util.

### Ziua 5 · 03.08
**Activități:** studiu pe capitolele cheie din *Deep Learning with Python* (Chollet) — tensori, straturi, overfitting, regularizări; note și exemple rulate.
**Competențe:** bazele Keras/TensorFlow, antrenare și validare de modele.
**Observații:** limbajul cărții a fost mai greu la început, dar exemplele de cod m-au ajutat mult să înțeleg ce înseamnă să „antrenezi” un model. → [notite-deep-learning.md](notite-deep-learning.md)

---

## Săptămâna 2 — VisionDemo, aplicația Android

### Ziua 6 · 04.08
**Activități:** start proiect VisionDemo — setup Android Studio, JDK 17, CameraX preview + analyzer; UI simplu (`PreviewView`, `TextView`, butoane).
**Competențe:** structura unui proiect Android, permisiuni, lifecycle-ul camerei.
**Observații:** greu cu erorile de Gradle și JDK, dar când a rulat preview-ul camerei pe telefon a fost o satisfacție reală.

### Ziua 7 · 05.08
**Activități:** integrare ML Kit Face Detection pentru ROI-ul feței; conversie `ImageProxy → Bitmap`, corectarea rotației; testare pe device.
**Competențe:** preprocesare de imagine, pipeline live.
**Observații:** prima dată când am simțit clar combinația dintre codul meu și un model AI care chiar „vede”.

### Ziua 8 · 06.08
**Activități:** integrare modele TensorFlow Lite (emoție / gen / vârstă) și clasa `Eag` — citirea shape-urilor de intrare/ieșire, normalizare, inferență, afișarea rezultatelor.
**Competențe:** TFLite Interpreter, maparea tensorilor, optimizări.
**Observații:** multe erori de compatibilitate între TensorFlow și numpy; am învățat să citesc mesajele de eroare și să fac downgrade/upgrade la pachete.

### Ziua 9 · 07.08
**Activități:** integrare MediaPipe Hand Landmarker; logica de numărare a degetelor pe baza unghiurilor articulațiilor, smoothing temporal, calibrarea pragurilor.
**Competențe:** geometrie 3D pe landmark-uri, filtrare temporală, UX.
**Observații:** detecția funcționa, dar numărarea era instabilă — am înțeles cât de important e să calibrezi pragurile și să folosești smoothing.

### Ziua 10 · 08.08
**Activități:** Text-to-Speech — raportare audio a emoției/genului/vârstei și a numărului de degete; toggle pentru lanternă la lumină slabă.
**Competențe:** integrare API-uri Android (TTS), acces cameră/torch.

---

## Săptămâna 3 — Optimizare, livrare, documentare

### Ziua 11 · 09.08
**Activități:** compromis FPS vs. acuratețe (rezoluția analyzer-ului, backpressure), reducerea lag-ului; fixuri Gradle / JVM target 17; rezolvarea erorilor de dependențe.
**Competențe:** profilare, rezolvarea conflictelor de build, Gradle.
**Observații:** am învățat să citesc Logcat și să îmi dau seama de unde vin problemele.

### Ziua 12 · 10.08
**Activități:** Git avansat — structurarea repo-ului, README, `.gitignore`; Git LFS pentru fișierele mari (`.tflite` / `.task`); rescrierea istoricului; push pe GitHub.
**Competențe:** management de artefacte mari, bune practici de repository.
**Observații:** la început primeam erori din cauza fișierelor prea mari, dar am învățat să folosesc Git LFS și să rescriu istoricul.

### Ziua 13 · 11.08
**Activități:** documentarea proiectului — scop, arhitectură, dependențe, instrucțiuni de build/run; capturi de ecran; notițe tehnice.
**Competențe:** comunicare tehnică, structurarea unui README.
**Observații:** am observat limitările aplicației, mai ales în lumină slabă, dar funcționează bine în condiții normale.

### Ziua 14 · 12.08
**Activități:** testare pe scenarii — lumină diferită, distanțe și poziții față/mână; validare TTS; verificarea stabilității; corecții minore de UI/UX.
**Competențe:** testare de sistem, calibrare de praguri, usability.

### Ziua 15 · 13.08
**Activități:** împachetarea livrabilelor — repo final pe GitHub, capturi și clip scurt, notițe despre lecțiile învățate; pregătirea prezentării.
**Competențe:** livrare de proiect, reflecție și sinteză.
**Observații:** am văzut proiectul complet și funcțional. Am învățat foarte multe în aceste 90 de ore.
