import numpy as np


class EMfield(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, param):
        self.param = param

        self.set_parameter = self.param.set_parameter
        self.general_parameter = self.param.general_parameter

        self.Xaxis = self.__init_field()
        self.Yaxis = self.__init_field()
        self.Zaxis = self.__init_field()

        return None

    def __init_field(self):
        return np.zeros(shape=(self.param.model_size["x"] + 1, self.param.model_size["y"] + 1, self.param.model_size["z"] + 1))

    def load_field(self):
        return None

    def update_field(self, N=1):
        return None

    def calc_scatterfield(self):
        return None

    def calc_totalfield(self):
        return None

    def calc_norm(self):
        self.norm = np.sqrt(
            self.Xaxis ** 2 +
            self.Yaxis ** 2 +
            self.Zaxis ** 2
        )
        return None

    def calc_phase(self):
        self.phase = 0
        return None
    
    # into pickle
    def save_state():
        return None

    # from pickle
    def load_state():
        return None