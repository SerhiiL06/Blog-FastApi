"""empty message

Revision ID: 1f4490f03520
Revises: 995149693a04
Create Date: 2023-11-25 18:59:49.418743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f4490f03520'
down_revision: Union[str, None] = '995149693a04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
