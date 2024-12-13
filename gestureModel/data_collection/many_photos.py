# ---------------------------------------------------------------------------- #

import os

# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #

def get_photo_file_paths(dir_path: str):
    filepaths = []
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        if os.path.isfile(path):
            filepaths.append(path)
    print(filepaths)
    return filepaths
