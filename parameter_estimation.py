import numpy as np
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import newton, least_squares
from UnifacDortmund import UnifacDortmund


tie_lines = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\UnifacDortmund\Experimental_Data\data\refined_lle_data.xlsx", engine="calamine")
group_contribution = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\UnifacDortmund\Experimental_Data\data\group_contribution.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\UnifacDortmund\Experimental_Data\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
    pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
).with_row_index()

tie_lines.filter(pl.col("WATER_L") > pl.col("WATER_H"))

tie_lines.columns

# Define the column suffixes for _L and _H
suffixes = ["FAME/FAEE", "GLYCEROL", "ALCOHOL", "OIL", "DAG", "MAG", "ACID", "WATER"]

# Define conditions where OIL_L > OIL_H, GLYCEROL_L > GLYCEROL_H, and WATER_L > WATER_H
condition = (
    (pl.col("OIL_L") > pl.col("OIL_H")))

# Swap values between columns ending with _L and _H
tie_lines = tie_lines.with_columns([
    pl.when(condition).then(pl.col(f"{col}_H")).otherwise(pl.col(f"{col}_L")).alias(f"{col}_L") for col in suffixes
] + [
    pl.when(condition).then(pl.col(f"{col}_L")).otherwise(pl.col(f"{col}_H")).alias(f"{col}_H") for col in suffixes
])

tie_lines

tie_lines.filter(pl.col("Ref")==46)

tie_lines = tie_lines.drop(["Type Alcohol"])
tie_lines_train = tie_lines.sample(fraction=0.8, with_replacement=False, seed=42).sort("index")
tie_lines_validate = tie_lines.filter(~tie_lines["index"].is_in(tie_lines_train["index"]))
tie_lines_train = tie_lines_train.drop(["index"])
tie_lines_validate = tie_lines_validate.drop(["index"])

group_contribution = group_contribution.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
tie_lines = tie_lines.drop(["index"])
group_tie_lines = tie_lines.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True)

def rachford_rice(x, Z, K): 
    return np.sum(Z*(K-1)/(1+(K-1)*x))

def rachford_rice_d1(x, Z, K): 
    return np.sum(-Z*(K-1)**2/(1+(K-1)*x)**2)

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

GIP_dortmund = np.ones((8, 8, 3), dtype = np.float64)
GIP_dortmund[:, :, 0] = GIP_unifac

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
    gamma_heavy = np.where(gamma_heavy == 0, 1e-20, gamma_heavy) 
    Ki = gamma_light/gamma_heavy 
    
    heavy_overall_mass_fraction = (1-tie_lines_np[:, -1].reshape(number_tie_lines, 1))
    sol = newton(rachford_rice, fprime=rachford_rice_d1, x0=heavy_overall_mass_fraction, args = (tie_lines_np[:, 0:8], Ki))
    calculated_w_light = tie_lines_np[:, 0:8]/(1+(Ki-1)*sol)
    calculated_w_heavy = Ki*calculated_w_light
    
    calculated_w_light = np.where(calculated_w_light >= 1, 0.999, calculated_w_light)  
    calculated_w_heavy = np.where(calculated_w_heavy >= 1, 0.999, calculated_w_heavy) 
    
    rearranged_w_light = calculated_w_light.copy()
    rearranged_w_heavy = calculated_w_heavy.copy()
    
    #for i in range(number_tie_lines):
        #if calculated_w_light[i, 1] > calculated_w_heavy[i, 1]:
        #rearranged_w_light[i, 1] = calculated_w_heavy[i, 1]  
        #rearranged_w_heavy[i, 1] = calculated_w_light[i, 1] 

        #elif calculated_w_light[i, 3] > calculated_w_heavy[i, 3]:
           #rearranged_w_light[i, 3] = calculated_w_heavy[i, 3] 
           #rearranged_w_heavy[i, 3] = calculated_w_light[i, 3] 
        
        #elif calculated_w_light[i, 7] > calculated_w_heavy[i, 7]:
           #rearranged_w_light[i, 7] = calculated_w_heavy[i, 7] 
           #rearranged_w_heavy[i, 7] = calculated_w_light[i, 7] 
    
    #all_w_light.append(rearranged_w_light)
    #all_w_heavy.append(rearranged_w_heavy)

    
    if all(calculated_w_light[:,1] > calculated_w_heavy[:,1]):
        rearranged_w_light = calculated_w_heavy
        rearranged_w_heavy = calculated_w_light 
        all_w_light.append(rearranged_w_light)
        all_w_heavy.append(rearranged_w_heavy)
    else:
        all_w_light.append(calculated_w_light)
        all_w_heavy.append(calculated_w_heavy)

    #all_w_light.append(calculated_w_light)
    #all_w_heavy.append(calculated_w_heavy)

        
final_w_light = np.vstack(all_w_light)
final_w_heavy = np.vstack(all_w_heavy)


results = np.hstack([final_w_light, final_w_heavy])
tie_lines_eval = tie_lines.select(['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H'])
tie_lines_eval_np = tie_lines_eval.to_numpy()
objective = np.sum((tie_lines_eval_np - results)**2, 1)/tie_lines_eval_np.shape[0]*100
np.sum(objective)

ref_results = pl.concat([tie_lines.select(["Ref", "Sub Ref"]), pl.DataFrame(objective, schema=["Squared Error"])], how="horizontal").with_row_index()
filtered_results = ref_results.filter(pl.col("Squared Error") > 0.1)
tie_lines_test = tie_lines.with_row_index()
tie_lines_test.filter(
    pl.col("Ref") == 5,
    pl.col("Sub Ref") == "a"
    )
#pl.DataFrame(results, schema=['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H']).write_excel("results.xlsx")

#filtered_results.write_excel("filtered_results.xlsx")

    
sns.set_theme(rc={'figure.figsize':(25,10)})
sns.scatterplot(x = range(tie_lines_eval_np.shape[0]), y = objective)
plt.show()

