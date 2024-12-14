# ---------------------------------------------------------------------------- #

import sys

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
from many_photos import get_photo_file_paths
from drawing import draw_landmarks_on_image

# ---------------------------------------------------------------------------- #

# Loading the model
base_options = python.BaseOptions(
    model_asset_path="/home/jojo/SIH_2024/Signa/gestureModel/hand_landmarker.task"
)
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# ---------------------------------------------------------------------------- #

def add_entry_and_display(filename: str, display: bool) -> None:
    image = mp.Image.create_from_file(filename)
    detection_result = detector.detect(image)

    # Converting the detection result to a dictionary to be appended to add_data
    data_list = list()
    add_data(detection_result, data_list, get_class_from_filename(filename))

    # Code to add data_list to CSV

    filename = "./hand_photo_data.csv"
    with open(filename, mode="a", newline="") as file:
        csv_writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
        if file.tell() == 0:
            csv_writer.writeheader()
        csv_writer.writerow(data_list[0])


    if len(sys.argv) == 3 and int(display) == 1:
        annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
    
        while True:
            cv.imshow("Window", cv.cvtColor(annotated_image, cv.COLOR_RGB2BGR))
            if cv.waitKey(1) == ord('q'):
                break

# ---------------------------------------------------------------------------- #

def main() -> None:
    if len(sys.argv) < 2:
        print("Too few command line arguments provided!")
        print("Usage: python collection.py <path_to_photo_directory> [<display_photo>]")
        print("<display_photo>{0, 1}= whether to display the annotated photo or not (default 0)")
        exit(1)
    elif len(sys.argv) > 3:
        print("Too many command line arguments provided!")
        print("Usage: python collection.py <path_to_photo_directory> [<display_photo>]")
        print("<display_photo>{0, 1}= whether to display the annotated photo or not (default 0)")
        exit(1)

    filepaths = get_photo_file_paths(sys.argv[1])
    if len(sys.argv[1]) == 2:
        for filepath in filepaths:
            add_entry_and_display(filepath, False)
    else:
        for filepath in filepaths:
            add_entry_and_display(filepath, int(sys.argv[2]) == 1)

# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
