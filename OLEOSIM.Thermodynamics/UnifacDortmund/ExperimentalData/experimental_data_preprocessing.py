import polars as pl
import numpy as np

raw_experimental_lle_data = (pl
                             .read_excel('raw_lle_data.xlsx', engine='calamine')
                             .drop(['Ref', 'Sub Ref', 'Temperature (K)', 'Type Alcohol',  'Tie lines'])).with_row_index()

columns_to_update = raw_experimental_lle_data.columns[9:17]

raw_experimental_lle_data = raw_experimental_lle_data.with_columns( 
    pl.when(pl.col(col)==0.0)
    .then(1e-20)
    .otherwise(pl.col(col))
    .alias(col) for col in columns_to_update
)


raw_experimental_lle_data = raw_experimental_lle_data.with_columns(
    
    phi_fame = (pl.col('FAME/FAEE_F') - pl.col('FAME/FAEE_H'))/(pl.col('FAME/FAEE_L') -  pl.col('FAME/FAEE_H')).alias('phi_fame'),
    
    phi_glycerol = (pl.col('GLYCEROL_F') - pl.col('GLYCEROL_H'))/(pl.col('GLYCEROL_L') -  pl.col('GLYCEROL_H')).alias('phi_glycerol'),

    phi_alcohol = (pl.col('ALCOHOL_F') - pl.col('ALCOHOL_H'))/(pl.col('ALCOHOL_L') -  pl.col('ALCOHOL_H')).alias('phi_alcohol'),

    phi_oil = (pl.col('OIL_F') - pl.col('OIL_H'))/(pl.col('OIL_L') -  pl.col('OIL_H')).alias('phi_oil'),

    phi_dag = (pl.col('DAG_F') - pl.col('DAG_H'))/(pl.col('DAG_L') -  pl.col('DAG_H')).alias('phi_dag'),

    phi_mag = (pl.col('MAG_F') - pl.col('MAG_H'))/(pl.col('MAG_L') -  pl.col('MAG_H')).alias('phi_mag'),

    phi_acid = (pl.col('ACID_F') - pl.col('ACID_H'))/(pl.col('ACID_L') -  pl.col('ACID_H')).alias('phi_acid'),

    phi_water = (pl.col('WATER_F') - pl.col('WATER_H'))/(pl.col('WATER_L') -  pl.col('WATER_H')).alias('phi_water'),
)

raw_experimental_lle_data

raw_experimental_lle_data.select(raw_experimental_lle_data.columns[2]) # Analizar manejarlo por indices en vez de nombres de columnas para generalizarlo, ir filtrando paso a paso por cada una de las condiciones. 