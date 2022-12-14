"""initial

Revision ID: c5cb4f476b4d
Revises: 
Create Date: 2022-08-02 15:44:33.364729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5cb4f476b4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=512), nullable=True),
    sa.Column('is_available_for_students', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
    sa.Column('is_available_for_instructors', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_city_is_available_for_instructors'), 'city', ['is_available_for_instructors'], unique=False)
    op.create_index(op.f('ix_city_is_available_for_students'), 'city', ['is_available_for_students'], unique=False)
    op.create_table('postal_code',
    sa.Column('index', sa.String(length=6), nullable=False),
    sa.Column('ops_name', sa.String(), nullable=True),
    sa.Column('ops_type', sa.String(), nullable=True),
    sa.Column('ops_subm', sa.String(length=6), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('autonom', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('city_1', sa.String(), nullable=True),
    sa.Column('actdate', sa.Date(), nullable=True),
    sa.Column('indexold', sa.String(length=6), nullable=True),
    sa.Column('ext_adm_region', sa.String(length=64), nullable=True),
    sa.Column('ext_district', sa.String(length=64), nullable=True),
    sa.Column('city_ref_id', sa.Integer(), nullable=True),
    sa.Column('timezone', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_ref_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('index')
    )
    op.create_index(op.f('ix_postal_code_area'), 'postal_code', ['area'], unique=False)
    op.create_index(op.f('ix_postal_code_autonom'), 'postal_code', ['autonom'], unique=False)
    op.create_index(op.f('ix_postal_code_city'), 'postal_code', ['city'], unique=False)
    op.create_index(op.f('ix_postal_code_city_1'), 'postal_code', ['city_1'], unique=False)
    op.create_index(op.f('ix_postal_code_city_ref_id'), 'postal_code', ['city_ref_id'], unique=False)
    op.create_index(op.f('ix_postal_code_ext_adm_region'), 'postal_code', ['ext_adm_region'], unique=False)
    op.create_index(op.f('ix_postal_code_ext_district'), 'postal_code', ['ext_district'], unique=False)
    op.create_index(op.f('ix_postal_code_region'), 'postal_code', ['region'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_postal_code_region'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_ext_district'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_ext_adm_region'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_city_ref_id'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_city_1'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_city'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_autonom'), table_name='postal_code')
    op.drop_index(op.f('ix_postal_code_area'), table_name='postal_code')
    op.drop_table('postal_code')
    op.drop_index(op.f('ix_city_is_available_for_students'), table_name='city')
    op.drop_index(op.f('ix_city_is_available_for_instructors'), table_name='city')
    op.drop_table('city')
    # ### end Alembic commands ###
