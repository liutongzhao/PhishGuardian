#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新邮件检测详情表中的紧急程度和重要程度数据
将英文枚举值转换为中文文字表述
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.email_detection_detail import EmailDetectionDetail
from sqlalchemy import text

def update_urgency_importance_data():
    """更新紧急程度和重要程度数据"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始更新紧急程度和重要程度数据...")
            
            # 更新紧急程度数据
            print("\n更新紧急程度数据:")
            
            # 将 'low' 改为 '普通'
            result1 = db.session.execute(
                text("UPDATE email_detection_details SET urgency_level = '普通' WHERE urgency_level = 'low'")
            )
            print(f"- 将 'low' 改为 '普通': {result1.rowcount} 条记录")
            
            # 将 'medium' 改为 '紧急'
            result2 = db.session.execute(
                text("UPDATE email_detection_details SET urgency_level = '紧急' WHERE urgency_level = 'medium'")
            )
            print(f"- 将 'medium' 改为 '紧急': {result2.rowcount} 条记录")
            
            # 将 'urgent' 改为 '紧急'
            result3 = db.session.execute(
                text("UPDATE email_detection_details SET urgency_level = '紧急' WHERE urgency_level = 'urgent'")
            )
            print(f"- 将 'urgent' 改为 '紧急': {result3.rowcount} 条记录")
            
            # 将 'high' 改为 '紧急'
            result4 = db.session.execute(
                text("UPDATE email_detection_details SET urgency_level = '紧急' WHERE urgency_level = 'high'")
            )
            print(f"- 将 'high' 改为 '紧急': {result4.rowcount} 条记录")
            
            # 更新重要程度数据
            print("\n更新重要程度数据:")
            
            # 将 'low' 改为 '低'
            result5 = db.session.execute(
                text("UPDATE email_detection_details SET importance_level = '低' WHERE importance_level = 'low'")
            )
            print(f"- 将 'low' 改为 '低': {result5.rowcount} 条记录")
            
            # 将 'medium' 改为 '中'
            result6 = db.session.execute(
                text("UPDATE email_detection_details SET importance_level = '中' WHERE importance_level = 'medium'")
            )
            print(f"- 将 'medium' 改为 '中': {result6.rowcount} 条记录")
            
            # 将 'high' 改为 '高'
            result7 = db.session.execute(
                text("UPDATE email_detection_details SET importance_level = '高' WHERE importance_level = 'high'")
            )
            print(f"- 将 'high' 改为 '高': {result7.rowcount} 条记录")
            
            # 将 'critical' 改为 '高'
            result8 = db.session.execute(
                text("UPDATE email_detection_details SET importance_level = '高' WHERE importance_level = 'critical'")
            )
            print(f"- 将 'critical' 改为 '高': {result8.rowcount} 条记录")
            
            # 提交更改
            db.session.commit()
            print("\n数据更新完成！")
            
            # 验证更新结果
            print("\n验证更新结果:")
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
            print(f"更新数据时发生错误: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    update_urgency_importance_data()