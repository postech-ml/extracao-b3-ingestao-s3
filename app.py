from extracao import extrair_dados, excluir_arquivos
from ingestao import Ingestao

def chamar_extracao():

    excluir_arquivos()

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

def chamar_ingestao(csv_file):
    try:
        if csv_file:
            Ingestao.processar_dados(csv_file)
            print("Ingestão concluída com sucesso.")
        else:
            print("Ingestão não realizada devido a erro na extração.")
    except Exception as e:
        print(f"Erro na ingestão: {e}")

if __name__ == "__main__":
    # download_dir = "/workspaces/extracao-b3-ingestao-s3/Arquivos CSV"
    csv_file = chamar_extracao()
    # chamar_ingestao(csv_file)