import json
import numpy as np
import numba

def load_config(config_path):
    """Load JSON config file
    
    Arguments:
        config_path {str(path)} -- relative/full path JSON file
    
    Returns:
        dict -- loaded JSON as dict
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return config
