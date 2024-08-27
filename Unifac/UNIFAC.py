import numpy as np
from dataclasses import dataclass, field

# Order of molecules: FAME, GLYCEROL, ALCOHOL, OIL, DAG, MAG, ACID, H2O
# Order of groups: CH, CH2, CH3, CH=CH, OH, CH2COO, COOH, H2O
@dataclass
class Unifac:
    """
        UNIFAC thermodynamical model coded to predict activity coefficients for oleochemical mixtures.
        
        Attributes:
            GIP (np.ndarray): Matrix of group interaction parameters, this must be a 8x8 matrix where each column and row represents a
            functional group. The order must be CH, CH2, CH3, CH=CH, OH, CH2COO, COOH, H2O for both the columns and rows.
            v (np.ndarray): Matrix of the number of times each group appears in each molecule of the mixture. This is a 8x8 matrix 
            where each column represents a molecule and each row a functional group. The order of the columns must be FAME/FAEE, GLYCEROL, ALCOHOL, OIL, DAG, MAG, ACID, H2O,
            the order of the rows must be CH, CH2, CH3, CH=CH, OH, CH2COO, COOH, H2O.
            MW (np.ndarray): Vector of molecular weights of the molecules in the system. This is a 1x8 vector that must have the following order
            FAME/FAEE, GLYCEROL, ALCOHOL, OIL, DAG, MAG, ACID, H2O.
            T (float): Temperature of the system in K.
            _R (np.ndarray): Group volume.
            _Q (np.ndarray): Group surface area.
            _zeta (float): Pseudo weighted average molar composition of the mixture.
    """
    GIP: np.ndarray 
    v: np.ndarray
    MW: np.ndarray
    T: float
    _R: np.ndarray = field(default=None)
    _Q: np.ndarray = field(default=None)
    _zeta: float = field(default=None)
    
    def _group_properties(self) -> None:
        """Instantiate the volume and surface area for each of the considered groups. These parameters are obtained from: 
            Magnussen, T., Rasmussen, P., & Fredenslund, A. (1981). UNIFAC parameter table for prediction of liquid-liquid equilibriums. Industrial & Engineering Chemistry Process Design and Development, 20(2), 331–339. https://doi.org/10.1021/i200013a024
        """        
        
        self._R = np.array([[0.4469, 0.6744, 0.9011, 1.1167, 1.0, 1.6764, 1.3013, 0.92]], dtype = np.float64)
        self._Q = np.array([[0.228, 0.54, 0.8488, 0.867, 1.2, 1.42, 1.224, 1.4]], dtype = np.float64)
        
    
    def _combinatorial_contribution(self, w: np.ndarray) -> np.ndarray:
            
        with np.errstate(divide='ignore', invalid='ignore'):
            r = np.sum(v*self._R.T, axis=0)/MW
            q = np.sum(v*self._Q.T, axis=0)/MW
            self._zeta = np.sum(w/MW)
            phi = r*w/np.sum(r*w)
            theta = q*w/np.sum(q*w)
            lngamma_c = np.nan_to_num(1 - self._zeta*MW*phi/w + np.log(self._zeta*MW*phi/w) - 5*q*MW*(1 - (phi/theta) - np.log(theta/phi)), nan=0.0) 
            return lngamma_c
    
    def _residual_contribution(self, w: np.ndarray) -> np.ndarray:
        
        with np.errstate(divide='ignore', invalid='ignore'):
            tao = np.exp(-GIP/T)
            Wk = np.sum(v*w/(MW*self._zeta), axis = 1)/np.sum(v*w/(MW*self._zeta))
            THETA = self._Q*Wk/np.sum(self._Q*Wk)
            lngamma_r_mix = self._Q*(1 - np.log(np.sum(THETA.T*tao, axis=0)) - np.sum(THETA*tao/np.sum(THETA.T*tao, axis=0), axis = 1))

            Wk_pure = np.nan_to_num(v/np.sum(v, axis=0), nan=0.0)
            THETA_pure = np.nan_to_num(self._Q.T*Wk_pure/np.sum(self._Q.T*Wk_pure, axis = 0), nan=0.0)
            lngamma_r_pure = np.zeros((8,8))    
            lngamma_r_pure = np.array([
                np.nan_to_num(self._Q * (1 - np.log(np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0)) - np.sum(THETA_pure[:, comp] * tao / np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0), axis=1)), nan=0) for comp in range(THETA_pure.shape[1])
            ]).reshape(8,8)
        
        lngamma_r = np.sum(np.array([v[:,comp]*(lngamma_r_mix - lngamma_r_pure[comp]) for comp in range(8)]).reshape(8,8), axis = 1)
        return lngamma_r
    
    def calculate_gamma(self, w: np.ndarray) -> np.ndarray:
        
        self.group_properties()
        lngamma_c = self.combinatorial_contribution(w)
        lngamma_r = self.residual_contribution(w) 
        gamma = np.exp(lngamma_c + lngamma_r)
        
        return gamma
    
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


w = np.array([[0.856, 0.028, 0.116, 0, 0, 0, 0, 0]], dtype = np.float64)
T = 298.15
v = np.array([
    [0.9044,     1.0,  0,   0, 0, 0, 0, 0],
    [12.9913,    2.0,  0,   0, 0, 0, 0, 0],
    [2.0,        0,    1.0, 0, 0, 0, 0, 0],
    [1.0435,     0,    0,   0, 0, 0, 0, 0],
    [0.9044,     3.0,  1.0, 0, 0, 0, 0, 0],
    [1.0,        0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0],
    [0,          0,    0,   0, 0, 0, 0, 0]
], dtype = np.float64)

MW = np.array([310.6056, 92.09, 32.04, 878.0, 648.264, 370.138, 262.7856, 18], dtype = np.float64)
w_test = np.array([[0.856, 0.028, 0.116, 0, 0, 0, 0, 0],
              [0.002265, 0.675, 0.323, 0, 0, 0, 0, 0]], dtype = np.float64)   

gamma = Unifac(GIP, v, MW, T).calculate_gamma(w)
phase_distribution = Unifac(GIP, v, MW, T)
np.apply_along_axis(phase_distribution.calculate_gamma, 1, w_test)