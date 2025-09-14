#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数据库服务
负责文本切割、向量化、存储和检索
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import hashlib
import re

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError as e:
    logging.error(f"向量数据库依赖缺失: {e}")
    raise ImportError("请安装向量数据库相关依赖: pip install chromadb sentence-transformers")

from config.rag_config import (
    CHROMA_CONFIG, EMBEDDING_CONFIG, RAG_CONFIG, METADATA_CONFIG,
    get_user_collection_name, get_vector_db_path
)

logger = logging.getLogger(__name__)


class VectorService:
    """向量数据库服务类"""
    
    def __init__(self):
        """初始化向量服务"""
        self._client = None
        self._embedding_model = None
        self._initialize_client()
        self._initialize_embedding_model()
    
    def _initialize_client(self):
        """初始化ChromaDB客户端"""
        try:
            # 完全禁用遥测功能的配置
            settings = Settings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
            
            # 设置环境变量禁用遥测
            import os
            os.environ['ANONYMIZED_TELEMETRY'] = 'False'
            os.environ['CHROMA_TELEMETRY_DISABLED'] = 'True'
            
            # 创建ChromaDB客户端
            self._client = chromadb.PersistentClient(
                path=get_vector_db_path(),
                settings=settings
            )
            logger.info(f"ChromaDB客户端初始化成功，数据库路径: {get_vector_db_path()}")
        except Exception as e:
            logger.error(f"ChromaDB客户端初始化失败: {e}")
            raise
    
    def _initialize_embedding_model(self):
        """初始化嵌入模型"""
        try:
            model_name = EMBEDDING_CONFIG["model_name"]
            cache_dir = EMBEDDING_CONFIG["model_cache_dir"]
            device = EMBEDDING_CONFIG["device"]
            
            # 设置模型缓存目录
            os.makedirs(cache_dir, exist_ok=True)
            
            # 加载SentenceTransformer模型
            self._embedding_model = SentenceTransformer(
                model_name,
                cache_folder=cache_dir,
                device=device
            )
            
            logger.info(f"嵌入模型加载成功: {model_name}")
        except Exception as e:
            logger.error(f"嵌入模型加载失败: {e}")
            # 如果模型加载失败，尝试清理缓存并重新下载
            try:
                import shutil
                model_cache_path = os.path.join(cache_dir, model_name.replace('/', '_'))
                if os.path.exists(model_cache_path):
                    logger.info(f"清理损坏的模型缓存: {model_cache_path}")
                    shutil.rmtree(model_cache_path)
                
                # 重新下载模型
                logger.info(f"重新下载嵌入模型: {model_name}")
                self._embedding_model = SentenceTransformer(
                    model_name,
                    cache_folder=cache_dir,
                    device=device
                )
                logger.info(f"嵌入模型重新下载成功: {model_name}")
            except Exception as retry_e:
                logger.error(f"重新下载嵌入模型失败: {retry_e}")
                raise retry_e
    
    def split_text(self, text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
        """
        将长文本分割成合适的块
        
        Args:
            text: 要分割的文本
            chunk_size: 块大小（字符数）
            chunk_overlap: 块重叠大小
            
        Returns:
            List[str]: 分割后的文本块列表
        """
        if not text or not text.strip():
            return []
        
        chunk_size = chunk_size or RAG_CONFIG["chunk_size"]
        chunk_overlap = chunk_overlap or RAG_CONFIG["chunk_overlap"]
        
        # 清理文本
        text = self._clean_text(text)
        
        # 如果文本长度小于块大小，直接返回
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # 计算当前块的结束位置
            end = start + chunk_size
            
            # 如果不是最后一块，尝试在句子边界处分割
            if end < len(text):
                # 寻找最近的句子结束符
                sentence_end = self._find_sentence_boundary(text, start, end)
                if sentence_end > start:
                    end = sentence_end
            
            # 提取当前块
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # 计算下一块的开始位置（考虑重叠）
            if end >= len(text):
                break
            start = max(start + 1, end - chunk_overlap)
        
        logger.info(f"文本分割完成，原文本长度: {len(text)}，分割成 {len(chunks)} 个块")
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符（保留中文、英文、数字、基本标点）
        text = re.sub(r'[^\u4e00-\u9fff\w\s.,!?;:()\[\]{}"\'-]', ' ', text)
        return text.strip()
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """寻找句子边界"""
        # 句子结束符
        sentence_endings = ['。', '！', '？', '.', '!', '?', '\n']
        
        # 从end位置向前搜索句子结束符
        for i in range(end - 1, start, -1):
            if text[i] in sentence_endings:
                return i + 1
        
        # 如果没找到句子结束符，返回原end位置
        return end
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        生成文本向量
        
        Args:
            texts: 文本列表
            
        Returns:
            np.ndarray: 向量数组
        """
        if not texts:
            return np.array([])
        
        try:
            # 生成向量
            embeddings = self._embedding_model.encode(
                texts,
                normalize_embeddings=EMBEDDING_CONFIG["normalize_embeddings"],
                show_progress_bar=len(texts) > 10
            )
            
            logger.info(f"向量生成完成，文本数量: {len(texts)}，向量维度: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"向量生成失败: {e}")
            raise
    
    def create_user_collection(self, user_id: int) -> str:
        """
        创建用户的向量集合
        
        Args:
            user_id: 用户ID
            
        Returns:
            str: 集合名称
        """
        collection_name = get_user_collection_name(str(user_id))
        
        try:
            # 检查集合是否已存在
            existing_collections = [col.name for col in self._client.list_collections()]
            
            if collection_name in existing_collections:
                logger.info(f"用户 {user_id} 的向量集合已存在: {collection_name}")
                return collection_name
            
            # 创建新集合
            collection = self._client.create_collection(
                name=collection_name,
                metadata={"user_id": str(user_id), "created_at": datetime.now().isoformat()}
            )
            
            logger.info(f"用户 {user_id} 的向量集合创建成功: {collection_name}")
            return collection_name
        except Exception as e:
            logger.error(f"创建用户 {user_id} 向量集合失败: {e}")
            raise
    
    def store_knowledge_vectors(self, user_id: int, knowledge_text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        存储用户知识库向量
        
        Args:
            user_id: 用户ID
            knowledge_text: 知识库文本
            metadata: 额外的元数据
            
        Returns:
            bool: 存储是否成功
        """
        try:
            # 创建或获取用户集合
            collection_name = self.create_user_collection(user_id)
            collection = self._client.get_collection(collection_name)
            
            # 清空现有数据（重新构建知识库）
            try:
                # 获取所有现有文档ID
                existing_data = collection.get()
                if existing_data['ids']:
                    collection.delete(ids=existing_data['ids'])
                    logger.info(f"清空用户 {user_id} 的现有向量数据，共删除 {len(existing_data['ids'])} 条记录")
                else:
                    logger.info(f"用户 {user_id} 的向量集合为空，无需清空")
            except Exception as e:
                logger.warning(f"清空用户 {user_id} 向量数据时出现异常: {e}")
            
            # 更新集合元数据
            try:
                collection.modify(metadata={"user_id": str(user_id), "updated_at": datetime.now().isoformat()})
            except Exception as e:
                logger.warning(f"更新集合元数据失败: {e}")
            
            # 分割文本
            text_chunks = self.split_text(knowledge_text)
            if not text_chunks:
                logger.warning(f"用户 {user_id} 的知识库文本为空或分割后无有效内容")
                return True
            
            # 生成向量
            embeddings = self.generate_embeddings(text_chunks)
            
            # 准备存储数据
            ids = []
            metadatas = []
            
            base_metadata = {
                "user_id": str(user_id),
                "data_type": "knowledge_base",
                "created_at": datetime.now().isoformat(),
                **(metadata or {})
            }
            
            for i, chunk in enumerate(text_chunks):
                # 生成唯一ID
                chunk_id = self._generate_chunk_id(user_id, chunk, i)
                ids.append(chunk_id)
                
                # 准备元数据
                chunk_metadata = {
                    **base_metadata,
                    "chunk_index": i,
                    "chunk_length": len(chunk),
                    "chunk_hash": hashlib.md5(chunk.encode()).hexdigest()[:8]
                }
                metadatas.append(chunk_metadata)
            
            # 存储到向量数据库
            collection.add(
                embeddings=embeddings.tolist(),
                documents=text_chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"用户 {user_id} 知识库向量存储成功，共 {len(text_chunks)} 个文本块")
            return True
            
        except Exception as e:
            logger.error(f"存储用户 {user_id} 知识库向量失败: {e}")
            return False
    
    def search_knowledge_base(self, user_id: int, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        在用户知识库中进行语义搜索
        
        Args:
            user_id: 用户ID
            query: 搜索查询
            top_k: 返回结果数量
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        try:
            collection_name = get_user_collection_name(str(user_id))
            
            # 检查集合是否存在
            existing_collections = [col.name for col in self._client.list_collections()]
            if collection_name not in existing_collections:
                logger.warning(f"用户 {user_id} 的知识库集合不存在")
                return []
            
            # 获取集合
            collection = self._client.get_collection(name=collection_name)
            
            # 生成查询向量
            query_embedding = self.generate_embeddings([query])[0]
            
            # 执行搜索
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=['documents', 'metadatas', 'distances']
            )
            
            # 格式化结果
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result_item = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'similarity': 1 - results['distances'][0][i] if results['distances'] and results['distances'][0] else 0.0
                    }
                    search_results.append(result_item)
            
            logger.info(f"用户 {user_id} 知识库搜索完成，查询: '{query}'，返回 {len(search_results)} 个结果")
            return search_results
            
        except Exception as e:
            logger.error(f"搜索用户 {user_id} 知识库失败: {e}")
            return []
    
    def _generate_chunk_id(self, user_id: int, chunk: str, index: int) -> str:
        """生成文本块的唯一ID"""
        content_hash = hashlib.md5(chunk.encode()).hexdigest()[:8]
        return f"user_{user_id}_chunk_{index}_{content_hash}"
    
    def search_knowledge(self, user_id: int, query: str, max_results: int = None) -> List[Dict[str, Any]]:
        """
        搜索用户知识库
        
        Args:
            user_id: 用户ID
            query: 查询文本
            max_results: 最大结果数量
            
        Returns:
            List[Dict]: 搜索结果列表
        """
        try:
            collection_name = get_user_collection_name(str(user_id))
            
            # 检查集合是否存在
            existing_collections = [col.name for col in self._client.list_collections()]
            if collection_name not in existing_collections:
                logger.warning(f"用户 {user_id} 的向量集合不存在")
                return []
            
            collection = self._client.get_collection(collection_name)
            
            # 生成查询向量
            query_embedding = self.generate_embeddings([query])[0]
            
            # 执行相似度搜索
            max_results = max_results or RAG_CONFIG["max_results"]
            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # 格式化结果
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )):
                    # 计算相似度分数（距离越小，相似度越高）
                    similarity_score = 1 - distance
                    
                    # 过滤低相似度结果
                    if similarity_score >= RAG_CONFIG["similarity_threshold"]:
                        formatted_results.append({
                            "content": doc,
                            "metadata": metadata,
                            "similarity_score": similarity_score,
                            "distance": distance,
                            "rank": i + 1
                        })
            
            logger.info(f"用户 {user_id} 知识库搜索完成，查询: '{query}'，返回 {len(formatted_results)} 个结果")
            return formatted_results
            
        except Exception as e:
            logger.error(f"搜索用户 {user_id} 知识库失败: {e}")
            return []
    
    def get_collection_stats(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户向量集合统计信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict: 统计信息
        """
        try:
            collection_name = get_user_collection_name(str(user_id))
            
            # 检查集合是否存在
            existing_collections = [col.name for col in self._client.list_collections()]
            if collection_name not in existing_collections:
                return {"exists": False, "count": 0}
            
            collection = self._client.get_collection(collection_name)
            count = collection.count()
            
            return {
                "exists": True,
                "collection_name": collection_name,
                "document_count": count,
                "metadata": collection.metadata
            }
            
        except Exception as e:
            logger.error(f"获取用户 {user_id} 向量集合统计失败: {e}")
            return {"exists": False, "error": str(e)}
    
    def delete_user_collection(self, user_id: int) -> bool:
        """
        删除用户的向量集合
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            collection_name = get_user_collection_name(str(user_id))
            
            # 检查集合是否存在
            existing_collections = [col.name for col in self._client.list_collections()]
            if collection_name not in existing_collections:
                logger.info(f"用户 {user_id} 的向量集合不存在，无需删除")
                return True
            
            # 删除集合
            self._client.delete_collection(collection_name)
            logger.info(f"用户 {user_id} 的向量集合删除成功")
            return True
            
        except Exception as e:
            logger.error(f"删除用户 {user_id} 向量集合失败: {e}")
            return False


# 全局向量服务实例
_vector_service_instance = None


def get_vector_service() -> VectorService:
    """获取向量服务实例（单例模式）"""
    global _vector_service_instance
    if _vector_service_instance is None:
        _vector_service_instance = VectorService()
    return _vector_service_instance