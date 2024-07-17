from extracao import extrair_dados
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
    
    csv_file = chamar_extracao()
    chamar_ingestao(csv_file)