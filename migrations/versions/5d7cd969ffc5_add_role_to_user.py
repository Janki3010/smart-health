"""Add role to user

Revision ID: 5d7cd969ffc5
Revises: 1090da7e3638
Create Date: 2025-06-09 10:53:39.472625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5d7cd969ffc5'
down_revision: Union[str, None] = '1090da7e3638'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Then add the column using the enum
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'role')