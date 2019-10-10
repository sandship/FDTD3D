from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import visualizer

from tqdm import tqdm

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)


    import matplotlib.pyplot as plt
    import seaborn as sns
    # do computation
    for _ in tqdm(range(5002)):
        efield.update_field(hfield)
        hfield.update_field(efield)

        if _ % 10 == 0:
            efield.calc_norm()
            plt.figure()
            sns.heatmap(efield.norm[:, 50, :], cmap="Reds")
            plt.savefig('./output/map_{}.png'.format(_))
            plt.close('all')

    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)