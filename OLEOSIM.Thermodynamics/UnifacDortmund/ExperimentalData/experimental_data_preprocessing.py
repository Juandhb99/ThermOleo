import polars as pl

raw_experimental_lle_data = (pl
                             .read_excel('raw_lle_data.xlsx', engine='calamine')
                             .drop(['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol',  'Tie lines'])).with_row_index()
raw_experimental_lle_data

