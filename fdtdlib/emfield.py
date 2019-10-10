import numpy as np
# import cupy as np

class Field(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        self.time = 0.0
        self.step = 0
        self.param = InitializedParameter

        self.set_parameter = self.param.set_parameter
        self.general_parameter = self.param.general_parameter

        self.Xaxis = self.init_field()
        self.Yaxis = self.init_field()
        self.Zaxis = self.init_field()

        return None

    def init_field(self):
        return np.zeros(
            shape=(self.param.model_size["x"], self.param.model_size["y"], self.param.model_size["z"])
        )

    def load_field(self):
        return None

    def calc_norm(self):
        self.norm = np.sqrt(
            self.Xaxis ** 2 +
            self.Yaxis ** 2 +
            self.Zaxis ** 2
        )
        return None

    def calc_phase(self):
        return None


class Efield(Field):
    """[summary]
    
    Arguments:
        Field {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        super().__init__(InitializedParameter)
        return None

    def update_field(self, Hfield):
        self.Xaxis[25, 25, 25] = np.sin(2.0 * 3.14159265 * self.param.freq * self.time)
        self.time = Hfield.time + self.param.dt /2.0
        self.step = Hfield.step + 1/2

        self.Xaxis = self.param.ce * self.Xaxis + self.param.de * (
                        (Hfield.Zaxis - np.roll(Hfield.Zaxis, shift=1, axis=1)) - 
                        (Hfield.Yaxis - np.roll(Hfield.Yaxis, shift=1, axis=2))
                    )

        self.Yaxis =  self.param.ce * self.Yaxis + self.param.de * (
                        (Hfield.Xaxis - np.roll(Hfield.Xaxis, shift=1, axis=2)) - 
                        (Hfield.Zaxis - np.roll(Hfield.Zaxis, shift=1, axis=0))
                    )

        self.Zaxis = self.param.ce * self.Zaxis + self.param.de * (
                        (Hfield.Yaxis - np.roll(Hfield.Yaxis, shift=1, axis=0)) - 
                        (Hfield.Xaxis - np.roll(Hfield.Xaxis, shift=1, axis=1))
                    )
        return None

    def calc_scatterfield(self):
        return None

    def calc_totalfield(self):
        return None

class Hfield(Field):
    """[summary]
    
    Arguments:
        Field {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        super().__init__(InitializedParameter)
        return None

    def update_field(self, Efield):
        Efield.Xaxis[22, 46, 46] = np.sin(2.0 * 3.14159265 * 3.0e9 * self.time)
        self.time = Efield.time + self.param.dt /2.0

        self.Xaxis += self.param.dh * (
                        (Efield.Zaxis - np.roll(Efield.Zaxis, shift=-1, axis=1)) - 
                        (Efield.Yaxis - np.roll(Efield.Yaxis, shift=-1, axis=2))
                    )

        self.Yaxis += self.param.dh * (
                        (Efield.Xaxis - np.roll(Efield.Xaxis, shift=-1, axis=2)) - 
                        (Efield.Zaxis - np.roll(Efield.Zaxis, shift=-1, axis=0))
                    )

        self.Zaxis += self.param.dh * (
                        (Efield.Yaxis - np.roll(Efield.Yaxis, shift=-1, axis=0)) - 
                        (Efield.Xaxis - np.roll(Efield.Xaxis, shift=-1, axis=1))
                    )
        return None