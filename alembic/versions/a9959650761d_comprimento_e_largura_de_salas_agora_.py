"""comprimento e largura de salas agora não é dado obrigatório no registro das salas de uma unidade

Revision ID: a9959650761d
Revises: b36450645de2
Create Date: 2025-03-11 14:42:07.232066

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a9959650761d'
down_revision: Union[str, None] = 'b36450645de2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tb_uni_salas', 'largura_sala',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.alter_column('tb_uni_salas', 'comprimento_sala',
               existing_type=mysql.FLOAT(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tb_uni_salas', 'comprimento_sala',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.alter_column('tb_uni_salas', 'largura_sala',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.create_table('tb_unidades',
    sa.Column('uni_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('uni_registro', mysql.VARCHAR(length=14), nullable=True),
    sa.Column('uni_cod_ue', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('uni_designador_categoria', mysql.VARCHAR(length=25), nullable=True),
    sa.Column('uni_nome', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('uni_cep', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('uni_logradouro', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('uni_numero_end', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('uni_bairro', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('uni_distrito', mysql.VARCHAR(length=2), nullable=True),
    sa.Column('uni_direcao', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('uni_telefone_direcao', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('uni_segmentos', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('uni_listada', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uni_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_demandas',
    sa.Column('dem_protocolo', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('dem_solicitante_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_direcionamento_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_dt_entrada', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('dem_dt_atendimento', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('dem_tipo_demanda', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_local', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('dem_sala', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('dem_descricao', mysql.VARCHAR(length=300), nullable=True),
    sa.Column('dem_status', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_prioridade', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_dt_final', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('dem_atendido_por_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_tempo_finalizacao', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('dem_observacoes', mysql.VARCHAR(length=300), nullable=True),
    sa.Column('dem_link_oficio', mysql.VARCHAR(length=200), nullable=True),
    sa.PrimaryKeyConstraint('dem_protocolo'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_rel_acesso_perm',
    sa.Column('rap_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rap_acesso_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rap_perm_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rap_ativo', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_dispositivos',
    sa.Column('disp_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('disp_serial', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('disp_tipo', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('disp_desc', mysql.VARCHAR(length=300), nullable=True),
    sa.PrimaryKeyConstraint('disp_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_permissao',
    sa.Column('perm_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('perm_nome', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('perm_desc', mysql.VARCHAR(length=150), nullable=False),
    sa.PrimaryKeyConstraint('perm_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_notificacoes',
    sa.Column('not_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('not_message', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('not_data', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('not_hora', mysql.VARCHAR(length=8), nullable=False),
    sa.Column('not_lida', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('not_protocolo', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('not_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_niveis_acesso',
    sa.Column('nva_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('nva_nome', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('nva_desc', mysql.VARCHAR(length=255), nullable=True),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('tb_usuarios',
    sa.Column('usuario_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('usuario_matricula', mysql.VARCHAR(length=15), nullable=False),
    sa.Column('usuario_vinculo', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('usuario_local', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('usuario_setor', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('usuario_cargo', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('usuario_nome', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('usuario_funcao', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('usuario_sala', mysql.VARCHAR(length=4), nullable=False),
    sa.Column('usuario_cpf', mysql.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('usuario_email', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('usuario_telefone', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('usuario_senha', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('usuario_tipo', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('usuario_ativo', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('usuario_situacao_rh', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('usuario_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('usuario_email', 'tb_usuarios', ['usuario_email'], unique=True)
    op.create_table('tb_categorias_dispositivo',
    sa.Column('cat_disp_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('cat_disp_nome', mysql.VARCHAR(length=80), nullable=True),
    sa.Column('cat_disp_modelo', mysql.VARCHAR(length=200), nullable=True),
    sa.Column('cat_disp_tipo', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('cat_disp_desc', mysql.VARCHAR(length=300), nullable=True),
    sa.PrimaryKeyConstraint('cat_disp_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )