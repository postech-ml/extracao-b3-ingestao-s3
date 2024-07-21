from io import StringIO
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
import os
from datetime import datetime

class Conversao:
    @staticmethod
    def processar_dados(csv_file):
        # Definir os diretórios
        parquet_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_parquet"

        # Verificar se o diretório de Parquet existe, se não, criar
        if not os.path.exists(parquet_dir):
            os.makedirs(parquet_dir)

        print(f"Arquivo CSV a ser processado: {csv_file}")

        # Ler os dados do CSV
        # dados = pd.read_csv(csv_file)
        # #  Ler os dados do CSV com encoding latin1
        # dados = pd.read_csv(csv_file, encoding='iso-8859-1')

       # Tentar decodificar o arquivo CSV com encoding 'latin1'
        try:
            # dados = pd.read_csv(csv_file, encoding='utf-8', delimiter=';')
            dados = pd.read_csv(StringIO(csv_file), sep="\t", encoding='utf-8')
        except pd.errors.ParserError:
            print("Erro ao processar o arquivo CSV. Verifique o delimitador e a estrutura do arquivo.")
            return

        # Transformar os dados em Parquet
        table = pa.Table.from_pandas(dados)
        original_filename = os.path.basename(csv_file)
        parquet_filename = os.path.splitext(original_filename)[0] + ".parquet"
        parquet_file = os.path.join(parquet_dir, parquet_filename)
        pq.write_table(table, parquet_file)
        print(f"Arquivo Parquet salvo em: {parquet_file}")

        # # Upload para o S3
        # s3_client = boto3.client('s3')
        # bucket_name = "nome-do-seu-bucket"
        # s3_key = f"raw/{datetime.now().strftime('%Y/%m/%d')}/{parquet_filename}"
        # s3_client.upload_file(parquet_file, bucket_name, s3_key)
        # print(f"Arquivo Parquet enviado para o S3: s3://{bucket_name}/{s3_key}")

if __name__ == "__main__":
    csv_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_csv"
    files = os.listdir(csv_dir)
    paths = [os.path.join(csv_dir, basename) for basename in files if basename.endswith('.csv')]

    if not paths:
        print("Nenhum arquivo CSV encontrado no diretório.")
    else:
        newest_file = max(paths, key=os.path.getctime)
        print(f"Arquivo CSV mais recente encontrado: {newest_file}")
        Conversao.processar_dados(newest_file)