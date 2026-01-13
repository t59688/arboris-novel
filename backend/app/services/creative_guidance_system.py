# AIMETA P=创意指导系统_写作建议生成|R=优劣势分析_指导建议|NR=不含内容生成|E=CreativeGuidanceSystem|X=internal|A=系统类|D=none|S=none|RD=./README.ai
"""
创意指导系统
基于情感分析和故事轨迹分析，提供智能的写作建议和创意指导
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class GuidanceType(Enum):
    """指导类型枚举"""
    PLOT_DEVELOPMENT = "plot_development"  # 情节发展
    EMOTION_PACING = "emotion_pacing"  # 情感节奏
    CHARACTER_ARC = "character_arc"  # 角色弧光
    CONFLICT_ESCALATION = "conflict_escalation"  # 冲突升级
    RESOLUTION_TIMING = "resolution_timing"  # 解决时机
    THEME_DEPTH = "theme_depth"  # 主题深度


class Priority(Enum):
    """优先级枚举"""
    CRITICAL = "critical"  # 严重问题，需要立即处理
    HIGH = "high"  # 高优先级
    MEDIUM = "medium"  # 中优先级
    LOW = "low"  # 低优先级


@dataclass
class GuidanceItem:
    """指导项"""
    type: GuidanceType
    priority: Priority
    title: str
    description: str
    specific_suggestions: List[str]
    affected_chapters: List[int]
    examples: Optional[List[str]] = None


@dataclass
class CreativeGuidance:
    """创意指导结果"""
    overall_assessment: str  # 总体评估
    strengths: List[str]  # 优势
    weaknesses: List[str]  # 不足
    guidance_items: List[GuidanceItem]  # 具体指导
    next_chapter_suggestions: List[str]  # 下一章建议
    long_term_planning: List[str]  # 长期规划建议


class CreativeGuidanceSystem:
    """创意指导系统"""
    
    def __init__(self):
        pass
    
    def generate_guidance(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict,
        current_chapter: int,
        foreshadowings: Optional[List[Dict]] = None
    ) -> CreativeGuidance:
        """
        生成创意指导
        
        Args:
            emotion_points: 情感点列表
            trajectory_analysis: 故事轨迹分析结果
            current_chapter: 当前章节编号
            foreshadowings: 伏笔列表（可选）
            
        Returns:
            CreativeGuidance: 创意指导结果
        """
        # 1. 总体评估
        overall_assessment = self._generate_overall_assessment(
            emotion_points, trajectory_analysis, current_chapter
        )
        
        # 2. 识别优势
        strengths = self._identify_strengths(emotion_points, trajectory_analysis)
        
        # 3. 识别不足
        weaknesses = self._identify_weaknesses(emotion_points, trajectory_analysis)
        
        # 4. 生成具体指导
        guidance_items = self._generate_guidance_items(
            emotion_points, trajectory_analysis, current_chapter, foreshadowings
        )
        
        # 5. 下一章建议
        next_chapter_suggestions = self._generate_next_chapter_suggestions(
            emotion_points, trajectory_analysis, current_chapter
        )
        
        # 6. 长期规划建议
        long_term_planning = self._generate_long_term_planning(
            trajectory_analysis, current_chapter
        )
        
        return CreativeGuidance(
            overall_assessment=overall_assessment,
            strengths=strengths,
            weaknesses=weaknesses,
            guidance_items=guidance_items,
            next_chapter_suggestions=next_chapter_suggestions,
            long_term_planning=long_term_planning
        )
    
    def _generate_overall_assessment(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict,
        current_chapter: int
    ) -> str:
        """生成总体评估"""
        shape = trajectory_analysis.get('shape', 'flat')
        confidence = trajectory_analysis.get('shape_confidence', 0.5)
        avg_intensity = trajectory_analysis.get('avg_intensity', 5.0)
        volatility = trajectory_analysis.get('volatility', 1.0)
        
        # 形状描述
        shape_names = {
            'rags_to_riches': '上升型',
            'riches_to_rags': '下降型',
            'man_in_hole': 'V型',
            'icarus': '倒V型',
            'cinderella': '波浪型',
            'oedipus': '复杂型',
            'flat': '平稳型',
        }
        
        assessment = f"您的故事目前呈现{shape_names.get(shape, '未知')}轨迹"
        
        if confidence > 0.7:
            assessment += "，形状特征明显"
        elif confidence > 0.5:
            assessment += "，形状特征较为清晰"
        else:
            assessment += "，形状特征尚不明确"
        
        assessment += f"。已完成 {current_chapter} 章，"
        
        # 情感强度评价
        if avg_intensity >= 7.0:
            assessment += "情感浓度较高，"
        elif avg_intensity >= 5.0:
            assessment += "情感浓度适中，"
        else:
            assessment += "情感浓度偏低，"
        
        # 波动性评价
        if volatility > 2.5:
            assessment += "情节跌宕起伏。"
        elif volatility > 1.5:
            assessment += "情节起伏适中。"
        else:
            assessment += "情节较为平缓。"
        
        return assessment
    
    def _identify_strengths(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict
    ) -> List[str]:
        """识别优势"""
        strengths = []
        
        volatility = trajectory_analysis.get('volatility', 1.0)
        avg_intensity = trajectory_analysis.get('avg_intensity', 5.0)
        turning_points = trajectory_analysis.get('turning_points', [])
        peak_chapters = trajectory_analysis.get('peak_chapters', [])
        
        # 情感强度优势
        if avg_intensity >= 6.5:
            strengths.append("情感表达充沛，能够有效调动读者情绪")
        
        # 波动性优势
        if 1.5 <= volatility <= 2.5:
            strengths.append("情节节奏把握得当，张弛有度")
        
        # 转折点优势
        if len(turning_points) >= 2:
            strengths.append(f"设置了 {len(turning_points)} 个有效的情节转折点，增强了故事的戏剧性")
        
        # 高潮优势
        if len(peak_chapters) >= 1:
            strengths.append("成功营造了情感高潮，给读者留下深刻印象")
        
        # 多维情感优势
        has_secondary_emotions = any(
            point.get('secondary_emotions') and len(point.get('secondary_emotions', [])) > 0
            for point in emotion_points
        )
        if has_secondary_emotions:
            strengths.append("情感表达多维度，层次丰富")
        
        if not strengths:
            strengths.append("故事具有发展潜力，继续保持创作")
        
        return strengths
    
    def _identify_weaknesses(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict
    ) -> List[str]:
        """识别不足"""
        weaknesses = []
        
        volatility = trajectory_analysis.get('volatility', 1.0)
        avg_intensity = trajectory_analysis.get('avg_intensity', 5.0)
        shape = trajectory_analysis.get('shape', 'flat')
        segments = trajectory_analysis.get('segments', [])
        
        # 情感强度不足
        if avg_intensity < 4.5:
            weaknesses.append("整体情感强度偏低，建议增强情感表达和冲突设置")
        
        # 波动性问题
        if volatility < 0.8:
            weaknesses.append("情节过于平淡，缺乏起伏，建议增加转折和冲突")
        elif volatility > 3.0:
            weaknesses.append("情节波动过于剧烈，可能导致读者疲劳，建议适当平衡")
        
        # 形状问题
        if shape == 'flat':
            weaknesses.append("故事结构较为平直，缺乏明显的情节弧线")
        
        # 片段问题
        if len(segments) < 2:
            weaknesses.append("故事结构过于简单，建议增加更多的情节层次")
        
        # 节奏问题
        pace_counts = {}
        for point in emotion_points:
            pace = point.get('pace', 'medium')
            pace_counts[pace] = pace_counts.get(pace, 0) + 1
        
        if pace_counts.get('slow', 0) > len(emotion_points) * 0.7:
            weaknesses.append("整体节奏偏慢，可能影响读者的阅读体验")
        elif pace_counts.get('fast', 0) > len(emotion_points) * 0.7:
            weaknesses.append("整体节奏过快，建议适当增加铺垫和细节描写")
        
        return weaknesses
    
    def _generate_guidance_items(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict,
        current_chapter: int,
        foreshadowings: Optional[List[Dict]] = None
    ) -> List[GuidanceItem]:
        """生成具体指导项"""
        guidance_items = []
        
        # 1. 情节发展指导
        plot_guidance = self._generate_plot_guidance(
            emotion_points, trajectory_analysis, current_chapter
        )
        if plot_guidance:
            guidance_items.append(plot_guidance)
        
        # 2. 情感节奏指导
        pacing_guidance = self._generate_pacing_guidance(emotion_points)
        if pacing_guidance:
            guidance_items.append(pacing_guidance)
        
        # 3. 冲突升级指导
        conflict_guidance = self._generate_conflict_guidance(
            emotion_points, trajectory_analysis
        )
        if conflict_guidance:
            guidance_items.append(conflict_guidance)
        
        # 4. 伏笔管理指导
        if foreshadowings:
            foreshadowing_guidance = self._generate_foreshadowing_guidance(
                foreshadowings, current_chapter
            )
            if foreshadowing_guidance:
                guidance_items.append(foreshadowing_guidance)
        
        # 5. 主题深度指导
        theme_guidance = self._generate_theme_guidance(
            emotion_points, trajectory_analysis
        )
        if theme_guidance:
            guidance_items.append(theme_guidance)
        
        # 按优先级排序
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
        }
        guidance_items.sort(key=lambda x: priority_order[x.priority])
        
        return guidance_items
    
    def _generate_plot_guidance(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict,
        current_chapter: int
    ) -> Optional[GuidanceItem]:
        """生成情节发展指导"""
        shape = trajectory_analysis.get('shape', 'flat')
        segments = trajectory_analysis.get('segments', [])
        
        if shape == 'flat' and len(segments) < 3:
            return GuidanceItem(
                type=GuidanceType.PLOT_DEVELOPMENT,
                priority=Priority.HIGH,
                title="情节结构需要加强",
                description="当前故事结构较为简单，缺乏明显的起承转合。建议增加更多的情节层次和转折点。",
                specific_suggestions=[
                    "在接下来的章节中引入新的冲突或挑战",
                    "设置一个意外的转折点，打破当前的平衡",
                    "增加次要情节线，丰富故事的层次感",
                    "考虑引入新角色或揭示隐藏信息",
                ],
                affected_chapters=list(range(current_chapter + 1, current_chapter + 4)),
                examples=[
                    "在平静的日常中突然出现危机",
                    "主角发现之前的认知是错误的",
                    "盟友背叛或敌人示好",
                ]
            )
        
        return None
    
    def _generate_pacing_guidance(
        self,
        emotion_points: List[Dict]
    ) -> Optional[GuidanceItem]:
        """生成情感节奏指导"""
        if not emotion_points:
            return None
        
        # 统计节奏分布
        pace_counts = {'slow': 0, 'medium': 0, 'fast': 0}
        for point in emotion_points:
            pace = point.get('pace', 'medium')
            pace_counts[pace] = pace_counts.get(pace, 0) + 1
        
        total = len(emotion_points)
        
        # 如果节奏过于单一
        if pace_counts['slow'] > total * 0.7:
            return GuidanceItem(
                type=GuidanceType.EMOTION_PACING,
                priority=Priority.MEDIUM,
                title="节奏偏慢，需要提速",
                description="故事整体节奏较慢，可能导致读者失去兴趣。建议适当加快节奏，增加紧张感。",
                specific_suggestions=[
                    "减少过多的环境描写和内心独白",
                    "增加对话和动作场景",
                    "压缩时间跨度，让事件更密集",
                    "在关键时刻使用短句和快节奏的叙述",
                ],
                affected_chapters=[p['chapter_number'] for p in emotion_points if p.get('pace') == 'slow'][:5],
            )
        elif pace_counts['fast'] > total * 0.7:
            return GuidanceItem(
                type=GuidanceType.EMOTION_PACING,
                priority=Priority.MEDIUM,
                title="节奏过快，需要缓冲",
                description="故事整体节奏过快，读者可能跟不上或感到疲劳。建议适当放慢节奏，增加铺垫。",
                specific_suggestions=[
                    "在高潮之间增加过渡章节",
                    "增加角色的内心活动和情感描写",
                    "适当增加环境和氛围的营造",
                    "给读者消化信息的时间",
                ],
                affected_chapters=[p['chapter_number'] for p in emotion_points if p.get('pace') == 'fast'][:5],
            )
        
        return None
    
    def _generate_conflict_guidance(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict
    ) -> Optional[GuidanceItem]:
        """生成冲突升级指导"""
        avg_intensity = trajectory_analysis.get('avg_intensity', 5.0)
        peak_chapters = trajectory_analysis.get('peak_chapters', [])
        
        if avg_intensity < 5.0 and len(peak_chapters) < 1:
            return GuidanceItem(
                type=GuidanceType.CONFLICT_ESCALATION,
                priority=Priority.HIGH,
                title="冲突强度不足",
                description="故事缺乏足够的冲突和张力，情感强度偏低。建议增强冲突设置，提升戏剧性。",
                specific_suggestions=[
                    "明确主角的目标和面临的障碍",
                    "增加对手的力量，让冲突更加激烈",
                    "设置时间限制或紧迫感",
                    "让主角面临艰难的选择和代价",
                    "增加内心冲突和道德困境",
                ],
                affected_chapters=[],
                examples=[
                    "主角必须在两个重要的人之间做出选择",
                    "时间紧迫，必须在截止日期前完成任务",
                    "对手突然变得更加强大和危险",
                ]
            )
        
        return None
    
    def _generate_foreshadowing_guidance(
        self,
        foreshadowings: List[Dict],
        current_chapter: int
    ) -> Optional[GuidanceItem]:
        """生成伏笔管理指导"""
        unresolved = [f for f in foreshadowings if f.get('status') == 'open']
        
        if len(unresolved) > 5:
            return GuidanceItem(
                type=GuidanceType.PLOT_DEVELOPMENT,
                priority=Priority.MEDIUM,
                title="未回收伏笔过多",
                description=f"当前有 {len(unresolved)} 个未回收的伏笔，可能导致读者困惑。建议逐步回收部分伏笔。",
                specific_suggestions=[
                    "优先回收设置时间较早的伏笔",
                    "可以将多个伏笔合并回收",
                    "不重要的伏笔可以考虑放弃",
                    "在高潮章节集中回收关键伏笔",
                ],
                affected_chapters=[f.get('chapter_number', 0) for f in unresolved[:5]],
            )
        
        return None
    
    def _generate_theme_guidance(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict
    ) -> Optional[GuidanceItem]:
        """生成主题深度指导"""
        # 检查情感多样性
        emotion_types = set()
        for point in emotion_points:
            emotion_types.add(point.get('primary_emotion', 'neutral'))
            for sec_emotion, _ in point.get('secondary_emotions', []):
                emotion_types.add(sec_emotion)
        
        if len(emotion_types) < 3:
            return GuidanceItem(
                type=GuidanceType.THEME_DEPTH,
                priority=Priority.LOW,
                title="情感维度可以更丰富",
                description="故事的情感表达较为单一，建议增加更多维度的情感，提升主题深度。",
                specific_suggestions=[
                    "探索角色的复杂情感，不只是单一的喜怒哀乐",
                    "增加角色之间的情感互动和碰撞",
                    "通过不同角色展现不同的情感视角",
                    "在冲突中展现情感的矛盾和转变",
                ],
                affected_chapters=[],
            )
        
        return None
    
    def _generate_next_chapter_suggestions(
        self,
        emotion_points: List[Dict],
        trajectory_analysis: Dict,
        current_chapter: int
    ) -> List[str]:
        """生成下一章建议"""
        suggestions = []
        
        if not emotion_points:
            suggestions.append("开始建立故事的基础设定和主要角色")
            suggestions.append("明确主角的目标和初始状态")
            return suggestions
        
        last_point = emotion_points[-1]
        last_intensity = last_point.get('primary_intensity', 5.0)
        last_pace = last_point.get('pace', 'medium')
        shape = trajectory_analysis.get('shape', 'flat')
        
        # 根据最后一章的情况给建议
        if last_intensity >= 8.0:
            suggestions.append("上一章情感强度很高，建议下一章适当放缓节奏，给读者喘息空间")
            suggestions.append("可以通过角色的反思或后续处理来延续高潮的影响")
        elif last_intensity <= 3.0:
            suggestions.append("上一章情感强度较低，建议下一章引入新的冲突或转折")
            suggestions.append("可以通过意外事件或新信息来打破平静")
        
        # 根据节奏给建议
        if last_pace == 'fast':
            suggestions.append("上一章节奏较快，可以考虑在下一章加入一些细节描写和情感铺垫")
        elif last_pace == 'slow':
            suggestions.append("上一章节奏较慢，建议下一章加快节奏，推进情节发展")
        
        # 根据形状给建议
        if shape == 'man_in_hole':
            suggestions.append("V型故事需要注意低谷后的上升要有足够的动力和理由")
        elif shape == 'icarus':
            suggestions.append("倒V型故事的下降需要合理的原因和充分的铺垫")
        
        return suggestions
    
    def _generate_long_term_planning(
        self,
        trajectory_analysis: Dict,
        current_chapter: int
    ) -> List[str]:
        """生成长期规划建议"""
        planning = []
        
        shape = trajectory_analysis.get('shape', 'flat')
        total_chapters = trajectory_analysis.get('total_chapters', 0)
        
        # 根据形状给长期规划建议
        if shape == 'flat':
            planning.append("建议规划一个明确的故事弧线，设定起点、发展、高潮和结局")
            planning.append("可以参考经典的三幕结构或英雄之旅模式")
        
        # 根据章节数给建议
        if total_chapters < 10:
            planning.append("故事尚处于早期阶段，建议明确整体的故事走向和预期章节数")
            planning.append("提前规划关键的转折点和高潮位置")
        elif total_chapters < 20:
            planning.append("故事进入中期，建议检查是否偏离了最初的规划")
            planning.append("确保主要伏笔都有回收的计划")
        else:
            planning.append("故事已经较长，建议开始考虑收尾的节奏")
            planning.append("逐步回收伏笔，解决主要冲突")
        
        planning.append("定期回顾和调整创作计划，保持故事的连贯性")
        planning.append("可以制作角色关系图和情节时间线，帮助把控全局")
        
        return planning


# 导出函数
def generate_creative_guidance(
    emotion_points: List[Dict],
    trajectory_analysis: Dict,
    current_chapter: int,
    foreshadowings: Optional[List[Dict]] = None
) -> Dict:
    """
    生成创意指导
    
    Returns:
        Dict: 创意指导结果字典
    """
    system = CreativeGuidanceSystem()
    result = system.generate_guidance(
        emotion_points, trajectory_analysis, current_chapter, foreshadowings
    )
    
    return {
        'overall_assessment': result.overall_assessment,
        'strengths': result.strengths,
        'weaknesses': result.weaknesses,
        'guidance_items': [
            {
                'type': item.type.value,
                'priority': item.priority.value,
                'title': item.title,
                'description': item.description,
                'specific_suggestions': item.specific_suggestions,
                'affected_chapters': item.affected_chapters,
                'examples': item.examples or [],
            }
            for item in result.guidance_items
        ],
        'next_chapter_suggestions': result.next_chapter_suggestions,
        'long_term_planning': result.long_term_planning,
    }
