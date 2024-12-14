# ---------------------------------------------------------------------------- #

import pandas as pd
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult
from handtypes import HandTypes

# ---------------------------------------------------------------------------- #

import re
import os

# ---------------------------------------------------------------------------- #

def get_class_from_filename(inp: str) -> str:
    inp = os.path.basename(inp)
    matcher = re.match(r"^[^_]+", inp)
    if matcher:
        return matcher.group(0)
    else:
        return ""


def add_data(detection_result: HandLandmarkerResult, data, element_class: str) -> None:
    element_dict = {}

    element_dict["element_class"] = element_class

    # Add the number of hands detected and update the values
    element_dict["num_hands"] = len(detection_result.handedness)

    # Handinality will help us in dynamic inputs
    if (element_dict["num_hands"] == 0):
        # Portmanteau of hand and cardinality
        handinality = HandTypes(0)
    elif (element_dict["num_hands"] == 1):
        # Either left or right
        handinality = HandTypes(1 if (detection_result.handedness[0][0].display_name == "Left") else 2)
    elif (element_dict["num_hands"] == 2):
        # Both are present
        handinality = HandTypes(3)
    else:
        raise ValueError("Too many hands on screen!")

    index_left = 0
    # Add the score using handinality
    element_dict["left_hand_score"] = 0.0
    element_dict["right_hand_score"] = 0.0
    print(f"Handinality: {handinality}\nNumber of hands: {element_dict['num_hands']}", end="\n\n")
    match (handinality):
        case HandTypes.L:
            element_dict["left_hand_score"] = detection_result.handedness[0][0].score
        case HandTypes.R:
            element_dict["right_hand_score"] = detection_result.handedness[0][0].score
        case HandTypes.LR:
            index_left = 0 if (detection_result.handedness[0][0].category_name == 'Left') else 1
            element_dict["left_hand_score"] = detection_result.handedness[index_left][0].score
            element_dict["right_hand_score"] = detection_result.handedness[1 - index_left][0].score
            # Converting from the handedness index to the data value 'index' in handedness of a particular element
            index_left = detection_result.handedness[index_left][0].index
            print(f"index_left is currently {index_left}")


    # Adding the elements of hand_landmarks
    # There are 21 elements for a single hand

    for i in range(21):
        element_dict[f"left_vtx_{i}_x"] = 100.0
        element_dict[f"left_vtx_{i}_y"] = 100.0
        element_dict[f"left_vtx_{i}_z"] = 100.0
        element_dict[f"left_vtx_{i}_visibility"] = 0.0
        element_dict[f"left_vtx_{i}_presence"] = 0.0
        element_dict[f"right_vtx_{i}_x"] = 100.0
        element_dict[f"right_vtx_{i}_y"] = 100.0
        element_dict[f"right_vtx_{i}_z"] = 100.0
        element_dict[f"right_vtx_{i}_visibility"] = 0.0
        element_dict[f"right_vtx_{i}_presence"] = 100.0

    match (handinality):
        case HandTypes.L:
            # There are 21 elements for a single hand
            for i in range(len(detection_result.hand_landmarks[index_left])):
                element_dict[f"left_vtx_{i}_x"] = detection_result.hand_world_landmarks[index_left][i].x
                element_dict[f"left_vtx_{i}_y"] = detection_result.hand_world_landmarks[index_left][i].y
                element_dict[f"left_vtx_{i}_z"] = detection_result.hand_world_landmarks[index_left][i].z
                element_dict[f"left_vtx_{i}_visibility"] = detection_result.hand_world_landmarks[index_left][i].visibility
                element_dict[f"left_vtx_{i}_presence"] = detection_result.hand_world_landmarks[index_left][i].presence

        case HandTypes.R:
            for i in range(len(detection_result.hand_landmarks[1 - index_left])):
                element_dict[f"right_vtx_{i}_x"] = detection_result.hand_world_landmarks[1 - index_left][i].x
                element_dict[f"right_vtx_{i}_y"] = detection_result.hand_world_landmarks[1 - index_left][i].y
                element_dict[f"right_vtx_{i}_z"] = detection_result.hand_world_landmarks[1 - index_left][i].z
                element_dict[f"right_vtx_{i}_visibility"] = detection_result.hand_world_landmarks[1 - index_left][i].visibility
                element_dict[f"right_vtx_{i}_presence"] = detection_result.hand_world_landmarks[1 - index_left][i].presence

        case HandTypes.LR:
            # There are 21 elements for a single hand
            for i in range(21):
                element_dict[f"left_vtx_{i}_x"] = detection_result.hand_world_landmarks[index_left][i].x
                element_dict[f"left_vtx_{i}_y"] = detection_result.hand_world_landmarks[index_left][i].y
                element_dict[f"left_vtx_{i}_z"] = detection_result.hand_world_landmarks[index_left][i].z
                element_dict[f"left_vtx_{i}_visibility"] = detection_result.hand_world_landmarks[index_left][i].visibility
                element_dict[f"left_vtx_{i}_presence"] = detection_result.hand_world_landmarks[index_left][i].presence
                element_dict[f"right_vtx_{i}_x"] = detection_result.hand_world_landmarks[1 - index_left][i].x
                element_dict[f"right_vtx_{i}_y"] = detection_result.hand_world_landmarks[1 - index_left][i].y
                element_dict[f"right_vtx_{i}_z"] = detection_result.hand_world_landmarks[1 - index_left][i].z
                element_dict[f"right_vtx_{i}_visibility"] = detection_result.hand_world_landmarks[1 - index_left][i].visibility
                element_dict[f"right_vtx_{i}_presence"] = detection_result.hand_world_landmarks[1 - index_left][i].presence

    data.append(element_dict)

    index_left = 0
    del index_left
    return
