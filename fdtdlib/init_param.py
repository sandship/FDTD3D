from fdtdlib import myutility as myutil
import numpy as np


class InitialzeSpaceParameter(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, config_path=r"./configure/settings.json"):
        self.setting = myutil.load_config(config_path)
        self.set_parameter = myutil.load_config(config_path)["parameter"]["set"]
        self.general_parameter = myutil.load_config(config_path)["parameter"]["general"]

        self.__load_model(self.setting["model"]["path"])
        self.model_size = {
            "x" : np.max(self.model[:, 0]),
            "y" : np.max(self.model[:, 1]),
            "z" : np.max(self.model[:, 2])
        }

        self.calc_parameter()

        return None

    def __load_model(self, path_):
        with open(path_, "r") as fh:
            lines = fh.readlines()
        
        lines = [[int(element) for element in line.split()] for line in lines]
        self.model = np.array(lines)
        return None

    def calc_parameter(self):
        self.dr = self.set_parameter["descrete"]
        self.c = self.general_parameter["c"]
        self.dt = 0.99 / (self.c * np.sqrt(3.0) * self.dr)

        self.mu = self.general_parameter["mu"]
        self.eps = self.general_parameter["eps"]
        self.sigma = self.general_parameter["sigma"]
        self.rho = self.general_parameter["rho"]

        self.ce = self.dt * self.eps / self.dr
        self.ch = self.dt * self.mu / self.dr

        return None

