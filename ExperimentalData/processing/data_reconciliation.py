import polars as pl
import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass, field


@dataclass
class MassBalanceReconciliation:
    """
        The mass balance reconciliation has the purpose to reconcile the mass compositions in each phase by fixing the overall composition and changing the phi, the heavy phase composition and recalculating
        the light phase composition. This process is done via a minimization of the squared differences of the experimental light and heavy phase compositions with the reconciled compositions. To produce results with
        physical meaning two constrains are applied. The first one assures that the calculated light phase composition is always greater than zero. And that the changing values of the heavy phase composition and the
        phi are greater than 0 and lesser than 1. 
        
        To apply the mass balance reconciliation the data must be referenced in order to group and to process by batches. Each batch must have the same number of dimensions because all the processing is done using
        matrices.
        
        Attributes:
            validated_data (pl.DataFrame): Dataframe of the previously validated data that must have the calculated phi values for each component. 
            reference_to_group (list[str]): List of the columns that will be used to group the experimental data and do the reconciliation.
            component_number: (int): Number of components in the experimental data.

    """    
    
    validated_data: pl.DataFrame
    reference_to_group: list[str]
    component_number: int
    phi_names: list[str] = field(default=None)


    def _minimization(self, min_variables: np.ndarray, min_fixed: np.ndarray, n_rows: int, n_columns: int, n_components: int) -> np.ndarray:
        """Minimization of the squared difference between the heavy and light phase experimental composition and the heavy and light phase reconciled composition
           to correct mass balance errors.

        Args:
            min_variables (np.ndarray): Variables to change to do the minimization, this are the heavy phase composition and the average phi.
            min_fixed (np.ndarray): Fixed variables, specifically the overrall or feed composition of the mixture.
            n_rows (int): Number of rows of the batch of experimental data.
            n_columns (int): Number of columns of the  batch of experimental data. 
            n_components (int): Number of components in the batch of experimental data. If the batch of experimental data has the same number of components
            than the self.component_number this variable will be equal to that attribute, if not it will correspond to the actual number of components in the experiment. 
            This difference may occur if the overrall database is generalized to several components in a vector form, where if the component doesn't exists it will take a value of zero.
            This zero valued components are not of interest when processing a batch of experimental data, therefore are discarded and this variable may have a different number.
         

        Returns:
            np.ndarray: Matrix of the squared differences between the light and heavy phase experimental compositions and the light and heavy phase reconciled compositions.
        """        

        min_variables = min_variables.reshape(n_rows, n_columns)         
        reconciled_light_composition = ((min_fixed[:, 0:n_components] - min_variables[:, 0:n_components]*(1-min_variables[:,-1].reshape(n_rows, 1)))/min_variables[:,-1].reshape(n_rows,1))
        return np.sum((min_fixed[:, n_components*2:n_components*3] - min_variables[:, 0:n_components])**2 + (min_fixed[:, n_components:n_components*2]-reconciled_light_composition)**2)
    
    def _reconciled_light_composition_constrain(self, min_variables: np.ndarray, min_fixed: np.ndarray, n_rows: int, n_columns: int, n_components: int) -> np.ndarray:
        """This constrain assures that the calculated light phase composition with the iterated heavy phase composition and phi is not less than zero. 

        Args:
            min_variables (np.ndarray): Variables to change to do the minimization, this are the heavy phase composition and the average phi.
            min_fixed (np.ndarray): Fixed variables, specifically the overrall or feed composition of the mixture.
            n_rows (int): Number of rows of the batch of experimental data.
            n_columns (int): Number of columns of the  batch of experimental data. 
            n_components (int): Number of components in the batch of experimental data. If the batch of experimental data has the same number of components
            than the self.component_number this variable will be equal to that attribute, if not it will correspond to the actual number of components in the experiment. 
            This difference may occur if the overrall database is generalized to several components in a vector form, where if the component doesn't exists it will take a value of zero.
            This zero valued components are not of interest when processing a batch of experimental data, therefore are discarded and this variable may have a different number.
         

        Returns:
            np.ndarray: Flatted matrix with the applied constrain
        """        
        min_variables = min_variables.reshape(n_rows, n_columns)         
        reconciled_light_composition = ((min_fixed[:, 0:n_components] - min_variables[:, 0:n_components]*(1-min_variables[:,-1].reshape(n_rows, 1)))/min_variables[:,-1].reshape(n_rows,1))
        lower_bound_constraint = reconciled_light_composition - 1e-5  
        upper_bound_constraint = 1 - reconciled_light_composition - 1e-5  
        return np.concatenate((lower_bound_constraint, upper_bound_constraint)).flatten()
    
    def _min_variables_constraints(self, min_variables: np.ndarray) -> np.ndarray:
        """This constrain assures that the iterated heavy phase composition and phi are not less than zero or greater than one.

        Args:
            min_variables (np.ndarray): Variables to change to do the minimization, this are the heavy phase composition and the average phi.

        Returns:
            np.ndarray: Matriz with the constrain applied to the min_variables.
        """        
        
        lower_bound_min_variables_constraint = min_variables - 1e-5  
        upper_bound_min_variables_constraint = 1 - min_variables - 1e-5  
        return np.concatenate((lower_bound_min_variables_constraint, upper_bound_min_variables_constraint))
    
    def reconciliation(self) -> None:
        """The reconciliation process is done by grouping the experimental data per batches of experiments in order to process them as matrices with the same dimensions.
           If the database contains experiments from different sources that have different components, for each batch the components that are not present will be masked to not affect the calculations.
           After processing, all the batches are concatenated, and transformed to a polars dataframe with the same columns as the original one, finally the data is saved in an excel file to the data folder as refined_lle_data.xslx
        """        

        reconcile_groups = []
        grouped = self.validated_data.group_by(self.reference_to_group, maintain_order=True)
        start_idx_overall_phase = 0
        start_idx_light_phase = self.component_number
        start_idx_heavy_phase = self.component_number*2
        start_idx_phi_exp = self.component_number*3
        end_idx_light_phase = start_idx_light_phase + self.component_number
        end_idx_heavy_phase = start_idx_heavy_phase + self.component_number
        end_idx_phi_exp = start_idx_phi_exp + self.component_number
        self.reference_to_group.append("index")
       
        for _, data in grouped: 
            reference_columns = data.select(self.reference_to_group)
            experiments_df = data.drop(self.reference_to_group)
            columns_names = experiments_df.columns
            columns_names.append("Reconcile phi")
            experiments_matrix = experiments_df.to_numpy()
            experiments_matrix = np.ma.array(experiments_matrix, mask=((experiments_matrix == 0.0) | (experiments_matrix == 1e-20)))
            n_rows = experiments_matrix.shape[0]

            mean_experimental_phi = np.mean(experiments_matrix[:, start_idx_phi_exp:end_idx_phi_exp], axis = 1).reshape(n_rows,1)
            min_variables = np.ma.concatenate([experiments_matrix[:, start_idx_heavy_phase:end_idx_heavy_phase], mean_experimental_phi], axis = 1)
            min_variables_idx = np.where(~min_variables.mask)
            min_fixed = experiments_matrix[:,start_idx_overall_phase:start_idx_phi_exp].compressed() 
            min_fixed_shape = min_fixed.shape
            min_fixed = min_fixed.reshape(n_rows, int(min_fixed_shape[0]/n_rows))
            min_variables_compressed = min_variables.compressed()
            min_variables_length = min_variables_compressed.shape[0]
            n_columns = int(min_variables_length/n_rows)
            n_components = self.component_number if n_columns-1 == self.component_number else n_columns-1

            constraints = [
                {
                    "type": "ineq", 
                    "fun": self._reconciled_light_composition_constrain, 
                    "args": (min_fixed, n_rows, n_columns, n_components)
                },
                {
                    "type": "ineq",
                    "fun": self._min_variables_constraints
                }
            ]
            
            results = minimize(self._minimization, min_variables_compressed, 
                           method="SLSQP", 
                           args = (min_fixed, n_rows, n_columns, n_components), 
                           constraints=constraints)

            reconciled_results = results.x
            min_variables[min_variables_idx[0], min_variables_idx[1]] = reconciled_results
            reconcile_data = np.hstack([experiments_matrix[:,0:start_idx_heavy_phase], min_variables[:,:-1], experiments_matrix[:, start_idx_phi_exp:end_idx_phi_exp], min_variables[:,-1].reshape(n_rows, 1)])
            reconcile_data[:, start_idx_light_phase:end_idx_light_phase] = (reconcile_data[:, 0:start_idx_light_phase] - reconcile_data[:, start_idx_heavy_phase:end_idx_heavy_phase]*(1-reconcile_data[:,-1].reshape(reconcile_data.shape[0],1)))/reconcile_data[:,-1].reshape(reconcile_data.shape[0],1)
            reconcile_data_df = pl.from_numpy(reconcile_data, columns_names)
            final_df = pl.concat([reference_columns, reconcile_data_df], how = "horizontal")
            reconcile_groups.append(final_df)
        
        reconcile_database = pl.concat(reconcile_groups).drop("index")
        reconcile_database = reconcile_database.drop(self.phi_names)
        reconcile_database.write_excel("refined_lle_data_v5.xlsx")


   
