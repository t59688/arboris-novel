# AIMETA P=情感分析器_基础情感识别|R=关键词匹配_情感评分|NR=不含多维分析|E=EmotionAnalyzer|X=internal|A=分析器类|D=none|S=none|RD=./README.ai
"""情感分析工具函数"""
import re
from typing import Optional, Tuple

# 情感关键词定义
EMOTION_KEYWORDS = {
    "喜悦": ["开心", "高兴", "快乐", "欣喜", "兴奋", "愉快", "欢乐", "笑", "笑容", "微笑"],
    "悲伤": ["悲伤", "难过", "伤心", "痛苦", "哭", "眼泪", "失落", "沮丧", "绝望", "悲痛"],
    "愤怒": ["愤怒", "生气", "恼怒", "怒火", "暴怒", "怒吼", "气愤", "愤恨", "憎恨", "厌恶"],
    "恐惧": ["害怕", "恐惧", "惊恐", "惊吓", "战栗", "颤抖", "惊慌", "恐怖", "畏惧", "惊惧"],
    "惊讶": ["惊讶", "惊奇", "震惊", "意外", "惊喜", "诧异", "惊呆", "惊愕", "吃惊", "瞪大"],
    "平静": ["平静", "安静", "宁静", "祥和", "淡然", "从容", "镇定", "沉着", "冷静", "无波"],
}

NARRATIVE_PHASE_KEYWORDS = {
    "事件": ["发生", "出现", "开始", "发起", "引发", "触发", "爆发"],
    "势力": ["力量", "势力", "阵营", "集团", "联盟", "对抗", "对立"],
    "挑衅1": ["挑衅", "冒犯", "侮辱", "挑战", "激怒", "惹怒"],
    "挑衅2": ["再次", "继续", "又一次", "再度", "不断"],
    "挑衅3": ["最后", "终于", "最终", "彻底"],
    "回击1": ["反击", "报复", "反抗", "对抗", "反驳"],
    "回击2": ["胜利", "成功", "赢", "战胜", "击败"],
    "回击3": ["逆转", "翻盘", "转机", "突破"],
    "回击4": ["和解", "结束", "平息", "化解", "解决"],
    "过渡": ["然而", "但是", "不过", "只是", "却"],
}

def analyze_emotion(text: str) -> Tuple[str, int]:
    """分析文本的主要情感和强度"""
    emotion_scores = {emotion: 0 for emotion in EMOTION_KEYWORDS}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            count = text.count(keyword)
            emotion_scores[emotion] += count
    
    # 找出最高分的情感
    max_emotion = max(emotion_scores, key=emotion_scores.get)
    max_score = emotion_scores[max_emotion]
    
    if max_score == 0:
        return "平静", 3
    
    # 计算强度 (1-10)
    intensity = min(10, max(1, max_score))
    
    # 根据感叹号和问号增加强度
    exclamation_count = text.count("！") + text.count("!")
    question_count = text.count("？") + text.count("?")
    intensity = min(10, intensity + exclamation_count // 3 + question_count // 5)
    
    return max_emotion, intensity

def detect_narrative_phase(text: str, summary: str = "") -> Optional[str]:
    """检测叙事阶段"""
    combined_text = text + " " + summary
    phase_scores = {phase: 0 for phase in NARRATIVE_PHASE_KEYWORDS}
    
    for phase, keywords in NARRATIVE_PHASE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in combined_text:
                phase_scores[phase] += 1
    
    max_phase = max(phase_scores, key=phase_scores.get)
    if phase_scores[max_phase] > 0:
        return max_phase
    return None

def generate_emotion_description(emotion: str, intensity: int, title: str) -> str:
    """生成情感描述"""
    intensity_words = {
        (1, 3): "轻微的",
        (4, 6): "明显的",
        (7, 8): "强烈的",
        (9, 10): "极度的",
    }
    
    for (low, high), word in intensity_words.items():
        if low <= intensity <= high:
            return f"《{title}》呈现{word}{emotion}情绪"
    
    return f"《{title}》的情感基调为{emotion}"
