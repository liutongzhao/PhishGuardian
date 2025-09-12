# RAG系统配置文件
import os
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
MODELS_DIR = DATA_DIR / "models"

# 确保目录存在
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# ChromaDB配置
CHROMA_CONFIG = {
    "persist_directory": str(VECTOR_DB_DIR),
    "collection_name_prefix": "user_",  # 用户Collection前缀
    "collection_name_suffix": "_knowledge",  # 用户Collection后缀
}

# 嵌入模型配置
EMBEDDING_CONFIG = {
    "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
    "model_cache_dir": str(MODELS_DIR),
    "device": "cpu",  # 可选: "cuda" 如果有GPU
    "normalize_embeddings": True,
}

# RAG检索配置
RAG_CONFIG = {
    "similarity_threshold": 0.7,  # 相似度阈值
    "max_results": 5,  # 最大检索结果数
    "chunk_size": 512,  # 文本分块大小
    "chunk_overlap": 50,  # 分块重叠大小
}

# 元数据配置
METADATA_CONFIG = {
    "required_fields": ["user_id", "data_type", "created_at"],
    "data_types": ["email", "document", "conversation", "threat_intel"],
    "categories": ["phishing", "normal", "suspicious", "unknown"],
}

# 环境变量配置
HF_ENDPOINT = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
HF_HOME = str(MODELS_DIR / "huggingface")

# 设置环境变量
os.environ["HF_ENDPOINT"] = HF_ENDPOINT
os.environ["HF_HOME"] = HF_HOME

def get_user_collection_name(user_id: str) -> str:
    """获取用户的Collection名称"""
    return f"{CHROMA_CONFIG['collection_name_prefix']}{user_id}{CHROMA_CONFIG['collection_name_suffix']}"

def get_vector_db_path() -> str:
    """获取向量数据库路径"""
    return str(VECTOR_DB_DIR)

def get_embedding_model_path() -> str:
    """获取嵌入模型路径"""
    return EMBEDDING_CONFIG["model_name"]