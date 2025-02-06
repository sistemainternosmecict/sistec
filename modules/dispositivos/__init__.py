from models.dispositivos import Dispositivo_model

class Dispositivo:
    def __init__(self, dados: dict = None):
        if dados:
            for chave, valor in dados.items():
                setattr(self, chave, valor)
        self.model = Dispositivo_model()
    
    def criar_dispositivo(self):
        novo_dispositivo = self.model.create_dispositivo(
            self.disp_serial, self.disp_tipo, self.disp_desc
        )
        return novo_dispositivo
    
    def atualizar_dispositivo(self, disp_id, novos_dados: dict):
        return self.model.update_dispositivo(
            disp_id,
            novos_dados.get("disp_serial"),
            novos_dados.get("disp_tipo"),
            novos_dados.get("disp_desc")
        )
    
    def obter_todos_dispositivos(self):
        return self.model.get_all_dispositivos()
    
    def obter_dispositivo_por_serial(self, disp_serial):
        return self.model.get_dispositivo_by_serial(disp_serial)
    
    def deletar_dispositivo(self, disp_id):
        return self.model.delete_dispositivo(disp_id)

class GerenciadorDispositivos:
    def registrar_dispositivo(self, dados: dict):
        disp = Dispositivo(dados)
        return disp.criar_dispositivo()
    
    def atualizar_dispositivo(self, disp_id, novos_dados: dict):
        disp = Dispositivo()
        dispositivo_existente = disp.obter_dispositivo_por_serial(novos_dados.get("disp_serial"))

        if not dispositivo_existente:
            return None  # Retorna None se o dispositivo não existir

        return disp.atualizar_dispositivo(disp_id, novos_dados)
    
    def listar_dispositivos(self):
        disp = Dispositivo()
        return disp.obter_todos_dispositivos()
    
    def buscar_dispositivo_por_serial(self, disp_serial):
        disp = Dispositivo()
        return disp.obter_dispositivo_por_serial(disp_serial)
    
    def remover_dispositivo(self, disp_id):
        disp = Dispositivo()
        return disp.deletar_dispositivo(disp_id)
