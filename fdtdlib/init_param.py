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

        self.model_id = self.load_model(self.setting["model"]["path"])

        self.model_size = {
            "x" : self.model_id.shape[0],
            "y" : self.model_id.shape[1],
            "z" : self.model_id.shape[2]
        }

        self.calc_parameter()
        self.set_pml()

        return None

    def load_model(self, path_):
        with open(path_, "r") as fh:
            lines = fh.readlines()
        lines = [[int(element) for element in line.split()] for line in lines]
        arr = self.transform_tidy_3darray(np.array(lines), to_form="3d-array")
        
        return self.expand_field(arr, expand=self.__calc_mergin())

    def expand_field(self, arr, expand={}):
        return arr

    def __calc_mergin(self):
        total_mergin = {}
        for k in self.set_parameter["mergin"].keys():
            total_mergin[k] = self.set_parameter["mergin"][k] + self.set_parameter["pml_thick"][k]
        return total_mergin
    
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
    
    def set_pml(self):
        return None

    def load_tissue_index(self, path_):
        self.tissues = myutil.load_config(path_)
        return None

    def set_tissue_param(self):
        """
        """
        def _trans_tissue_param(x, key=""):
            return self.tissues[str(int(x))][key]

        def _trans_tissue_id_to_value(arr, key):
            __func = np.vectorize(_trans_tissue_param)
            return __func(arr.ravel(), key=key).reshape(arr.shape[0], arr.shape[1], arr.shape[2])
        
        self.load_tissue_index(self.setting["model"]["property"])
        
        self.name =  _trans_tissue_id_to_value(self.model_id, key="name")
        self.eps =   _trans_tissue_id_to_value(self.model_id, key="epsr")
        self.mu =    _trans_tissue_id_to_value(self.model_id, key="mur")
        self.sigma = _trans_tissue_id_to_value(self.model_id, key="sigma")
        self.rho =   _trans_tissue_id_to_value(self.model_id, key="rho")

        self.mu *= self.general_parameter["mu0"]
        self.eps *= self.general_parameter["eps0"]

        return None
    

    def transform_tidy_3darray(self, raw_data, to_form="3d-array"):
        if to_form == "3d-array":
            tidy = raw_data.copy()
            tidy_size = {
                "x" : np.max(tidy[:, 0]) - np.min(tidy[:, 0]) + 1,
                "y" : np.max(tidy[:, 1]) - np.min(tidy[:, 1]) + 1,
                "z" : np.max(tidy[:, 2]) - np.min(tidy[:, 2]) + 1
            }

            darray = np.zeros(shape=(tidy_size["x"], tidy_size["y"], tidy_size["z"]))
            for item in tidy:
                darray[item[0], item[1], item[2]] = item[3]

            return darray
        elif to_form == "tidy":
            darray = raw_data.copy()
            darray_size = darray.shape

            ###

        else:
            raise ArgumentError