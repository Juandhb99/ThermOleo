import numpy as np
import polars as pl
from scipy.optimize import newton
from dataclasses import dataclass, field


@dataclass
class CalculateComps:
    
    @staticmethod
    def _process_data(input_data, group_contribution_data, split_fraction):
        
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
    def _rachford_rice(x, Z, K):
        return np.sum(Z*(K-1)/(1+(K-1)*x))
   
    @staticmethod 
    def _rachford_rice_d1(x, Z, K): 
        return np.sum(-Z*(K-1)**2/(1+(K-1)*x)**2)
    
    @staticmethod
    def _define_GIP(A, B, C):
        
        GIP = np.ones((8, 8, 3), dtype=np.float64) 
        GIP[:, :, 0] = A
        GIP[:, :, 1] = B
        GIP[:, :, 2] = C
        
        return GIP
    
    @staticmethod
    def calculate_comps(data, group_contribution_data, comps_MW, thermo_model, GIP):
        
    
        group_tie_lines = data.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)
        all_w_light = []
        all_w_heavy = []

        for name, data in group_tie_lines:
            number_tie_lines = data.shape[0]
            tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
            v = group_contribution_data.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
            experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
            experiment_MW.reshape(8)
            
            gamma_light = np.zeros((number_tie_lines, 8))
            gamma_heavy = np.zeros((number_tie_lines, 8))
            mask_light = tie_lines_np[:, 8:16] == 0
            mask_heavy = tie_lines_np[:, 16:24] == 0
            phase_distribution = thermo_model(GIP, v, experiment_MW.reshape(8), name[2])
            gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 8:16]) 
            gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 16:24]) 
            gamma_light[mask_light] = 1
            gamma_heavy[mask_heavy] = 1  
            gamma_light = np.where(gamma_light == 0, 1e-20, gamma_light) 
            gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
            Ki = gamma_light / gamma_heavy
            
            heavy_overall_mass_fraction = (1 - tie_lines_np[:, -1].reshape(number_tie_lines, 1))
            sol = newton(CalculateComps._rachford_rice, fprime=CalculateComps._rachford_rice_d1, x0=heavy_overall_mass_fraction, args=(tie_lines_np[:, 0:8], Ki))
            calculated_w_light = tie_lines_np[:, 0:8] / (1 + (Ki - 1) * sol)
            calculated_w_heavy = Ki * calculated_w_light
            
            calculated_w_light = np.where(calculated_w_light >= 1, 0.999, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy >= 1, 0.999, calculated_w_heavy) 
            calculated_w_light = np.where(calculated_w_light < 0, 0, calculated_w_light)  
            calculated_w_heavy = np.where(calculated_w_heavy < 0, 0, calculated_w_heavy) 
            
            condition_GLY = calculated_w_light[:, 1] > calculated_w_heavy[:, 1]
            condition_OIL_1 = calculated_w_light[:, 3] > calculated_w_heavy[:, 3] 
            condition_OIL_2 = tie_lines_np[:, 11] < tie_lines_np[:, 19]
            combined_OIL_1 = condition_OIL_1 & condition_OIL_2
            
            condition_OIL_3 = calculated_w_light[:, 3] < calculated_w_heavy[:, 3] 
            condition_OIL_4 = tie_lines_np[:, 11] > tie_lines_np[:, 19]
            combined_OIL_2 = condition_OIL_3 & condition_OIL_4
            
            total_condition = condition_GLY | combined_OIL_1 | combined_OIL_2

            calculated_w_light[total_condition], calculated_w_heavy[total_condition] = (
                calculated_w_heavy[total_condition],
                calculated_w_light[total_condition])
            
            all_w_light.append(calculated_w_light)
            all_w_heavy.append(calculated_w_heavy)

        final_w_light = np.vstack(all_w_light)
        final_w_heavy = np.vstack(all_w_heavy)
        results = np.hstack([final_w_light, final_w_heavy])
        results = np.nan_to_num(results, nan=1)
        
        return results

        
    
    
    