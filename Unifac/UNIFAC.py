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
        """Calculate the combinatorial contribution of the UNIFAC model.

        Args:
            w (np.ndarray): Mass fraction compositions.

        Returns:
            np.ndarray: Vector of combinatorial contributions per component.
        """            
        with np.errstate(divide='ignore', invalid='ignore'):
            r = np.sum(self.v*self._R.T, axis=0)/self.MW
            q = np.sum(self.v*self._Q.T, axis=0)/self.MW
            self._zeta = np.sum(w/self.MW)
            phi = r*w/np.sum(r*w)
            theta = q*w/np.sum(q*w)
            lngamma_c = np.nan_to_num(1 - self._zeta*self.MW*phi/w + np.log(self._zeta*self.MW*phi/w) - 5*q*self.MW*(1 - (phi/theta) - np.log(theta/phi)), nan=0.0) 
            return lngamma_c
    
    def _residual_contribution(self, w: np.ndarray) -> np.ndarray:
        """Calculate the residual contribution of the UNIFAC model.

        Args:
            w (np.ndarray): Mass fraction compositions.

        Returns:
            np.ndarray: Vector of combinatorial contributions per component.
        """        
        with np.errstate(divide='ignore', invalid='ignore'):
            tao = np.exp(-self.GIP/self.T)
            Wk = np.sum(self.v*w/(self.MW*self._zeta), axis = 1)/np.sum(self.v*w/(self.MW*self._zeta))
            THETA = self._Q*Wk/np.sum(self._Q*Wk)
            lngamma_r_mix = self._Q*(1 - np.log(np.sum(THETA.T*tao, axis=0)) - np.sum(THETA*tao/np.sum(THETA.T*tao, axis=0), axis = 1))

            Wk_pure = np.nan_to_num(self.v/np.sum(self.v, axis=0), nan=0.0)
            THETA_pure = np.nan_to_num(self._Q.T*Wk_pure/np.sum(self._Q.T*Wk_pure, axis = 0), nan=0.0)
            lngamma_r_pure = np.zeros((8,8))    
            lngamma_r_pure = np.array([
                np.nan_to_num(self._Q * (1 - np.log(np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0)) - np.sum(THETA_pure[:, comp] * tao / np.sum(THETA_pure[:, comp].reshape(1, 8).T * tao, axis=0), axis=1)), nan=0) for comp in range(THETA_pure.shape[1])
            ]).reshape(8,8)
        
        lngamma_r = np.sum(np.array([self.v[:,comp]*(lngamma_r_mix - lngamma_r_pure[comp]) for comp in range(8)]).reshape(8,8), axis = 1)
        return lngamma_r
    
    def calculate_gamma(self, w: np.ndarray) -> np.ndarray:
        """Calculate gamma activity coefficient from the sum of the combinatorial and residual contribution.

        Args:
            w (np.ndarray): Mass fraction compositions.

        Returns:
            np.ndarray: Vector of activity coefficients per component.
        """        
        self._group_properties()
        lngamma_c = self._combinatorial_contribution(w)
        lngamma_r = self._residual_contribution(w) 
        gamma = np.exp(lngamma_c + lngamma_r)
        
        return gamma
