import numpy as np

from src import myutility as myutil

class Model(object):
    def __init__(self, config_path=r"./configure/settings.json"):
        self.Config = myutil.load_config(config_path)["config"]
        self.Parameter = myutil.load_config(config_path)["parameter"]

        self.isMetal = np.zeros(
            shape=(self.config["size"]["x"], self.config["size"]["y"], self.config["size"]["z"])
        )
        
        self.PermLabel = np.zeros(
            shape=(self.config["size"]["x"], self.config["size"]["y"], self.config["size"]["z"])
        )