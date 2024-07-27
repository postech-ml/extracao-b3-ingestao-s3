from extracao import extrair_dados
from conversao import Conversao
from ingestao import Ingestao

def chamar_extracao():
    try:
        csv_file = extrair_dados()
        if csv_file:
            print("Extração concluída com sucesso.")
            return csv_file
        else:
            print("Erro na extração.")
            return None
    except Exception as e:
        print(f"Erro na extração: {e}")
        return None

def chamar_conversao(csv_file):
    try:
        if csv_file:
            Conversao.processar_dados(csv_file)
            print("Conversão concluída com sucesso.")
        else:
            print("Conversão não realizada devido a erro na extração.")
    except Exception as e:
        print(f"Erro na conversão: {e}")



def chamar_ingestao():
    try:
        ingestor = Ingestao(nome_bucket="ing-dados-b3")  # Substitua pelo nome do seu bucket
        ingestor.carregar_parquet_mais_recente(caminho_diretorio="/workspaces/extracao-b3-ingestao-s3/arquivos_parquet")  # Substitua pelo caminho do diretório
        print("Ingestão concluída com sucesso.")
    except Exception as e:
        print(f"Erro na ingestão: {e}")        

if __name__ == "__main__":
    
    csv_file = chamar_extracao()
    # csv_file = "/workspaces/extracao-b3-ingestao-s3/IBOVDia_19-07-24.csv"
    chamar_conversao(csv_file)
    chamar_ingestao()