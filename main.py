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
    for _ in tqdm(range(502)):
        efield.update_field(hfield)
        hfield.update_field(efield)
        
<<<<<<< HEAD
    # result
    efield.calc_norm()
    efield.calc_phase()

=======
        if _ % 10 == 1:
            # result
            efield.calc_norm()
            efield.calc_phase()

            import matplotlib.pyplot as plt
            import seaborn as sns
            sns.heatmap(efield.norm[46, :, :], cmap="Reds")
            plt.savefig('test_{}.png'.format(_))
            plt.close('all')
>>>>>>> 3c663933c8922088371ad5317372c90716b0d5cd

    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)