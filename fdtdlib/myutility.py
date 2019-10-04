import json

def load_config(config_path):
    """
    """
    with open(config_path, "r") as f:
        config = json.loads(f.read())
    return config