class GSheetManager:
    _nome_planilha = None
    _nome_pagina = None
    def __init__(self, nome_da_planilha:str, nome_da_pagina:str, cliente_gspread:object) -> None:
        self._nome_planilha = nome_da_planilha
        self._nome_pagina = nome_da_pagina
        self._definir_cliente(cliente_gspread)
        self._ativar_planilha()

    def _definir_cliente(self, cliente_gspread:object):
        self._cliente = cliente_gspread
    
    def _ativar_planilha(self):
        self._planilha_ativa = self._cliente.open(self._nome_planilha).worksheet(self._nome_pagina)

    def definir_pagina(self, nome_da_pagina:str):
        self._nome_pagina = nome_da_pagina
        self._ativar_planilha()
    
    def obter_dados(self) -> list:
        return self._planilha_ativa.get_all_values()
    
    def inserir_dados(self, dados:list) -> bool:
        try:
            self._planilha_ativa.append_row(dados)
            return True
        except Exception as e:
            print(e)
            return False

    def atualizar_direcionamento(self, id, valor):
        try:
            cell_row = id + 3
            cell_col = 6
            self._planilha_ativa.update_cell(cell_row, cell_col, valor)
            return True
        except Exception as e:
            print(e)
            return False
        
    def atualizar_prioridade(self, id, valor):
        try:
            cell_row = id + 3
            cell_col = 2
            self._planilha_ativa.update_cell(cell_row, cell_col, valor)
            return True
        except Exception as e:
            print(e)
            return False
        
    def atualizar_local(self, id, valor):
        try:
            cell_row = id + 3
            cell_col = 7
            self._planilha_ativa.update_cell(cell_row, cell_col, valor)
            return True
        except Exception as e:
            print(e)
            return False
    
    # Métodos relacionados a troca de status
    def atualizar_status(self, id, valor):
        idx = id + 3
        try:
            valores = self._planilha_ativa.row_values(idx)
            cell_row = id + 3
            cell_col = 9
            diff = None
            if valor == 'finalizada' or valor == 'encerrada':
                from datetime import datetime
                cell_col = 10
                data_atual = datetime.now()
                data_atual_formatada = data_atual.strftime("%d/%m/%Y")
                self._planilha_ativa.update_cell(cell_row, cell_col, data_atual_formatada)
                cell_col = 12
                diff = data_atual - datetime.strptime(valores[2], '%d/%m/%Y')
                self._planilha_ativa.update_cell(cell_row, cell_col, str(diff.days))
            cell_col = 9
            self._planilha_ativa.update_cell(cell_row, cell_col, valor)
            return True
        except Exception as e:
            print(e)
            return False
        
    def transferir_dados_entre_abas(self, id:int, destino:str):
        idx = id + 3
        try:
            planilha_destino = self._cliente.open(self._nome_planilha).worksheet(destino)
            valores = self._planilha_ativa.row_values(idx)
            if valores:
                planilha_destino.append_row(valores)
                self._planilha_ativa.delete_rows(idx)
            return {'transferido':True, 'demanda':valores}
        except Exception as e:
            print(e)
            return False