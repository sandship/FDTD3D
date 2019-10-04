import time

from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.EMfield(param)
    hfield = emfield.EMfield(param)

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