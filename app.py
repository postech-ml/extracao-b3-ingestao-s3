from extracao import extrair_dados
from ingestao import Ingestao
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Aplicação de Extração e Ingestão de Dados"

@app.route('/extrair')
def chamar_extracao():
    try:
        csv_file = extrair_dados()
        if csv_file:
            print("Extração concluída com sucesso.")
            return jsonify({"message": "Extração concluída com sucesso.", "file": csv_file})
        else:
            return jsonify({"message": "Erro na extração."}), 500
    except Exception as e:
        print(f"Erro na extração: {e}")
        return jsonify({"message": f"Erro na extração: {e}"}), 500

# @app.route('/ingestao')
# def chamar_ingestao():
#     try:
#         csv_file = extrair_dados()
#         if csv_file:
#             Ingestao.processar_dados(csv_file)
#             print("Ingestão concluída com sucesso.")
#             return jsonify({"message": "Ingestão concluída com sucesso."})
#         else:
#             print("Ingestão não realizada devido a erro na extração.")
#             return jsonify({"message": "Ingestão não realizada devido a erro na extração."}), 500
#     except Exception as e:
#         print(f"Erro na ingestão: {e}")
#         return jsonify({"message": f"Erro na ingestão: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)