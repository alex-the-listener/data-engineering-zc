import argparse
import os
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Determine local file name from URL
    file_name = url.split('/')[-1]

    print(f"Downloading {file_name} from {url}...")
    os.system(f"curl -sSL {url} -o {file_name}")

    # Create Database Engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if file_name.endswith('.parquet'):
        print(f"Reading Parquet file: {file_name}")
        parquet_file = pq.ParquetFile(file_name)
        
        # Read the first batch to set up table schema
        first_batch = next(parquet_file.iter_batches(batch_size=100000))
        df = first_batch.to_pandas()
        
        print(f"Creating schema for '{table_name}'...")
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        print(f"Ingesting records into '{table_name}'...")
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

        # Stream remaining batches
        for batch in parquet_file.iter_batches(batch_size=100000):
            df_batch = batch.to_pandas()
            df_batch.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    elif file_name.endswith('.csv'):
        print(f"Reading CSV file: {file_name}")
        df = pd.read_csv(file_name)

        print(f"Creating schema for '{table_name}'...")
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        print(f"Ingesting records into '{table_name}'...")
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    # Clean up downloaded file
    if os.path.exists(file_name):
        os.remove(file_name)

    print(f"Finished ingesting {file_name} into table '{table_name}'!\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest dataset to Postgres')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table to write to')
    parser.add_argument('--url', required=True, help='url of the dataset file')

    args = parser.parse_args()
    main(args)