from models.rel_acesso_perm import RelAcessoPermn_model

rap_model = RelAcessoPermn_model()
res = rap_model.remover_rel_acesso_perm(1)
print(res)