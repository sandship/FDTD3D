from fdtdlib import emfield
from fdtdlib import init_param
from fdtdlib import visualizer

import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

# TODO:
# 以下任意の順番で潰していく.
# 01) 各成分の電磁界に異なる更新係数を適用することで, 細線近似および誘電体・金属端面を計算可とする.
# 02) 励振波源を置いて直接解FDTDを解く場合と, 電磁界を読み込んで散乱解FDTDを解く場合の二種類を選択可とする.
# 03) 10gSAR等のExposure KPIを計算可とする.（1gSAR, 10gSAR, wbSAR, E99.9)
# 04) 各関数内でCuPyでの置き換え, GPU計算適用による高速化.
# 05) STL形式等の3D-modelを読み込みBoxel化する関数を追加し, 任意モデルでのFDTD計算適用可とする.
# 06) MoMを実装し, MoM-FDTD法による連成解析を可とする.
# 07) Antennaの指向性利得, 反射係数, f特等, アンテナ性能評価を可とする.
# 08) Ray-Tracing法を実装し, FDTD法によるAntenna性能評価と連成解析可とする.
# 09) 周期境界条件等の実装によりメタマテリアルの計算を可とする.
# 10) 異方性媒質の計算を可とする.
# 11) 機械学習による目的形状等の自動＋効率的な探索を可とする.

def main():
    # load model and initialize field
    param = init_param.InitialzeSpaceParameter()

    efield = emfield.Efield(param)
    hfield = emfield.Hfield(param)

    efield_sub = emfield.Efield(param, shift_phase=3.14159265/2.0)
    hfield_sub = emfield.Hfield(param)

    with open(r'./output/tl.dat', "a+") as f:
        # do computation
        for _ in tqdm(range(5002)):
            efield.update_field(hfield)
            hfield.update_field(efield)
            
            efield_sub.update_field(hfield_sub)
            hfield_sub.update_field(efield_sub)
            
            f.write("{},{},{},{},{},{},{}\n".format(_,
                efield.Xaxis[50, 50, 50], efield_sub.Xaxis[50, 50, 50],
                efield.Yaxis[50, 50, 50], efield_sub.Yaxis[50, 50, 50],
                efield.Zaxis[50, 50, 50], efield_sub.Zaxis[50, 50, 50],
                )
            )

            if _ % 10 == 0:
                efield.calc_norm()
                efield_sub.calc_norm()

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