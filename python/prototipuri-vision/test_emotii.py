import cv2, time
from deepface import DeepFace

# --- setări ---
DETECT_EVERY = 5     # detectează fața la fiecare N cadre
EMO_EVERY    = 3     # recalculează emoția la fiecare N cadre
TARGET_MAX   = 640   # latura mare la care micșorăm frame-ul pentru viteză
BACKEND      = 'opencv'  # detector rapid: 'opencv' (nu 'mtcnn')

# detector ultra-rapid pentru fallback: Haar
haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

last_box = None      # (x, y, w, h) în coordonate originale
last_emo = "..."
i = 0
t0 = time.time()

def resize_keep(frame, target_max=TARGET_MAX):
    h, w = frame.shape[:2]
    s = target_max / max(h, w)
    if s < 1.0:
        frame_small = cv2.resize(frame, (int(w*s), int(h*s)))
    else:
        frame_small = frame
        s = 1.0
    return frame_small, s

while True:
    ok, frame = cap.read()
    if not ok: break
    i += 1

    # 1) downscale pt. viteză
    small, s = resize_keep(frame, TARGET_MAX)

    # 2) detectăm doar din când în când
    need_detect = (last_box is None) or (i % DETECT_EVERY == 0)
    if need_detect:
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(gray, 1.1, 4, minSize=(80,80))
        if len(faces) > 0:
            # alege cea mai mare față
            x,y,w,h = max(faces, key=lambda b: b[2]*b[3])
            # scalează la coordonate originale
            x0 = int(x / s); y0 = int(y / s); w0 = int(w / s); h0 = int(h / s)
            last_box = (x0, y0, w0, h0)
        else:
            last_box = None

    # 3) dacă avem o față, recalculează emoția mai rar
    if last_box is not None and (i % EMO_EVERY == 0):
        x, y, w, h = last_box
        x = max(0, x); y = max(0, y)
        roi = frame[y:y+h, x:x+w]
        try:
            res = DeepFace.analyze(
                roi,
                actions=['emotion'],
                detector_backend=BACKEND,   # rapid
                enforce_detection=False
            )
            if isinstance(res, list): res = res[0]
            last_emo = res.get('dominant_emotion', last_emo)
        except Exception:
            pass

    # 4) desenare UI
    if last_box is not None:
        x,y,w,h = last_box
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, last_emo, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # FPS
    fps = 1.0 / (time.time() - t0)
    t0 = time.time()
    cv2.putText(frame, f"FPS: {fps:.1f}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Fast Emotions", frame)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]: break

cap.release(); cv2.destroyAllWindows()
