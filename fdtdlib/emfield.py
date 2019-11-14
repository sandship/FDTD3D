import numpy as np
import cupy as cp

class Field(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, setupParam):
        self.time = 0.0
        self.param = setupParam
        self.set_parameter = self.param.set_parameter
        self.general_parameter = self.param.general_parameter

        self.Xaxis = self.init_field()
        self.Yaxis = self.init_field()
        self.Zaxis = self.init_field()

        return None

    def init_field(self):
        self.shape = (self.param.model_size["x"], self.param.model_size["y"], self.param.model_size["z"])
        return cp.zeros(shape=self.shape)

    def load_field(self):
        return None

    def calc_norm(self):
        self.norm = cp.sqrt(
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
    def __init__(self, setupParam, shift_phase=0.0):
        self.shift_phase = shift_phase
        super().__init__(setupParam)
        return None

    def _feed_efield(self):
        self.Zaxis[32, 47, 47] = cp.sin(2.0 * np.pi * 3.0e9 * self.time + self.shift_phase)
        return None

    def update_field(self, Hfield):
        self.time = Hfield.time + self.param.dt /2.0
        self._feed_efield()

        self.Xaxis = self.param.ce * self.Xaxis + self.param.de * (
                        (Hfield.Zaxis - cp.roll(Hfield.Zaxis, shift=1, axis=1)) - 
                        (Hfield.Yaxis - cp.roll(Hfield.Yaxis, shift=1, axis=2))
                    )

        self.Yaxis =  self.param.ce * self.Yaxis + self.param.de * (
                        (Hfield.Xaxis - cp.roll(Hfield.Xaxis, shift=1, axis=2)) - 
                        (Hfield.Zaxis - cp.roll(Hfield.Zaxis, shift=1, axis=0))
                    )

        self.Zaxis = self.param.ce * self.Zaxis + self.param.de * (
                        (Hfield.Yaxis - cp.roll(Hfield.Yaxis, shift=1, axis=0)) - 
                        (Hfield.Xaxis - cp.roll(Hfield.Xaxis, shift=1, axis=1))
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
    def __init__(self, setupParam, shift_phase=0.0):
        self.shift_phase = shift_phase
        super().__init__(setupParam)
        return None

    def update_field(self, Efield):
        self.time = Efield.time + self.param.dt /2.0
        Efield._feed_efield()

        self.Xaxis = self.param.ch * self.Xaxis + self.param.dh * (
                        (Efield.Zaxis - cp.roll(Efield.Zaxis, shift=-1, axis=1)) - 
                        (Efield.Yaxis - cp.roll(Efield.Yaxis, shift=-1, axis=2))
                    )

        self.Yaxis = self.param.ch * self.Yaxis + self.param.dh * (
                        (Efield.Xaxis - cp.roll(Efield.Xaxis, shift=-1, axis=2)) - 
                        (Efield.Zaxis - cp.roll(Efield.Zaxis, shift=-1, axis=0))
                    )

        self.Zaxis = self.param.ch * self.Zaxis + self.param.dh * (
                        (Efield.Yaxis - cp.roll(Efield.Yaxis, shift=-1, axis=0)) - 
                        (Efield.Xaxis - cp.roll(Efield.Xaxis, shift=-1, axis=1))
                    )
        return None