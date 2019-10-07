import numpy as np

X = np.arange(0.0, 1.0, 0.002)
Y = np.arange(0.0, 1.0, 0.002)
Z = np.arange(0.0, 1.0, 0.002)

xxx, yyy, zzz = np.meshgrid(X, Y, Z)
