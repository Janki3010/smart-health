"""added field in EmailToken model

Revision ID: 1090da7e3638
Revises: d6cb559a0e98
Create Date: 2025-06-05 14:17:09.104039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1090da7e3638'
down_revision: Union[str, None] = 'd6cb559a0e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('email_tokens', sa.Column('expires_at', sa.TIMESTAMP(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    pass
