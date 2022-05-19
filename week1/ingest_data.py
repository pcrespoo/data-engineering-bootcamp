#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
import pandas as pd
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    database = params.db
    url = params.url
    host = params.host
    table_name = params.table_name
    port = params.port

    #download the parquet and convert to csv
    parquet_name = 'output.parquet'
    os.system(f'wget {url} -O {parquet_name}')
    csv_name = 'output.csv'

    df_parquet = pd.read_parquet(parquet_name, engine='pyarrow')
    df_parquet['tpep_pickup_datetime'] = pd.to_datetime(df_parquet['tpep_pickup_datetime'])
    df_parquet['tpep_dropoff_datetime'] = pd.to_datetime(df_parquet['tpep_dropoff_datetime'])
    df_parquet.to_csv(csv_name,sep=';')

    #create a conn with Postgres
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    #read data in chunks
    df_iter = pd.read_csv(csv_name,sep=';',iterator=True, chunksize=100000,index_col=0)

    #create a first chunk
    df = next(df_iter)

    #adjust date columns 
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

    #create table
    df.head(0).to_sql(con=engine, name=table_name, if_exists='replace')

    #insert chunks of data into the table
    while True:
        t_start = time()
        
        df = next(df_iter)
        
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        
        df.to_sql(con=engine, name=table_name, if_exists='append')
        
        t_final = time()
        
        print(f'chunk insertion took {t_final - t_start}')

if __name__ == '__main__':
    #parse the CLI parameters
    parser = argparse.ArgumentParser(description='Ingest csv data to postgresql')
    parser.add_argument('--user', help='username for postgresql')
    parser.add_argument('--password', help='password for postgresql')
    parser.add_argument('--port', help='port for postgresql')
    parser.add_argument('--host', help='host for postgresql')
    parser.add_argument('--db', help='database name')
    parser.add_argument('--table_name', help='name of the table')
    parser.add_argument('--url', help='url of the csv file')
    args = parser.parse_args()

    main(args)
