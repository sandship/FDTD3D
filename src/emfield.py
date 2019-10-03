import numpy as np

from src import myutility as myutil

class EMfield(object):
    def __init__(self, config_path=r"./configure/settings.json"):
        self.Config = myutil.load_config(config_path)["config"]
        self.Parameter = myutil.load_config(config_path)["parameter"]

        self.Xaxis = np.random.uniform(
            size=(self.Config["size"]["x"], self.Config["size"]["y"], self.Config["size"]["z"])
        )
        self.Yaxis = np.random.uniform(
            size=(self.Config["size"]["x"], self.Config["size"]["y"], self.Config["size"]["z"])
        )
        self.Zaxis = np.random.uniform(
            size=(self.Config["size"]["x"], self.Config["size"]["y"], self.Config["size"]["z"])
        )

    def norm(self):
        self.norm = np.sqrt(
            np.power(self.Xaxis, 2) 
            + np.power(self.Yaxis, 2) 
            + np.power(self.Zaxis, 2)
        )
        return self.norm

    def phase(self):
        self.phase = 0
        return self.phase

    def next(self):
        return None