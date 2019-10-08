import numpy as np

class Field(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, InitializedParameter):
        self.param = InitializedParameter

        self.set_parameter = self.param.set_parameter
        self.general_parameter = self.param.general_parameter

        self.Xaxis = self.init_field()
        self.Yaxis = self.init_field()
        self.Zaxis = self.init_field()

        return None

    def init_field(self):
        return np.zeros(shape=(self.param.model_size["x"] + 1, self.param.model_size["y"] + 1, self.param.model_size["z"] + 1))

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
        self.phase = 0
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
        self.Xaxis = self.Xaxis + \
                    self.param.ce * (
                        (Hfield.Zaxis - np.roll(Hfield.Zaxis, (0, 1, 0))) - 
                        (Hfield.Yaxis - np.roll(Hfield.Yaxis, (0, 0, 1)))
                    )

        self.Yaxis = self.Yaxis + \
                    self.param.ce * (
                        (Hfield.Xaxis - np.roll(Hfield.Xaxis, (0, 0, 1))) - 
                        (Hfield.Zaxis - np.roll(Hfield.Zaxis, (1, 0, 0)))
                    )

        self.Zaxis = self.Zaxis + \
                    self.param.ce * (
                        (Hfield.Yaxis - np.roll(Hfield.Yaxis, (1, 0, 0))) - 
                        (Hfield.Xaxis - np.roll(Hfield.Xaxis, (0, 1, 0)))
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
        self.Xaxis = self.Xaxis + \
                    self.param.ch * (
                        (Efield.Zaxis - np.roll(Efield.Zaxis, (0, -1, 0))) - 
                        (Efield.Yaxis - np.roll(Efield.Yaxis, (0, 0, -1)))
                    )

        self.Yaxis = self.Yaxis + \
                    self.param.ch * (
                        (Efield.Xaxis - np.roll(Efield.Xaxis, (0, 0, -1))) - 
                        (Efield.Zaxis - np.roll(Efield.Zaxis, (-1, 0, 0)))
                    )

        self.Zaxis = self.Zaxis + \
                    self.param.ch * (
                        (Efield.Yaxis - np.roll(Efield.Yaxis, (-1, 0, 0))) - 
                        (Efield.Xaxis - np.roll(Efield.Xaxis, (0, -1, 0)))
                    )

        return None