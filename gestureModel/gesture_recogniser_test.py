import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode_module
from mediapipe.framework.formats import landmark_pb2

import numpy as np
import cv2 as cv


base_options = python.BaseOptions(model_asset_path="/home/jojo/SIH_2024/Signa/gestureModel/gesture_recognizer.task")
video_mode = running_mode_module.VisionTaskRunningMode("VIDEO")    # Running mode
image_mode = running_mode_module.VisionTaskRunningMode("IMAGE")    # Running mode
options = vision.GestureRecognizerOptions(base_options=base_options, num_hands=2, running_mode=image_mode)
detector = vision.GestureRecognizer.create_from_options(options)

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
    
    recognizer_result = detector.recognize(mp_image)

    if len(recognizer_result.gestures) > 0:
        top_gesture = recognizer_result.gestures[0][0]
        top_landmarks_list = recognizer_result.hand_landmarks
        annotated_image = mp_image.numpy_view().copy()

        for top_landmarks in top_landmarks_list:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in top_landmarks
            ])

        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks_proto,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

        some_random_variable_name = top_gesture.category_name
        if some_random_variable_name.__str__() == "Thumb_Up":
            some_random_variable_name = "Good"
        print(f"{some_random_variable_name}")

    else:
        annotated_image = mp_image.numpy_view().copy()

    cv.imshow('Skelly', cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))
    
    # Display the resulting frame
    if cv.waitKey(1) == ord('q'):
       break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
