import cv2, time, threading
import pyttsx3
import easyocr
import numpy as np

# ---- setări ----
LANGS = ['ro', 'en']          # limbi OCR (adaugă 'de','fr' etc. dacă e nevoie)
MIN_CONF = 0.55               # prag încrederii OCR (0..1)
SAY_COOLDOWN = 2.0            # secunde între anunțuri audio pentru același titlu
ROTATIONS = [0, 90, -90]      # încearcă și rotiri (cotoare verticale)
DRAW_BOXES = True

# ---- TTS ----
engine = pyttsx3.init()
engine.setProperty('rate', 185)
engine.setProperty('volume', 1.0)
def speak_async(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=run, daemon=True).start()

# ---- OCR ----
reader = easyocr.Reader(LANGS, gpu=False)  # pe CPU

# ---- utilitare ----
def preprocess(img):
    # mică corecție de contrast și denoise ușor (ajută OCR)
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.bilateralFilter(g, d=7, sigmaColor=60, sigmaSpace=60)
    g = cv2.equalizeHist(g)
    return g

def try_ocr(frame):
    """ Încearcă OCR pe cadre rotite; returnează o listă de (text, conf, box) """
    results = []
    for rot in ROTATIONS:
        img = frame if rot == 0 else cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE if rot==90 else cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = preprocess(img)
        # format rezultat easyocr: [ [bbox, text, conf], ... ]
        out = reader.readtext(gray, detail=1, paragraph=False)
        # re-proiectăm box-urile înapoi pe frame-ul original dacă am rotit
        for (box, text, conf) in out:
            if not text or conf < MIN_CONF:
                continue
            box = np.array(box, dtype=np.float32)
            if rot != 0:
                # inversează rotația pentru box
                h, w = frame.shape[:2]
                if rot == 90:
                    box = np.array([[p[1], w - p[0]] for p in box])
                elif rot == -90:
                    box = np.array([[h - p[1], p[0]] for p in box])
            results.append((text.strip(), float(conf), box.astype(int)))
    return results

def likely_title(text):
    """ Heuristică simplă: filtrează fragmente banale (ex. 'the', 'and', coduri) """
    t = text.strip()
    if len(t) < 3: return False
    # evită linii prea „numerice” (coduri/ISBN parțiale)
    digits = sum(ch.isdigit() for ch in t)
    if digits > len(t)*0.6: return False
    # multe titluri au majuscule inițiale sau cuvinte > 3 litere
    words = [w for w in t.split() if len(w) >= 3]
    return len(words) >= 1

# ---- video ----
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

print("Taste: ESC/Q = exit | A = audio ON/OFF | S = snapshot")
audio_on = True
last_said = {}  # titlu -> timestamp

t0 = time.time()
while True:
    ok, frame = cap.read()
    if not ok: break

    # downscale pentru viteză (opțional)
    H, W = frame.shape[:2]
    scale = 960 / max(H, W)
    if scale < 1.0:
        frame_small = cv2.resize(frame, (int(W*scale), int(H*scale)))
    else:
        frame_small = frame

    # OCR
    results = try_ocr(frame_small)

    # grupare / desen
    shown = set()
    for text, conf, box in results:
        if not likely_title(text):
            continue
        # evită repetări ale aceluiași text în același cadru
        key = text.lower()
        if key in shown:
            continue
        shown.add(key)

        # box + label
        if DRAW_BOXES:
            pts = box.reshape(-1,1,2)
            cv2.polylines(frame_small, [pts], True, (0,255,0), 2)
            cv2.putText(frame_small, f"{text} ({conf:.2f})",
                        (box[0][0], max(20, box[0][1]-10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

        # TTS cu anti-spam
        now = time.time()
        last = last_said.get(key, 0.0)
        if audio_on and (now - last) >  SAY_COOLDOWN:
            speak_async(text)
            last_said[key] = now

    # HUD
    fps = 1.0/(time.time()-t0); t0 = time.time()
    cv2.putText(frame_small, f"OCR FPS:{fps:.1f} | Audio:{'ON' if audio_on else 'OFF'}",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Book Title Reader", frame_small)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]: break
    elif k == ord('a'): audio_on = not audio_on
    elif k == ord('s'): cv2.imwrite(f"title_snap_{int(time.time())}.jpg", frame)

cap.release(); cv2.destroyAllWindows()
