# ---------------------------------------------------------------------------- #

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision.core import vision_task_running_mode as running_mode_module
import numpy as np
import cv2 as cv
import csv
import sys

# ---------------------------------------------------------------------------- #

from data_converter import add_data, get_class_from_filename
from drawing import draw_landmarks_on_image

# ---------------------------------------------------------------------------- #

if len(sys.argv) < 2:
    print("Too few command line arguments provided!")
    exit()
elif len(sys.argv) > 3:
    print("Too many command line arguments provided!")
    exit()

# Loading the model
base_options = python.BaseOptions(model_asset_path="/home/jojo/SIH_2024/Signa/gestureModel/hand_landmarker.task")
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

print(sys.argv[1])

image = mp.Image.create_from_file(sys.argv[1])
detection_result = detector.detect(image)

# Converting the detection result to a dictionary to be appended to add_data
data_list = list()
add_data(detection_result, data_list, get_class_from_filename(sys.argv[1]))

# ---------------------------------------------------------------------------- #
# Code to add data_list to CSV

filename = "./hand_photo_data.csv"
with open(filename, mode="a", newline="") as file:
    csv_writer = csv.DictWriter(file, fieldnames=data_list[0].keys())

    if file.tell() == 0:
        csv_writer.writeheader()

    csv_writer.writerow(data_list[0])

# ---------------------------------------------------------------------------- #


if len(sys.argv) == 3 and int(sys.argv[2]) == 1:
    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    
    while True:
        cv.imshow("Window", cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))
        if cv.waitKey(1) == ord('q'):
            break

