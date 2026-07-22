"""add bands, t_shirt_sizes, product_variants and evolve products table

Revision ID: b7e8f9a0b1c2
Revises: a1b2c3d4e5f6
Create Date: 2026-07-15 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7e8f9a0b1c2"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # --- bands ---
    op.create_table(
        "bands",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("formed_year", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_bands_slug"), "bands", ["slug"], unique=False)

    # --- t_shirt_sizes ---
    op.create_table(
        "t_shirt_sizes",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("size", sa.String(length=10), nullable=False),
        sa.Column("chest_min_cm", sa.Integer(), nullable=True),
        sa.Column("chest_max_cm", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("size"),
    )

    # --- evolve products table ---
    op.drop_index(op.f("ix_products_sku"), table_name="products")
    op.drop_constraint("products_sku_key", table_name="products", type_="unique")
    op.drop_column("products", "sku")
    op.drop_column("products", "price")
    op.drop_column("products", "stock_quantity")

    op.add_column("products", sa.Column("band_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("products", sa.Column("fit", sa.String(length=20), nullable=False, server_default="unisex"))
    op.create_index(op.f("ix_products_band_id"), "products", ["band_id"], unique=False)

    # --- product_variants ---
    op.create_table(
        "product_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("size_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("color", sa.String(length=50), server_default="black", nullable=False),
        sa.Column("sku", sa.String(length=50), nullable=False),
        sa.Column("unit_price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("stock_quantity", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
        sa.UniqueConstraint("product_id", "size_id", "color", name="uq_product_variant"),
    )
    op.create_index(op.f("ix_product_variants_product_id"), "product_variants", ["product_id"], unique=False)
    op.create_index(op.f("ix_product_variants_size_id"), "product_variants", ["size_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""

    # drop product_variants
    op.drop_index(op.f("ix_product_variants_size_id"), table_name="product_variants")
    op.drop_index(op.f("ix_product_variants_product_id"), table_name="product_variants")
    op.drop_table("product_variants")

    # revert products columns
    op.drop_index(op.f("ix_products_band_id"), table_name="products")
    op.drop_column("products", "fit")
    op.drop_column("products", "band_id")

    op.add_column("products", sa.Column("stock_quantity", sa.Integer(), server_default="0", nullable=False))
    op.add_column("products", sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False))
    op.add_column("products", sa.Column("sku", sa.String(length=50), nullable=False))
    op.create_unique_constraint("products_sku_key", "products", ["sku"])
    op.create_index(op.f("ix_products_sku"), "products", ["sku"], unique=False)

    # drop t_shirt_sizes
    op.drop_table("t_shirt_sizes")

    # drop bands
    op.drop_index(op.f("ix_bands_slug"), table_name="bands")
    op.drop_table("bands")
