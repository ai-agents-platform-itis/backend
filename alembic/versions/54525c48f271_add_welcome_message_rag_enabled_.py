"""add welcome_message, rag_enabled, knowledge_docs

Revision ID: 54525c48f271
Revises: 0599272539a1
Create Date: 2026-07-10 11:32:54.630910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54525c48f271'
down_revision: Union[str, Sequence[str], None] = '0599272539a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # welcome_message — можно NULL, старая запись просто останется без приветствия
    op.add_column('campaigns', sa.Column('welcome_message', sa.Text(), nullable=True))
    
    # rag_enabled — сначала nullable
    op.add_column('campaigns', sa.Column('rag_enabled', sa.Boolean(), nullable=True))
    
    # Проставляем дефолт для существующих записей
    op.execute("UPDATE campaigns SET rag_enabled = FALSE WHERE rag_enabled IS NULL")
    
    # Теперь делаем NOT NULL
    op.alter_column('campaigns', 'rag_enabled', nullable=False)
    
    # Создаём таблицу knowledge_docs
    op.create_table(
        'knowledge_docs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('campaign_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_path', sa.String(500), nullable=False),
        sa.Column('content_text', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('knowledge_docs')
    op.drop_column('campaigns', 'rag_enabled')
    op.drop_column('campaigns', 'welcome_message')
