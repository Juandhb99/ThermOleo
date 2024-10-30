import numpy as np
import polars as pl
from Unifac import Unifac
from UnifacDortmund import UnifacDortmund
from PhaseCalculation import CalculateComps as cc

tie_lines = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\ExperimentalData\data\refined_lle_data_v4.xlsx", engine="calamine")
group_contribution = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\ExperimentalData\data\group_contribution.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\ExperimentalData\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
        pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
    ).with_row_index()

tie_lines = tie_lines.drop(["Type Alcohol"])
tie_lines = tie_lines.drop(["Type Alcohol"])
tie_lines_train = tie_lines.sample(fraction=0.8, with_replacement=False, seed=42).sort("index")
tie_lines_validate = tie_lines.filter(~tie_lines["index"].is_in(tie_lines_train["index"]))
tie_lines_train = tie_lines_train.drop(["index"])
tie_lines_validate = tie_lines_validate.drop(["index"])

group_contribution = group_contribution.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
tie_lines = tie_lines.drop(["index"])
group_tie_lines = tie_lines_train.group_by(["Ref", "Sub Ref", "Temperature (K)"], maintain_order=True) 
    
def predict(params):
    
    A = np.array([-3214.25, -1718.09, -3079.37, 1295.55, 1249.74, 2900.56, 2900.56, 2900.56, -388.62, 259.13, 4925.67, 4925.67, 4925.67, 1047.08, -2424.84, 
                  2544.80, 2544.80, 2544.80, 258.51, -3227.03, 3714.86, 3714.86, 3714.86, -987.18, -688.85, 20930.91, 5084.03, -1210.44, -4618.51, -14448.32])
    
    B = params[0:30]
    C = params[30:60]
    GIP = cc.define_GIP(A, B, C)
    
    results_list = []
    for name, data in group_tie_lines:
        print(name)
        tie_lines_np = data.drop(["Ref", "Sub Ref", "Temperature (K)"]).to_numpy()
        v = group_contribution.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW = comps_MW.filter((pl.col("Ref") == name[0]) & (pl.col("Sub Ref") == name[1])).drop(["Ref", "Sub Ref"]).to_numpy()
        experiment_MW.reshape(8) 
        results_list.append(cc.calculate_comps(tie_lines_np[:,0:8], v, experiment_MW, name[2], thermo_model, GIP, initial_guess=tie_lines_np[:,8:25]))
    
    results_total = np.vstack(results_list) 
    pl.DataFrame(results_total, schema=['FAME/FAEE_L', 'GLYCEROL_L', 'ALCOHOL_L', 'OIL_L', 'DAG_L', 'MAG_L', 'ACID_L', 'WATER_L', 'FAME/FAEE_H', 'GLYCEROL_H', 'ALCOHOL_H', 'OIL_H', 'DAG_H', 'MAG_H', 'ACID_H', 'WATER_H']).write_excel("results_predict.xlsx") 
    


if __name__ == "__main__":
    
    print(predict_comps())