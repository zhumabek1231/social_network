"""add group tables

Revision ID: 729944e687a1
Revises: ec0b25d8ef75
Create Date: 2026-09-17 09:50:33.120492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '729944e687a1'
down_revision: Union[str, Sequence[str], None] = 'ec0b25d8ef75'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('group_people', 'user', new_column_name='user_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('group_people', 'user_id', new_column_name='user')