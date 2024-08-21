from dataclasses import dataclass, field
import polars as pl
import numpy as np
from acid_properties import acid_reference, acid_properties

@dataclass
class AcidProfileCoeff:
    
   path_to_data: str 
   save_path: str
   acid_names: list[str] = field(default=None)
   mol_comp_names: list[str] = field(default=None)
   references: list[str] = field(default=None)

   def load_data(self):
      
      FA_profiles = (pl.read_excel(self.path_to_data, engine="calamine"))
      self.references = FA_profiles.select(["Ref", "Sub Ref", "MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?"])
      self.acid_names = list(acid_reference.keys())
      self.mol_comp_names = ["moles_" + name for name in self.acid_names]

      experiment_profiles = FA_profiles.select(self.acid_names)
      
      return experiment_profiles

   def process_FA_profiles(self, experiment_profiles):
      
      experiment_profiles = experiment_profiles.with_columns(
         
         (pl.col(name)/acid_properties[i][0]).alias(f"moles_{name}") for i, name in enumerate(self.acid_names) # a base of 1 is used.
      )

      experiment_profiles = experiment_profiles.drop(self.acid_names)
      experiment_profiles = experiment_profiles.with_columns(pl.sum_horizontal(pl.all()).alias("Total"))

      experiment_profiles = experiment_profiles.with_columns(
         
         (pl.col(self.mol_comp_names)/pl.col("Total"))
         
         ).with_row_index() 

      return experiment_profiles


   def extract_properties(self, acid_properties):
         
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
   

   def coefficient_calculation(self, struct: dict, m_values, n_values, p_values):
      
      molar_frac = np.array(list(struct.values()))
      m =  np.dot(molar_frac, m_values)
      n =  np.dot(molar_frac, n_values)
      p =  np.dot(molar_frac, p_values) 
      
      return m, n, p


   def calculate_profile_coeffs(self):
       
      experiment_profiles = self.load_data()
      experiment_profiles = self.process_FA_profiles(experiment_profiles)      
      PM_values, m_values, n_values, p_values = self.extract_properties(acid_properties.values())
      
      experiment_profiles = experiment_profiles.with_columns(
         
         pl.struct(self.mol_comp_names)
         .map_elements(lambda x:  dict(zip(("m", "n", "p"), self.coefficient_calculation(x, m_values, n_values, p_values))))
         .alias("result")
      ).unnest("result")
      
      coefficients = experiment_profiles.select(["m", "n", "p"])
      coefficients = pl.concat([self.references, coefficients], how="horizontal")
      coefficients.write_excel(self.save_path + "\profile_coeffs.xlsx")            


profile_coeffs = AcidProfileCoeff(r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\Thermodynamics\UnifacDortmund\Experimental_Data\data\acid_profile.xlsx",
                                  r"D:\Juan\proyectos_personales\Maestría\Materias\Tesis\oleosim\Thermodynamics\UnifacDortmund\Experimental_Data\data")

profile_coeffs.calculate_profile_coeffs()