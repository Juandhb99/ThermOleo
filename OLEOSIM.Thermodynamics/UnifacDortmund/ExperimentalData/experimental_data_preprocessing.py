import polars as pl
from dataclasses import dataclass, field

@dataclass
class ExperimentalValidation:
    
    """The ExperimentalValidation class is a data processing pipeline which is responsible for doing 
       the experimental validation of the mass balances for LLE ternary equilibriums using the PHI phase distribution coefficient. To do this the component must respect the following restrictions
       
       The sum of all component mass fractions in the light phase = 1
       
       The sum of all component mass fractions in the heavy phase = 1
       
       The experimental phase distribution known as phi 
       
    
    

    Returns:
        _type_: _description_
    """    
  
    path_to_data: str  
    component_list: list[str]
    column_list_to_remove: list[str]

    num_components: int = field(default=None)
    phi_names: list[str] = field(default=None) 
    

    def _preprocess_data(self):
        
        raw_data = (pl.read_excel(self.path_to_data, engine='calamine')
                             .drop(self.column_list_to_remove)).with_row_index()

        
        self.num_components = len(self.component_list) 
        self.phi_names = ['phi_' + name for name in self.component_list]
        
        raw_data = raw_data.with_columns( 
        
            [pl.when(pl.nth(i)==0.0)
            .then(1e-20)
            .otherwise(pl.nth(i))
            .alias(raw_data.columns[i])
            for i in range(self.num_components+1, self.num_components*2+1)]
            
        )
        
        return raw_data
    
    def _calculate_experimental_phi(self, raw_data): 
              
        experimental_phi = raw_data.select(
            
            [((pl.nth(i) - pl.nth(i+self.num_components*2))/(pl.nth(i+self.num_components) - pl.nth(i+self.num_components*2)))
            .alias(f'phi_{self.component_list[i-1]}') 
            for i in range(1, self.num_components + 1)]
        ).with_row_index()
        
        return experimental_phi
    
    def _validate_experimental_phi(self, struct: dict) -> int:    
        
        filtered_data = {key:value for key, value in struct.items() if value != 0.0} 
     
        if any(value <= 0.001 or value >= 0.995 for value in filtered_data.values()):
            return 0 
        
        average_phi = sum(filtered_data.values())/len(filtered_data)
        
        if any(abs(value - average_phi) >= 0.1 for value in filtered_data.values()):
            return 0
            
        return 1
    
    def validate_data(self):
        
       raw_data = self._preprocess_data() 
       experimental_phi = self._calculate_experimental_phi(raw_data)  
       experimental_phi = experimental_phi.with_columns(
                       pl.struct(self.phi_names)
                       .map_elements(self._validate_experimental_phi)
                       .alias('Validated')
        )
      
       validated_data = raw_data.join(experimental_phi, on='index') 
       return validated_data
        
        
            
        

validated_data = ExperimentalValidation('raw_lle_data.xlsx', 
                                        ['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        ['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol',  'Tie lines']).validate_data()

validated_data
validated_data.filter(pl.col('Validated')==1)


