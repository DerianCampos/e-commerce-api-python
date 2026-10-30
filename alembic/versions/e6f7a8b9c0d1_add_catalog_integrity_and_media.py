"""add catalog integrity and media

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-10-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6f7a8b9c0d1'
down_revision: Union[str, None] = 'd5e6f7a8b9c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("bands", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("bands", sa.Column("image_url", sa.String(length=500), nullable=True))
    op.add_column("products", sa.Column("image_url", sa.String(length=500), nullable=True))

    op.create_foreign_key(
        "fk_products_band_id_bands",
        "products",
        "bands",
        ["band_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_product_variants_product_id_products",
        "product_variants",
        "products",
        ["product_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_product_variants_size_id_t_shirt_sizes",
        "product_variants",
        "t_shirt_sizes",
        ["size_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_orders_user_id_users",
        "orders",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_order_items_order_id_orders",
        "order_items",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_order_items_product_variant_id_product_variants",
        "order_items",
        "product_variants",
        ["product_variant_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_unique_constraint(
        "uq_product_variants_product_size_color",
        "product_variants",
        ["product_id", "size_id", "color"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_product_variants_product_size_color", "product_variants", type_="unique")
    op.drop_constraint(
        "fk_order_items_product_variant_id_product_variants", "order_items", type_="foreignkey"
    )
    op.drop_constraint("fk_order_items_order_id_orders", "order_items", type_="foreignkey")
    op.drop_constraint("fk_orders_user_id_users", "orders", type_="foreignkey")
    op.drop_constraint(
        "fk_product_variants_size_id_t_shirt_sizes", "product_variants", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_product_variants_product_id_products", "product_variants", type_="foreignkey"
    )
    op.drop_constraint("fk_products_band_id_bands", "products", type_="foreignkey")
    op.drop_column("products", "image_url")
    op.drop_column("bands", "image_url")
    op.drop_column("bands", "description")
