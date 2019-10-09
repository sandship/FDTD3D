from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()
    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    # do computation
    for _ in range(200):
        efield.update_field(hfield)
        hfield.update_field(efield)

    # result
    efield.calc_norm()
    efield.calc_phase()
    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)