"""add anomaly indices

Revision ID: 71ce5a37b820
Revises: 3dec55e6129c
Create Date: 2026-06-19 14:40:44.911275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '71ce5a37b820'
down_revision: Union[str, Sequence[str], None] = '3dec55e6129c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "risk_analyses",
        sa.Column(
            "anomaly_indices",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE risk_analyses
        SET anomaly_indices = '[]'::jsonb
        WHERE anomaly_indices IS NULL
        """
    )

    op.alter_column(
        "risk_analyses",
        "anomaly_indices",
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "risk_analyses",
        "anomaly_indices",
    )
