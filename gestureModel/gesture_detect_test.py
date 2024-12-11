import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode_module

import numpy as np
import cv2 as cv

from drawing import draw_landmarks_on_image

base_options = python.BaseOptions(model_asset_path="/home/jojo/SIH_2024/Signa/gestureModel/hand_landmarker.task")
video_mode = running_mode_module.VisionTaskRunningMode("VIDEO")    # Running mode
image_mode = running_mode_module.VisionTaskRunningMode("IMAGE")    # Running mode
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2, running_mode=image_mode)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

iterations: int = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here

    # Convert the frame received from OpenCV to a MediaPipe’s Image object
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    
    detection_result = detector.detect(mp_image)
    if iterations >= 0:
        if len(detection_result.hand_landmarks) == 0:
            print("No Hands")
            pass
        elif len(detection_result.hand_landmarks) == 1:
            print("One Hand", len(detection_result.hand_landmarks[0]), end="\n\n")
        else:
            print("Two Hands", len(detection_result.hand_landmarks[0]), len(detection_result.hand_landmarks[1]), end="\n\n")
        iterations += 1

    annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
    cv.imshow('Skelly', cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))
    
    # Display the resulting frame
    if cv.waitKey(1) == ord('q'):
       break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
