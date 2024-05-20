import polars as pl
import numpy as np

raw_data = (pl.read_excel('raw_lle_data.xlsx', engine='calamine')
                             .drop(['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol',  'Tie lines'])).with_row_index()


list_components = ['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER']
phi_names = ['phi_' + name for name in list_components]
num_components = len(list_components)

# Make the light phase compositions that are 0 a very small number to avoid division by 0
raw_data = raw_data.with_columns( 
   
    [pl.when(pl.nth(i)==0.0)
    .then(1e-20)
    .otherwise(pl.nth(i))
    .alias(raw_data.columns[i])
    for i in range(num_components+1, num_components*2+1)]
    
)

# Calculate the experimental phi
experimental_phi = raw_data.select(
    
    [((pl.nth(i) - pl.nth(i+num_components*2))/(pl.nth(i+num_components) - pl.nth(i+num_components*2)))
    .alias(f'phi_{list_components[i-1]}') 
    for i in range(1, num_components + 1)]
).with_row_index()

experimental_phi


def validated_phi(struct: dict):
    
       
    filtered_data = {key:value for key, value in struct.items() if value != 0.0 and value != None} 
      
    for key in filtered_data.keys():
        
        print(filtered_data[key])  
        if filtered_data[key] <= 0.001 or filtered_data[key] >= 0.995:     
            return 0
        
    average_phi = sum(filtered_data.values())/len(filtered_data) 
    
    for key in filtered_data.keys(): 
        
        deviation = abs(filtered_data[key] - average_phi)
        
        if deviation >= 0.1:
            
            return 0
        
    return 1
        
            
            
             
        
    

test = experimental_phi.with_columns(
                       pl.struct(phi_names)
                       .map_elements(validated_phi)
                       .alias('test')
)


test.filter(pl.col('test') == 1)

test_dict = {'item1':1, 'item2':2, 'item3':0.0}

filtered_data = {key:value for key, value in test_dict.items() if value != 0.0}

filtered_data
test_dict['item1']

sum(test_dict.values())

len(test_dict)

for keys in test_dict.keys():
    print(keys)

raw_data.select(raw_data.columns[2]) # Analizar manejarlo por indices en vez de nombres de columnas para generalizarlo, ir filtrando paso a paso por cada una de las condiciones. 