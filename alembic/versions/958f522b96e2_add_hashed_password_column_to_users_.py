"""add_hashed_password_column_to_users_table

Revision ID: 958f522b96e2
Revises: ddbc238de69e
Create Date: 2026-03-25 22:29:19.967908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '958f522b96e2'
down_revision: Union[str, None] = 'ddbc238de69e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add hashed_password column (nullable initially for existing rows)
    op.add_column(
        'users',
        sa.Column('hashed_password', sa.String(60), nullable=True)
    )

    # If you have existing users, you may want to set a default placeholder hash
    # or handle them separately. For new databases, we can make it NOT NULL.
    # Uncomment the following to make it NOT NULL after setting defaults:
    # op.alter_column('users', 'hashed_password', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'hashed_password')

