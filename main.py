from fdtdlib import emfield
from fdtdlib import initialize
from fdtdlib import visualizer

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

def main():
    # load model and initialize field
    param = initialize.parameterSetup(r'./configure/settings.json')

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    efield_sub = emfield.Efield(param, shift_phase=np.pi/2.0)
    hfield_sub = emfield.Hfield(param)

    print(f'{efield.shape}')
    for _ in tqdm(range(5002)):
        efield.update_field(hfield)
        hfield.update_field(efield)
        
        # efield_sub.update_field(hfield_sub)
        # hfield_sub.update_field(efield_sub)
        
        if _ % 10 == 0:
            efield.calc_norm()
        #     efield_sub.calc_norm()


    return None


if __name__ == "__main__":
    main()