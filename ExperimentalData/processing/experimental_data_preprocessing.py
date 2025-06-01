import polars as pl
import numpy as np
from dataclasses import dataclass, field

@dataclass
class ExperimentalValidation:
    
    """
       Data processing pipeline which is responsible for doing the experimental validation of the tie lines in the experimental LLE ternary equilibriums using the phi (mass phase fraction of the light phase) and mass balance restrictions. 
       
       The phi distribution coefficient is calculated with the following formulas:
 
       phi = (wi_overall - wi_heavy)/(wi_light - wi_heavy) (i is the subscript of each component in th mixture)
       
       Once the  is calculated it must satisfy the following mass balance restriction:
       
       1. 0 < phi < 1
       
       2. phi_1 = phi_2 = phi_3 = phi_i
       
       If the phi doesn't satisfy both  restrictions the respective tie line is discarded.
       
       Attributes:

            path_to_data (str): Directory path to experimental data. The class at the moment only reads excel files. The data must be organized such that the overall compositions are followed by the light phase compositions and then the heavy phase compositions.
            component_list (list[str]): List with the name of the components in the data
            column_list_to_remove (list[str]): List of columns to remove. For processing the data all the columns that don't contain experimental data must remove and their names must be in this list.
            error_threshold (float): Error threshold for data validation. If the error of the experimenal phi with respect to the average phi is higher than the error_threshold the tie line will be removed. This can take a value between 1 or 0.
            
            num_components (int) = None: Number of components according to the list of components attribute
            phi_names (list[str]) = None: List of names for the PHI mass phase fraction columns to generate
    """    
  
    path_to_data: str  
    component_list: list[str]
    column_list_to_remove: list[str]
    error_threshold: float

    num_components: int = field(default=None)
    phi_names: list[str] = field(default=None) 
    

    def _load_data(self) -> pl.DataFrame:
        """Load data from excel file and instantiate class attributes

        Returns:
            pl.DataFrame: Raw experimental data.
        """        
        raw_data = (pl.read_excel(self.path_to_data, engine="calamine")).with_row_index()
        additional_columns = raw_data.select(self.column_list_to_remove).with_row_index() 
        raw_data = raw_data.drop(self.column_list_to_remove)

        
        self.num_components = len(self.component_list) 
        self.phi_names = ["phi_" + name for name in self.component_list]

        return raw_data, additional_columns
    
    def _swap_values(self, raw_data: pl.DataFrame) -> pl.DataFrame:
        """Reorganize the data to have in the heavy phase the biggest composition of oil in each tie line.

        Args:
            raw_data (pl.DataFrame): Experimental data

        Returns:
            pl.DataFrame: Experimental data with the organized phases. 
        """      
       
        condition_oil = pl.col("OIL_L") > pl.col("OIL_H")
        condition_glycerol = pl.col("GLYCEROL_L") > pl.col("GLYCEROL_H")
        condition_water = pl.col("WATER_L") > pl.col("WATER_H")

        # Swap values between columns ending with _L and _H based on oil condition
        raw_data = raw_data.with_columns([
            pl.when(condition_oil).then(pl.col(f"{col}_H")).otherwise(pl.col(f"{col}_L")).alias(f"{col}_L") for col in self.component_list
        ] + [
            pl.when(condition_oil).then(pl.col(f"{col}_L")).otherwise(pl.col(f"{col}_H")).alias(f"{col}_H") for col in self.component_list
        ]) 

        # Swap values between columns ending with _L and _H based on glycerol condition
        raw_data = raw_data.with_columns([
            pl.when(condition_glycerol).then(pl.col(f"{col}_H")).otherwise(pl.col(f"{col}_L")).alias(f"{col}_L") for col in self.component_list
        ] + [
            pl.when(condition_glycerol).then(pl.col(f"{col}_L")).otherwise(pl.col(f"{col}_H")).alias(f"{col}_H") for col in self.component_list
        ])
        
        raw_data = raw_data.with_columns([
            pl.when(condition_water).then(pl.col(f"{col}_H")).otherwise(pl.col(f"{col}_L")).alias(f"{col}_L") for col in self.component_list
        ] + [
            pl.when(condition_water).then(pl.col(f"{col}_L")).otherwise(pl.col(f"{col}_H")).alias(f"{col}_H") for col in self.component_list
        ])
        
        
        return raw_data  
        
    def _preprocess_data(self, raw_data: pl.DataFrame) -> pl.DataFrame:
        """Load the dataframe from the path given, and remove possible calculations indeterminations by changing the 0 fraction of the light phase compositions to 1e-20
        also instanciate the num_components and phi_names attributes. 

        Returns:
            pl.DataFrame: Loaded dataa in a dataframe with the adjusments to avoid indeterminations.
        """        
  
        raw_data = raw_data.with_columns( 
        
            [pl.when(pl.nth(i)==0.0)
            .then(1e-20)
            .otherwise(pl.nth(i))
            .alias(raw_data.columns[i])
            for i in range(self.num_components+1, self.num_components*2+1)]   # The parameters in the range function consider the columns with compositions of the light phase  
            
        ) 
            
        return raw_data
    
    
    def _calculate_experimental_phi(self, raw_data: pl.DataFrame) -> pl.DataFrame: 
        """Calculates the experimental phi value for the light phase according to the mass balance formula for each component in the data

        Args:
            raw_data (pl.DataFrame): data adjusted to avoid indeterminations

        Returns:
            pl.DataFrame: Experimentally calculated phi
        """              
        experimental_phi = raw_data.select(
            
            [((pl.nth(i) - pl.nth(i+self.num_components*2))/(pl.nth(i+self.num_components) - pl.nth(i+self.num_components*2)))
            .alias(f"phi_{self.component_list[i-1]}") 
            for i in range(1, self.num_components + 1)]
        ).with_row_index()
        
        return experimental_phi
    
    def _validate_experimental_phi(self, struct: dict) -> int:    
        """Check that the experimental phi satisfy the mass balance restrictions. If one phi for a tie line doesn't satisfies both restrictions it will return a 0, otherwise if its satisfies both restrictions will return a 1.
           The conditions are the following: The phi value must be between 0.001 and 0.995 to consider the tie line as suitable. The absolute error between each phi and the average phi of the experimental tie line must not be higher than 0.2.

        Args:
            struct (dict): Columns where the experimental phi are saved

        Returns:
            int: Either 0 if the tie line doesn't satisfies both restrictions or 1 if it does.
        """            
        filtered_data = {key:value for key, value in struct.items() if value != 0.0} 
     
        if any(value <= 0.001 or value >= 0.995 for value in filtered_data.values()):
            return 0 
        
        average_phi = sum(filtered_data.values())/len(filtered_data)
        
        if any(abs(value - average_phi)/average_phi >= self.error_threshold or np.isnan(average_phi) for value in filtered_data.values()):
            return 0
            
        return 1
    
    def calculate_phi(self) -> pl.DataFrame:
        """Calculate the experimental phi and return the raw data dataframe with the experimental phi calculated, it only returns the dataframe with these new columns
           with no additional processing done to the data.

        Returns:
            pl.DataFrame: Raw_data with added columns that have the calculated experimental phi.
        """        
        raw_data, additional_columns = self._load_data() 
        raw_data = self._preprocess_data(raw_data=raw_data) 
        experimental_phi = self._calculate_experimental_phi(raw_data=raw_data) 
        phi_data = raw_data.join(experimental_phi, on="index")  
        return additional_columns.join(phi_data, on="index")
    
    def validate_data(self) -> pl.DataFrame:
        """Run all the preprocessing and output a combined dataframe with the experimental data, experimental phi and where only the validated tie lines remain. 
        The validation of the tie lines is done via a row wise application of the _validate_experimental_phi() function, where the pl.struct is used for better performance.

        Returns:
            pl.DataFrame: Join dataframe with the experimental data, the experimental phi and the indication of validated data 
        """        
        raw_data, additional_columns = self._load_data() 
        raw_data = self._swap_values(raw_data)
        raw_data = self._preprocess_data(raw_data) 
        experimental_phi = self._calculate_experimental_phi(raw_data=raw_data)  
        experimental_phi = experimental_phi.with_columns(
                        pl.struct(self.phi_names)
                        .map_elements(self._validate_experimental_phi, return_dtype=int)
                        .alias("Validated")
                     
            ).filter(pl.col("Validated")==1)
       
        
        validated_data = raw_data.join(experimental_phi, on="index") 
        validated_data = additional_columns.join(validated_data, on="index")
        validated_data = validated_data.drop("Validated")
         
        return validated_data, self.phi_names
        
        
            
        



