from openpyxl import load_workbook

class Lista_rh:
    __arquivo = "listaRh.xlsx"
    def __init__(self):
        self.__funcionarios = []
        self.carregar_funcionarios()

    def carregar_funcionarios(self):
        wb = load_workbook(self.__arquivo)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            registro = {
                'local_de_trabalho': row[0],
                'matricula': row[1],
                'nome': row[2],
                'cargo': row[3],
            }
            self.__funcionarios.append(registro)
    
    def buscar_por_matricula(self, matricula):
        matricula_temp = matricula.split('-')[0]
        return next((funcionario for funcionario in self.__funcionarios if funcionario['matricula'].split('-')[0] == matricula_temp), None)