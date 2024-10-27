import numpy as np
from Unifac import Unifac
from UnifacDortmund import UnifacDortmund
from PhaseCalculation import CalculateComps as cc

def main(GIP_dortmund, v, MW, T, w):
    phase_distribution = UnifacDortmund(GIP_dortmund, v, MW, T)
    return np.apply_along_axis(phase_distribution.calculate_gamma, 1, w) # Apply the function per row of the matrix

def predict_test():
    
    data = np.array([[0.40, 0.40, 0.2, 0, 0, 0, 0, 0], 
                     [0.385, 0.385, 0.230, 0, 0, 0, 0, 0]])
    
    v = np.array([[0.904, 1, 0, 3.713, 2.808, 1.904, 0.904, 0],
                  [12.991, 2, 0, 40.974, 27.982, 14.991, 12.991, 0],
                  [2, 0, 1, 3, 2, 1, 1, 0],
                  [1.044, 0, 0, 3.131, 2.087, 1.044, 1.044, 0],
                  [0.904, 3, 1, 2.713, 1.808, 0.904, 0.904, 0],
                  [1, 0, 0, 3, 2, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1],
                  ])
    
    data_MW = np.array([[324.140, 92.090, 32.040, 968.420, 659.280, 350.140, 296.140, 18]])
    temp = 298.15
    
    thermo_model = UnifacDortmund

    A = np.array([-3214.25, -1718.09, -3079.37, 1295.55, 1249.74, 2900.56, 2900.56, 2900.56, -388.62, 259.13, 4925.67, 4925.67, 4925.67, 1047.08, -2424.84, 
                  2544.80, 2544.80, 2544.80, 258.51, -3227.03, 3714.86, 3714.86, 3714.86, -987.18, -688.85, 20930.91, 5084.03, -1210.44, -4618.51, -14448.32])
    

    
    params = np.loadtxt(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\Evaluation\results\UDortmundParamsV5.out")
    B = params[0:30]
    C = params[30:60]
    
    params
    
    GIP = cc.define_GIP(A, B, C)

    results = cc.calculate_comps(data, v, data_MW, temp, thermo_model, GIP)
    
    return results
    


if __name__ == "__main__":
    
    print(predict_test())