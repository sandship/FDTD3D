from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import visualizer

import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    efield_sub = emfield.Efield(param, shift_phase=3.14159265/2.0)
    hfield_sub = emfield.Hfield(param)

    with open(r'./output/tl.dat', "a+") as f:
        for _ in tqdm(range(5002)):
            efield.update_field(hfield)
            hfield.update_field(efield)
            
            efield_sub.update_field(hfield_sub)
            hfield_sub.update_field(efield_sub)
            
            # for debug
            f.write("{},{},{},{},{},{},{}\n".format(_,
                efield.Xaxis[50, 50, 50], efield_sub.Xaxis[50, 50, 50],
                efield.Yaxis[50, 50, 50], efield_sub.Yaxis[50, 50, 50],
                efield.Zaxis[50, 50, 50], efield_sub.Zaxis[50, 50, 50],
                )
            )

            if _ % 10 == 0:
                efield.calc_norm()
                efield_sub.calc_norm()


    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)