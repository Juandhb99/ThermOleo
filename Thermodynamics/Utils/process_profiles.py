import dataclasses
import polars as pl
import numpy as np
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

def extract_properties(properties):
   
   PM_values = []
   m_values = []
   n_values = []
   p_values = []
   
   for properties in acid_properties:

      PM_coeff = [0]
      m_coeff = properties[1] 
      n_coeff = properties[2] 
      p_coeff = properties[3] 

      PM_values.append(PM_coeff)
      m_values.append(m_coeff)
      n_values.append(n_coeff)
      p_values.append(p_coeff)
   
   PM_values = np.array(PM_values)
   m_values = np.array(m_values)
   n_values = np.array(n_values)
   p_values = np.array(p_values)
   
  
   
   
def calculate_coefficients(struct):
   
   values = np.array(list(struct.values()))

      
      
   return 0
   
     
test = experiment_profiles.with_columns(pl.struct(pl.all()))

test[0]
test_np = np.array(list(acid_reference.keys()))
test_np[0]