"""remove band slug and formed_year

Revision ID: c4d5e6f7a8b9
Revises: b7e8f9a0b1c2
Create Date: 2026-07-21 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c4d5e6f7a8b9"
down_revision: Union[str, None] = "b7e8f9a0b1c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove slug and formed_year columns from bands."""
    op.drop_index(op.f("ix_bands_slug"), table_name="bands")
    op.drop_constraint("bands_slug_key", table_name="bands", type_="unique")
    op.drop_column("bands", "slug")
    op.drop_column("bands", "formed_year")


def downgrade() -> None:
    """Restore slug and formed_year columns to bands."""
    op.add_column("bands", sa.Column("slug", sa.String(length=180), nullable=False))
    op.add_column("bands", sa.Column("formed_year", sa.Integer(), nullable=True))
    op.create_unique_constraint("bands_slug_key", "bands", ["slug"])
    op.create_index(op.f("ix_bands_slug"), "bands", ["slug"], unique=False)
