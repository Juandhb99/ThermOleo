import numpy as np

# Order of molecules: FAME, ALCOHOL, GLYCEROL, ACID, OIL, MG, DG, H2O
# Order of groups: CH, CH2, CH3, CH=CH, OH, CH2COO, COOH. H2O

GIP = np.array([
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74], 
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [2900.56,  2900.56,   2900.56,     0,     -388.62,  -964.53,  5084.03,  -987.18],
       [4925.67,  4925.67,   4925.67,   259.13,     0,      947.89, -1210.44,  -4618.51], 
       [2544.80,  2544.80,   2544.80,   1047.08, -2424.84,    0,    -685.81,    134.70], 
       [3714.86,  3714.86,   3714.86,   258.51,  -3227.03,  594.79,     0,      3239.57],
       [20930.91, 20930.91,  20930.91,  -688.85, -14448.32, 1158.19, -1429.48,     0]
       ], dtype = np.float64)


w = np.array([[0.856, 0.116, 0.028, 0, 0, 0, 0, 0]], dtype = np.float64)
T = 298.15
v = np.array([
    [0.9044,     0,    1.0, 0, 0, 0, 0, 0],
    [12.9913,    0,    2.0, 0, 0, 0, 0, 0],
    [2.0,        1.0,  0,   0, 0, 0, 0, 0],
    [1.0435,     0,    0,   0, 0, 0, 0, 0],
    [0.9044,     1.0,  3.0, 0, 0, 0, 0, 0],
    [1.0,        0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0]
], dtype = np.float64)

MW = np.array([310.6056, 32.04, 92.09, 878.0, 648.264, 370.138, 262.7856, 18], dtype = np.float64)

R = np.array([[0.4469, 0.6744, 0.9011, 1.1167, 1.0, 1.6764, 1.3013, 0.92]], dtype = np.float64)
Q = np.array([[0.228, 0.54, 0.8488, 0.867, 1.2, 1.42, 1.224, 1.4]], dtype = np.float64)

# Combinatorial contribution
r = np.sum(v*R.T, axis=0)/MW
q = np.sum(v*Q.T, axis=0)/MW
zeta = np.sum(w/MW)
phi = r*w/np.sum(r*w)
theta = q*w/np.sum(q*w)
with np.errstate(divide='ignore', invalid='ignore'):
    lngamma_c = np.nan_to_num(1 - zeta*MW*phi/w + np.log(zeta*MW*phi/w) - 5*q*MW*(1 - (phi/theta) - np.log(theta/phi)), nan=0.0) 

# Residual contribution
tao = np.exp(-GIP/T)
Wk = np.sum(v*w/(MW*zeta), axis = 1)/np.sum(v*w/(MW*zeta))
THETA = Q*Wk/np.sum(Q*Wk)
lngamma_r = Q*(1 - np.log(np.sum(THETA.T*tao, axis=0)) - np.sum(THETA*tao/np.sum(THETA.T*tao, axis=0), axis = 1))


with np.errstate(divide='ignore', invalid='ignore'):
    Wk_pure = np.nan_to_num(v/np.sum(v, axis=0), nan=0.0)
    THETA_pure = np.nan_to_num(Q.T*Wk_pure/np.sum(Q.T*Wk_pure, axis = 0), nan=0.0)
    lngamma_r_pure = np.zeros((8,8))    
    lngamma_r_pure = np.array([
        np.nan_to_num(
            Q * (1 - np.log(np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0)) - 
                np.sum(THETA_pure[:, comp] * tao / np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0), axis=1)),
            nan=0
        )
        for comp in range(THETA_pure.shape[1])
    ]).reshape(8,8)


lngamma_r_pure
