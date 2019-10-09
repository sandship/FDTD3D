import json
import numpy as np
import numba

def load_config(config_path):
    """
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return config


def transform_tidy_3darray(raw_data, to_form="3d-array"):
    if to_form == "3d-array":
        tidy = raw_data.copy()
        tidy_size = {
            "x" : np.max(tidy[:, 0]) + 1,
            "y" : np.max(tidy[:, 1]) + 1,
            "z" : np.max(tidy[:, 2]) + 1
        }

        darray = np.zeros(shape=(tidy_size["x"], tidy_size["y"], tidy_size["z"]))
        for item in tidy:
            darray[item[0], item[1], item[2]] = item[3]

        return darray
    elif to_form == "tidy":
        darray = raw_data.copy()
        darray_size = darray.shape
        
        ###

    else:
        raise ArgumentError

if __name__ == "__main__":
    with open(r'../asset/model/testmodel.dat', "r") as fh:
        lines = fh.readlines()
    lines = [[int(element) for element in line.split()] for line in lines]
    tidy = np.array(lines)
    darray = transform_tidy_3darray(tidy, to_form='3d-array')