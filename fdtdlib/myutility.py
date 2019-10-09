import json
import numpy as np
import numba

def load_config(config_path):
    """
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return config

if __name__ == "__main__":
    with open(r'../asset/model/testmodel.dat', "r") as fh:
        lines = fh.readlines()
    lines = [[int(element) for element in line.split()] for line in lines]
    tidy = np.array(lines)
    darray = transform_tidy_3darray(tidy, to_form='3d-array')