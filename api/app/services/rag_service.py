from typing import Dict, List, Any, Optional
from datetime import datetime
import pytz
from app.models.user_email_binding import UserEmailBinding
from app.models.email import Email, EmailDetectionStatus
from app.models.email_detection_detail import EmailDetectionDetail, UrgencyLevel, ImportanceLevel, DetectionStatus
from app.services.vector_service import get_vector_service
from app import db
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """RAG知识库服务类"""
    
    @staticmethod
    def get_user_knowledge_text(user_id: int) -> Dict[str, Any]:
        """
        获取用户的知识库文本数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 包含用户知识库文本的字典
        """
        try:
            # 1. 获取用户邮箱绑定信息
            bindings = UserEmailBinding.get_user_bindings(user_id, active_only=False)
            
            # 2. 获取用户所有邮件
            emails = Email.get_user_emails(user_id, active_only=False)
            
            # 3. 组织知识库文本
            knowledge_text = RAGService._organize_knowledge_text(user_id, bindings, emails)
            
            # 存储到向量数据库
            vector_service = get_vector_service()
            vector_stored = vector_service.store_knowledge_vectors(
                user_id=user_id,
                knowledge_text=knowledge_text,
                metadata={
                    'bindings_count': len(bindings),
                    'emails_count': len(emails),
                    'source': 'user_knowledge_base'
                }
            )
            
            return {
                'success': True,
                'user_id': user_id,
                'knowledge_text': knowledge_text,
                'bindings_count': len(bindings),
                'emails_count': len(emails),
                'vector_stored': vector_stored,
                'generated_at': datetime.now(pytz.timezone('Asia/Shanghai')).isoformat()
            }
            
        except Exception as e:
            logging.error(f"获取用户知识库文本失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'user_id': user_id
            }
    
    @staticmethod
    def search_knowledge_base(user_id: int, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        在用户知识库中进行语义搜索
        
        Args:
            user_id: 用户ID
            query: 搜索查询
            top_k: 返回结果数量
            
        Returns:
            Dict: 搜索结果
        """
        try:
            vector_service = get_vector_service()
            search_results = vector_service.search_knowledge_base(
                user_id=user_id,
                query=query,
                top_k=top_k
            )
            
            return {
                'success': True,
                'user_id': user_id,
                'query': query,
                'results': search_results,
                'results_count': len(search_results) if search_results else 0,
                'searched_at': datetime.now(pytz.timezone('Asia/Shanghai')).isoformat()
            }
            
        except Exception as e:
            logging.error(f"搜索用户知识库失败: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'user_id': user_id,
                'query': query
            }
    
    @staticmethod
    def _organize_knowledge_text(user_id: int, bindings: List[UserEmailBinding], emails: List[Email]) -> str:
        """
        组织用户知识库文本
        
        Args:
            user_id: 用户ID
            bindings: 邮箱绑定列表
            emails: 邮件列表
            
        Returns:
            str: 组织好的知识库文本
        """
        text_parts = []
        
        # 添加用户基本信息
        text_parts.append(f"=== 用户 {user_id} 的知识库信息 ===")
        text_parts.append(f"生成时间: {datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')}")
        text_parts.append("")
        
        # 1. 邮箱绑定信息部分
        text_parts.append("=== 邮箱绑定信息 ===")
        if not bindings:
            text_parts.append("该用户暂未绑定任何邮箱。")
        else:
            text_parts.append(f"该用户共绑定了 {len(bindings)} 个邮箱账户:")
            text_parts.append("")
            
            for i, binding in enumerate(bindings, 1):
                text_parts.append(f"邮箱绑定 {i}:")
                text_parts.append(f"  - 邮箱地址: {binding.email_address}")
                text_parts.append(f"  - 邮箱厂商: {binding.provider_display_name}")
                text_parts.append(f"  - IMAP服务器: {binding.imap_server}")
                text_parts.append(f"  - SMTP服务器: {binding.smtp_server}")
                text_parts.append(f"  - 绑定状态: {'启用' if binding.is_active else '禁用'}")
                text_parts.append(f"  - 是否删除: {'是' if binding.is_deleted else '否'}")
                text_parts.append(f"  - 最新邮件UID: {binding.last_uid or '无'}")
                text_parts.append(f"  - 绑定时间: {binding.created_at.strftime('%Y-%m-%d %H:%M:%S') if binding.created_at else '未知'}")
                text_parts.append(f"  - 更新时间: {binding.updated_at.strftime('%Y-%m-%d %H:%M:%S') if binding.updated_at else '未知'}")
                text_parts.append("")
        
        text_parts.append("")
        
        # 2. 邮件信息部分
        text_parts.append("=== 邮件信息 ===")
        if not emails:
            text_parts.append("该用户暂无任何邮件记录。")
        else:
            # 统计信息
            total_emails = len(emails)
            pending_emails = len([e for e in emails if e.detection_status == EmailDetectionStatus.PENDING.value])
            detecting_emails = len([e for e in emails if e.detection_status == EmailDetectionStatus.DETECTING.value])
            success_emails = len([e for e in emails if e.detection_status == EmailDetectionStatus.SUCCESS.value])
            failed_emails = len([e for e in emails if e.detection_status == EmailDetectionStatus.FAILED.value])
            deleted_emails = len([e for e in emails if e.is_deleted])
            
            text_parts.append(f"该用户共有 {total_emails} 封邮件:")
            text_parts.append(f"  - 待检测邮件: {pending_emails} 封")
            text_parts.append(f"  - 检测中邮件: {detecting_emails} 封")
            text_parts.append(f"  - 检测成功邮件: {success_emails} 封")
            text_parts.append(f"  - 检测失败邮件: {failed_emails} 封")
            text_parts.append(f"  - 已删除邮件: {deleted_emails} 封")
            text_parts.append("")
            
            # 详细邮件信息
            text_parts.append("详细邮件列表:")
            text_parts.append("")
            
            for i, email in enumerate(emails, 1):
                # 获取检测详情
                detection_detail = EmailDetectionDetail.find_by_email_id(email.id)
                
                text_parts.append(f"邮件 {i} (ID: {email.id}):")
                text_parts.append(f"  基本信息:")
                text_parts.append(f"    - 邮件UID: {email.email_uid}")
                text_parts.append(f"    - 主题: {email.subject or '无主题'}")
                text_parts.append(f"    - 发送方: {email.sender or '未知'}")
                text_parts.append(f"    - 邮件日期: {email.email_date.strftime('%Y-%m-%d %H:%M:%S') if email.email_date else '未知'}")
                text_parts.append(f"    - 邮箱地址: {email.email_address}")
                text_parts.append(f"    - 邮箱厂商: {email.provider_display_name}")
                # 检测状态转换
                status_map = {
                    'PENDING': '等待检测',
                    'DETECTING': '检测中',
                    'SUCCESS': '检测完成',
                    'FAILED': '检测失败'
                }
                status_display = status_map.get(EmailDetectionStatus(email.detection_status).name, '未知状态')
                text_parts.append(f"    - 检测状态: {status_display}")
                text_parts.append(f"    - 是否删除: {'是' if email.is_deleted else '否'}")
                text_parts.append(f"    - 创建时间: {email.created_at.strftime('%Y-%m-%d %H:%M:%S') if email.created_at else '未知'}")
                
                # 邮件完整内容
                if email.content:
                    text_parts.append(f"    - 邮件内容: {email.content}")
                else:
                    text_parts.append(f"    - 邮件内容: 无内容")
                
                # 检测详情信息
                if detection_detail:
                    text_parts.append(f"  检测详情:")
                    text_parts.append(f"    - 检测阶段: 第{detection_detail.detection_stage}阶段")
                    text_parts.append(f"    - 并行检测完成: {'是' if detection_detail.parallel_detection_completed else '否'}")
                    
                    # 各项检测状态转换
                    detection_status_map = {
                        'NOT_DETECTED': '未检测',
                        'DETECTING': '检测中',
                        'COMPLETED': '检测完成',
                        'FAILED': '检测失败',
                        'SKIPPED': '跳过检测'
                    }
                    
                    content_status = detection_status_map.get(DetectionStatus(detection_detail.content_detection_status).name, '未知状态')
                    url_status = detection_status_map.get(DetectionStatus(detection_detail.url_detection_status).name, '未知状态')
                    metadata_status = detection_status_map.get(DetectionStatus(detection_detail.metadata_detection_status).name, '未知状态')
                    
                    text_parts.append(f"    - 邮件正文检测状态: {content_status}")
                    text_parts.append(f"    - 邮件URL检测状态: {url_status}")
                    text_parts.append(f"    - 邮件元数据检测状态: {metadata_status}")
                    
                    # 检测权重详细解释
                    text_parts.append(f"    - 正文检测权重: {detection_detail.content_weight} (该权重表示正文检测结果在最终判定中的重要程度)")
                    text_parts.append(f"    - URL检测权重: {detection_detail.url_weight} (该权重表示URL检测结果在最终判定中的重要程度)")
                    text_parts.append(f"    - 元数据检测权重: {detection_detail.metadata_weight} (该权重表示元数据检测结果在最终判定中的重要程度)")
                    
                    # 钓鱼概率详细解释
                    text_parts.append(f"    - 正文钓鱼概率: {detection_detail.content_phishing_probability} (通过对邮件正文内容的分析检测，该邮件正文部分为钓鱼邮件的概率)")
                    text_parts.append(f"    - URL钓鱼概率: {detection_detail.url_phishing_probability} (通过对邮件中包含的URL链接的检测，这些URL为恶意钓鱼链接的概率)")
                    text_parts.append(f"    - 元数据钓鱼概率: {detection_detail.metadata_phishing_probability} (通过对邮件元数据信息的分析，该邮件元数据部分显示钓鱼特征的概率)")
                    
                    # 置信度详细解释
                    text_parts.append(f"    - 正文检测置信度: {detection_detail.content_confidence} (系统对正文检测结果准确性的信心程度，数值越高表示结果越可靠)")
                    text_parts.append(f"    - URL检测置信度: {detection_detail.url_confidence} (系统对URL检测结果准确性的信心程度，数值越高表示结果越可靠)")
                    text_parts.append(f"    - 元数据检测置信度: {detection_detail.metadata_confidence} (系统对元数据检测结果准确性的信心程度，数值越高表示结果越可靠)")
                    
                    # 检测结果详细解释
                    text_parts.append(f"    - 正文检测结果: 通过对邮件正文内容的深度分析，判定该正文部分{'是' if detection_detail.content_is_phishing else '不是'}钓鱼邮件")
                    text_parts.append(f"    - URL检测结果: 通过对邮件中包含的URL链接进行安全检测，判定这些URL{'是' if detection_detail.url_is_phishing else '不是'}恶意钓鱼链接")
                    text_parts.append(f"    - 元数据检测结果: 通过对邮件头部信息、发送方信息等元数据的分析，判定该邮件的元数据{'显示' if detection_detail.metadata_is_phishing else '未显示'}钓鱼特征")
                    
                    # 最终结果详细解释
                    text_parts.append(f"    - 最终融合分数: {detection_detail.final_fusion_score} (综合正文、URL、元数据三个维度的检测结果，经过权重计算得出的最终风险评分)")
                    text_parts.append(f"    - 最终检测结论: 经过多维度综合分析，该邮件{'被判定为钓鱼邮件' if detection_detail.final_is_phishing else '被判定为安全邮件'}")
                    
                    # 邮件分析完整信息
                    if detection_detail.email_summary:
                        text_parts.append(f"    - 邮件内容摘要: {detection_detail.email_summary}")
                    
                    if detection_detail.email_type:
                        text_parts.append(f"    - 邮件类型分类: {detection_detail.email_type}")
                    
                    # 紧急程度和重要程度转换
                    urgency_map = {
                        'LOW': '低紧急',
                        'MEDIUM': '中等紧急', 
                        'HIGH': '高紧急',
                        'CRITICAL': '极紧急'
                    }
                    importance_map = {
                        'LOW': '低重要',
                        'MEDIUM': '中等重要',
                        'HIGH': '高重要', 
                        'CRITICAL': '极重要'
                    }
                    
                    urgency_display = urgency_map.get(detection_detail.urgency_level, detection_detail.urgency_level)
                    importance_display = importance_map.get(detection_detail.importance_level, detection_detail.importance_level)
                    
                    text_parts.append(f"    - 邮件紧急程度: {urgency_display} (表示该邮件需要处理的紧急程度)")
                    text_parts.append(f"    - 邮件重要程度: {importance_display} (表示该邮件内容的重要性级别)")
                    
                    # 检测原因完整信息
                    if detection_detail.content_reason:
                        text_parts.append(f"    - 正文检测详细原因: {detection_detail.content_reason}")
                    
                    if detection_detail.url_reason:
                        text_parts.append(f"    - URL检测详细原因: {detection_detail.url_reason}")
                    
                    if detection_detail.metadata_reason:
                        text_parts.append(f"    - 元数据检测详细原因: {detection_detail.metadata_reason}")
                    
                    if detection_detail.final_reason:
                        text_parts.append(f"    - 最终判定详细理由: {detection_detail.final_reason}")
                    
                    text_parts.append(f"    - 检测详情创建时间: {detection_detail.created_at.strftime('%Y-%m-%d %H:%M:%S') if detection_detail.created_at else '未知'}")
                    text_parts.append(f"    - 检测详情更新时间: {detection_detail.updated_at.strftime('%Y-%m-%d %H:%M:%S') if detection_detail.updated_at else '未知'}")
                else:
                    text_parts.append(f"  检测详情: 该邮件尚未进行检测或检测详情不存在")
                
                text_parts.append("")
        
        text_parts.append("=== 知识库信息结束 ===")
        
        return "\n".join(text_parts)
    
    @staticmethod
    def print_user_knowledge(user_id: int) -> None:
        """
        打印用户知识库文本到控制台
        
        Args:
            user_id: 用户ID
        """
        result = RAGService.get_user_knowledge_text(user_id)
        
        if result['success']:
            print("\n" + "="*80)
            print(f"用户 {user_id} 的知识库文本")
            print("="*80)
            print(result['knowledge_text'])
            print("="*80)
            print(f"统计信息: 邮箱绑定 {result['bindings_count']} 个，邮件 {result['emails_count']} 封")
            print(f"生成时间: {result['generated_at']}")
            print("="*80 + "\n")
        else:
            print(f"\n获取用户 {user_id} 知识库失败: {result['error']}\n")