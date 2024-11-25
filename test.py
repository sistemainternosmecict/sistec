from modules.usuarios import GerenciadorPermissoes

ger_per = GerenciadorPermissoes()
# res = ger_per.registrar_permissao({"perm_nome": "test3", "perm_desc":"teste de descrição"})
# res = ger_per.atualizar_permissao({"perm_id": 1, "perm_desc":"teste"})
res = ger_per.remover_permissao(1)
print(res)
