from fdtdlib import myutility as myutil
import numpy as np

class InitialzeSpaceParameter(object):
    """This class is nitializer for parameters used in FDTD.
    Instantiate this, and we can set the calculation spaces 
    for FDTD along with your CONFIG (`./configure/setting.json`) and MODELs.

    Returns:
        [type] -- [description]
    """
    def __init__(self, config_path=r"./configure/settings.json"):
        self.setting = myutil.load_config(config_path)
        self.set_parameter = myutil.load_config(config_path)["parameter"]["set"]
        self.general_parameter = myutil.load_config(config_path)["parameter"]["general"]

        self.freq = self.set_parameter["freq"]

        self.dr = self.set_parameter["descrete"]
        self.c = self.general_parameter["c"]
        self.dt = 0.99 * self.dr / (self.c * np.sqrt(3.0))

        self.model_id = self.load_model(self.setting["model"]["path"])

        self.model_size = {
            "x" : self.model_id.shape[0],
            "y" : self.model_id.shape[1],
            "z" : self.model_id.shape[2]
        }

        self.calc_parameter(self.model_id)

        return None

    def load_model(self, path_):
        """This method LOADs the calculation model, 
        which includes PERMITIBITY and METAL.
        
        Arguments:
            path_ {str} -- full/relative path of model.
        
        Returns:
            np.ndarray -- numpy 3d-array, each elements indicates the tissue ID.
            Note: the tissue ID is bound with properties in `./asset/properties/*`, and the file path described in `setting.json`.
        """
        with open(path_, "r") as fh:
            lines = fh.readlines()
        lines = [[int(element) for element in line.split()] for line in lines]

        arr = self.transform_tidy_3darray(np.array(lines), to_form="3d-array")
        arr = self.expand_field(arr, expand=self.__expansion_num())

        return arr

    def transform_tidy_3darray(self, raw_data, to_form="3d-array"):
        """this method TRANSFORM matually tidy np.array (shape is (n, 4)) and 3-d ndarray (shape is (nx, ny, nz)).
        
        Arguments:
            raw_data {np.array} -- Target np.array for transformation.
        
        Keyword Arguments:
            to_form {str} -- The flag of transformation.
            If you input "3d-array", this method transform tidy array to 3-d ndarray (default: {"3d-array"}).
        
        Raises:
            AttributeError: This error indicate you do not input "3d-array" nor "tidy" into "to_form" argument.
        
        Returns:
            np.array -- Transformed array.
        """
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
            tidy = np.zeros((darray_size[0]*darray_size[1]*darray_size[2], 4))
            
            cnt = 0
            for i in range(darray_size[0]):
                for j in range(darray_size[1]):
                    for k in range(darray_size[2]):
                        tidy[cnt, 0] = i
                        tidy[cnt, 1] = j
                        tidy[cnt, 2] = k
                        tidy[cnt, 3] = darray[i, j, k]
                        cnt += 1
            return tidy
        else:
            print("You must input valid value ('3d-array' or 'tidy') into the argument 'to_form'.")
            raise AttributeError

    def expand_field(self, arr, expand={}):
        """This method EXPANDs isometrically the 3d-array=(N, N, N) into 3d-array=(N+2*expand["x"], N+2*expand["y"], N+2*expand["z"]).
        The center point of expanded array is shifted from (N/2, N/2, N/2) => (N/2 + expand["x"], N/2 + expand["y"], N/2 + expand["z"])

        Arguments:
            arr {np.ndarray} -- numpy 3d-array
        
        Keyword Arguments:
            expand {dict} -- the expand Num for each axis "x", "y", "z" (default: empty)
        
        Returns:
            np.ndarray -- expanded ndarray
        """
        rarr = np.zeros((
            arr.shape[0] + 2 * expand["x"], 
            arr.shape[1] + 2 * expand["y"], 
            arr.shape[2] + 2 * expand["z"]
        ))
        
        rarr[
            expand["x"] : -expand["x"], 
            expand["y"] : -expand["y"], 
            expand["z"] : -expand["z"]
        ] = arr
        
        return rarr

    def __expansion_num(self):
        """this internal method CALC the total expansion num, from num of PML layers and space mergin.
        
        Returns:
            dict -- expansion number for each axis.
        """
        total_mergin = {}
        for k in self.set_parameter["mergin"].keys():
            total_mergin[k] = self.set_parameter["mergin"][k] + self.set_parameter["pml_thick"]

        return total_mergin
    
    def calc_parameter(self, model_id_array):
        """this method CALC the parameter for FDTD update coefficient
        from the tissue's electromagnetic parameter.

        Arguments:
            model_id_array {np.array (shape=(nx, ny, nz))} -- numpy 3d-array. each element indicates the tissue_id.

        Returns:
            some np.array, ce, de, dh.
        """
        self.set_tissue_param(model_id_array)
        
        self.set_pml()

        self.ce = (2.0 * self.eps - self.sigma * self.dt)/(2.0 * self.eps + self.sigma * self.dt)
        self.de = 2.0 * self.dt /((2.0 * self.eps * self.dr) + (self.sigma * self.dt * self.dr))
        self.dh = self.dt /(self.dr * self.mu)

        return None

    def load_tissue_index(self, path_):
        """Load electromagnetic parameter JSON.
        
        Arguments:
            path_ {str} -- full/relative JSON file path of electromagnetic parameter of models (metal and permitivity).
        
        Returns:
            dict -- [description]
        """
        self.tissues = myutil.load_config(path_)

        return self.tissues

    def set_tissue_param(self, model_id_array):
        """This method translate tissue id into actual electromagnetic parameter.
        
        Arguments:
            model_id_array {np.array (shape=(nx, ny, nz))} -- numpy 3d-array. each element indicates the tissue_id.
        
        Returns:
            3d-array, indicates electromagnetic parameters.
        """
        def _trans_tissue_id_to_value(arr, key):
            """this method derive electromagnetic parameter from dict (self.tissue)
            
            Arguments:
                arr {ndarray} -- model-ID array (numpy 3d-array)
                key {string} -- the kind of parameter ('name', 'epsr', 'mur', 'sigma', 'rho')
            
            Returns:
                np.array -- 3d-array indicates electromagnetic parameter of the each point.
            """
            def _trans_tissue_param(x, key=""):
                """this method seach the electromagnetic parameter by using x and key.
                
                Arguments:
                    x {float or int} -- model-ID
                    key {string} -- the kind of parameter ('name', 'epsr', 'mur', 'sigma', 'rho')
                """
                return self.tissues[str(int(x))][key]

            __func = np.vectorize(_trans_tissue_param)
            return __func(arr.ravel(), key=key).reshape(arr.shape[0], arr.shape[1], arr.shape[2])
        
        self.load_tissue_index(self.setting["model"]["property"])
        
        self.name =  _trans_tissue_id_to_value(model_id_array, key="name")
        self.eps =   _trans_tissue_id_to_value(model_id_array, key="epsr")
        self.mu =    _trans_tissue_id_to_value(model_id_array, key="mur")
        self.sigma = _trans_tissue_id_to_value(model_id_array, key="sigma")
        self.rho =   _trans_tissue_id_to_value(model_id_array, key="rho")

        self.mu *= self.general_parameter["mu0"]
        self.eps *= self.general_parameter["eps0"]

        return None

    def set_pml(self):
        """This method sets conductivity, represents Berenger PML boundary.
        """
        pmlN = self.set_parameter["pml_thick"]
        __M = self.set_parameter["pml_dimension"]
        __R = self.set_parameter["pml_reflection_coefficient"]

        for ln in range(pmlN):
            # TODO: 
            # 右辺内の定数を変数で置き換える。

            self.sigma[ln : ln + 1, :, :] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))
            self.sigma[:, ln : ln + 1, :] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))
            self.sigma[:, :, ln : ln + 1] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))
            
            self.sigma[-(ln + 1) : -ln, :, :] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))
            self.sigma[:, -(ln + 1) : -ln, :] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))
            self.sigma[:, :, -(ln + 1) : -ln] = ((pmlN - ln)/pmlN) ** __M * ((__M + 1) * 6/(2 * pmlN * self.dr * 377))

        return None
