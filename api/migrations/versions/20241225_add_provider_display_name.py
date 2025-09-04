"""Add provider_display_name field to user_email_bindings

Revision ID: 20241225_add_provider_display_name
Revises: 
Create Date: 2024-12-25 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20241225_add_provider_display_name'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 检查表是否存在
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # 检查 user_email_bindings 表是否存在
    if 'user_email_bindings' not in inspector.get_table_names():
        print("user_email_bindings table does not exist, skipping migration")
        return
    
    # 检查字段是否已存在
    columns = [col['name'] for col in inspector.get_columns('user_email_bindings')]
    
    # 添加新的 provider_display_name 字段（如果不存在）
    if 'provider_display_name' not in columns:
        op.add_column('user_email_bindings', sa.Column('provider_display_name', sa.String(100), nullable=True, comment='邮箱厂商显示名称'))
    else:
        print("provider_display_name column already exists, skipping add column")
    
    # 检查 email_providers 表是否存在，如果存在则更新数据
    if 'email_providers' in inspector.get_table_names():
        # 从 email_providers 表中获取 display_name 并更新到 user_email_bindings 表
        op.execute("""
            UPDATE user_email_bindings 
            SET provider_display_name = (
                SELECT display_name 
                FROM email_providers 
                WHERE email_providers.id = user_email_bindings.provider_id
            )
            WHERE EXISTS (
                SELECT 1 FROM email_providers 
                WHERE email_providers.id = user_email_bindings.provider_id
            )
        """)
    else:
        # 如果 email_providers 表不存在，使用 provider_name 作为默认值
        op.execute("""
            UPDATE user_email_bindings 
            SET provider_display_name = provider_name
        """)
    
    # SQLite不支持ALTER COLUMN SET NOT NULL，跳过此步骤
    # 模型中已定义nullable=False，新记录会自动遵循此约束
    print("Skipping nullable=False constraint for SQLite compatibility")
    
    # 删除旧的 provider_name 字段（如果存在）
    current_columns = [col['name'] for col in inspector.get_columns('user_email_bindings')]
    if 'provider_name' in current_columns:
        op.drop_column('user_email_bindings', 'provider_name')
    else:
        print("provider_name column does not exist, skipping drop column")


def downgrade():
    # 添加回 provider_name 字段
    op.add_column('user_email_bindings', sa.Column('provider_name', sa.String(100), nullable=True, comment='邮箱厂商名称'))
    
    # 从 email_providers 表中获取 name 并更新到 user_email_bindings 表
    op.execute("""
        UPDATE user_email_bindings 
        SET provider_name = (
            SELECT name 
            FROM email_providers 
            WHERE email_providers.id = user_email_bindings.provider_id
        )
    """)
    
    # 将字段设置为非空
    op.alter_column('user_email_bindings', 'provider_name', nullable=False)
    
    # 删除 provider_display_name 字段
    op.drop_column('user_email_bindings', 'provider_display_name')