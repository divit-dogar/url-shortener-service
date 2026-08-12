"""Add refresh tokens table

Revision ID: 5b1c38be4959
Revises: 64b9cae18b13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "5b1c38be4959"
down_revision: Union[str, Sequence[str], None] = "64b9cae18b13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create refresh_tokens table."""

    op.create_table(
        "refresh_tokens",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),

        sa.Column(
            "token",
            sa.String(length=500),
            nullable=False,
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_refresh_tokens_id",
        "refresh_tokens",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_refresh_tokens_user_id",
        "refresh_tokens",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        "ix_refresh_tokens_token",
        "refresh_tokens",
        ["token"],
        unique=True,
    )


def downgrade() -> None:
    """Drop refresh_tokens table."""

    op.drop_index(
        "ix_refresh_tokens_token",
        table_name="refresh_tokens",
    )

    op.drop_index(
        "ix_refresh_tokens_user_id",
        table_name="refresh_tokens",
    )

    op.drop_index(
        "ix_refresh_tokens_id",
        table_name="refresh_tokens",
    )

    op.drop_table("refresh_tokens")