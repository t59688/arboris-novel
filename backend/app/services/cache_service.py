# AIMETA P=缓存服务_Redis缓存操作|R=缓存读写_失效|NR=不含业务逻辑|E=CacheService|X=internal|A=服务类|D=redis|S=cache|RD=./README.ai
import redis
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CacheService:
    """Redis 缓存服务"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # 测试连接
            self.redis_client.ping()
            logger.info("Redis 连接成功")
        except Exception as e:
            logger.warning(f"Redis 连接失败: {e}，缓存功能将被禁用")
            self.redis_client = None
        
        self.EMOTION_CURVE_TTL = 7 * 24 * 3600  # 7 天
        self.EMOTION_META_TTL = 24 * 3600  # 1 天
        self.EMOTION_TASK_TTL = 3600  # 1 小时
    
    def is_available(self) -> bool:
        """检查 Redis 是否可用"""
        return self.redis_client is not None
    
    def get_emotion_curve(self, novel_id: str) -> Optional[Dict]:
        """获取缓存的情感曲线"""
        if not self.is_available():
            return None
        
        try:
            key = f"emotion_curve:{novel_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"获取情感曲线缓存失败: {e}")
        
        return None
    
    def set_emotion_curve(self, novel_id: str, data: Dict) -> bool:
        """设置情感曲线缓存"""
        if not self.is_available():
            return False
        
        try:
            key = f"emotion_curve:{novel_id}"
            self.redis_client.setex(
                key,
                self.EMOTION_CURVE_TTL,
                json.dumps(data, default=str, ensure_ascii=False)
            )
            logger.info(f"情感曲线缓存已设置: {novel_id}")
            return True
        except Exception as e:
            logger.warning(f"设置情感曲线缓存失败: {e}")
            return False
    
    def get_emotion_meta(self, novel_id: str) -> Optional[Dict]:
        """获取情感分析元数据"""
        if not self.is_available():
            return None
        
        try:
            key = f"emotion_meta:{novel_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"获取情感元数据缓存失败: {e}")
        
        return None
    
    def set_emotion_meta(self, novel_id: str, meta: Dict) -> bool:
        """设置情感分析元数据"""
        if not self.is_available():
            return False
        
        try:
            key = f"emotion_meta:{novel_id}"
            self.redis_client.setex(
                key,
                self.EMOTION_META_TTL,
                json.dumps(meta, default=str, ensure_ascii=False)
            )
            logger.info(f"情感元数据缓存已设置: {novel_id}")
            return True
        except Exception as e:
            logger.warning(f"设置情感元数据缓存失败: {e}")
            return False
    
    def get_chapter_emotion(self, novel_id: str, chapter_id: str) -> Optional[Dict]:
        """获取单个章节的情感缓存"""
        if not self.is_available():
            return None
        
        try:
            key = f"emotion:{novel_id}:{chapter_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"获取章节情感缓存失败: {e}")
        
        return None
    
    def set_chapter_emotion(self, novel_id: str, chapter_id: str, data: Dict) -> bool:
        """设置单个章节的情感缓存"""
        if not self.is_available():
            return False
        
        try:
            key = f"emotion:{novel_id}:{chapter_id}"
            self.redis_client.setex(
                key,
                self.EMOTION_CURVE_TTL,
                json.dumps(data, default=str, ensure_ascii=False)
            )
            return True
        except Exception as e:
            logger.warning(f"设置章节情感缓存失败: {e}")
            return False
    
    def invalidate_emotion_cache(self, novel_id: str) -> bool:
        """清除情感曲线缓存"""
        if not self.is_available():
            return False
        
        try:
            keys = self.redis_client.keys(f"emotion*:{novel_id}*")
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"已清除情感曲线缓存: {novel_id}")
            return True
        except Exception as e:
            logger.warning(f"清除情感曲线缓存失败: {e}")
            return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取异步任务状态"""
        if not self.is_available():
            return None
        
        try:
            key = f"task:{task_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"获取任务状态失败: {e}")
        
        return None
    
    def set_task_status(self, task_id: str, status: Dict) -> bool:
        """设置异步任务状态"""
        if not self.is_available():
            return False
        
        try:
            key = f"task:{task_id}"
            self.redis_client.setex(
                key,
                self.EMOTION_TASK_TTL,
                json.dumps(status, default=str, ensure_ascii=False)
            )
            return True
        except Exception as e:
            logger.warning(f"设置任务状态失败: {e}")
            return False
