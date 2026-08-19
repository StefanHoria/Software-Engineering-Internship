import cv2, csv, time, os, collections
from datetime import datetime
from deepface import DeepFace

BACKEND = 'opencv'         # rapid; poți încerca și 'mtcnn'
ACTIONS = ['emotion','age','gender']
DETECT_EVERY = 5           # detectează fața la fiecare N cadre
EMO_SMOOTH_N = 5           # lățimea ferestrei pt. smoothing

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    raise SystemExit("Camera nu s-a putut deschide pe index 0.")

# CSV log
os.makedirs("out", exist_ok=True)
csv_path = os.path.join("out", f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
logf = open(csv_path, "w", newline="", encoding="utf-8")
logger = csv.writer(logf); logger.writerow(["ts","face_id","emotion","conf","age","gender","x","y","w","h","fps"])

# Video recording
writer = None; recording = False

def resize_keep(frame, target_max=640):
    h, w = frame.shape[:2]
    s = target_max / max(h, w)
    if s < 1.0:
        frame_small = cv2.resize(frame, (int(w*s), int(h*s)))
    else:
        frame_small, s = frame, 1.0
    return frame_small, s

haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
last_boxes = []  # list of (x,y,w,h)
emo_hist = collections.defaultdict(lambda: collections.deque(maxlen=EMO_SMOOTH_N))
t0 = time.time(); i = 0

def smooth_label(face_id, probs_dict):
    # calculează media mobile pe emoții
    emo_hist[face_id].append(probs_dict)
    # agregăm pe chei
    avg = {}
    for snap in emo_hist[face_id]:
        for k,v in snap.items(): avg[k] = avg.get(k, 0.0) + float(v)
    for k in avg: avg[k] /= len(emo_hist[face_id])
    emo = max(avg, key=avg.get)
    return emo, avg[emo]

while True:
    ok, frame = cap.read()
    if not ok: break
    i += 1

    # 1) detectare față(țe) din când în când (rapid cu Haar)
    need_detect = (i % DETECT_EVERY == 0) or (not last_boxes)
    if need_detect:
        small, s = resize_keep(frame, 640)
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(gray, 1.1, 4, minSize=(80,80))
        last_boxes = []
        for (x,y,w,h) in faces:
            x0,y0,w0,h0 = int(x/s), int(y/s), int(w/s), int(h/s)
            last_boxes.append((x0,y0,w0,h0))

    # 2) analiză atribute pentru fiecare față (emoție/age/gender)
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    for idx, (x,y,w,h) in enumerate(last_boxes):
        x=max(0,x); y=max(0,y)
        roi = frame[y:y+h, x:x+w]
        try:
            res = DeepFace.analyze(
                roi, actions=ACTIONS,
                detector_backend=BACKEND, enforce_detection=False
            )
            if isinstance(res, list): res = res[0]

            # smoothing pe emoții (folosim dictul cu probabilități)
            probs = res.get('emotion', {}) if isinstance(res.get('emotion', {}), dict) else {}
            emo, conf = (res['dominant_emotion'], 1.0)
            if probs:
                emo, conf = smooth_label(idx, probs)

            age = res.get('age', '?')
            gender = res.get('gender', '?')

            # UI
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            label = f"{emo} ({conf:.2f}) | {age} | {gender}"
            cv2.putText(frame, label, (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255,255,255), 2)

            # log CSV
            fps = 1.0/(time.time()-t0)
            logger.writerow([ts, idx, emo, f"{conf:.3f}", age, gender, x, y, w, h, f"{fps:.2f}"])
        except Exception:
            pass

    # FPS overlay
    fps = 1.0/(time.time()-t0); t0 = time.time()
    cv2.putText(frame, f"FPS: {fps:.1f}  Rec:{'ON' if recording else 'OFF'}  Bkd:{BACKEND}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # 3) video record
    if recording and writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        h,w = frame.shape[:2]
        out_path = os.path.join("out", f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        writer = cv2.VideoWriter(out_path, fourcc, 20.0, (w,h))
    if recording and writer is not None:
        writer.write(frame)

    cv2.imshow("DeepFace Demo Plus", frame)
    k = cv2.waitKey(1) & 0xFF
    if k in [27, ord('q')]:  # ESC/Q = exit
        break
    elif k == ord('s'):      # S = snapshot
        shot = os.path.join("out", f"shot_{datetime.now().strftime('%H%M%S')}.jpg")
        cv2.imwrite(shot, frame)
    elif k == ord('r'):      # R = record toggle
        recording = not recording
        if not recording and writer is not None:
            writer.release(); writer = None
    elif k == ord('+'):      # + = detectează mai rar (mai mult FPS)
        DETECT_EVERY = min(DETECT_EVERY+1, 15)
    elif k == ord('-'):      # - = detectează mai des (mai precis tracking)
        DETECT_EVERY = max(DETECT_EVERY-1, 1)

# cleanup
if writer is not None: writer.release()
cap.release(); cv2.destroyAllWindows(); logf.close()
print(f"Log salvat: {csv_path}")
