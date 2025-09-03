from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, desc, asc, func, text
from sqlalchemy.orm import Query
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PaginationHelper:
    """分页辅助类"""
    
    @staticmethod
    def paginate_query(query: Query, page: int = 1, per_page: int = 20, 
                      max_per_page: int = 100) -> Dict[str, Any]:
        """对查询进行分页
        
        Args:
            query: SQLAlchemy查询对象
            page: 页码（从1开始）
            per_page: 每页数量
            max_per_page: 每页最大数量
            
        Returns:
            Dict: 分页结果
        """
        # 限制每页数量
        per_page = min(per_page, max_per_page)
        page = max(1, page)
        
        try:
            # 执行分页查询
            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'items': pagination.items,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_prev': pagination.has_prev,
                    'has_next': pagination.has_next,
                    'prev_num': pagination.prev_num,
                    'next_num': pagination.next_num
                }
            }
        except Exception as e:
            logger.error(f'Pagination error: {str(e)}')
            return {
                'items': [],
                'pagination': {
                    'page': 1,
                    'per_page': per_page,
                    'total': 0,
                    'pages': 0,
                    'has_prev': False,
                    'has_next': False,
                    'prev_num': None,
                    'next_num': None
                }
            }
    
    @staticmethod
    def build_pagination_info(page: int, per_page: int, total: int) -> Dict[str, Any]:
        """构建分页信息
        
        Args:
            page: 当前页码
            per_page: 每页数量
            total: 总数量
            
        Returns:
            Dict: 分页信息
        """
        pages = (total + per_page - 1) // per_page  # 向上取整
        
        return {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages,
            'has_prev': page > 1,
            'has_next': page < pages,
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if page < pages else None
        }


class QueryBuilder:
    """查询构建器"""
    
    @staticmethod
    def apply_filters(query: Query, model, filters: Dict[str, Any]) -> Query:
        """应用过滤条件
        
        Args:
            query: SQLAlchemy查询对象
            model: 模型类
            filters: 过滤条件字典
            
        Returns:
            Query: 应用过滤条件后的查询对象
        """
        for field, value in filters.items():
            if value is None:
                continue
            
            # 检查字段是否存在
            if not hasattr(model, field):
                continue
            
            column = getattr(model, field)
            
            # 根据值类型应用不同的过滤条件
            if isinstance(value, dict):
                # 复杂过滤条件
                query = QueryBuilder._apply_complex_filter(query, column, value)
            elif isinstance(value, list):
                # IN条件
                if value:  # 只有非空列表才应用过滤
                    query = query.filter(column.in_(value))
            else:
                # 简单等值过滤
                query = query.filter(column == value)
        
        return query
    
    @staticmethod
    def _apply_complex_filter(query: Query, column, filter_dict: Dict[str, Any]) -> Query:
        """应用复杂过滤条件
        
        Args:
            query: SQLAlchemy查询对象
            column: 数据库列
            filter_dict: 过滤条件字典
            
        Returns:
            Query: 应用过滤条件后的查询对象
        """
        for operator, value in filter_dict.items():
            if operator == 'eq':
                query = query.filter(column == value)
            elif operator == 'ne':
                query = query.filter(column != value)
            elif operator == 'gt':
                query = query.filter(column > value)
            elif operator == 'gte':
                query = query.filter(column >= value)
            elif operator == 'lt':
                query = query.filter(column < value)
            elif operator == 'lte':
                query = query.filter(column <= value)
            elif operator == 'like':
                query = query.filter(column.like(f'%{value}%'))
            elif operator == 'ilike':
                query = query.filter(column.ilike(f'%{value}%'))
            elif operator == 'in':
                if isinstance(value, list) and value:
                    query = query.filter(column.in_(value))
            elif operator == 'not_in':
                if isinstance(value, list) and value:
                    query = query.filter(~column.in_(value))
            elif operator == 'is_null':
                if value:
                    query = query.filter(column.is_(None))
                else:
                    query = query.filter(column.isnot(None))
            elif operator == 'between':
                if isinstance(value, list) and len(value) == 2:
                    query = query.filter(column.between(value[0], value[1]))
        
        return query
    
    @staticmethod
    def apply_search(query: Query, model, search_term: str, 
                    search_fields: List[str]) -> Query:
        """应用搜索条件
        
        Args:
            query: SQLAlchemy查询对象
            model: 模型类
            search_term: 搜索词
            search_fields: 搜索字段列表
            
        Returns:
            Query: 应用搜索条件后的查询对象
        """
        if not search_term or not search_fields:
            return query
        
        search_conditions = []
        
        for field in search_fields:
            if hasattr(model, field):
                column = getattr(model, field)
                # 使用ILIKE进行不区分大小写的模糊搜索
                search_conditions.append(column.ilike(f'%{search_term}%'))
        
        if search_conditions:
            query = query.filter(or_(*search_conditions))
        
        return query
    
    @staticmethod
    def apply_sorting(query: Query, model, sort_by: str = None, 
                     sort_order: str = 'asc') -> Query:
        """应用排序
        
        Args:
            query: SQLAlchemy查询对象
            model: 模型类
            sort_by: 排序字段
            sort_order: 排序顺序 ('asc' 或 'desc')
            
        Returns:
            Query: 应用排序后的查询对象
        """
        if not sort_by or not hasattr(model, sort_by):
            # 默认按ID降序排序
            if hasattr(model, 'id'):
                return query.order_by(desc(model.id))
            return query
        
        column = getattr(model, sort_by)
        
        if sort_order.lower() == 'desc':
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))
        
        return query
    
    @staticmethod
    def apply_date_range(query: Query, model, date_field: str, 
                        start_date: datetime = None, 
                        end_date: datetime = None) -> Query:
        """应用日期范围过滤
        
        Args:
            query: SQLAlchemy查询对象
            model: 模型类
            date_field: 日期字段名
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            Query: 应用日期过滤后的查询对象
        """
        if not hasattr(model, date_field):
            return query
        
        column = getattr(model, date_field)
        
        if start_date:
            query = query.filter(column >= start_date)
        
        if end_date:
            # 如果结束日期没有时间部分，添加23:59:59
            if end_date.time() == end_date.min.time():
                end_date = end_date.replace(hour=23, minute=59, second=59)
            query = query.filter(column <= end_date)
        
        return query


