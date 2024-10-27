import numpy as np
import polars as pl
from scipy.optimize import newton
from dataclasses import dataclass


@dataclass
class CalculateComps: 
    """ 
        Algorithm to calculate the phase compositions using UNIFAC or UNIFAC Dortmund, the procedure to calculate the phase compositions
        is iterative and is described in this paper "Costa, É. D., & Braga, J. P. (2024). The Rachford-Rice equation: application to ternary diagram. Revista Brasileira De Ensino De Física,
        46. https://doi.org/10.1590/1806-9126-rbef-2024-0077".
    """    
    
    @staticmethod 
    def rachford_rice(x: np.ndarray, Z: np.ndarray, K: np.ndarray) -> np.ndarray: 
        """The rachford_rice method, applies the vectorized calculation of the rachford_rice algorithm for each tie line using mass fractions.
        Args:
            x (np.ndarray): Overrall mass fraction of the heavy phase, this is a nx1 matrix, where n will be the number of tie lines in the data.  
            Z (np.ndarray): Mass composition of the feed, this is a nx8 matrix, where n will be the number of tie lines in the data.
            K (np.ndarray): Matriz of distribution coefficients for each component in the mixture calculated from the activiy coefficient in each phase. This is a nx8 matrix where n will be the number of tie lines in the data.

        Returns:
            np.ndarray: Matrix of size 1xn that is the sum of the rachford-rice equation result for each component in the mixture.
        """         
        # Clamp K values to prevent overflow
        K = np.clip(K, -1e10, 1e10)  # Adjust limits as necessary
        return np.sum(Z*(K-1)/(1+(K-1)*x))
   
    @staticmethod 
    def rachford_rice_d1(x: np.ndarray, Z: np.ndarray, K: np.ndarray) -> np.ndarray: 
        """The rachford_rice_d1 method, applies the vectorized calculation of the first derivative of the rachford_rice algorithm for each tie line using mass fractions.
        Args:
            x (np.ndarray): Overrall mass fraction of the heavy phase, this is a nx1 matrix, where n will be the number of tie lines in the data.  
            Z (np.ndarray): Mass composition of the feed, this is a nx8 matrix, where n will be the number of tie lines in the data.
            K (np.ndarray): Matrix of distribution coefficients for each component in the mixture calculated from the activiy coefficient in each phase. This is a nx8 matrix where n will be the number of tie lines in the data.

        Returns:
            np.ndarray: Matrix of size 1xn that is the sum of the rachford-rice first derivative equation result for each component in the mixture.
        """    
        # Clamp K values to prevent overflow
        K = np.clip(K, -1e10, 1e10)  # Adjust limits as necessary
        return np.sum(-Z*(K-1)**2/(1+(K-1)*x)**2)
    
    @staticmethod
    def define_GIP(params_a: np.ndarray, params_b: np.ndarray, params_c: np.ndarray) -> np.ndarray:
        """The define GIP method, uses as an input the a, b and c parameters organized as a numpy array of 30 elements. Each array has only the non zero parameters,
        and the method organizes the values into the matrices for the complete GIP which include the pairs where the value is 0 or the value is repeated when the subgroup
        comes from the same group. In case that the thermodynamic model to use is UNIFAC, the params_b and params_c must contain all zeros.

        Args:
            params_a (np.ndarray): GIP for term A
            params_b (np.ndarray): GIP for term B
            params_c (np.ndarray): GIP for term B

        Returns:
            np.ndarray:Matrix of group interaction parameters, this must be a 8x8x3 matrix where each column and row represents a
            functional group. The order must be CH, CH2, CH3, CH=CH, OH, CH2COO, COOH, H2O for both the columns and rows. The a, b and c GIP for the 
            unifac dortmund model are respectively must be the first, second and third layer of the GIP matrix. 
        """        
       
        A = params_a.reshape((6,5))
        B = params_b.reshape((6,5))
        C = params_c.reshape((6,5))
         
        GIP = np.zeros((8, 8, 3), dtype=np.float64) 
        
        GIP[:, :, 0] =  np.array([  [0,          0,          0,        A[0][0], A[0][1], A[0][2],  A[0][3],  A[0][4]], 
                                    [0,          0,          0,        A[0][0], A[0][1], A[0][2],  A[0][3],  A[0][4]],
                                    [0,          0,          0,        A[0][0], A[0][1], A[0][2],  A[0][3],  A[0][4]],
                                    [A[1][0], A[1][0],    A[1][0],        0,    A[2][0], A[2][1],  A[2][2],  A[2][3]],
                                    [A[1][1], A[1][1],    A[1][1],   A[4][0],       0,   A[2][4],  A[3][0],  A[3][1]], 
                                    [A[1][2], A[1][2],    A[1][2],   A[4][1],  A[4][4],      0,    A[3][2],  A[3][3]], 
                                    [A[1][3], A[1][3],    A[1][3],   A[4][2],  A[5][0],  A[5][2],      0,    A[3][4]],
                                    [A[1][4], A[1][4],    A[1][4],   A[4][3],  A[5][1],  A[5][3], A[5][4],       0  ]  
                                    ], dtype = np.float64) 
                            
            
        GIP[:, :, 1] = np.array([   [0,          0,          0,       B[0][0], B[0][1], B[0][2],  B[0][3],  B[0][4]], 
                                    [0,          0,          0,       B[0][0], B[0][1], B[0][2],  B[0][3],  B[0][4]],
                                    [0,          0,          0,       B[0][0], B[0][1], B[0][2],  B[0][3],  B[0][4]],
                                    [B[1][0], B[1][0],    B[1][0],      0,     B[2][0], B[2][1],  B[2][2],  B[2][3]],
                                    [B[1][1], B[1][1],    B[1][1],   B[4][0],     0,    B[2][4],  B[3][0],  B[3][1]], 
                                    [B[1][2], B[1][2],    B[1][2],   B[4][1],  B[4][4],      0,   B[3][2],  B[3][3]], 
                                    [B[1][3], B[1][3],    B[1][3],   B[4][2],  B[5][0],  B[5][2],     0,    B[3][4]],
                                    [B[1][4], B[1][4],    B[1][4],   B[4][3],  B[5][1],  B[5][3], B[5][4],      0  ]  
                                    ], dtype = np.float64)
                
        
        GIP[:, :, 2] = np.array([   [0,          0,          0,       C[0][0], C[0][1], C[0][2],  C[0][3],  C[0][4]], 
                                    [0,          0,          0,       C[0][0], C[0][1], C[0][2],  C[0][3],  C[0][4]],
                                    [0,          0,          0,       C[0][0], C[0][1], C[0][2],  C[0][3],  C[0][4]],
                                    [C[1][0], C[1][0],    C[1][0],      0,     C[2][0], C[2][1],  C[2][2],  C[2][3]],
                                    [C[1][1], C[1][1],    C[1][1],   C[4][0],     0,    C[2][4],  C[3][0],  C[3][1]], 
                                    [C[1][2], C[1][2],    C[1][2],   C[4][1],  C[4][4],     0,    C[3][2],  C[3][3]], 
                                    [C[1][3], C[1][3],    C[1][3],   C[4][2],  C[5][0],  C[5][2],     0,    C[3][4]],
                                    [C[1][4], C[1][4],    C[1][4],   C[4][3],  C[5][1],  C[5][3], C[5][4],      0  ]  
                                        ], dtype = np.float64)
                        
        return GIP
    
    @staticmethod
    def calculate_comps(data: np.ndarray, v: np.ndarray, data_MW: np.ndarray, temperature: float, thermo_model, GIP: np.ndarray) -> np.ndarray:
        """The calculate_comps method, calculates the component mass fraction in each of the phases following the procedure presented
        by "Costa, É. D., & Braga, J. P. (2024). The Rachford-Rice equation: application to ternary diagram. Revista Brasileira De Ensino De Física,
        46. https://doi.org/10.1590/1806-9126-rbef-2024-0077".

        Args:
            data (np.ndarray): Global/feed compositions.
            v (np.ndarray):  Matrix of the number of times each group appears in each molecule of the mixture. This is a 8x8 matrix 
            data_MW (np.ndarray): Vector of molecular weights of the molecules in the system. This is a 1x8 vector that must have the following order
            FAME/FAEE, GLYCEROL, ALCOHOL, OIL, DAG, MAG, ACID, H2O.
            temperature (float): Temperature of the system in K.
            thermo_model (Unifac/UnifacDortmund): Thermodynamic model to use, either UNIFAC or UNIFAC Dortmund.
            GIP (np.ndarray): Matrix of group interaction parameters, this must be a 8x8x3 matrix where each column and row represents a
            functional group. The order must be CH, CH2, CH3, CH=CH, OH, CH2COO, COOH, H2O for both the columns and rows. The a, b and c GIP for the 
            unifac dortmund model are respectively must be the first, second and third layer of the GIP matrix. 

        Returns:
            np.ndarray: Component mass fraction in each phase. This will be two matrices of time 
        """       
        comp_results = np.zeros((data.shape[0], 16)) 
        phase_distribution = thermo_model(GIP, v, data_MW, temperature)
        mask_light = data == 0
        mask_heavy = data == 0 

        initial_w_light_guess = np.random.random((data.shape[0], 8))
        initial_w_heavy_guess = np.random.random((data.shape[0], 8))
 
        initial_w_light_guess[mask_light] = 0
        initial_w_heavy_guess[mask_heavy] = 0

        initial_w_light_guess = initial_w_light_guess/initial_w_light_guess.sum(axis = 1, keepdims=True)
        initial_w_heavy_guess = initial_w_heavy_guess/initial_w_heavy_guess.sum(axis = 1, keepdims=True)
 
        phi_guess = np.full((data.shape[0], 8), 0.5)
        iter = 0
        while True:
            
            iter += 1
            gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, initial_w_light_guess).reshape(data.shape[0], 8) 
            gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, initial_w_heavy_guess).reshape(data.shape[0], 8)     
            gamma_light[mask_light] = 1
            gamma_heavy[mask_heavy] = 1  
            gamma_light = np.where(gamma_light == 0, 1e-20, gamma_light) 
            gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
            Ki = gamma_light / gamma_heavy
            
            sol = newton(CalculateComps.rachford_rice, fprime=CalculateComps.rachford_rice_d1, x0=phi_guess, args=(data, Ki), maxiter=150, tol = 1e-1)
            calculated_w_light = data / (1 + (Ki - 1) * sol)
            calculated_w_heavy = Ki * calculated_w_light
            
            calculated_w_light = np.where(calculated_w_light >= 1, 0.999, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy >= 1, 0.999, calculated_w_heavy) 
            calculated_w_light = np.where(calculated_w_light < 0, 0, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy < 0, 0, calculated_w_heavy) 
            
            light_error = np.absolute(calculated_w_light - initial_w_light_guess)
            heavy_error = np.absolute(calculated_w_heavy - initial_w_heavy_guess) 
                        
            if (light_error < 0.001).all() & (heavy_error < 0.001).all() or iter >= 40:
                 
                condition_GLY = calculated_w_light[:, 1] > calculated_w_heavy[:, 1]
                condition_OIL_1 = calculated_w_light[:, 3] > calculated_w_heavy[:, 3] 
                condition_OIL_2 = calculated_w_light[:, 7] > calculated_w_heavy[:, 7] 
                condition_OIL_3 = calculated_w_light[:, 3] > calculated_w_light[:, 7] 
                combined_OIL_1 = condition_OIL_1 & condition_OIL_2 & condition_OIL_3
             
                total_condition = condition_GLY | combined_OIL_1 

                calculated_w_light[total_condition], calculated_w_heavy[total_condition] = (calculated_w_heavy[total_condition], calculated_w_light[total_condition])
                
                comp_results[:, 0:8] = calculated_w_light     
                comp_results[:, 8:16] = calculated_w_heavy     
                
                break
            
            else:
                initial_w_light_guess = calculated_w_light
                initial_w_heavy_guess = calculated_w_heavy 
             
        return comp_results

        
    
    
    