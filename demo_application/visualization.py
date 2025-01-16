import math
import sys
import cv2
import time
from ultralytics import YOLO
from collections import Counter

# Change to 'tuned' to use it as the default one
DEFAULT_MODEL = "synthetic"

configuration_dict = {
    "synthetic": {
        "model_path": "../final_models/yolov8m_synthetic.pt",
        "class_names": [
            "10c",
            "10d",
            "10h",
            "10s",
            "2c",
            "2d",
            "2h",
            "2s",
            "3c",
            "3d",
            "3h",
            "3s",
            "4c",
            "4d",
            "4h",
            "4s",
            "5c",
            "5d",
            "5h",
            "5s",
            "6c",
            "6d",
            "6h",
            "6s",
            "7c",
            "7d",
            "7h",
            "7s",
            "8c",
            "8d",
            "8h",
            "8s",
            "9c",
            "9d",
            "9h",
            "9s",
            "Ac",
            "Ad",
            "Ah",
            "As",
            "Jc",
            "Jd",
            "Jh",
            "Js",
            "Kc",
            "Kd",
            "Kh",
            "Ks",
            "Qc",
            "Qd",
            "Qh",
            "Qs",
        ],
    },
    "tuned": {
        "model_path": "../final_models/yolov8m_tuned.pt",
        "class_names": ["10h", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "Ah", "Jh", "Kh", "Qh"],
    },
}

print("Loading application...")

configuration_model = sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_MODEL

if configuration_model not in configuration_dict.keys():
    print(f"Allowed parameters for model are {configuration_dict.keys()}. Defaulting to {DEFAULT_MODEL}...")
    configuration_model = DEFAULT_MODEL

current_config = configuration_dict.get(configuration_model)

# Load the model and class names
model = YOLO(current_config["model_path"], verbose=False)
classNames = current_config["class_names"]

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Window title
window_title = f"Playing Cards Detection - Model: {configuration_model}"


def aggregate_detections(detections):
    """Aggregate and deduplicate detections from multiple frames."""
    # Flatten list of detections and count occurrences
    flattened = [item for sublist in detections for item in sublist]
    counts = Counter(flattened)

    # Determine final detections (e.g., cards appearing in 3+ frames)
    final_detections = [key for key, count in counts.items() if count >= 3]
    final_detections.sort()

    return final_detections


def capture_and_process_frames(cap, num_frames=10, interval=0.2):
    """Capture multiple frames and process them."""
    all_detections = []

    for _ in range(num_frames):
        ret, frame = cap.read()
        if ret:
            results = model(frame)
            frame_detections = []

            # Process results
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    frame_detections.append(classNames[cls])

            all_detections.append(frame_detections)
            time.sleep(interval)  # Short delay between frames

    # Aggregate results from all frames
    return aggregate_detections(all_detections)


while True:
    success, img = cap.read()
    cv2.imshow(window_title, img)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("c"):
        print("Capturing and processing frames...")
        detected_objects = capture_and_process_frames(cap, num_frames=10, interval=0.2)
        if detected_objects:
            print(f"Aggregated Detections: {detected_objects}")
        else:
            print("No consistent detections.")

cap.release()
cv2.destroyAllWindows()
