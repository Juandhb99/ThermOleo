import numpy as np
import polars as pl
from scipy.optimize import newton
from dataclasses import dataclass, field


@dataclass
class CalculateComps:
    
    """
        Algorithm to calculate the phase compositions using UNIFAC or UNIFAC Dortmund, the procedure to calculate the phase compositions
        is iterative and is described in this paper "Costa, É. D., & Braga, J. P. (2024). The Rachford-Rice equation: application to ternary diagram. Revista Brasileira De Ensino De Física,
        46. https://doi.org/10.1590/1806-9126-rbef-2024-0077".

    """    
    
    @staticmethod
    def process_data(input_data: pl.DataFrame, group_contribution_data: pl.DataFrame, split_fraction: float):
        """The process data method, takes the a group of global compositions each with their one temperature conditions and transforms them from 
        polars dataframe format to numpy for predicting the phase compositions. 

        Args:
            input_data (pl.DataFrame): _description_
            group_contribution_data (_type_): _description_
            split_fraction (_type_): _description_

        Returns:
            _type_: _description_
        """  
        # changes this function.
              
        input_data = input_data.with_columns( pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
        ).with_row_index()

        input_data = input_data.drop(["Type Alcohol"])
        input_data_train = input_data.sample(fraction=split_fraction, with_replacement=False, seed=42).sort("index")
        input_data_validate = input_data.filter(~input_data["index"].is_in(input_data_train["index"]))
        input_data_train = input_data_train.drop(["index"])
        input_data_validate = input_data_validate.drop(["index"])
        input_data = input_data.drop(["index"])
        
        group_contribution_data = group_contribution_data.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
        comps_MW = comps_MW.drop(["Type Alcohol"])
        #group_tie_lines = input_data_train.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)

        return input_data, input_data_train, input_data_validate, group_contribution_data
   
    @staticmethod 
    def rachford_rice(x: np.ndarray, Z: np.ndarray, K: np.ndarray): 
        """The rachford_rice method, applies the vectorized calculation of the rachford_rice algorithm for each tie line using mass fractions.
        Args:
            x (np.ndarray): Overrall mass fraction of the heavy phase, this is a nx1 matrix, where n will be the number of tie lines in the data.  
            Z (np.ndarray): Mass composition of the feed, this is a nx8 matrix, where n will be the number of tie lines in the data.
            K (np.ndarray): Matriz of distribution coefficients for each component in the mixture calculated from the activiy coefficient in each phase. This is a nx8 matrix where n will be the number of tie lines in the data.

        Returns:
            np.ndarray: Matrix of size 1xn that is the sum of the rachford-rice equation result for each component in the mixture.
        """        
        return np.sum(Z*(K-1)/(1+(K-1)*x))
   
    @staticmethod 
    def rachford_rice_d1(x, Z, K): 
        """The rachford_rice_d1 method, applies the vectorized calculation of the first derivative of the rachford_rice algorithm for each tie line using mass fractions.
        Args:
            x (np.ndarray): Overrall mass fraction of the heavy phase, this is a nx1 matrix, where n will be the number of tie lines in the data.  
            Z (np.ndarray): Mass composition of the feed, this is a nx8 matrix, where n will be the number of tie lines in the data.
            K (np.ndarray): Matriz of distribution coefficients for each component in the mixture calculated from the activiy coefficient in each phase. This is a nx8 matrix where n will be the number of tie lines in the data.

        Returns:
            np.ndarray: Matrix of size 1xn that is the sum of the rachford-rice first derivative equation result for each component in the mixture.
        """   
        return np.sum(-Z*(K-1)**2/(1+(K-1)*x)**2)
    
    @staticmethod
    def define_GIP(A, B, C):
        
        GIP = np.ones((8, 8, 3), dtype=np.float64) 
        GIP[:, :, 0] = A
        GIP[:, :, 1] = B
        GIP[:, :, 2] = C
        
        return GIP
    
    @staticmethod
    def calculate_comps(data, v, data_MW, temperature, thermo_model, GIP):
       
         
        phase_distribution = thermo_model(GIP, v, data_MW, temperature)

        initial_w_light_guess = np.random.random((data.shape[0], 8))
        initial_w_heavy_guess = np.random.random((data.shape[0], 8))
        
        initial_w_light_guess[data == 0] = 0
        initial_w_heavy_guess[data == 0] = 0

        initial_w_light_guess = initial_w_light_guess/initial_w_light_guess.sum(axis = 1, keepdims=True)
        initial_w_heavy_guess = initial_w_heavy_guess/initial_w_heavy_guess.sum(axis = 1, keepdims=True)

        mask_light = initial_w_light_guess == 0
        mask_heavy = initial_w_heavy_guess == 0 
        phi_guess = np.full((data.shape[0], 8), 0.5)

        while True:
           
            gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, initial_w_light_guess).reshape(data.shape[0], 8) 
            gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, initial_w_heavy_guess).reshape(data.shape[0], 8)     
            gamma_light[mask_light] = 1
            gamma_heavy[mask_heavy] = 1  
            gamma_light = np.where(gamma_light == 0, 1e-20, gamma_light) 
            gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
            Ki = gamma_light / gamma_heavy
            
            sol = newton(CalculateComps.rachford_rice, fprime=CalculateComps.rachford_rice_d1, x0=phi_guess, args=(data, Ki))
            calculated_w_light = data / (1 + (Ki - 1) * sol)
            calculated_w_heavy = Ki * calculated_w_light
            
            calculated_w_light = np.where(calculated_w_light >= 1, 0.999, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy >= 1, 0.999, calculated_w_heavy) 
            calculated_w_light = np.where(calculated_w_light < 0, 0, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy < 0, 0, calculated_w_heavy) 
            
            light_error = (calculated_w_light - initial_w_light_guess)
            heavy_error = (calculated_w_heavy - initial_w_heavy_guess) 
                        
            if (light_error < 0.0001).all() & (heavy_error < 0.0001).all():
            
                condition_GLY = calculated_w_light[:, 1] > calculated_w_heavy[:, 1]
                condition_OIL_1 = calculated_w_light[:, 3] > calculated_w_heavy[:, 3] 
                condition_OIL_2 = calculated_w_light[:, 7] > calculated_w_heavy[:, 7] 
                condition_OIL_3 = calculated_w_light[:, 3] > calculated_w_light[:, 7] 
                combined_OIL_1 = condition_OIL_1 & condition_OIL_2 & condition_OIL_3
             
                total_condition = condition_GLY | combined_OIL_1 

                calculated_w_light[total_condition], calculated_w_heavy[total_condition] = (calculated_w_heavy[total_condition], calculated_w_light[total_condition])
                
                break
            
            else:
                initial_w_light_guess = calculated_w_light
                initial_w_heavy_guess = calculated_w_heavy
             
        return calculated_w_light, calculated_w_heavy

        
    
    
    