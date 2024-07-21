import os
import boto3
from datetime import datetime
import glob
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

class Ingestao:
    def __init__(self, nome_bucket):
        self.nome_bucket = nome_bucket
        self.cliente_s3 = boto3.client('s3', 
            aws_access_key_id='SEU_ACCESS_KEY_ID',
            aws_secret_access_key='SEU_SECRET_ACCESS_KEY'
            aws_session_token='SEU_SESSION_TOKEN'
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
# ingestor = Ingestao(nome_bucket="nome-do-seu-bucket")
# ingestor.carregar_parquet_mais_recente(caminho_diretorio="/caminho/do/diretorio")