from dataclasses import dataclass, field
import polars as pl
import numpy as np
from acid_properties import acid_reference, acid_properties

@dataclass
class AcidProfileCoeff:
   """
      Acid profile calculation process, it takes the acid_properties database, with the information about the number of CH2 (m), C=C (n) and OH (p) groups
      in each of the fatty acids, and creates a new excel file with the coefficients for each of the experimental profiles found in the database.py file 
      in the Experimental_Data folder of UNIFAC Dortmund. This class calculates the coefficients of the characteristic molecule for use in the LLE modelling.
      To execute this process it is needed to create the object and run the calculate_profile_coeffs methods. 
      
      Attributes:
         path_to_data (str): Path to the experimental data of the fatty acid profiles.
         save_path (str): Path to save the new excel file with the calculated coefficients. 
         acid_names (list[str]): list of the fatty acids, determined from the database. 
         mol_comp_names (list[str]): List of the names of fatty acids with the prefix mol_.
         References (list[str]): List of the column names that are references in the experimental database. 
   """    
   path_to_data: str 
   save_path: str
   _acid_names: list[str] = field(default=None)
   _mol_comp_names: list[str] = field(default=None)
   _references: list[str] = field(default=None)

   def _load_data(self) -> pl.DataFrame:
      """Load the data from the defined path.

      Returns:
          pl.DataFrame: Dataframe for processing
      """            
      
      FA_profiles = (pl.read_excel(self.path_to_data, engine="calamine"))
      self.references = FA_profiles.select(["Ref", "Sub Ref", "MAG/DAG Profile?", "Additional FAME Profile?", "Acid mix Profile?"])
      self.acid_names = list(acid_reference.keys())
      self.mol_comp_names = ["moles_" + name for name in self.acid_names]

      experiment_profiles = FA_profiles.select(self.acid_names)
      
      return experiment_profiles

   def _calculate_molar_comps(self, experiment_profiles: pl.DataFrame) -> pl.DataFrame:
      """Convert the mass compositions to molar compositions, using as a calculation base of 1.

      Args:
          experiment_profiles (pl.DataFrame): Loaded dataframe with the data.

      Returns:
          pl.DataFrame: Dataframe with molar compositions.
      """      
      experiment_profiles = experiment_profiles.with_columns(
         
         (pl.col(name)/acid_properties[i][0]).alias(f"moles_{name}") for i, name in enumerate(self.acid_names) 
      )

      experiment_profiles = experiment_profiles.drop(self.acid_names)
      experiment_profiles = experiment_profiles.with_columns(pl.sum_horizontal(pl.all()).alias("Total"))

      experiment_profiles = experiment_profiles.with_columns(
         
         (pl.col(self.mol_comp_names)/pl.col("Total"))
         
         ).with_row_index() 

      return experiment_profiles


   def _extract_characteristics(self, acid_properties: dict) -> tuple[np.ndarray]:
      """Extract the characteristics of the fatty acids from the database.

      Args:
          acid_properties (dict): Fatty acid properties.

      Returns:
          tuple[np.ndarray]: Tuple of np arrays that contain each of the characteristics from the fatty acids.
      """       
      acid_properties_values = acid_properties.values()  
      PM_values = []
      m_values = []
      n_values = []
      p_values = []
      
      for properties in acid_properties_values:

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
      
      return (PM_values, m_values, n_values, p_values)
   

   def _coefficient_calculation(self, struct: dict, m_values: np.ndarray, n_values: np.ndarray, p_values: np.ndarray)-> tuple[np.ndarray]:
      """Calculate the m, n and p coefficients for the characteristic molecule.

      Args:
          struct (dict): Fatty acid profile for each experimental reference.
          m_values (np.ndarray): CH2 quantity for the fatty acid.
          n_values (np.ndarray): CH=CH quantity for the fatty acid.
          p_values (np.ndarray): OH quantity for the fatty acid.

      Returns:
          tuple[np.ndarray]: Tuple of np arrays with the coefficients.
      """      
      molar_frac = np.array(list(struct.values()))
      m =  np.dot(molar_frac, m_values)
      n =  np.dot(molar_frac, n_values)
      p =  np.dot(molar_frac, p_values) 
      
      return m, n, p


   def calculate_profile_coeffs(self) -> None:
      """Calculate the average coefficients for each experiment from the fatty acid profile composition and generate new excel with the information.
      """       
      experiment_profiles = self._load_data()
      experiment_profiles = self._calculate_molar_comps(experiment_profiles)      
      PM_values, m_values, n_values, p_values = self._extract_characteristics(acid_properties)
      
      experiment_profiles = experiment_profiles.with_columns(
         
         pl.struct(self.mol_comp_names)
         .map_elements(lambda x:  dict(zip(("m", "n", "p"), self._coefficient_calculation(x, m_values, n_values, p_values))))
         .alias("result")
      ).unnest("result")
      
      coefficients = experiment_profiles.select(["m", "n", "p"]) 
      coefficients = pl.concat([self.references, coefficients], how="horizontal")
      coefficients.write_excel(self.save_path + "\profile_coeffs.xlsx")            

