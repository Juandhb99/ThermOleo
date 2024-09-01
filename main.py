import numpy as np
from Unifac import Unifac
from UnifacDortmund import UnifacDortmund


def main(GIP_dortmund, v, MW, T, w):
    phase_distribution = UnifacDortmund(GIP_dortmund, v, MW, T)
    return np.apply_along_axis(phase_distribution.calculate_gamma, 1, w) # Apply the function per row of the matrix


if __name__ == "__main__":
    
    GIP_unifac = np.array([
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74], 
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [2900.56,  2900.56,   2900.56,     0,     -388.62,  -964.53,  5084.03,  -987.18],
       [4925.67,  4925.67,   4925.67,   259.13,     0,      947.89, -1210.44,  -4618.51], 
       [2544.80,  2544.80,   2544.80,   1047.08, -2424.84,    0,    -685.81,    134.70], 
       [3714.86,  3714.86,   3714.86,   258.51,  -3227.03,  594.79,     0,      3239.57],
       [20930.91, 20930.91,  20930.91,  -688.85, -14448.32, 1158.19, -1429.48,     0]
       ], dtype = np.float64)

    GIP_dortmund = np.zeros((8, 8, 3), dtype = np.float64)
    GIP_dortmund[:, :, 0] = GIP_unifac
    
    T = 298.15
    v = np.array([
    [0.9044,     1.0,  0,   0, 0, 0, 0, 0],
    [12.9913,    2.0,  0,   0, 0, 0, 0, 0],
    [2.0,        0,    1.0, 0, 0, 0, 0, 0],
    [1.0435,     0,    0,   0, 0, 0, 0, 0],
    [0.9044,     3.0,  1.0, 0, 0, 0, 0, 0],
    [1.0,        0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0]], dtype = np.float64)

    MW = np.array([324.139909, 92.09, 32.04, 878.0, 648.264, 370.138, 262.7856, 18], dtype = np.float64)
    w = np.array([[0.856, 0.028, 0.116, 0, 0, 0, 0, 0],
              [0.002265, 0.675, 0.323, 0, 0, 0, 0, 0]], dtype = np.float64) 
    
    print(main(GIP_dortmund, v, MW, T, w))