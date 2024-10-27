import numpy as np
import polars as pl
from scipy.optimize import newton, minimize 
from sklearn.metrics import root_mean_squared_error
from dataclasses import dataclass
from predict_comps import CalculateComps as cc 


@dataclass
class ParameterCorrelation:
   
    @staticmethod
    def eval(params, group_tie_lines, group_contribution, comps_MW, thermo_model, data_eval):
       
        A = params[0:30]
        B = params[30:60]
        C = params[60:90]
        
        GIP = cc.define_GIP(A, B, C)
        
        all_w_light = []
        all_w_heavy = []

        for name, data in group_tie_lines:
            number_tie_lines = data.shape[0]
            tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
            v = group_contribution.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
            experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
            experiment_MW.reshape(8)
            
            phase_distribution = thermo_model(GIP, v, experiment_MW.reshape(8), name[2])
            gamma_light = np.zeros((number_tie_lines, 8))
            gamma_heavy = np.zeros((number_tie_lines, 8))
            mask_light = tie_lines_np[:, 8:16] == 0
            mask_heavy = tie_lines_np[:, 16:24] == 0
            gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 8:16]) 
            gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 16:24]) 
            gamma_light[mask_light] = 1
            gamma_heavy[mask_heavy] = 1  
            gamma_light = np.where(gamma_light == 0, 1e-20, gamma_light) 
            gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
            Ki = gamma_light / gamma_heavy
            
            heavy_overall_mass_fraction = (1 - tie_lines_np[:, -1].reshape(number_tie_lines, 1))
            sol = newton(cc.rachford_rice, fprime=cc.rachford_rice_d1, x0=heavy_overall_mass_fraction, args=(tie_lines_np[:, 0:8], Ki))
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
        
        tie_lines_eval = data_eval.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
        tie_lines_eval_np = tie_lines_eval.to_numpy()    
        mask = tie_lines_eval_np == 0
        results[mask] = 0
        
        return root_mean_squared_error(tie_lines_eval_np, results)
    
    def correlate_parameters(self, algorithm, group_tie_lines, group_contribution, comps_MW, thermo_model, data_eval):
       
        initial_params = np.random.uniform(0, 0.3, 60) 
        opt = minimize(self.eval, initial_params, method=algorithm, args=(group_tie_lines, group_contribution, comps_MW, thermo_model, data_eval))
        
        return opt, opt.x 
