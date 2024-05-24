import polars as pl
import numpy as np
from experimental_data_preprocessing import ExperimentalValidation


raw_data =  raw_data = (pl.read_excel('data/raw_lle_data.xlsx', engine='calamine')).with_row_index()


validated_data = ExperimentalValidation(path_to_data='data/raw_lle_data.xlsx', 
                                        component_list=['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        column_list_to_remove=['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol']).validate_data()


grouped = validated_data.group_by(['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'], maintain_order=True)

name_list = []
data_list = []
for name, data in grouped:
    name_list.append(name)
    data_list.append(data)

test_df = data_list[0].drop(['index','Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'])

test_np = test_df.to_numpy()


test_df
test_np[0][0] = 0.45

test_np
