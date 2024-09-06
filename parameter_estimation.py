import polars as pl
import numpy as np
from scipy.optimize import minimize, newton
from UnifacDortmund import UnifacDortmund


tie_lines = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\refined_lle_data.xlsx", engine="calamine")
coeffs = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\profile_coeffs.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
    
    pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
)


tie_lines = tie_lines.drop(["Type Alcohol"])
coeffs = coeffs.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
group_tie_lines = tie_lines.group_by(["Ref", "Sub Ref", "Temperature (K)"])

result = comps_MW.filter(
    (pl.col("Ref") == 19) & (pl.col("Sub Ref") == "a")
)

result
i = 0
for name, data in group_tie_lines:
    i += 1
    print(name)
    print(i)
    
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

test_tie_lines = tie_lines.filter(
    (pl.col("Ref") == 19) & (pl.col("Sub Ref") == "a") & (pl.col("Temperature (K)") == 293.15)
)

test_tie_lines

test_tie_lines_np = test_tie_lines.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()

test_coeffs = coeffs.filter(
    (pl.col("Ref") == 19) & (pl.col("Sub Ref") == "a")
).drop(["Ref", "Sub Ref"]).to_numpy()

test_comps_MW = comps_MW.filter(
    (pl.col("Ref") == 19) & (pl.col("Sub Ref") == "a")
).drop(["Ref", "Sub Ref"]).to_numpy()

test_tie_lines_np

v = np.array([
    [test_coeffs[0][2],     1.0,  0,                   3*test_coeffs[0][2] + 1, 2*test_coeffs[0][2] + 1, test_coeffs[0][2] + 1, test_coeffs[0][2],  0],
    [test_coeffs[0][0],     2.0,  test_coeffs[0][3],   3*test_coeffs[0][0] + 2, 2*test_coeffs[0][0] + 2, test_coeffs[0][0] + 2, test_coeffs[0][0] , 0],
    [2.0,                   0,    1.0,                 3.0,                     2.0,                     1.0,                   1.0,                0],
    [test_coeffs[0][1],     0,    0,                   3*test_coeffs[0][1],     2*test_coeffs[0][1],     test_coeffs[0][1],     test_coeffs[0][1],  0],
    [test_coeffs[0][2],     3.0,  1.0,                 3*test_coeffs[0][2],     2*test_coeffs[0][2],     test_coeffs[0][2],     test_coeffs[0][2],  0],
    [1.0,                   0,    0,                   3.0,                     2.0,                     1.0,                   0,                  0],
    [0,                     0,    0,                   0,                       0,                       0,                     1.0,                0],
    [0,                     0,    0,                   0,                       0,                       0,                     0,                  1.0]])



test_comps_MW.reshape(8)
test_tie_lines_np[:, 8:16]
GIP_dortmund[:, :, 0]

phase_distribution = UnifacDortmund(GIP_dortmund, v, test_comps_MW.reshape(8), 293.15)
gamma_light = np.zeros((5, 8))
gamma_heavy = np.zeros((5, 8))
mask_light = test_tie_lines_np[:, 8:16] == 0
mask_heavy = test_tie_lines_np[:, 16:24] == 0
gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, test_tie_lines_np[:, 8:16]) 
gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, test_tie_lines_np[:, 16:24]) 
gamma_light[mask_light] = 1
gamma_heavy[mask_heavy] = 1
Ki = gamma_light/gamma_heavy
rachford_rice = np.sum(test_tie_lines_np[:, 0:8]*(Ki-1)/(1+(Ki-1)*test_tie_lines_np[:, -1].reshape(5, 1)), 1)
rachford_rice

def rachford_rice(x, Z, K): 
    return np.sum(Z*(K-1)/(1+(K-1)*x))

sol = newton(rachford_rice, x0=test_tie_lines_np[:, -1].reshape(5, 1), args = (test_tie_lines_np[:, 0:8], Ki))
sol

calculated_w_light = test_tie_lines_np[:, 0:8]/(1+(Ki-1)*sol)
calculated_w_heavy = Ki*calculated_w_light

calculated_w_light
calculated_w_heavy



