"""Add user profile model

Revision ID: dc25efd5d867
Revises:
Create Date: 2024-12-26 18:22:18.359904

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc25efd5d867"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ("user_profile",)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userprofile",
        sa.Column(
            "user_id", sqlmodel.sql.sqltypes.AutoString(length=30), nullable=False
        ),
        sa.Column(
            "last_name", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False
        ),
        sa.Column(
            "first_name", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False
        ),
        sa.Column(
            "patronymic", sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("userprofile")
    # ### end Alembic commands ###
