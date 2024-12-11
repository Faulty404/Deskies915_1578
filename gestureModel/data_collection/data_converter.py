import pandas as pd
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

from handtypes import HandTypes


def add_data(detection_result: HandLandmarkerResult, data) -> None:

    element_dict = {}

    # Add the number of hands detected and update the values
    element_dict["num_hands"] = len(detection_result.handedness)

    # Handinality will help us in dynamic inputs
    if (element_dict["num_hands"] in {0, 2}):
        # Portmanteau of hand and cardinality
        handinality = HandTypes(element_dict["num_hands"])
    elif (element_dict["num_hands"] == 1):
        # Either left or right
        handinality = HandTypes(1 if (detection_result.handedness[0].display_name == "Left") else 2)
    else:
        raise ValueError("Too many hands on screen!")

    # Add the score using handinality
    element_dict["left_hand_score"] = 0.0
    element_dict["right_hand_score"] = 0.0
    match (handinality):
        case HandTypes.N:
            break
        case HandTypes.L:
            element_dict["left_hand_score"] = detection_result.handedness[0].score
            break
        case HandTypes.R:
            element_dict["right_hand_score"] = detection_result.handedness[0].score
            break
        case HandTypes.LR:
            index_left = 0 if (detection_result.handedness[0].category_name is 'Left') else 1
            element_dict["left_hand_score"] = detection_result.handedness[index_left].score
            element_dict["right_hand_score"] = detection_result.handedness[1 - index_left].score
            # Converting from the handedness index to the data value 'index' in handedness of a particular element
            index_left = detection_result.handedness[index_left].index
            break
    
    # Adding the elements of hand_landmarks
    match (handinality):
        case HandTypes.N:
            # There are 21 elements for a single hand
            for i in range(21):
                element_dict["left_vtx_{i}_x"] = None
                element_dict["left_vtx_{i}_y"] = None
                element_dict["left_vtx_{i}_z"] = None
                element_dict["left_vtx_{i}_visibility"] = None
                element_dict["left_vtx_{i}_presence"] = None
                element_dict["right_vtx_{i}_x"] = None
                element_dict["right_vtx_{i}_y"] = None
                element_dict["right_vtx_{i}_z"] = None
                element_dict["right_vtx_{i}_visibility"] = None
                element_dict["right_vtx_{i}_presence"] = None
            break

        case HandTypes.LR:
            # There are 21 elements for a single hand
            for i in range(21):
                element_dict["left_vtx_{i}_x"] = detection_result.hand_landmarks[index_left][i].x
                element_dict["left_vtx_{i}_y"] = detection_result.hand_landmarks[index_left][i].y
                element_dict["left_vtx_{i}_z"] = detection_result.hand_landmarks[index_left][i].z
                element_dict["left_vtx_{i}_visibility"] = detection_result.hand_landmarks[index_left][i].visibility
                element_dict["left_vtx_{i}_presence"] = detection_result.hand_landmarks[index_left][i].presence
                element_dict["right_vtx_{i}_x"] = detection_result.hand_landmarks[1 - index_left][i].x
                element_dict["right_vtx_{i}_y"] = detection_result.hand_landmarks[1 - index_left][i].y
                element_dict["right_vtx_{i}_z"] = detection_result.hand_landmarks[1 - index_left][i].z
                element_dict["right_vtx_{i}_visibility"] = detection_result.hand_landmarks[1 - index_left][i].visibility
                element_dict["right_vtx_{i}_presence"] = detection_result.hand_landmarks[1 - index_left][i].presence
            break

    index_left = 0
    del index_left
    return
