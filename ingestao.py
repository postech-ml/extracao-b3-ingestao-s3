# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
# import boto3
# import os
# from datetime import datetime

# class Ingestao:
#     @staticmethod
#     def processar_dados():
#         # Definir o caminho do arquivo CSV baixado
#         csv_file = "/path/to/download/directory/nome_do_arquivo.csv"  # Substitua pelo nome correto do arquivo

#         # Ler os dados do CSV
#         dados = pd.read_csv(csv_file)

#         # Transformar os dados em Parquet
#         table = pa.Table.from_pandas(dados)
#         data_d_1 = datetime.now()  # Substitua pela data correta se necessário
#         parquet_file = f"/path/to/save/dados_pregao_{data_d_1.strftime('%Y%m%d')}.parquet"
#         pq.write_table(table, parquet_file)

#         # Upload para o S3
#         s3_client = boto3.client('s3')
#         bucket_name = "nome-do-seu-bucket"
#         s3_key = f"raw/{data_d_1.strftime('%Y/%m/%d')}/dados_pregao.parquet"
#         s3_client.upload_file(parquet_file, bucket_name, s3_key)

# if __name__ == "__main__":
#     Ingestao.processar_dados()

# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
# import boto3
# import os
# from datetime import datetime

# class Ingestao:
#     @staticmethod
#     def processar_dados():
#         # Definir os diretórios
#         csv_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_csv"
#         parquet_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_parquet"

#         # Verificar se o diretório de Parquet existe, se não, criar
#         if not os.path.exists(parquet_dir):
#             os.makedirs(parquet_dir)

#         # Encontrar o arquivo CSV mais recente no diretório
#         files = os.listdir(csv_dir)
#         paths = [os.path.join(csv_dir, basename) for basename in files if basename.endswith('.csv')]

#         if not paths:
#             print("Nenhum arquivo CSV encontrado no diretório.")
#             return

#         newest_file = max(paths, key=os.path.getctime)
#         print(f"Arquivo CSV mais recente encontrado: {newest_file}")

#         # Ler os dados do CSV
#         dados = pd.read_csv(newest_file)

#         # Transformar os dados em Parquet
#         table = pa.Table.from_pandas(dados)
#         original_filename = os.path.basename(newest_file)
#         parquet_filename = os.path.splitext(original_filename)[0] + ".parquet"
#         parquet_file = os.path.join(parquet_dir, parquet_filename)
#         pq.write_table(table, parquet_file)
#         print(f"Arquivo Parquet salvo em: {parquet_file}")

#         # # Upload para o S3
#         # s3_client = boto3.client('s3')
#         # bucket_name = "nome-do-seu-bucket"
#         # s3_key = f"raw/{datetime.now().strftime('%Y/%m/%d')}/{parquet_filename}"
#         # s3_client.upload_file(parquet_file, bucket_name, s3_key)
#         # print(f"Arquivo Parquet enviado para o S3: s3://{bucket_name}/{s3_key}")

# if __name__ == "__main__":
#     Ingestao.processar_dados()

# 

# import pandas as pd
# import pyarrow as pa
# import pyarrow.parquet as pq
# import boto3
# import os
# from datetime import datetime

# class Ingestao:
#     @staticmethod
#     def processar_dados(csv_file):
#         # Definir os diretórios
#         parquet_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_parquet"

#         # Verificar se o diretório de Parquet existe, se não, criar
#         if not os.path.exists(parquet_dir):
#             os.makedirs(parquet_dir)

#         print(f"Arquivo CSV a ser processado: {csv_file}")

#         # Ler os dados do CSV
#         dados = pd.read_csv(csv_file)
#         #  Ler os dados do CSV com encoding latin1
#         dados = pd.read_csv(csv_file, encoding='latin1')

#         # Transformar os dados em Parquet
#         table = pa.Table.from_pandas(dados)
#         original_filename = os.path.basename(csv_file)
#         parquet_filename = os.path.splitext(original_filename)[0] + ".parquet"
#         parquet_file = os.path.join(parquet_dir, parquet_filename)
#         pq.write_table(table, parquet_file)
#         print(f"Arquivo Parquet salvo em: {parquet_file}")

#         # Upload para o S3
#         s3_client = boto3.client('s3')
#         bucket_name = "nome-do-seu-bucket"
#         s3_key = f"raw/{datetime.now().strftime('%Y/%m/%d')}/{parquet_filename}"
#         s3_client.upload_file(parquet_file, bucket_name, s3_key)
#         print(f"Arquivo Parquet enviado para o S3: s3://{bucket_name}/{s3_key}")

# if __name__ == "__main__":
#     csv_dir = "/workspaces/extracao-b3-ingestao-s3/arquivos_csv"
#     files = os.listdir(csv_dir)
#     paths = [os.path.join(csv_dir, basename) for basename in files if basename.endswith('.csv')]

#     if not paths:
#         print("Nenhum arquivo CSV encontrado no diretório.")
#     else:
#         newest_file = max(paths, key=os.path.getctime)
#         print(f"Arquivo CSV mais recente encontrado: {newest_file}")
#         Ingestao.processar_dados(newest_file)

import os
import boto3
from datetime import datetime
import glob

class Ingestao:
    def __init__(self, nome_bucket):
        self.nome_bucket = nome_bucket
        self.cliente_s3 = boto3.client('s3', 
            aws_access_key_id='SEU_ACCESS_KEY_ID',
            aws_secret_access_key='SEU_SECRET_ACCESS_KEY'
        )

    def carregar_parquet_mais_recente(self, caminho_diretorio):
        # Encontrar o arquivo Parquet mais recente no diretório
        lista_arquivos = glob.glob(caminho_diretorio + '/*.parquet')
        arquivo_mais_recente = max(lista_arquivos, key=os.path.getctime)

        # Gerar a chave S3 para o upload
        data_atual = datetime.now().strftime('%Y/%m/%d')
        chave_s3 = f"raw/{data_atual}/" + os.path.basename(arquivo_mais_recente)

        # Fazer o upload do arquivo para o S3
        self.cliente_s3.upload_file(arquivo_mais_recente, self.nome_bucket, chave_s3)
        print(f"Arquivo Parquet mais recente '{arquivo_mais_recente}' enviado para o bucket '{self.nome_bucket}' com a chave '{chave_s3}'.")

# Utilize a classe Ingestao para fazer o upload do arquivo Parquet mais recente
ingestor = Ingestao(nome_bucket="nome-do-seu-bucket")
ingestor.carregar_parquet_mais_recente(caminho_diretorio="/caminho/do/diretorio")