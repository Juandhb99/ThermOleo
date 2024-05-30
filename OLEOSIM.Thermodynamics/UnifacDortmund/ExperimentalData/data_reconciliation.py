import polars as pl
import numpy as np
from experimental_data_preprocessing import ExperimentalValidation
from scipy.optimize import minimize

raw_data =  raw_data = (pl.read_excel('data/raw_lle_data.xlsx', engine='calamine')).with_row_index()


validated_data = ExperimentalValidation(path_to_data='data/raw_lle_data.xlsx', 
                                        component_list=['FAME/FAEE', 'GLYCEROL', 'ALCOHOL', 'OIL', 'DAG', 'MAG', 'ACID', 'WATER'], 
                                        column_list_to_remove=['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol']).validate_data()


grouped = validated_data.group_by(['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'], maintain_order=True)

final_reconcile_data = []
for _, data in grouped:
    reference_columns = data.select(['index','Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'])
    test_df = data.drop(['index','Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol'])
    columns_names = test_df.columns
    columns_names.append('Reconcile phi')
    test_np = test_df.to_numpy()


    total_components = 8
    start_idx_overall_phase = 0
    start_idx_light_phase = total_components
    start_idx_heavy_phase = total_components*2
    start_idx_phi_exp = total_components*3


    test_np = np.ma.array(test_np, mask=((test_np == 0.0) | (test_np == 1e-20)))
    rows = test_np.shape[0]

    #extract the experimental phi compositions
    test_np_row = np.mean(test_np[:, start_idx_phi_exp:start_idx_phi_exp+total_components], axis = 1).reshape(rows,1)
    initial_guess = np.ma.concatenate([test_np[:, start_idx_heavy_phase:start_idx_heavy_phase+total_components], test_np_row], axis = 1)
    initial_guess_form = initial_guess.shape 
    initial_guess_idx = np.where(~initial_guess.mask)
    constants = test_np[:,start_idx_overall_phase:start_idx_phi_exp].compressed() 
    constants_shape = constants.shape
    constants = constants.reshape(rows, int(constants_shape[0]/rows))
    initial_guess_compressed = initial_guess.compressed()
    final_shape = initial_guess_compressed.shape[0]

    columns = int(final_shape/rows)
    end_idx = total_components if columns-1 == total_components else columns-1


    def reconciliation(x, const, rows, columns, end_idx):
    # x  = matriz de valores iniciales para la fase pesada y el fi 
    # const = matriz con los valores fijos de las composiciones en las tres fases
    # rows = cantidad de filas (muestras) del experimento a reconciliar
    # final_shape = longitud de la matriz x cuando se alimenta como comprimido para remover las máscaras, al dividir esta longitud por el número de rows, se vuelve al tamaño de la matriz original
    # end_idx = Cantidad de componentes, si al comprimir y remover las mascaras de la matriz x se calcula el numero de componentes nuevamente al dividar la longitud del vector comprimido por el número de filas, si este valor es igual al total de componentes el end_idx = total components si no, toma el valor calculado.     
        x = x.reshape(rows, columns) # calcular la segunda dimension por fuera e ingresarla como argumento
        
        light_phase_composition_reconcile = ((const[:, 0:end_idx] - x[:, 0:end_idx]*(1-x[:,-1].reshape(rows, 1)))/x[:,-1].reshape(rows,1))
        return np.sum((const[:, end_idx*2:end_idx*3] - x[:, 0:end_idx])**2 + (const[:, end_idx:end_idx*2]- light_phase_composition_reconcile)**2)

    #arreglar indicies para que tenga en cuenta los compressed.

    res = minimize(reconciliation, initial_guess_compressed, method='nelder-mead', args = (constants, rows, columns, end_idx))

    results = res.x
    initial_guess[initial_guess_idx[0], initial_guess_idx[1]] = results
    reconcile_data = np.hstack([test_np[:,0:start_idx_heavy_phase], initial_guess[:,:-1], test_np[:, start_idx_phi_exp:start_idx_phi_exp+total_components], initial_guess[:,-1].reshape(rows, 1)])
    reconcile_data[:, start_idx_light_phase:start_idx_light_phase+total_components] = (reconcile_data[:, 0:start_idx_light_phase] - reconcile_data[:, start_idx_heavy_phase:start_idx_heavy_phase+total_components]*(1-reconcile_data[:,-1].reshape(reconcile_data.shape[0],1)))/reconcile_data[:,-1].reshape(reconcile_data.shape[0],1)
    reconcile_data_df = pl.from_numpy(reconcile_data, columns_names)
    final_df = pl.concat([reference_columns, reconcile_data_df], how = 'horizontal')

    final_reconcile_data.append(final_df)


final_total_data = pl.concat(final_reconcile_data)
final_total_data