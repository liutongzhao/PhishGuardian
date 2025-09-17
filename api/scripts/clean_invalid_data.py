#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理邮件检测详情表中的异常数据
将无效的紧急程度和重要程度值设置为默认值
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.email_detection_detail import EmailDetectionDetail
from sqlalchemy import text

def clean_invalid_data():
    """清理无效的紧急程度和重要程度数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始清理无效数据...")
            
            # 清理紧急程度异常数据
            print("\n清理紧急程度异常数据:")
            
            # 将非法值设置为默认值'普通'
            result1 = db.session.execute(
                text("UPDATE email_detection_details SET urgency_level = '普通' WHERE urgency_level NOT IN ('普通', '紧急')")
            )
            print(f"- 清理紧急程度异常数据: {result1.rowcount} 条记录")
            
            # 清理重要程度异常数据
            print("\n清理重要程度异常数据:")
            
            # 将非法值设置为默认值'低'
            result2 = db.session.execute(
                text("UPDATE email_detection_details SET importance_level = '低' WHERE importance_level NOT IN ('低', '中', '高')")
            )
            print(f"- 清理重要程度异常数据: {result2.rowcount} 条记录")
            
            # 提交更改
            db.session.commit()
            print("\n数据清理完成！")
            
            # 验证清理结果
            print("\n验证清理结果:")
            urgency_counts = db.session.execute(
                text("SELECT urgency_level, COUNT(*) as count FROM email_detection_details GROUP BY urgency_level")
            ).fetchall()
            
            importance_counts = db.session.execute(
                text("SELECT importance_level, COUNT(*) as count FROM email_detection_details GROUP BY importance_level")
            ).fetchall()
            
            print("紧急程度分布:")
            for row in urgency_counts:
                print(f"  {row[0]}: {row[1]} 条")
                
            print("重要程度分布:")
            for row in importance_counts:
                print(f"  {row[0]}: {row[1]} 条")
                
        except Exception as e:
            print(f"清理数据时发生错误: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    clean_invalid_data()