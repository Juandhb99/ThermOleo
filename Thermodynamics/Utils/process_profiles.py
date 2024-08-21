import dataclasses
import polars as pl
import numpy as np
from acid_properties import acid_reference, acid_properties


FA_profiles = (pl.read_excel(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\Thermodynamics\UnifacDortmund\Experimental_Data\data\acid_profile.xlsx", engine="calamine"))
FA_profiles.describe()
acid_names = list(acid_reference.keys())
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



def extract_properties(acid_properties):
   
   PM_values = []
   m_values = []
   n_values = []
   p_values = []
   
   for properties in acid_properties:

      PM_coeff = properties[0]
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
   
   return PM_values, m_values, n_values, p_values
   
PM_values, m_values, n_values, p_values = extract_properties(acid_properties.values())

def calculate_m_coefficients(struct: dict, m_values, n_values, p_values):
   
   molar_frac = np.array(list(struct.values()))
   m =  np.dot(molar_frac, m_values)
   n =  np.dot(molar_frac, n_values)
   p =  np.dot(molar_frac, p_values) 
   
   return m, n, p

experiment_profiles.describe()      
m_values
   
experiment_profiles = experiment_profiles.with_columns(
   
   pl.struct(mol_comp_names)
   .map_elements(lambda x:  dict(zip(("m", "n", "p"), calculate_m_coefficients(x, m_values, n_values, p_values))))
   .alias("result")
).unnest("result")

