from datetime import datetime
class GSheetManager:
    _nome_planilha = None
    _nome_pagina = None
    def __init__(self, nome_da_planilha:str, nome_da_pagina:str, cliente_gspread:object) -> None:
        self._nome_planilha = nome_da_planilha
        self._nome_pagina = nome_da_pagina
        self.data_atual = datetime.now()
        self._definir_cliente(cliente_gspread)
        self._ativar_planilha()

    def _definir_cliente(self, cliente_gspread:object):
        self._cliente = cliente_gspread
    
    def _ativar_planilha(self):
        self._planilha_ativa = self._cliente.open(self._nome_planilha).worksheet(self._nome_pagina)
        return True

    def definir_pagina(self, nome_da_pagina:str):
        self._nome_pagina = nome_da_pagina
        if self._ativar_planilha():
            return True
    
    def obter_dados(self) -> list:
        return self._planilha_ativa.get_all_values()
    
    def inserir_dados(self, dados:list) -> bool:
        if type(dados) == list:
            try:
                self._planilha_ativa.append_row(dados)
                return True
            except Exception as e:
                print(e)
            return False
        return False

    def atualizar_direcionamento(self, id, valor:str) -> bool:
        if type(valor) == str:
            try:
                cell_row = id + 1
                cell_col = 7
                self._planilha_ativa.update_cell(cell_row, cell_col, valor)
                return True
            except Exception as e:
                print(e)
            return False
        return False
        
    def atualizar_prioridade(self, id, valor:str) -> bool:
        if type(valor) == str:
            try:
                cell_row = id + 1
                cell_col = 2
                self._planilha_ativa.update_cell(cell_row, cell_col, valor)
                return True
            except Exception as e:
                print(e)
            return False
        return False
        
    def atualizar_local(self, id, valor:str)->bool:
        if type(valor) == str:
            try:
                cell_row = id + 1
                cell_col = 8
                self._planilha_ativa.update_cell(cell_row, cell_col, valor)
                return True
            except Exception as e:
                print(e)
            return False
        return False
    
    # Métodos relacionados a troca de status
    def atualizar_status(self, id, valor:str) -> bool:
        idx = id + 1
        if type(valor) == str:
            try:
                valores = self._planilha_ativa.row_values(idx)
                cell_row = idx
                cell_col = 4
                diff = None

                if valores[3] == "-":
                    self._planilha_ativa.update_cell(cell_row, cell_col, self.data_atual.strftime("%d/%m/%Y"))
                
                cell_col = 11
                if valor == 'finalizada' or valor == 'encerrada':
                    cell_col = 12
                    data_atual_formatada = self.data_atual.strftime("%d/%m/%Y")
                    self._planilha_ativa.update_cell(cell_row, cell_col, data_atual_formatada)
                    cell_col = 14
                    diff = self.data_atual - datetime.strptime(valores[2], '%d/%m/%Y')
                    self._planilha_ativa.update_cell(cell_row, cell_col, str(diff.days))
                    cell_col = 11
                self._planilha_ativa.update_cell(cell_row, cell_col, valor)
                return True
            except Exception as e:
                print(e)
            return False
        return False
        
    def transferir_dados_entre_abas(self, id:int, destino:str) -> bool:
        idx = id + 1
        if type(destino) == str:
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
        return False
    
    def obter_linha_pelo_protocolo(self, protocolo:int):
        celula_protocolo = self._planilha_ativa.find(str(protocolo))
        return celula_protocolo.row - 1
