# AIMETA P=增强情感分析_多维情感识别|R=8种情感_叙事阶段_转折点|NR=不含基础分析|E=EmotionAnalyzerEnhanced|X=internal|A=分析器类|D=none|S=none|RD=./README.ai
"""
多维情感分析增强模块
扩展原有的单维情感分析，增加多个维度的情感识别和分析
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class EmotionType(Enum):
    """情感类型枚举"""
    JOY = "joy"  # 喜悦
    SADNESS = "sadness"  # 悲伤
    ANGER = "anger"  # 愤怒
    FEAR = "fear"  # 恐惧
    SURPRISE = "surprise"  # 惊讶
    DISGUST = "disgust"  # 厌恶
    ANTICIPATION = "anticipation"  # 期待
    TRUST = "trust"  # 信任
    NEUTRAL = "neutral"  # 中性


class NarrativePhase(Enum):
    """叙事阶段枚举"""
    EXPOSITION = "exposition"  # 铺垫/开端
    RISING_ACTION = "rising_action"  # 上升/发展
    CLIMAX = "climax"  # 高潮
    FALLING_ACTION = "falling_action"  # 下降/结局
    RESOLUTION = "resolution"  # 解决/尾声


@dataclass
class EmotionPoint:
    """情感点数据结构"""
    chapter_number: int
    chapter_id: str
    title: str
    
    # 主情感
    primary_emotion: EmotionType
    primary_intensity: float  # 0-10
    
    # 次要情感（可能有多个）
    secondary_emotions: List[Tuple[EmotionType, float]]
    
    # 叙事阶段
    narrative_phase: NarrativePhase
    
    # 情感节奏
    pace: str  # slow, medium, fast
    
    # 转折点标记
    is_turning_point: bool
    turning_point_type: Optional[str]  # emotional_shift, plot_twist, revelation
    
    # 情感描述
    description: str
    
    # 原始分数（用于计算）
    raw_scores: Dict[str, float]


class EnhancedEmotionAnalyzer:
    """增强的情感分析器"""
    
    def __init__(self):
        # 情感关键词词典（扩展版）
        self.emotion_keywords = {
            EmotionType.JOY: {
                'positive': ['快乐', '喜悦', '高兴', '开心', '欢乐', '愉快', '幸福', '满足', '欣喜', '兴奋', '激动', '振奋'],
                'actions': ['笑', '微笑', '大笑', '欢呼', '庆祝', '拥抱'],
                'weight': 1.0
            },
            EmotionType.SADNESS: {
                'positive': ['悲伤', '难过', '痛苦', '伤心', '忧郁', '沮丧', '失落', '绝望', '哀伤', '悲痛', '心碎'],
                'actions': ['哭', '流泪', '哽咽', '叹气', '低头'],
                'weight': 1.0
            },
            EmotionType.ANGER: {
                'positive': ['愤怒', '生气', '恼怒', '暴怒', '激怒', '恨', '憎恶', '愤慨', '怒火'],
                'actions': ['怒吼', '咆哮', '砸', '摔', '打', '踢'],
                'weight': 1.0
            },
            EmotionType.FEAR: {
                'positive': ['恐惧', '害怕', '惊恐', '恐慌', '畏惧', '担心', '忧虑', '不安', '紧张', '焦虑'],
                'actions': ['颤抖', '退缩', '逃跑', '躲藏', '尖叫'],
                'weight': 1.0
            },
            EmotionType.SURPRISE: {
                'positive': ['惊讶', '惊奇', '震惊', '惊愕', '意外', '吃惊', '诧异'],
                'actions': ['瞪大眼睛', '张大嘴', '愣住', '呆住'],
                'weight': 0.8
            },
            EmotionType.ANTICIPATION: {
                'positive': ['期待', '期望', '盼望', '渴望', '向往', '憧憬', '希望', '等待'],
                'actions': ['准备', '计划', '筹备'],
                'weight': 0.7
            },
            EmotionType.TRUST: {
                'positive': ['信任', '相信', '信赖', '依靠', '依赖', '托付'],
                'actions': ['握手', '承诺', '发誓'],
                'weight': 0.6
            },
        }
        
        # 叙事阶段关键词
        self.narrative_keywords = {
            NarrativePhase.EXPOSITION: ['开始', '起初', '最初', '介绍', '背景', '设定'],
            NarrativePhase.RISING_ACTION: ['发展', '逐渐', '越来越', '开始', '进展', '推进'],
            NarrativePhase.CLIMAX: ['高潮', '顶点', '巅峰', '关键', '决战', '对决', '爆发', '终于'],
            NarrativePhase.FALLING_ACTION: ['之后', '随后', '接着', '结果', '最终'],
            NarrativePhase.RESOLUTION: ['结束', '完结', '尾声', '终章', '落幕', '收尾'],
        }
        
        # 节奏关键词
        self.pace_keywords = {
            'slow': ['缓慢', '慢慢', '徐徐', '悠悠', '平静', '安静', '沉思', '回忆'],
            'medium': ['正常', '平稳', '稳定', '持续', '进行'],
            'fast': ['快速', '迅速', '急速', '飞快', '突然', '猛然', '瞬间', '立刻', '马上', '冲', '跑', '追'],
        }
    
    def analyze_multidimensional_emotion(
        self, 
        content: str, 
        summary: str = "",
        chapter_number: int = 0
    ) -> EmotionPoint:
        """
        多维情感分析
        
        Args:
            content: 章节内容
            summary: 章节摘要
            chapter_number: 章节编号
            
        Returns:
            EmotionPoint: 多维情感分析结果
        """
        text = content + " " + summary
        
        # 1. 计算各情感维度的分数
        emotion_scores = self._calculate_emotion_scores(text)
        
        # 2. 确定主情感和次要情感
        primary_emotion, primary_intensity = self._get_primary_emotion(emotion_scores)
        secondary_emotions = self._get_secondary_emotions(emotion_scores, primary_emotion)
        
        # 3. 检测叙事阶段
        narrative_phase = self._detect_narrative_phase(text, chapter_number)
        
        # 4. 分析情感节奏
        pace = self._analyze_pace(text)
        
        # 5. 检测转折点
        is_turning_point, turning_point_type = self._detect_turning_point(
            text, emotion_scores, chapter_number
        )
        
        # 6. 生成情感描述
        description = self._generate_enhanced_description(
            primary_emotion, primary_intensity, secondary_emotions, narrative_phase, pace
        )
        
        return EmotionPoint(
            chapter_number=chapter_number,
            chapter_id="",  # 需要外部填充
            title="",  # 需要外部填充
            primary_emotion=primary_emotion,
            primary_intensity=primary_intensity,
            secondary_emotions=secondary_emotions,
            narrative_phase=narrative_phase,
            pace=pace,
            is_turning_point=is_turning_point,
            turning_point_type=turning_point_type,
            description=description,
            raw_scores=emotion_scores
        )
    
    def _calculate_emotion_scores(self, text: str) -> Dict[str, float]:
        """计算各情感维度的分数"""
        scores = {}
        text_length = len(text)
        
        for emotion_type, keywords_data in self.emotion_keywords.items():
            score = 0.0
            weight = keywords_data.get('weight', 1.0)
            
            # 统计正面关键词
            for keyword in keywords_data.get('positive', []):
                count = text.count(keyword)
                score += count * 2.0 * weight
            
            # 统计动作关键词
            for keyword in keywords_data.get('actions', []):
                count = text.count(keyword)
                score += count * 1.5 * weight
            
            # 归一化到 0-10
            normalized_score = min(10.0, (score / max(text_length / 1000, 1)) * 10)
            scores[emotion_type.value] = round(normalized_score, 2)
        
        # 如果所有分数都很低，设置为中性
        if max(scores.values()) < 1.0:
            scores['neutral'] = 5.0
        
        return scores
    
    def _get_primary_emotion(self, scores: Dict[str, float]) -> Tuple[EmotionType, float]:
        """获取主要情感"""
        if 'neutral' in scores and scores['neutral'] > 4.0:
            return EmotionType.NEUTRAL, scores['neutral']
        
        max_emotion = max(scores.items(), key=lambda x: x[1])
        emotion_type = EmotionType(max_emotion[0]) if max_emotion[0] != 'neutral' else EmotionType.NEUTRAL
        intensity = max_emotion[1]
        
        return emotion_type, intensity
    
    def _get_secondary_emotions(
        self, 
        scores: Dict[str, float], 
        primary_emotion: EmotionType
    ) -> List[Tuple[EmotionType, float]]:
        """获取次要情感（分数 > 3.0 且不是主情感）"""
        secondary = []
        
        for emotion_str, score in scores.items():
            if emotion_str == 'neutral':
                continue
            
            emotion_type = EmotionType(emotion_str)
            if emotion_type != primary_emotion and score >= 3.0:
                secondary.append((emotion_type, score))
        
        # 按分数降序排列
        secondary.sort(key=lambda x: x[1], reverse=True)
        
        # 最多返回 3 个次要情感
        return secondary[:3]
    
    def _detect_narrative_phase(self, text: str, chapter_number: int) -> NarrativePhase:
        """检测叙事阶段"""
        phase_scores = {}
        
        for phase, keywords in self.narrative_keywords.items():
            score = sum(text.count(keyword) for keyword in keywords)
            phase_scores[phase] = score
        
        # 如果关键词不明显，根据章节编号推断
        if max(phase_scores.values()) < 2:
            if chapter_number <= 3:
                return NarrativePhase.EXPOSITION
            elif chapter_number <= 8:
                return NarrativePhase.RISING_ACTION
            elif chapter_number <= 12:
                return NarrativePhase.CLIMAX
            elif chapter_number <= 15:
                return NarrativePhase.FALLING_ACTION
            else:
                return NarrativePhase.RESOLUTION
        
        return max(phase_scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_pace(self, text: str) -> str:
        """分析情感节奏"""
        pace_scores = {}
        
        for pace, keywords in self.pace_keywords.items():
            score = sum(text.count(keyword) for keyword in keywords)
            pace_scores[pace] = score
        
        if max(pace_scores.values()) == 0:
            return 'medium'
        
        return max(pace_scores.items(), key=lambda x: x[1])[0]
    
    def _detect_turning_point(
        self, 
        text: str, 
        emotion_scores: Dict[str, float],
        chapter_number: int
    ) -> Tuple[bool, Optional[str]]:
        """检测是否为转折点"""
        # 转折点关键词
        turning_keywords = {
            'emotional_shift': ['突然', '忽然', '意外', '没想到', '竟然'],
            'plot_twist': ['真相', '原来', '其实', '秘密', '揭露', '发现'],
            'revelation': ['明白', '理解', '领悟', '醒悟', '意识到'],
        }
        
        for tp_type, keywords in turning_keywords.items():
            count = sum(text.count(keyword) for keyword in keywords)
            if count >= 3:
                return True, tp_type
        
        # 情感强度超过 8.0 也可能是转折点
        if max(emotion_scores.values()) >= 8.0:
            return True, 'emotional_shift'
        
        return False, None
    
    def _generate_enhanced_description(
        self,
        primary_emotion: EmotionType,
        intensity: float,
        secondary_emotions: List[Tuple[EmotionType, float]],
        narrative_phase: NarrativePhase,
        pace: str
    ) -> str:
        """生成增强的情感描述"""
        emotion_names = {
            EmotionType.JOY: "喜悦",
            EmotionType.SADNESS: "悲伤",
            EmotionType.ANGER: "愤怒",
            EmotionType.FEAR: "恐惧",
            EmotionType.SURPRISE: "惊讶",
            EmotionType.ANTICIPATION: "期待",
            EmotionType.TRUST: "信任",
            EmotionType.NEUTRAL: "平静",
        }
        
        phase_names = {
            NarrativePhase.EXPOSITION: "故事铺垫",
            NarrativePhase.RISING_ACTION: "情节发展",
            NarrativePhase.CLIMAX: "故事高潮",
            NarrativePhase.FALLING_ACTION: "情节回落",
            NarrativePhase.RESOLUTION: "故事收尾",
        }
        
        pace_names = {
            'slow': "节奏缓慢",
            'medium': "节奏平稳",
            'fast': "节奏紧凑",
        }
        
        # 主情感描述
        intensity_desc = "强烈" if intensity >= 7.0 else "明显" if intensity >= 4.0 else "轻微"
        desc = f"{intensity_desc}的{emotion_names[primary_emotion]}"
        
        # 次要情感描述
        if secondary_emotions:
            secondary_names = [emotion_names[e[0]] for e in secondary_emotions[:2]]
            desc += f"，伴随{'/'.join(secondary_names)}"
        
        # 叙事阶段
        desc += f"。{phase_names[narrative_phase]}"
        
        # 节奏
        desc += f"，{pace_names[pace]}"
        
        return desc


# 导出函数（保持向后兼容）
def analyze_multidimensional_emotion(content: str, summary: str = "", chapter_number: int = 0) -> Dict:
    """
    多维情感分析函数（向后兼容接口）
    
    Returns:
        Dict: 包含多维情感分析结果的字典
    """
    analyzer = EnhancedEmotionAnalyzer()
    result = analyzer.analyze_multidimensional_emotion(content, summary, chapter_number)
    
    return {
        'primary_emotion': result.primary_emotion.value,
        'primary_intensity': result.primary_intensity,
        'secondary_emotions': [(e[0].value, e[1]) for e in result.secondary_emotions],
        'narrative_phase': result.narrative_phase.value,
        'pace': result.pace,
        'is_turning_point': result.is_turning_point,
        'turning_point_type': result.turning_point_type,
        'description': result.description,
        'raw_scores': result.raw_scores,
    }