class DatabaseHelper:
    """数据库辅助类"""
    
    @staticmethod
    def safe_commit(db: SQLAlchemy, rollback_on_error: bool = True) -> Tuple[bool, Optional[str]]:
        """安全提交数据库事务
        
        Args:
            db: SQLAlchemy实例
            rollback_on_error: 出错时是否回滚
            
        Returns:
            Tuple[bool, Optional[str]]: (是否成功, 错误信息)
        """
        try:
            db.session.commit()
            return True, None
        except Exception as e:
            logger.error(f'Database commit error: {str(e)}')
            if rollback_on_error:
                db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def bulk_insert(db: SQLAlchemy, model_class, data_list: List[Dict[str, Any]], 
                   batch_size: int = 1000) -> Tuple[bool, int, Optional[str]]:
        """批量插入数据
        
        Args:
            db: SQLAlchemy实例
            model_class: 模型类
            data_list: 数据列表
            batch_size: 批次大小
            
        Returns:
            Tuple[bool, int, Optional[str]]: (是否成功, 插入数量, 错误信息)
        """
        if not data_list:
            return True, 0, None
        
        try:
            inserted_count = 0
            
            for i in range(0, len(data_list), batch_size):
                batch = data_list[i:i + batch_size]
                
                # 创建模型实例
                instances = [model_class(**data) for data in batch]
                
                # 批量添加
                db.session.add_all(instances)
                db.session.commit()
                
                inserted_count += len(instances)
            
            return True, inserted_count, None
            
        except Exception as e:
            logger.error(f'Bulk insert error: {str(e)}')
            db.session.rollback()
            return False, 0, str(e)
    
    @staticmethod
    def bulk_update(db: SQLAlchemy, model_class, updates: List[Dict[str, Any]], 
                   id_field: str = 'id') -> Tuple[bool, int, Optional[str]]:
        """批量更新数据
        
        Args:
            db: SQLAlchemy实例
            model_class: 模型类
            updates: 更新数据列表，每个字典必须包含id_field
            id_field: ID字段名
            
        Returns:
            Tuple[bool, int, Optional[str]]: (是否成功, 更新数量, 错误信息)
        """
        if not updates:
            return True, 0, None
        
        try:
            updated_count = 0
            
            for update_data in updates:
                if id_field not in update_data:
                    continue
                
                record_id = update_data.pop(id_field)
                
                # 执行更新
                result = db.session.query(model_class).filter(
                    getattr(model_class, id_field) == record_id
                ).update(update_data)
                
                updated_count += result
            
            db.session.commit()
            return True, updated_count, None
            
        except Exception as e:
            logger.error(f'Bulk update error: {str(e)}')
            db.session.rollback()
            return False, 0, str(e)
    
    @staticmethod
    def get_table_stats(db: SQLAlchemy, model_class) -> Dict[str, Any]:
        """获取表统计信息
        
        Args:
            db: SQLAlchemy实例
            model_class: 模型类
            
        Returns:
            Dict: 统计信息
        """
        try:
            total_count = db.session.query(model_class).count()
            
            stats = {
                'total_count': total_count,
                'table_name': model_class.__tablename__
            }
            
            # 如果有created_at字段，获取最新和最旧的记录时间
            if hasattr(model_class, 'created_at'):
                latest = db.session.query(func.max(model_class.created_at)).scalar()
                oldest = db.session.query(func.min(model_class.created_at)).scalar()
                
                stats.update({
                    'latest_record': latest.isoformat() if latest else None,
                    'oldest_record': oldest.isoformat() if oldest else None
                })
            
            # 如果有updated_at字段，获取最近更新时间
            if hasattr(model_class, 'updated_at'):
                last_updated = db.session.query(func.max(model_class.updated_at)).scalar()
                stats['last_updated'] = last_updated.isoformat() if last_updated else None
            
            return stats
            
        except Exception as e:
            logger.error(f'Get table stats error: {str(e)}')
            return {
                'total_count': 0,
                'table_name': model_class.__tablename__,
                'error': str(e)
            }
    
    @staticmethod
    def execute_raw_query(db: SQLAlchemy, query: str, 
                         params: Dict[str, Any] = None) -> Tuple[bool, Any, Optional[str]]:
        """执行原始SQL查询
        
        Args:
            db: SQLAlchemy实例
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            Tuple[bool, Any, Optional[str]]: (是否成功, 结果, 错误信息)
        """
        try:
            result = db.session.execute(text(query), params or {})
            
            # 如果是SELECT查询，获取结果
            if query.strip().upper().startswith('SELECT'):
                rows = result.fetchall()
                # 转换为字典列表
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in rows]
                return True, data, None
            else:
                # 对于INSERT/UPDATE/DELETE，返回影响的行数
                db.session.commit()
                return True, result.rowcount, None
                
        except Exception as e:
            logger.error(f'Raw query error: {str(e)}')
            db.session.rollback()
            return False, None, str(e)
    
    @staticmethod
    def cleanup_old_records(db: SQLAlchemy, model_class, date_field: str, 
                           days_to_keep: int = 30) -> Tuple[bool, int, Optional[str]]:
        """清理旧记录
        
        Args:
            db: SQLAlchemy实例
            model_class: 模型类
            date_field: 日期字段名
            days_to_keep: 保留天数
            
        Returns:
            Tuple[bool, int, Optional[str]]: (是否成功, 删除数量, 错误信息)
        """
        if not hasattr(model_class, date_field):
            return False, 0, f'Field {date_field} not found in model'
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            column = getattr(model_class, date_field)
            
            # 删除旧记录
            deleted_count = db.session.query(model_class).filter(
                column < cutoff_date
            ).delete()
            
            db.session.commit()
            
            logger.info(f'Cleaned up {deleted_count} old records from {model_class.__tablename__}')
            return True, deleted_count, None
            
        except Exception as e:
            logger.error(f'Cleanup old records error: {str(e)}')
            db.session.rollback()
            return False, 0, str(e)