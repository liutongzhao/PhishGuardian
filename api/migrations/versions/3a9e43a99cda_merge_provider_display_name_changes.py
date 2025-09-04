"""merge provider display name changes

Revision ID: 3a9e43a99cda
Revises: 20241225_add_provider_display_name, 36a0919dd72b
Create Date: 2025-09-04 15:39:12.026735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a9e43a99cda'
down_revision = ('20241225_add_provider_display_name', '36a0919dd72b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
