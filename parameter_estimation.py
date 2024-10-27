import numpy as np
import polars as pl
from UnifacDortmund import UnifacDortmund


tie_lines = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\refined_lle_data_v4.xlsx", engine="calamine")
group_contribution = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\group_contribution.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
    pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
).with_row_index()

tie_lines = tie_lines.drop(["Type Alcohol"])
tie_lines_train = tie_lines.sample(fraction=0.8, with_replacement=False, seed=42).sort("index")
tie_lines_validate = tie_lines.filter(~tie_lines["index"].is_in(tie_lines_train["index"]))
tie_lines_train = tie_lines_train.drop(["index"])
tie_lines_validate = tie_lines_validate.drop(["index"])

#tie_lines_train.write_excel("train_data_V2.xlsx")
#tie_lines_validate.write_excel("validate_data_V2.xlsx")


group_contribution = group_contribution.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
tie_lines = tie_lines.drop(["index"])
group_tie_lines = tie_lines_train.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)

def rachford_rice(x, Z, K): 
    return np.sum(Z*(K-1)/(1+(K-1)*x))

def rachford_rice_d1(x, Z, K): 
    return np.sum(-Z*(K-1)**2/(1+(K-1)*x)**2)

A = np.array([
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74], 
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [2900.56,  2900.56,   2900.56,     0,     -388.62,  -964.53,  5084.03,  -987.18],
       [4925.67,  4925.67,   4925.67,   259.13,     0,      947.89, -1210.44,  -4618.51], 
       [2544.80,  2544.80,   2544.80,   1047.08, -2424.84,    0,    -685.81,    134.70], 
       [3714.86,  3714.86,   3714.86,   258.51,  -3227.03,  594.79,     0,      3239.57],
       [20930.91, 20930.91,  20930.91,  -688.85, -14448.32, 1158.19, -1429.48,     0]
       ], dtype = np.float64)

# Define the objective function
def objective_function(params):
    
    init_B = params[0:30].reshape((6,5))
    init_C = params[30:61].reshape((6,5))
  
    GIP_dortmund = np.ones((8, 8, 3), dtype=np.float64)
    GIP_dortmund[:, :, 0] = A
    GIP_dortmund[:, :, 1] = np.array([
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]], 
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]],
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]],
       [init_B[1][0], init_B[1][0],    init_B[1][0],        0,       init_B[2][0], init_B[2][1],  init_B[2][2],  init_B[2][3]],
       [init_B[1][1], init_B[1][1],    init_B[1][1],   init_B[4][0],           0,  init_B[2][4],  init_B[3][0],  init_B[3][1]], 
       [init_B[1][2], init_B[1][2],    init_B[1][2],   init_B[4][1],  init_B[4][4],      0,       init_B[3][2],  init_B[3][3]], 
       [init_B[1][3], init_B[1][3],    init_B[1][3],   init_B[4][2],  init_B[5][0],  init_B[5][2],      0,       init_B[3][4]],
       [init_B[1][4], init_B[1][4],    init_B[1][4],   init_B[4][3],  init_B[5][1],  init_B[5][3], init_B[5][4],        0   ]  
       ], dtype = np.float64)


    GIP_dortmund[:, :, 2] = np.array([
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]], 
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]],
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]],
       [init_C[1][0], init_C[1][0],    init_C[1][0],        0,       init_C[2][0], init_C[2][1],  init_C[2][2],  init_C[2][3]],
       [init_C[1][1], init_C[1][1],    init_C[1][1],   init_C[4][0],           0,  init_C[2][4],  init_C[3][0],  init_C[3][1]], 
       [init_C[1][2], init_C[1][2],    init_C[1][2],   init_C[4][1],  init_C[4][4],      0,       init_C[3][2],  init_C[3][3]], 
       [init_C[1][3], init_C[1][3],    init_C[1][3],   init_C[4][2],  init_C[5][0],  init_C[5][2],      0,       init_C[3][4]],
       [init_C[1][4], init_C[1][4],    init_C[1][4],   init_C[4][3],  init_C[5][1],  init_C[5][3], init_C[5][4],        0   ]  
       ], dtype = np.float64)
    
    all_w_light = []
    all_w_heavy = []

    for name, data in group_tie_lines:
        number_tie_lines = data.shape[0]
        tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
        v = group_contribution.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW.reshape(8)
        
        phase_distribution = UnifacDortmund(GIP_dortmund, v, experiment_MW.reshape(8), name[2])
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
        sol = newton(rachford_rice, fprime=rachford_rice_d1, x0=heavy_overall_mass_fraction, args=(tie_lines_np[:, 0:8], Ki))
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
    tie_lines_eval = tie_lines_train.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
    tie_lines_eval_np = tie_lines_eval.to_numpy()    
    mask = tie_lines_eval_np == 0
    results[mask] = 0
    
    # Calculate the objective function value
    # np.sum((tie_lines_eval_np - results) ** 2) / tie_lines_eval_np.shape[0] * 100 
    return root_mean_squared_error(tie_lines_eval_np, results)



init_total = np.random.uniform(0, 0.3, 60)
#res = least_squares(objective_function, init_total, method="dogbox")
res = minimize(objective_function, init_total, method = "SLSQP")
res
res.x
#np.savetxt("UDortmundParamsV5.out", res.x)

########################################################################################################

