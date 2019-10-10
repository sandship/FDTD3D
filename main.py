from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import visualizer

from tqdm import tqdm

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    efield_sub = emfield.Efield(param, shift_phase=3.14159265/2.0)
    hfield_sub = emfield.Hfield(param)

    import matplotlib.pyplot as plt
    import seaborn as sns
    with open('./output/time_line.dat', "a+") as f:
        # do computation
        for _ in tqdm(range(5002)):
            efield.update_field(hfield)
            hfield.update_field(efield)
            
            efield_sub.update_field(hfield_sub)
            hfield_sub.update_field(efield_sub)
            
            if _ % 10 == 0:
                efield.calc_norm()
                efield_sub.calc_norm()

                plt.figure()
                sns.heatmap(efield.norm[:, 50, :], cmap="Reds")
                plt.savefig('./output/map_{}.png'.format(_))
                plt.close('all')
            
            f.write('{},{},{}\n'.format(_, efield.Xaxis[46, 46, 46], efield_sub.Xaxis[46, 46, 46]))



    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)