@dataclass
class CalculateMW:
   """
      Calculate the molecular weights of the 8 components considered in the equilibrium. For the Oil, DAG, MAG, FA and FAME/FAEE, the 
      molecular weight is calculated using the pseudo molecule and the m, n, p and b parameters. The b parameters where manually defined in the 
      database by correlating the reference to the experimental tie line database. To use this class, create the object and run the calculate_MW method
      after calculating the MW, the additional columns are removed manually after associating for each reference the correct compositions, when different,
      FA profiles are used.
      
      Attributes:
         path_to_data (str): Path to the experimental data of the fatty acid profiles.
         save_path (str): Path to save the new excel file with the calculated coefficients.  
   """ 
   path: str 
   save_path: str

   def calculate_MW(self) -> None:   
      """Calculate the MW for each component.
      """      
      coeff_data = (pl.read_excel(self.path, engine="calamine"))
      coeff_data = coeff_data.with_columns(
         (15*2 + 14*pl.col("m") + 26*pl.col("n") + 30*pl.col("p") + 58 + 14*pl.col("b")).alias("MW_FAME/FAEE"),
         pl.lit(92.09).alias("MW_Glycerol"),
         pl.when(pl.col("b") == 0).then(32.04).when(pl.col("b") == 1).then(46.07).when(pl.col("b") == 2).then(60.09).otherwise(None).alias("MW_Alcohol"),
         (15*3 + 14*(3*pl.col("m")+2) + 26*3*pl.col("n") + 13*(3*pl.col("p")+1) + 17*3*pl.col("p") + 58*3).alias("MW_Oil"),
         (15*2 + 14*(2*pl.col("m")+2) + 26*2*pl.col("n") + 13*(2*pl.col("p")+1) + 17*2*pl.col("p") + 58*2).alias("MW_DAG"),
         (15 + 14*(pl.col("m")+2) + 26*pl.col("n") + 13*(pl.col("p")+1) + 17*pl.col("p") + 58).alias("MW_MAG"),
         (15 + 14*pl.col("m") + 26*pl.col("n") + 30*pl.col("p") + 45).alias("MW_FA"),
         pl.lit(18).alias("MW_H2O") 
      )
      
      comp_MW = coeff_data.drop(["m", "n", "p", "b"])      
      comp_MW.write_excel(self.save_path + "\comps_MW.xlsx")
      

comps_mw = CalculateMW(r"C:\Juan\Maestría\Code\oleosim\UnifacDortmund\Experimental_Data\data\profile_coeffs.xlsx", 
                       r"C:\Juan\Maestría\Code\oleosim\UnifacDortmund\Experimental_Data\data")

comps_mw.calculate_MW()