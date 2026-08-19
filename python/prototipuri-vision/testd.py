import cv2, time
from deepface import DeepFace
import mediapipe as mp

# -------- setări ----------
BACKEND = 'opencv'   # detector față rapid pentru DeepFace
ACTIONS = ['emotion']  # poți adăuga 'age','gender' dacă vrei
SHOW_FPS = True

# -------- inițializări ----
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

t0 = time.time()
last_emo = "..."

def count_fingers(lm, handedness_label, w, h):
    """
    lm: landmark list (21 puncte) cu coordonate normalizate [0..1]
    handedness_label: 'Left' sau 'Right' (din mediapipe)
    w,h: dimensiuni cadru
    Returnează număr degete ridicate (0..5).
    Logica:
      - pentru index/middle/ring/pinky: vârful degetului (tip) mai sus (y mai mic) decât articulația PIP
      - pentru thumb: test pe axa X (în funcție de mâna stângă/dreaptă)
    """
    # indexul landmark-urilor cheie
    tips  = [4, 8, 12, 16, 20]      # deget mare, index, mijlociu, inelar, mic
    pips  = [3, 6, 10, 14, 18]      # articulații PIP (proximal)
    x = [lm[i].x for i in range(21)]
    y = [lm[i].y for i in range(21)]

    up = 0

    # degetele (index..pinky): vârful mai sus decât PIP => ridicat
    for tip, pip in zip(tips[1:], pips[1:]):
        if y[tip] < y[pip]:   # coord y mic = mai sus în imagine
            up += 1

    # degetul mare: comparăm pe axa X.
    # Pentru mâna dreaptă: thumb ridicat când x[tip] < x[pip] (vârful spre stânga)
    # Pentru mâna stângă: opus (vârful spre dreapta)
    if handedness_label == "Right":
        if x[tips[0]] < x[pips[0]]:
            up += 1
    else:  # Left
        if x[tips[0]] > x[pips[0]]:
            up += 1

    return up

while True:
    ok, frame = cap.read()
    if not ok: break

    # ====== EMOȚII (față) ======
    try:
        res = DeepFace.analyze(
            frame,
            actions=ACTIONS,
            detector_backend=BACKEND,
            enforce_detection=False
        )
        faces = res if isinstance(res, list) else [res]
        for f in faces:
            x,y,w,h = f['region'].values()
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            label = f.get('dominant_emotion', '...')
            last_emo = label
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    except Exception:
        pass

    # ====== DEGETE (mână) ======
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    total_hands = 0
    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_lms, handed in zip(result.multi_hand_landmarks, result.multi_handedness):
            total_hands += 1
            # desenează schelet mână
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

            # handedness: "Left" / "Right"
            handed_label = handed.classification[0].label

            # număr degete
            h, w = frame.shape[:2]
            fingers = count_fingers(hand_lms.landmark, handed_label, w, h)

            # poziție text: în dreptul încheieturii (landmark 0)
            cx, cy = int(hand_lms.landmark[0].x * w), int(hand_lms.landmark[0].y * h)
            cv2.putText(frame, f"{handed_label}: {fingers}", (cx+10, cy-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # ====== HUD / FPS ======
    if SHOW_FPS:
        fps = 1.0/(time.time()-t0); t0 = time.time()
        cv2.putText(frame, f"FPS: {fps:.1f} | Hands: {total_hands} | Emo: {last_emo}",
                    (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Emotii + Numara Degete", frame)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]: break

cap.release()
cv2.destroyAllWindows()
