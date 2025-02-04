from flask import Blueprint, jsonify, request, send_file, abort, send_from_directory
from modules.geratermo.modules.data_compiler import DataCompiler
from modules.geratermo.modules.pdf_constructor import PdfConstructor
import os

bp_termos = Blueprint('termos', __name__, url_prefix='/termos')

def list_pdfs(directory):
    export_path = os.path.join(directory, "export")
    print(export_path)
    if not os.path.exists(export_path):
        return {"error": "Pasta 'export' não encontrada"}
    
    files_info = []
    for file in os.listdir(export_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(export_path, file)
            file_info = {
                "name": file,
                "size_kb": round(os.path.getsize(file_path) / 1024, 2),
                "path": file_path,
                "last_modified": os.path.getmtime(file_path)
            }
            files_info.append(file_info)
    
    return files_info

def limpar_pdfs():
    if not os.path.isdir("./export"):
        print(f"O diretório './export' não existe ou não é válido.")
        return

    for arquivo in os.listdir("./export"):
        caminho_arquivo = os.path.join("./export", arquivo)
        if arquivo.endswith(".pdf") and os.path.isfile(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
                print(f"Removido: {caminho_arquivo}")
            except Exception as e:
                print(f"Erro ao excluir {caminho_arquivo}: {e}")

@bp_termos.route("/gerar", methods=["POST"])
def gerar_um_termo():
    dados = request.json
    data_comp = DataCompiler()
    data_comp.set_data(dados)
    data_from_compiler = data_comp.define_first_paragraph()
    pdf_build = PdfConstructor(data_from_compiler, "Termo de responsabilidade", data_comp.get_data())
    if pdf_build:
        return jsonify({
            "compiled_data":data_comp.get_data(),
            "generated":True,
            "number":pdf_build.get_pdf_number()
        })
    return "Erro ao gerar."

@bp_termos.route("/buscar/<int:numero>", methods=["GET"])
def buscar_dados_termo(numero):
    export = os.path.abspath("export")
    filename = f"{numero}.pdf"
    path = os.path.join(export, filename)

    if os.path.exists(path):
        return send_file(path, mimetype="application/pdf", as_attachment=False)
    else:
        abort(404, description="PDF não encontrado!")

@bp_termos.route("/dir", methods=["GET"])
def get_pdfs():
    directory = os.getcwd()
    files_info = list_pdfs(directory)
    return jsonify(files_info)