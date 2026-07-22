"""add products table

Revision ID: a1b2c3d4e5f6
Revises: 43a57a0d9e2c
Create Date: 2026-07-15 10:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "43a57a0d9e2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_table("products")
