"""Add URL status and analytics fields

Revision ID: 64b9cae18b13
Revises: 3ec8c9a558e4
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "64b9cae18b13"
down_revision: Union[str, Sequence[str], None] = "3ec8c9a558e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""

    # ---------------------------------------------------------
    # short_urls
    # ---------------------------------------------------------

    with op.batch_alter_table("short_urls") as batch_op:

        batch_op.add_column(
            sa.Column(
                "custom_alias",
                sa.String(length=50),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=True,
                server_default=sa.true(),
            )
        )

        batch_op.create_unique_constraint(
            "uq_short_urls_custom_alias",
            ["custom_alias"],
        )

    # ---------------------------------------------------------
    # click_analytics
    # ---------------------------------------------------------

    with op.batch_alter_table("click_analytics") as batch_op:

        # Preserve existing click timestamps.
        batch_op.alter_column(
            "clicked_at",
            new_column_name="visited_at",
        )

        # Increase IP address storage from 45 to 100 characters.
        batch_op.alter_column(
            "ip_address",
            existing_type=sa.String(length=45),
            type_=sa.String(length=100),
        )

        batch_op.add_column(
            sa.Column(
                "browser",
                sa.String(length=100),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "operating_system",
                sa.String(length=100),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "device",
                sa.String(length=100),
                nullable=True,
            )
        )


def downgrade() -> None:
    """Downgrade database schema."""

    # ---------------------------------------------------------
    # click_analytics
    # ---------------------------------------------------------

    with op.batch_alter_table("click_analytics") as batch_op:

        batch_op.drop_column("device")
        batch_op.drop_column("operating_system")
        batch_op.drop_column("browser")

        batch_op.alter_column(
            "ip_address",
            existing_type=sa.String(length=100),
            type_=sa.String(length=45),
        )

        # Restore original column name.
        batch_op.alter_column(
            "visited_at",
            new_column_name="clicked_at",
        )

    # ---------------------------------------------------------
    # short_urls
    # ---------------------------------------------------------

    with op.batch_alter_table("short_urls") as batch_op:

        batch_op.drop_constraint(
            "uq_short_urls_custom_alias",
            type_="unique",
        )

        batch_op.drop_column("is_active")
        batch_op.drop_column("custom_alias")