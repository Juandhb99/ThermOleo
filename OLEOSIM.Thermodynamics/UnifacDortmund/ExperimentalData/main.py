from experimental_data_preprocessing import ExperimentalValidation
from pprint import pprint
def main():
    validated_data = ExperimentalValidation(path_to_data='data/raw_lle_data.xlsx', 
                                        component_list=['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        column_list_to_remove=['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol',  'Tie lines']).validate_data()

    return validated_data

if __name__ == '__main__':
    pprint(main())
