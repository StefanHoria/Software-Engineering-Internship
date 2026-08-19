import cv2, time
from deepface import DeepFace
import mediapipe as mp

# ---- setări ----
BACKEND = 'opencv'        # detector folosit de DeepFace pe ROI
ACTIONS = ['emotion', 'age', 'gender']     # poți adăuga 'age','gender'
TARGET_MAX = 640          # downscale pentru viteză
DETECT_EVERY = 5          # caută fața din nou la fiecare N cadre

# ---- init ----
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=0,
                       min_detection_confidence=0.6, min_tracking_confidence=0.6)

def resize_keep(frame, target_max=TARGET_MAX):
    h, w = frame.shape[:2]
    s = target_max / max(h, w)
    if s < 1:
        return cv2.resize(frame, (int(w*s), int(h*s))), s
    return frame, 1.0

def count_fingers(lm, handed_label):
    tips = [4,8,12,16,20]; pips = [3,6,10,14,18]
    x = [p.x for p in lm]; y = [p.y for p in lm]
    up = sum(y[t] < y[p] for t,p in zip(tips[1:], pips[1:]))
    if handed_label == "Right":   # mare pe axa X
        up += 1 if x[tips[0]] < x[pips[0]] else 0
    else:
        up += 1 if x[tips[0]] > x[pips[0]] else 0
    return up

last_face = None     # (x,y,w,h) în coordonate originale
last_emo  = "..."
t0 = time.time()
i = 0

while True:
    ok, frame = cap.read()
    if not ok: break
    i += 1

    # ====== HANDS (mediapipe) ======
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res_h = hands.process(rgb)
    if res_h.multi_hand_landmarks and res_h.multi_handedness:
        for lms, handed in zip(res_h.multi_hand_landmarks, res_h.multi_handedness):
            mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS)
            lbl = handed.classification[0].label  # "Left"/"Right"
            fingers = count_fingers(lms.landmark, lbl)
            h, w = frame.shape[:2]
            cx, cy = int(lms.landmark[0].x*w), int(lms.landmark[0].y*h)
            cv2.putText(frame, f"{lbl}:{fingers}", (cx+10, cy-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # ====== FACE FIND (rapid cu Haar, la fiecare N cadre) ======
    need_detect = (last_face is None) or (i % DETECT_EVERY == 0)
    if need_detect:
        small, s = resize_keep(frame, TARGET_MAX)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(gray, 1.1, 4, minSize=(80,80))
        if len(faces) > 0:
            # cea mai mare față
            x,y,w,h = max(faces, key=lambda b: b[2]*b[3])
            x = int(x/s); y = int(y/s); w = int(w/s); h = int(h/s)
            last_face = (x,y,w,h)
        else:
            last_face = None

    # ====== EMOTIONS (DeepFace) pe ROI față ======
    if last_face is not None:
        x,y,w,h = last_face
        x=max(0,x); y=max(0,y)
        roi = frame[y:y+h, x:x+w]
        try:
            res = DeepFace.analyze(
                roi, actions=ACTIONS,
                detector_backend=BACKEND,
                enforce_detection=False
            )
            if isinstance(res, list): res = res[0]
            emo = res.get('dominant_emotion', last_emo)
            age = res.get('age', '?')
            dom_gender = res.get('dominant_gender', None)
            if dom_gender is None:
                # dacă modelul returnează doar dictul de genuri
                gdict = res.get('gender', {})
                dom_gender = max(gdict, key=gdict.get) if isinstance(gdict, dict) and gdict else '?'

            last_emo = emo  # păstrează emoția pt. afișare între cadre

            # desenează ROI și eticheta completă
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"{emo} | {age} | {dom_gender}"
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        except Exception as e:
            # debug pe ecran dacă vrei:
            cv2.putText(frame, "no emotion", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
    else:
        cv2.putText(frame, "no face", (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    # ====== HUD / FPS ======
    fps = 1.0/(time.time()-t0); t0 = time.time()
    cv2.putText(frame, f"FPS:{fps:.1f} | Bkd:{BACKEND}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Emotii + Degete (robust)", frame)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]: break

cap.release(); cv2.destroyAllWindows()
