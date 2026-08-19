import cv2, time, threading
from deepface import DeepFace
import mediapipe as mp
import pyttsx3

# ---------- setări ----------
BACKEND = 'opencv'               # detector față pt DeepFace (rapid)
ACTIONS = ['emotion']            # poți adăuga 'age','gender'
SAY_COOLDOWN = 1.5               # secunde între anunțuri pt aceeași mână
TARGET_MAX = 640                 # downscale pt viteză
DETECT_EVERY = 5                 # detectăm fața din nou la fiecare N cadre

# ---------- TTS ----------
engine = pyttsx3.init()
engine.setProperty('rate', 185)  # viteză vorbire (ajustează după plac)
engine.setProperty('volume', 1.0)

def speak_async(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=run, daemon=True).start()

tts_enabled = True  # apasă V în fereastră ca să pornești/oprești anunțurile

# ---------- funcții utilitare ----------
def resize_keep(frame, target_max=TARGET_MAX):
    h, w = frame.shape[:2]
    s = target_max / max(h, w)
    if s < 1.0:
        return cv2.resize(frame, (int(w*s), int(h*s))), s
    return frame, 1.0

def count_fingers(lm, handed_label):
    tips = [4,8,12,16,20]; pips = [3,6,10,14,18]
    x = [p.x for p in lm]; y = [p.y for p in lm]
    up = sum(y[t] < y[p] for t,p in zip(tips[1:], pips[1:]))  # index..pinky
    if handed_label == "Right":
        up += 1 if x[tips[0]] < x[pips[0]] else 0  # thumb pe axa X
    else:
        up += 1 if x[tips[0]] > x[pips[0]] else 0
    return up

# ---------- inițializări video & modele ----------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=0,
                       min_detection_confidence=0.6, min_tracking_confidence=0.6)

last_face = None
last_emo  = "..."
t0 = time.time()
i = 0

# cooldown separat pe fiecare mână
last_said = {"Left": {"count": None, "t": 0.0}, "Right": {"count": None, "t": 0.0}}

print("Taste: ESC/Q = ieșire | V = toggle voice ON/OFF | S = snapshot")

while True:
    ok, frame = cap.read()
    if not ok: break
    i += 1

    # ====== HANDS + DEGETE ======
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res_h = hands.process(rgb)
    total_hands = 0
    if res_h.multi_hand_landmarks and res_h.multi_handedness:
        for lms, handed in zip(res_h.multi_hand_landmarks, res_h.multi_handedness):
            total_hands += 1
            mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS)
            lbl = handed.classification[0].label  # "Left" / "Right"
            fingers = count_fingers(lms.landmark, lbl)
            h, w = frame.shape[:2]
            cx, cy = int(lms.landmark[0].x*w), int(lms.landmark[0].y*h)
            cv2.putText(frame, f"{lbl}:{fingers}", (cx+10, cy-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            # TTS cu anti-spam: vorbim doar dacă s-a schimbat numărul sau a trecut cooldown
            now = time.time()
            prev = last_said[lbl]["count"]
            prev_t = last_said[lbl]["t"]
            if tts_enabled and (prev != fingers or (now - prev_t) > SAY_COOLDOWN):
                # frază simplă în RO; dacă vocea e ENG, tot o va pronunța ok
                speak_async(f"Hand { 'left' if lbl=='Left' else 'right' }: {fingers}")
                last_said[lbl]["count"] = fingers
                last_said[lbl]["t"] = now

    # ====== FACE FIND (Haar periodic) ======
    need_detect = (last_face is None) or (i % DETECT_EVERY == 0)
    if need_detect:
        small, s = resize_keep(frame, TARGET_MAX)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(gray, 1.1, 4, minSize=(80,80))
        if len(faces) > 0:
            x,y,w,h = max(faces, key=lambda b: b[2]*b[3])
            x = int(x/s); y = int(y/s); w = int(w/s); h = int(h/s)
            last_face = (x,y,w,h)
        else:
            last_face = None

    # ====== EMOȚII (DeepFace) pe ROI ======
    if last_face is not None:
        x,y,w,h = last_face
        x=max(0,x); y=max(0,y)
        roi = frame[y:y+h, x:x+w]
        try:
            res = DeepFace.analyze(
                roi, actions=ACTIONS,
                detector_backend=BACKEND, enforce_detection=False
            )
            if isinstance(res, list): res = res[0]
            last_emo = res.get('dominant_emotion', last_emo)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.putText(frame, last_emo, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        except Exception:
            cv2.putText(frame, "no emotion", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # ====== HUD / FPS ======
    fps = 1.0/(time.time()-t0); t0 = time.time()
    cv2.putText(frame, f"FPS:{fps:.1f} | TTS:{'ON' if tts_enabled else 'OFF'}",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Emotii + Degete + TTS", frame)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]: break
    elif k == ord('v'):      # toggle voice
        tts_enabled = not tts_enabled
    elif k == ord('s'):      # snapshot
        cv2.imwrite(f"snapshot_{int(time.time())}.jpg", frame)

cap.release(); cv2.destroyAllWindows()
