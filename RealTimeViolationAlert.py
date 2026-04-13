import cv2
from ultralytics import YOLO
import mediapipe as mp
from datetime import datetime
import time

# -----------------------------
# LOAD MODELS
# -----------------------------
model = YOLO("yolov8s.pt")  # Better accuracy

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

# -----------------------------
# ALERT ENGINE
# -----------------------------
class AlertEngine:
    def __init__(self):
        self.risk_score = 0
        self.phone_count = 0
        self.person_violation_count = 0
        self.face_missing_count = 0
        self.look_away_count = 0

        self.last_phone_time = 0  # cooldown
        self.last_person_time = 0

    def alert(self, msg):
        print("\n⚠ ALERT:", msg)
        print("Time:", datetime.now().strftime("%H:%M:%S"))
        print("Risk Score:", self.risk_score)

    def update_risk(self, violation):
        scores = {
            "PHONE": 60,
            "MULTIPLE_PERSON": 40,
            "FACE_MISSING": 20,
            "LOOKING_AWAY": 10
        }
        self.risk_score += scores.get(violation, 0)

# -----------------------------
# INIT
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

engine = AlertEngine()

print("✅ AI Proctoring Started (Press 'q' to exit)")

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # -----------------------------
    # YOLO DETECTION
    # -----------------------------
    results = model(frame, imgsz=640, conf=0.25, verbose=False)

    person_count = 0
    phone_detected = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # PERSON
            if cls == 0 and conf > 0.5:
                person_count += 1
                color = (0, 255, 0)
                label = f"Person {conf:.2f}"

            # PHONE
            elif cls == 67 and conf > 0.3:
                phone_detected = True
                color = (0, 0, 255)
                label = f"Phone {conf:.2f}"

            else:
                continue

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    current_time = time.time()

    # -----------------------------
    # MULTIPLE PERSON (with cooldown)
    # -----------------------------
    if person_count > 1 and current_time - engine.last_person_time > 3:
        engine.person_violation_count += 1
        engine.last_person_time = current_time

        engine.update_risk("MULTIPLE_PERSON")
        engine.alert("Multiple persons detected")

        if engine.person_violation_count >= 3:
            print("\n❌ TERMINATED: Multiple persons detected 3 times")
            break

    # -----------------------------
    # PHONE DETECTION (3 TIMES + cooldown)
    # -----------------------------
    if phone_detected and current_time - engine.last_phone_time > 3:
        engine.phone_count += 1
        engine.last_phone_time = current_time

        engine.update_risk("PHONE")
        engine.alert("Mobile phone detected")

        print("Phone Count:", engine.phone_count)

        if engine.phone_count >= 3:
            print("\n❌ TERMINATED: Phone detected 3 times")
            break

    # -----------------------------
    # FACE + LOOKING AWAY
    # -----------------------------
    face_results = face_mesh.process(frame_rgb)

    if not face_results.multi_face_landmarks:
        engine.face_missing_count += 1

        if engine.face_missing_count > 20:
            engine.update_risk("FACE_MISSING")
            engine.alert("Face not visible")

    else:
        engine.face_missing_count = 0

        landmarks = face_results.multi_face_landmarks[0].landmark

        left_eye = landmarks[33]
        right_eye = landmarks[263]

        center_x = (left_eye.x + right_eye.x) / 2

        if center_x < 0.35 or center_x > 0.65:
            engine.look_away_count += 1
        else:
            engine.look_away_count = 0

        if engine.look_away_count > 15:
            engine.update_risk("LOOKING_AWAY")
            engine.alert("Looking away detected")

    # -----------------------------
    # RISK TERMINATION
    # -----------------------------
    if engine.risk_score >= 120:
        print("\n❌ TERMINATED: High cheating risk detected")
        break

    # -----------------------------
    # DISPLAY
    # -----------------------------
    cv2.putText(frame, f"Persons: {person_count}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Phone Count: {engine.phone_count}",
                (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Risk Score: {engine.risk_score}",
                (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.putText(frame, f"Look Away: {engine.look_away_count}",
                (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

    cv2.imshow("Advanced AI Proctoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
cv2.destroyAllWindows()

print("Monitoring Ended.")