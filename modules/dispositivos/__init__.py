from models.categorias_dispositivos import Categoria_dispositivo_model
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
    
    def obter_dispositivo_por_serial(self, disp_serial:str):
        return self.model.get_dispositivo_by_serial(disp_serial)
    
    def deletar_dispositivo(self, disp_id):
        return self.model.delete_dispositivo(disp_id)

class GerenciadorDispositivos:
    def registrar_dispositivo(self, dados: dict):
        disp = Dispositivo(dados)
        return disp.criar_dispositivo()
    
    def atualizar_dispositivo(self, disp_serial:str, novos_dados: dict):
        disp = Dispositivo()
        dispositivo_existente = disp.obter_dispositivo_por_serial(disp_serial)

        print(disp_serial, novos_dados, dispositivo_existente)

        if not dispositivo_existente:
            return {"found":False}

        return disp.atualizar_dispositivo(dispositivo_existente.disp_id, novos_dados)
    
    def listar_dispositivos(self):
        disp = Dispositivo()
        return disp.obter_todos_dispositivos()
    
    def buscar_dispositivo_por_serial(self, disp_serial):
        disp = Dispositivo()
        return disp.obter_dispositivo_por_serial(disp_serial)
    
    def remover_dispositivo(self, disp_id):
        disp = Dispositivo()
        return disp.deletar_dispositivo(disp_id)

# class Categoria_dispositivo:
#     def __init__(self, dados: dict = None):
#         if dados:
#             for chave, valor in dados.items():
#                 setattr(self, chave, valor)
#         self.model = Categoria_dispositivo_model()

#     def criar_categoria(self):
#         nova_categoria = self.model.create_categoria(
#             self.cat_disp_nome,
#             self.cat_disp_modelo,
#             self.cat_disp_tipo,
#             self.cat_disp_desc
#         )
#         return nova_categoria

# class Gerenciador_categorias:
#     def registrar_categoria(self, dados: dict):
#         categoria = Categoria_dispositivo(dados)
#         print(categoria)
#         return categoria.criar_categoria()

class Categoria_dispositivo:
    def __init__(self, dados: dict = None):
        if dados:
            for chave, valor in dados.items():
                setattr(self, chave, valor)
        self.model = Categoria_dispositivo_model()

    def criar_categoria(self):
        nova_categoria = self.model.create_categoria(
            self.cat_disp_nome,
            self.cat_disp_modelo,
            self.cat_disp_tipo,
            self.cat_disp_desc
        )
        return nova_categoria

    def ler_categoria_por_id(self, categoria_id):
        return dict(self.model.get_categoria_by_id(categoria_id))


class Gerenciador_categorias:
    def __init__(self):
        self.model = Categoria_dispositivo_model()

    def registrar_categoria(self, dados: dict):
        categoria = Categoria_dispositivo(dados)
        return categoria.criar_categoria()

    def listar_todas_categorias(self):
        obj_list = self.model.get_all_categorias()
        result_list = []
        for obj in obj_list:
            result_list.append(model_to_dict(obj))   
        return result_list

    def obter_categoria_por_id(self, categoria_id):
        return model_to_dict(self.model.get_categoria_by_id(categoria_id))

    def atualizar_categoria(self, categoria_id, novos_dados):
        return self.model.update_categoria(categoria_id, **novos_dados)

    def excluir_categoria(self, categoria_id):
        return self.model.delete_categoria(categoria_id)
    
def model_to_dict(model):
    return {column: getattr(model, column) for column in model.__table__.columns.keys()}