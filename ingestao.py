import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import os
from datetime import datetime

class Ingestao:
    @staticmethod
    def processar_dados():
        # Definir o caminho do arquivo CSV baixado
        csv_file = "/path/to/download/directory/nome_do_arquivo.csv"  # Substitua pelo nome correto do arquivo

        # Ler os dados do CSV
        dados = pd.read_csv(csv_file)

        # Transformar os dados em Parquet
        table = pa.Table.from_pandas(dados)
        data_d_1 = datetime.now()  # Substitua pela data correta se necessário
        parquet_file = f"/path/to/save/dados_pregao_{data_d_1.strftime('%Y%m%d')}.parquet"
        pq.write_table(table, parquet_file)

        # Upload para o S3
        s3_client = boto3.client('s3')
        bucket_name = "nome-do-seu-bucket"
        s3_key = f"raw/{data_d_1.strftime('%Y/%m/%d')}/dados_pregao.parquet"
        s3_client.upload_file(parquet_file, bucket_name, s3_key)

if __name__ == "__main__":
    Ingestao.processar_dados()