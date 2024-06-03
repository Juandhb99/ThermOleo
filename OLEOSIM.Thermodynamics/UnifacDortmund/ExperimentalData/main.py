from experimental_data_preprocessing import ExperimentalValidation
from data_reconciliation import MassBalanceReconciliation
from pprint import pprint

def main():
    validated_data = ExperimentalValidation(path_to_data='data/raw_lle_data.xlsx', 
                                        component_list=['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        column_list_to_remove=['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol']).validate_data()
    
    MassBalanceReconciliation(validated_data, ['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'], 8).reconciliation()

    return validated_data

if __name__ == '__main__':
    pprint(main())
