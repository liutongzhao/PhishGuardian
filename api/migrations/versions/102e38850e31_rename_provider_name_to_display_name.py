"""rename_provider_name_to_display_name

Revision ID: 102e38850e31
Revises: 3a9e43a99cda
Create Date: 2025-09-04 15:45:59.351621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '102e38850e31'
down_revision = '3a9e43a99cda'
branch_labels = None
depends_on = None


def upgrade():
    # 检查表是否存在
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'user_email_bindings' not in inspector.get_table_names():
        print("user_email_bindings table does not exist, skipping migration")
        return
    
    # 检查 provider_display_name 字段是否已存在
    columns = [col['name'] for col in inspector.get_columns('user_email_bindings')]
    
    if 'provider_display_name' not in columns:
        # 添加新的 provider_display_name 字段
        op.add_column('user_email_bindings', sa.Column('provider_display_name', sa.String(100), nullable=True, comment='邮箱厂商显示名称'))
        print("Added provider_display_name column")
    else:
        print("provider_display_name column already exists")
    
    # 更新数据：将 provider_name 的值替换为对应 email_providers 表中的 display_name
    if 'provider_name' in columns and 'provider_display_name' in [col['name'] for col in inspector.get_columns('user_email_bindings')]:
        if 'email_providers' in inspector.get_table_names():
            conn.execute(sa.text("""
                UPDATE user_email_bindings 
                SET provider_display_name = (
                    SELECT ep.display_name 
                    FROM email_providers ep 
                    WHERE ep.name = user_email_bindings.provider_name
                )
                WHERE EXISTS (
                    SELECT 1 FROM email_providers ep 
                    WHERE ep.name = user_email_bindings.provider_name
                )
            """))
        else:
            # 如果 email_providers 表不存在，使用 provider_name 作为默认值
            conn.execute(sa.text("""
                UPDATE user_email_bindings 
                SET provider_display_name = provider_name
            """))
        print("Updated provider_display_name with data from provider_name")
    else:
        print("Skipping data update - required columns not found or already processed")
    
    # 将字段设置为非空（SQLite不支持直接修改，跳过）
    print("Skipping nullable=False constraint for SQLite compatibility")
    
    # 删除旧的 provider_name 字段（如果存在）
    if 'provider_name' in columns:
        op.drop_column('user_email_bindings', 'provider_name')
        print("Dropped provider_name column")
    else:
        print("provider_name column does not exist, skipping drop")


def downgrade():
    # 添加回 provider_name 字段
    op.add_column('user_email_bindings', sa.Column('provider_name', sa.String(100), nullable=True))
    
    # 从 provider_display_name 恢复数据到 provider_name
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'email_providers' in inspector.get_table_names():
        conn.execute(sa.text("""
            UPDATE user_email_bindings 
            SET provider_name = (
                SELECT ep.name 
                FROM email_providers ep 
                WHERE ep.display_name = user_email_bindings.provider_display_name
            )
            WHERE EXISTS (
                SELECT 1 FROM email_providers ep 
                WHERE ep.display_name = user_email_bindings.provider_display_name
            )
        """))
    else:
        conn.execute(sa.text("""
            UPDATE user_email_bindings 
            SET provider_name = provider_display_name
        """))
    
    # 删除 provider_display_name 字段
    op.drop_column('user_email_bindings', 'provider_display_name')
