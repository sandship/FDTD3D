from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary
from fdtdlib import visualizer

from tqdm import tqdm

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    # do computation
    for _ in tqdm(range(5002)):
        efield.update_field(hfield)
        hfield.update_field(efield)
        
        with open('./output/dot_tl.log', "a+") as f:
            if _ % 100 == 1:
                # result
                efield.calc_norm()
                efield.calc_phase()

                import matplotlib.pyplot as plt
                import seaborn as sns
                sns.heatmap(efield.norm[50, :, :], cmap="Reds", vmin=0, vmax=0.005)
                plt.savefig('./output/suface_{}.png'.format(_))
                plt.close('all')

                plt.plot(efield.norm[46, 46, :])
                plt.savefig('./output/line_{}.png'.format(_))
                plt.close('all')

            f.write("{},{},{}\n".format(str(efield.Xaxis[50, 50, 50]), str(efield.Yaxis[50, 50, 50]), str(efield.Zaxis[50, 50, 50])))

    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)