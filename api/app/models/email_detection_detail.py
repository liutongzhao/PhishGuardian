from datetime import datetime
import pytz
from enum import Enum
from app import db


class UrgencyLevel(Enum):
    """紧急程度枚举"""
    NORMAL = '普通'    # 普通
    URGENT = '紧急'    # 紧急


class ImportanceLevel(Enum):
    """重要程度枚举"""
    LOW = '低'         # 低
    MEDIUM = '中'      # 中
    HIGH = '高'        # 高


class DetectionStatus(Enum):
    """检测状态枚举"""
    NOT_DETECTED = 0   # 未检测（默认状态）
    DETECTING = 1      # 检测中
    COMPLETED = 2      # 检测完成
    NO_NEED = 3        # 无需检测


class EmailDetectionDetail(db.Model):
    """邮件检测详情模型"""
    __tablename__ = 'email_detection_details'
    
    # 基础字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键ID')
    email_id = db.Column(db.Integer, nullable=False, index=True, comment='邮件ID，关联emails表')
    
    # 权重字段
    content_weight = db.Column(db.Float, default=0.0, nullable=False, comment='正文检测权重')
    metadata_weight = db.Column(db.Float, default=0.0, nullable=False, comment='元数据检测权重')
    url_weight = db.Column(db.Float, default=0.0, nullable=False, comment='URL检测权重')
    
    # 检测阶段字段
    detection_stage = db.Column(db.Integer, default=1, nullable=False, comment='检测阶段：1-第一阶段，2-第二阶段，3-第三阶段，4-第四阶段')
    parallel_detection_completed = db.Column(db.Boolean, default=False, nullable=False, comment='第二阶段并行检测是否全部完成')
    
    # 检测状态字段
    content_detection_status = db.Column(db.Integer, default=DetectionStatus.NOT_DETECTED.value, nullable=False, comment='正文检测状态：0-未检测，1-检测中，2-检测完成，3-无需检测')
    url_detection_status = db.Column(db.Integer, default=DetectionStatus.NOT_DETECTED.value, nullable=False, comment='URL检测状态：0-未检测，1-检测中，2-检测完成，3-无需检测')
    metadata_detection_status = db.Column(db.Integer, default=DetectionStatus.NOT_DETECTED.value, nullable=False, comment='元数据检测状态：0-未检测，1-检测中，2-检测完成，3-无需检测')
    
    # 钓鱼概率字段
    content_phishing_probability = db.Column(db.Float, default=0.0, nullable=False, comment='正文检测为钓鱼的概率')
    url_phishing_probability = db.Column(db.Float, default=0.0, nullable=False, comment='URL检测为钓鱼的概率')
    metadata_phishing_probability = db.Column(db.Float, default=0.0, nullable=False, comment='元数据检测为钓鱼的概率')
    
    # 置信度字段
    content_confidence = db.Column(db.Float, default=0.0, nullable=False, comment='正文检测置信度')
    url_confidence = db.Column(db.Float, default=0.0, nullable=False, comment='URL检测置信度')
    metadata_confidence = db.Column(db.Float, default=0.0, nullable=False, comment='元数据检测置信度')
    
    # 检测结果字段
    content_is_phishing = db.Column(db.Boolean, default=False, nullable=False, comment='正文是否为钓鱼')
    url_is_phishing = db.Column(db.Boolean, default=False, nullable=False, comment='URL是否为钓鱼')
    metadata_is_phishing = db.Column(db.Boolean, default=False, nullable=False, comment='元数据是否为钓鱼')
    
    # 检测原因字段
    content_reason = db.Column(db.Text, nullable=True, comment='正文检测原因')
    url_reason = db.Column(db.Text, nullable=True, comment='URL检测原因')
    metadata_reason = db.Column(db.Text, nullable=True, comment='元数据检测原因')
    
    # 最终结果字段
    final_fusion_score = db.Column(db.Float, default=0.0, nullable=False, comment='最终融合分数')
    final_is_phishing = db.Column(db.Boolean, default=False, nullable=False, comment='最终判定结果（是否为钓鱼）')
    final_reason = db.Column(db.Text, nullable=True, comment='最终判定理由')
    
    # 邮件分析字段
    email_summary = db.Column(db.Text, nullable=True, comment='邮件摘要')
    email_type = db.Column(db.String(100), nullable=True, comment='邮件类型（可为任意字符串）')
    urgency_level = db.Column(db.String(20), default=UrgencyLevel.NORMAL.value, nullable=False, comment='紧急程度')
    importance_level = db.Column(db.String(20), default=ImportanceLevel.MEDIUM.value, nullable=False, comment='重要程度')
    
    # 日程相关字段
    need_schedule = db.Column(db.Integer, default=0, nullable=False, comment='是否需要日程：0-不需要，1-需要')
    schedule_name = db.Column(db.String(255), nullable=True, comment='日程名称')
    schedule_time = db.Column(db.DateTime, nullable=True, comment='日程时间')
    
    # 保留字段
    reserved_field1 = db.Column(db.Text, nullable=True, comment='保留字段1')
    reserved_field2 = db.Column(db.Text, nullable=True, comment='保留字段2')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), onupdate=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False, comment='更新时间')
    
    def __repr__(self):
        return f'<EmailDetectionDetail {self.id}: Email {self.email_id}>'
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'email_id': self.email_id,
            
            # 权重信息
            'content_weight': self.content_weight,
            'metadata_weight': self.metadata_weight,
            'url_weight': self.url_weight,
            
            # 钓鱼概率
            'content_phishing_probability': self.content_phishing_probability,
            'url_phishing_probability': self.url_phishing_probability,
            'metadata_phishing_probability': self.metadata_phishing_probability,
            
            # 置信度
            'content_confidence': self.content_confidence,
            'url_confidence': self.url_confidence,
            'metadata_confidence': self.metadata_confidence,
            
            # 检测阶段
            'detection_stage': self.detection_stage,
            'parallel_detection_completed': self.parallel_detection_completed,
            
            # 检测状态
            'content_detection_status': self.content_detection_status,
            'url_detection_status': self.url_detection_status,
            'metadata_detection_status': self.metadata_detection_status,
            
            # 检测结果
            'content_is_phishing': self.content_is_phishing,
            'url_is_phishing': self.url_is_phishing,
            'metadata_is_phishing': self.metadata_is_phishing,
            
            # 检测原因
            'content_reason': self.content_reason,
            'url_reason': self.url_reason,
            'metadata_reason': self.metadata_reason,
            
            # 最终结果
            'final_fusion_score': self.final_fusion_score,
            'final_is_phishing': self.final_is_phishing,
            'final_reason': self.final_reason,
            
            # 邮件分析
            'email_summary': self.email_summary,
            'email_type': self.email_type,
            'urgency_level': self.urgency_level,
            'importance_level': self.importance_level,
            
            # 日程相关
            'need_schedule': self.need_schedule,
            'schedule_name': self.schedule_name,
            'schedule_time': self.schedule_time.isoformat() if self.schedule_time else None,
            
            # 保留字段
            'reserved_field1': self.reserved_field1,
            'reserved_field2': self.reserved_field2,
            
            # 时间戳
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_email_id(cls, email_id):
        """根据邮件ID查找检测详情"""
        return cls.query.filter_by(email_id=email_id).first()
    
    @classmethod
    def get_phishing_emails(cls, limit=None):
        """获取钓鱼邮件检测详情"""
        query = cls.query.filter_by(final_is_phishing=True)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    @classmethod
    def get_safe_emails(cls, limit=None):
        """获取安全邮件检测详情"""
        query = cls.query.filter_by(final_is_phishing=False)
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_content_detection(self, weight, probability, confidence, is_phishing, reason):
        """更新正文检测结果"""
        self.content_weight = weight
        self.content_phishing_probability = probability
        self.content_confidence = confidence
        self.content_is_phishing = is_phishing
        self.content_reason = reason
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    def update_url_detection(self, weight, probability, confidence, is_phishing, reason):
        """更新URL检测结果"""
        self.url_weight = weight
        self.url_phishing_probability = probability
        self.url_confidence = confidence
        self.url_is_phishing = is_phishing
        self.url_reason = reason
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    def update_metadata_detection(self, weight, probability, confidence, is_phishing, reason):
        """更新元数据检测结果"""
        self.metadata_weight = weight
        self.metadata_phishing_probability = probability
        self.metadata_confidence = confidence
        self.metadata_is_phishing = is_phishing
        self.metadata_reason = reason
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))
    
    def update_final_result(self, fusion_score, is_phishing, reason):
        """更新最终检测结果"""
        self.final_fusion_score = fusion_score
        self.final_is_phishing = is_phishing
        self.final_reason = reason
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))
        self.reserved_field1 = '1'
        self.detection_stage = 4
        self.reserved_field2 = '0'
    
    def update_email_analysis(self, summary, email_type, urgency_level, importance_level):
        """更新邮件分析结果"""
        self.email_summary = summary
        self.email_type = email_type
        self.urgency_level = urgency_level
        self.importance_level = importance_level
        self.updated_at = datetime.now(pytz.timezone('Asia/Shanghai'))