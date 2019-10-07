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
        self.mu = self.model.copy()
        self.eps = self.model.copy()
        self.sigma = self.model.copy()
        self.rho = self.model.copy()

        return None

