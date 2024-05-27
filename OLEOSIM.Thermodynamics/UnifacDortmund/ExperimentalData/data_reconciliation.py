import polars as pl
import numpy as np
from experimental_data_preprocessing import ExperimentalValidation
from scipy.optimize import minimize

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

test_df = data_list[0].drop(['index','Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol', 'Validated'])

test_np = test_df.to_numpy()

total_components = 8
start_idx_overall_phase = 0
start_idx_light_phase = total_components
start_idx_heavy_phase = total_components*2
start_idx_phi_exp = total_components*3


test_np = np.ma.array(test_np, mask=((test_np == 0.0) | (test_np == 1e-20)))
rows = test_np.shape[0]
#extract the experimental phi compositions
test_np_row = np.mean(test_np[:, start_idx_phi_exp:start_idx_phi_exp+total_components], axis = 1).reshape(3,1)
initial_guess = np.ma.concatenate([test_np[:, start_idx_light_phase:start_idx_light_phase+total_components], test_np_row], axis = 1)
constants = test_np[:,start_idx_overall_phase:start_idx_phi_exp].compressed()
constants_shape = constants.shape
constants = constants.reshape(rows, int(constants_shape[0]/rows))
initial_guess
initial_guess = initial_guess.compressed()
final_shape = initial_guess.shape[0]

end_idx_guess = int(final_shape/rows)-1
end_idx = total_components if end_idx_guess == total_components else end_idx_guess

def reconciliation(x, const, rows, final_shape, end_idx):
   # x  = matriz de valores iniciales para la fase pesada y el fi 
   # const = matriz con los valores fijos de las composiciones en las tres fases
   # rows = cantidad de filas (muestras) del experimento a reconciliar
   # final_shape = longitus de la matriz x cuando se alimenta como comprimido para remover las máscaras, al dividir esta longitud por el número de rows, se vuelve al tamaño de la matriz original
   # end_idx = Cantidad de componentes, si al comprimir y remover las mascaras de la matriz x se calcula el numero de componentes nuevamente al dividar la longitud del vector comprimido por el número de filas, si este valor es igual al total de componentes el end_idx = total components si no, toma el valor calculado.     
    x = x.reshape(rows, int(final_shape/rows)) # calcular la segunda dimension por fuera e ingresarla como argumento
    light_phase_composition_reconcile = ((const[:, 0:end_idx] - x[:, 0:end_idx]*(1-x[:,-1].reshape(rows, 1)))/x[:,-1].reshape(rows,1))
    return np.sum((const[:, end_idx*2:end_idx*3] - x[:, 0:end_idx])**2 + (const[:, end_idx:end_idx*2]- light_phase_composition_reconcile)**2)

#arreglar indicies para que tenga en cuenta los compressed.

res = minimize(reconciliation, initial_guess, method='nelder-mead', args = (constants, rows, final_shape, end_idx))

results = res.x.reshape(3,4)
new_phi_average = results[:,-1].reshape(3,1)

new_test = np.hstack([test_np, new_phi_average])
new_test[:, 8:11] = results[:,0:3]

new_test