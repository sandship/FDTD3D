import time
import pickle

from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.EMfield(param)
    hfield = emfield.EMfield(param)

    with open("param_pickle.pkl", "wb") as fb:
        pickle.dump(param, fb)
    with open("ef_pickle.pkl", "wb") as fb:
        pickle.dump(efield, fb)
    with open("hf_pickle.pkl", "wb") as fb:
        pickle.dump(hfield, fb)

    # do computation
    efield.update_field()
    hfield.update_field()

    # result
    efield.calc_norm()
    efield.calc_phase()

    print(efield.norm)

    return None


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)