import os
import sys
import polars as pl
import numpy as np
from UnifacDortmund import UnifacDortmund


tie_lines = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\refined_lle_data.xlsx", engine="calamine")
coeffs = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\profile_coeffs.xlsx", engine="calamine")
comps_MW = pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\UnifacDortmund\Experimental_Data\data\comps_MW.xlsx", engine="calamine")

tie_lines = tie_lines.with_columns(
    
    pl.col("Sub Ref").str.slice(0, 1).alias("Sub Ref")
)


tie_lines = tie_lines.drop(["Temperature (K)", "Type Alcohol"])
coeffs = coeffs.drop(["MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?", "Type Alcohol"])
comps_MW = comps_MW.drop(["Type Alcohol"])
group_tie_lines = tie_lines.group_by(["Ref", "Sub Ref"])

result = comps_MW.filter(
    (pl.col("Ref") == 19) & (pl.col("Sub Ref") == "a")
)

result

for name, data in group_tie_lines:
    print(name[0])
    print(data.drop(["Ref", "Sub Ref"]))
    