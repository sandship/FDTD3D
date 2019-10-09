from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import boundary

from memory_profiler import profile

@profile
def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()
    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    # do computation
    for _ in range(4000):
        efield.update_field(hfield)
        hfield.update_field(efield)

    # result
    efield.calc_norm()

    for _ in efield.norm[:, 25, 25]:
        print(_)

    efield.calc_phase()
    return None


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)