A = np.array([

       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74], 
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [0,          0,          0,     -3214.25, -1718.09, -3079.37, 1295.55,  1249.74],
       [2900.56,  2900.56,   2900.56,     0,     -388.62,  -964.53,  5084.03,  -987.18],
       [4925.67,  4925.67,   4925.67,   259.13,     0,      947.89, -1210.44,  -4618.51], 
       [2544.80,  2544.80,   2544.80,   1047.08, -2424.84,    0,    -685.81,    134.70], 
       [3714.86,  3714.86,   3714.86,   258.51,  -3227.03,  594.79,     0,      3239.57],
       [20930.91, 20930.91,  20930.91,  -688.85, -14448.32, 1158.19, -1429.48,     0]
       ], dtype = np.float64)

#params = np.loadtxt(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\Evaluation\results\UDortmundParamsV3.out")
params = res.x
#params = np.zeros(60)
init_B = params[0:30].reshape((6,5))
init_C = params[30:61].reshape((6,5))


GIP_dortmund = np.ones((8, 8, 3), dtype = np.float64)
GIP_dortmund[:, :, 0] = A
GIP_dortmund[:, :, 1] = np.array([
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]], 
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]],
       [0,          0,                       0,        init_B[0][0], init_B[0][1], init_B[0][2],  init_B[0][3],  init_B[0][4]],
       [init_B[1][0], init_B[1][0],    init_B[1][0],        0,       init_B[2][0], init_B[2][1],  init_B[2][2],  init_B[2][3]],
       [init_B[1][1], init_B[1][1],    init_B[1][1],   init_B[4][0],           0,  init_B[2][4],  init_B[3][0],  init_B[3][1]], 
       [init_B[1][2], init_B[1][2],    init_B[1][2],   init_B[4][1],  init_B[4][4],      0,       init_B[3][2],  init_B[3][3]], 
       [init_B[1][3], init_B[1][3],    init_B[1][3],   init_B[4][2],  init_B[5][0],  init_B[5][2],      0,       init_B[3][4]],
       [init_B[1][4], init_B[1][4],    init_B[1][4],   init_B[4][3],  init_B[5][1],  init_B[5][3], init_B[5][4],        0   ]  
       ], dtype = np.float64)


GIP_dortmund[:, :, 2] = np.array([
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]], 
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]],
       [0,          0,                       0,        init_C[0][0], init_C[0][1], init_C[0][2],  init_C[0][3],  init_C[0][4]],
       [init_C[1][0], init_C[1][0],    init_C[1][0],        0,       init_C[2][0], init_C[2][1],  init_C[2][2],  init_C[2][3]],
       [init_C[1][1], init_C[1][1],    init_C[1][1],   init_C[4][0],           0,  init_C[2][4],  init_C[3][0],  init_C[3][1]], 
       [init_C[1][2], init_C[1][2],    init_C[1][2],   init_C[4][1],  init_C[4][4],      0,       init_C[3][2],  init_C[3][3]], 
       [init_C[1][3], init_C[1][3],    init_C[1][3],   init_C[4][2],  init_C[5][0],  init_C[5][2],      0,       init_C[3][4]],
       [init_C[1][4], init_C[1][4],    init_C[1][4],   init_C[4][3],  init_C[5][1],  init_C[5][3], init_C[5][4],        0   ]  
       ], dtype = np.float64)

#group_tie_lines = tie_lines_validate.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)
group_tie_lines = tie_lines.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)

all_w_light = []
all_w_heavy = []

for name, data in group_tie_lines:
    number_tie_lines = data.shape[0]
    tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
    v = group_contribution.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
    experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy() 
    experiment_MW.reshape(8)
    
    phase_distribution = UnifacDortmund(GIP_dortmund, v, experiment_MW.reshape(8), name[2])
    gamma_light = np.zeros((number_tie_lines, 8))
    gamma_heavy = np.zeros((number_tie_lines, 8))
    mask_feed = tie_lines_np[:, 0:8] == 0  
    mask_light = tie_lines_np[:, 8:16] == 0
    mask_heavy = tie_lines_np[:, 16:24] == 0
    gamma_light = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 8:16]) 
    gamma_heavy = np.apply_along_axis(phase_distribution.calculate_gamma, 1, tie_lines_np[:, 16:24]) 
    gamma_light[mask_light] = 1
    gamma_heavy[mask_heavy] = 1  
    gamma_light = np.where(gamma_light == 0, 1e-20, gamma_light) 
    gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
    Ki = gamma_light/gamma_heavy 
    
    heavy_overall_mass_fraction = (1-tie_lines_np[:, -1].reshape(number_tie_lines, 1))
    sol = newton(rachford_rice, fprime=rachford_rice_d1, x0=heavy_overall_mass_fraction, args = (tie_lines_np[:, 0:8], Ki))
    calculated_w_light = tie_lines_np[:, 0:8]/(1+(Ki-1)*sol)
    calculated_w_heavy = Ki*calculated_w_light
    
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
#tie_lines_eval = tie_lines_validate.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
tie_lines_eval = tie_lines.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
tie_lines_eval_np = tie_lines_eval.to_numpy()
mask = tie_lines_eval_np == 0
results[mask] = 0
objective = root_mean_squared_error(tie_lines_eval_np, results)
objective
#np.sum(objective)

ref_results = pl.concat([tie_lines.select(["Ref", "Sub Ref"]), pl.DataFrame(objective, schema=["Squared Error"])], how="horizontal").with_row_index()
filtered_results = ref_results.filter(pl.col("Squared Error") > 0.05)
tie_lines_test = tie_lines.with_row_index()
pl.DataFrame(results, schema=['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H']).write_excel("results_validate_V3.xlsx")
#filtered_results.write_excel("filtered_results2.xlsx")