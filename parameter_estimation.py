import os
import time
import json
import numpy as np
import polars as pl
from sklearn.metrics import root_mean_squared_error
from scipy.optimize import  minimize, least_squares, differential_evolution
from Unifac import Unifac
from UnifacDortmund import UnifacDortmund
from PhaseCalculation import CalculateComps as cc

start_time = time.time()
tie_lines = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\ExperimentalData\data\refined_lle_data_v5.xlsx", engine="calamine")
group_contribution = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\ExperimentalData\data\group_contribution.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\ExperimentalData\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
        pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
    ).with_row_index()

tie_lines = tie_lines.drop(["Type Alcohol"])
tie_lines_train = tie_lines.sample(fraction=0.8, with_replacement=False, seed=42).sort("index")
tie_lines_validate = tie_lines.filter(~tie_lines["index"].is_in(tie_lines_train["index"]))
tie_lines_train = tie_lines_train.drop(["index"])
tie_lines_validate = tie_lines_validate.drop(["index"])

group_contribution = group_contribution.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
tie_lines = tie_lines.drop(["index"])
group_tie_lines = tie_lines_train.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)     

tie_lines_eval = tie_lines_train.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
tie_lines_eval_np = tie_lines_eval.to_numpy()    
thermo_model = UnifacDortmund
evaluation_log = []

def predict_comps(params: np.ndarray, tie_lines_eval_np: np.ndarray):

    A = np.array([-3214.25, -1718.09, -3079.37, 1295.55, 1249.74, 2900.56, 2900.56, 2900.56, -388.62, 259.13, 4925.67, 4925.67, 4925.67, 1047.08, -2424.84, 
                  2544.80, 2544.80, 2544.80, 258.51, -3227.03, 3714.86, 3714.86, 3714.86, -987.18, -688.85, 20930.91, 5084.03, -1210.44, -4618.51, -14448.32]) 
    B = params[0:30]
    C = params[30:60]
    
    GIP = cc.define_GIP(A, B, C)
    
    results_list = []
    for name, data in group_tie_lines:
        tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
        v = group_contribution.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW.reshape(8) 
        results_list.append(cc.calculate_comps(tie_lines_np[:,0:8], v, experiment_MW, name[2], thermo_model, GIP, initial_guess=tie_lines_np[:,8:25]))
    
    results_total = np.vstack(results_list) 
    mask = tie_lines_eval_np == 0
    results_total[mask] = 0 
    value = root_mean_squared_error(tie_lines_eval_np, results_total)

    log_entry = {
        
        "value": value,
        "params": params.tolist()
    }    
    
    evaluation_log.append(log_entry)
    
    with open("differential_evolution_log_(1-11-24).json", "w") as json_file:
        json.dump(evaluation_log, json_file, indent=4 )

    print("Func evaluation: ", value)
    return value

if __name__ == "__main__":
    
    #init_total = np.random.uniform(0, 0.5, 60)
    bounds = [(0, 0.5)]*60
    #res = minimize(predict_comps, init_total, method = "Nelder-Mead", args=(tie_lines_eval_np, ))
    #res = least_squares(fun=predict_comps, x0=init_total, args=(tie_lines_eval_np,))
    res = differential_evolution(func = predict_comps, bounds=bounds, args=(tie_lines_eval_np,))
    print("The final value of the function is: ", res.fun)
    end_time = time.time()
    print(f"Total time: {end_time - start_time:.2f} seconds")
    np.savetxt("UDortmundParamsV1.out", res.x)
    