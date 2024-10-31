import polars as pl
from experimental_data_preprocessing import ExperimentalValidation
from data_reconciliation import MassBalanceReconciliation
from pprint import pprint

def main():
    validated_data, phi_names = ExperimentalValidation(path_to_data=r"C:\Juan\Maestría\Code\oleosim\ExperimentalData\data\raw_lle_data.xlsx", 
                                        component_list=['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        column_list_to_remove=['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'],
                                        error_threshold=0.20).validate_data()
    
    MassBalanceReconciliation(validated_data, ['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'], 8, phi_names).reconciliation()

    return validated_data

if __name__ == '__main__':
    main()
