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

        self._load_model(self.setting["model"]["path"])

        self.calc_parameter()

        return None

    def _load_model(self, path_):
        with open(path_, "r") as fh:
            lines = fh.readlines()
        
        lines = [[int(element) for element in line.split()] for line in lines]
        self.model = np.array(lines)

        self.model_size = {
            "x" : np.max(self.model[:, 0]) + 1,
            "y" : np.max(self.model[:, 1]) + 1,
            "z" : np.max(self.model[:, 2]) + 1
        }
        
        self.model = myutil.transform_tidy_3darray(self.model, to_form="3d-array")

        return None

    def calc_parameter(self):
        self.set_tissue_param()

        self.dr = self.set_parameter["descrete"]
        self.c = self.general_parameter["c"]
        self.dt = 0.99 * self.dr / (self.c * np.sqrt(3.0))
        
        self.ce = (2.0 * self.eps - self.sigma * self.dt)/(2.0 * self.eps + self.sigma * self.dt)
        self.de = 2.0 * self.dt /((2.0 * self.eps * self.dr) + (self.sigma * self.dt * self.dr))
        self.dh = self.dt /(self.dr * self.mu)

        self.freq = self.set_parameter["freq"]

        return None
    
    def set_tissue_param(self):
        self._load_tissue_index(self.setting["model"]["property"])
        
        self.name =  self._set_field_update_parameter(self.model.copy(), key="name")
        self.eps =   self._set_field_update_parameter(self.model.copy(), key="epsr")
        self.mu =    self._set_field_update_parameter(self.model.copy(), key="mur")
        self.sigma = self._set_field_update_parameter(self.model.copy(), key="sigma")
        self.rho =   self._set_field_update_parameter(self.model.copy(), key="rho")

        self.mu *= self.general_parameter["mu0"]
        self.eps *= self.general_parameter["eps0"]

        return None
    
    def _load_tissue_index(self, path_):
        self.tissues = myutil.load_config(path_)
        return None

    def _translate_tissue_param(self, x, key=""):
        return self.tissues[str(int(x))][key]

    def _set_field_update_parameter(self, arr, key):
        __func = np.vectorize(self._translate_tissue_param)
        return __func(arr.ravel(), key=key).reshape(arr.shape[0], arr.shape[1], arr.shape[2])