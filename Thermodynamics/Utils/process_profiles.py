import dataclasses
import polars as pl
from acid_properties import acid_reference, acid_properties


FA_profiles = (pl.read_excel(r"C:\Juan\Maestría\Code\oleosim\Thermodynamics\UnifacDortmund\Experimental_Data\data\acid_profile.xlsx", engine="calamine"))
acid_names = list(acid_reference.values())
mol_comp_names = ["moles_" + name for name in acid_names]
experiment_profiles = FA_profiles.select(acid_names)

experiment_profiles = experiment_profiles.with_columns(
    
   (pl.col(name)/acid_properties[i][0]).alias(f"moles_{name}") for i, name in enumerate(acid_names) # a base of 1 is used.
)

experiment_profiles = experiment_profiles.drop(acid_names)
experiment_profiles = experiment_profiles.with_columns(pl.sum_horizontal(pl.all()).alias("Total"))
experiment_profiles = experiment_profiles.with_columns(
   
   (pl.col(mol_comp_names)/pl.col("Total"))
   
   ).with_row_index() 


def calculate_coefficients(struct):
   
   for key, value in struct.items():
      
      return 0
   
     
test = experiment_profiles.with_columns(pl.struct(pl.all()))

test[0]
acid_properties.items()