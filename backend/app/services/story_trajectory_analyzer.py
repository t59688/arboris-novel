# AIMETA P=故事轨迹分析_6种故事形状识别|R=形状识别_关键点检测|NR=不含内容生成|E=StoryTrajectoryAnalyzer|X=internal|A=分析器类|D=none|S=none|RD=./README.ai
"""
故事轨迹分析模块
基于情感曲线识别 6 种基本故事形状，并提供轨迹分析
"""
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import statistics


class TrajectoryShape(Enum):
    """故事轨迹形状枚举（基于 Kurt Vonnegut 的故事形状理论）"""
    RAGS_TO_RICHES = "rags_to_riches"  # 上升型：从低谷到高峰
    RICHES_TO_RAGS = "riches_to_rags"  # 下降型：从高峰到低谷
    MAN_IN_HOLE = "man_in_hole"  # V型：下降后上升
    ICARUS = "icarus"  # 倒V型：上升后下降
    CINDERELLA = "cinderella"  # 波浪型：起伏多次
    OEDIPUS = "oedipus"  # 复杂型：先升后降再升
    FLAT = "flat"  # 平稳型：情感变化不大


@dataclass
class TrajectorySegment:
    """轨迹片段"""
    start_chapter: int
    end_chapter: int
    direction: str  # 'rising', 'falling', 'stable'
    intensity_change: float  # 强度变化量
    avg_intensity: float  # 平均强度


@dataclass
class TrajectoryAnalysis:
    """故事轨迹分析结果"""
    shape: TrajectoryShape
    shape_confidence: float  # 0-1，匹配度
    
    # 轨迹统计
    total_chapters: int
    avg_intensity: float
    intensity_range: Tuple[float, float]  # (min, max)
    volatility: float  # 波动性（标准差）
    
    # 轨迹片段
    segments: List[TrajectorySegment]
    
    # 关键点
    peak_chapters: List[int]  # 高峰章节
    valley_chapters: List[int]  # 低谷章节
    turning_points: List[int]  # 转折点章节
    
    # 描述
    description: str
    recommendations: List[str]


class StoryTrajectoryAnalyzer:
    """故事轨迹分析器"""
    
    def __init__(self):
        self.min_chapters_for_analysis = 3  # 最少需要的章节数
    
    def analyze_trajectory(
        self, 
        emotion_points: List[Dict]
    ) -> TrajectoryAnalysis:
        """
        分析故事轨迹
        
        Args:
            emotion_points: 情感点列表，每个点包含 chapter_number 和 intensity
            
        Returns:
            TrajectoryAnalysis: 轨迹分析结果
        """
        if len(emotion_points) < self.min_chapters_for_analysis:
            return self._create_insufficient_data_result(len(emotion_points))
        
        # 提取强度序列
        intensities = [point.get('primary_intensity', point.get('intensity', 5.0)) 
                      for point in emotion_points]
        chapters = [point.get('chapter_number', i+1) 
                   for i, point in enumerate(emotion_points)]
        
        # 1. 计算基本统计
        avg_intensity = statistics.mean(intensities)
        intensity_range = (min(intensities), max(intensities))
        volatility = statistics.stdev(intensities) if len(intensities) > 1 else 0.0
        
        # 2. 识别轨迹片段
        segments = self._identify_segments(chapters, intensities)
        
        # 3. 识别关键点
        peak_chapters = self._find_peaks(chapters, intensities)
        valley_chapters = self._find_valleys(chapters, intensities)
        turning_points = self._find_turning_points(chapters, intensities)
        
        # 4. 识别故事形状
        shape, confidence = self._identify_shape(segments, intensities)
        
        # 5. 生成描述和建议
        description = self._generate_description(shape, segments, avg_intensity, volatility)
        recommendations = self._generate_recommendations(shape, segments, volatility)
        
        return TrajectoryAnalysis(
            shape=shape,
            shape_confidence=confidence,
            total_chapters=len(emotion_points),
            avg_intensity=round(avg_intensity, 2),
            intensity_range=intensity_range,
            volatility=round(volatility, 2),
            segments=segments,
            peak_chapters=peak_chapters,
            valley_chapters=valley_chapters,
            turning_points=turning_points,
            description=description,
            recommendations=recommendations
        )
    
    def _identify_segments(
        self, 
        chapters: List[int], 
        intensities: List[float]
    ) -> List[TrajectorySegment]:
        """识别轨迹片段"""
        segments = []
        
        if len(intensities) < 2:
            return segments
        
        # 使用滑动窗口识别趋势
        window_size = max(2, len(intensities) // 4)
        i = 0
        
        while i < len(intensities):
            end_idx = min(i + window_size, len(intensities))
            segment_intensities = intensities[i:end_idx]
            
            # 计算趋势
            if len(segment_intensities) < 2:
                break
            
            start_intensity = segment_intensities[0]
            end_intensity = segment_intensities[-1]
            intensity_change = end_intensity - start_intensity
            avg_intensity = statistics.mean(segment_intensities)
            
            # 判断方向
            if intensity_change > 0.5:
                direction = 'rising'
            elif intensity_change < -0.5:
                direction = 'falling'
            else:
                direction = 'stable'
            
            segments.append(TrajectorySegment(
                start_chapter=chapters[i],
                end_chapter=chapters[end_idx - 1],
                direction=direction,
                intensity_change=round(intensity_change, 2),
                avg_intensity=round(avg_intensity, 2)
            ))
            
            i = end_idx
        
        return segments
    
    def _find_peaks(self, chapters: List[int], intensities: List[float]) -> List[int]:
        """找到高峰章节（局部最大值）"""
        peaks = []
        
        for i in range(1, len(intensities) - 1):
            if intensities[i] > intensities[i-1] and intensities[i] > intensities[i+1]:
                if intensities[i] >= 7.0:  # 只记录强度 >= 7.0 的高峰
                    peaks.append(chapters[i])
        
        # 如果没有找到，选择全局最大值
        if not peaks and intensities:
            max_idx = intensities.index(max(intensities))
            peaks.append(chapters[max_idx])
        
        return peaks
    
    def _find_valleys(self, chapters: List[int], intensities: List[float]) -> List[int]:
        """找到低谷章节（局部最小值）"""
        valleys = []
        
        for i in range(1, len(intensities) - 1):
            if intensities[i] < intensities[i-1] and intensities[i] < intensities[i+1]:
                if intensities[i] <= 4.0:  # 只记录强度 <= 4.0 的低谷
                    valleys.append(chapters[i])
        
        # 如果没有找到，选择全局最小值
        if not valleys and intensities:
            min_idx = intensities.index(min(intensities))
            valleys.append(chapters[min_idx])
        
        return valleys
    
    def _find_turning_points(self, chapters: List[int], intensities: List[float]) -> List[int]:
        """找到转折点（方向改变的点）"""
        turning_points = []
        
        if len(intensities) < 3:
            return turning_points
        
        for i in range(1, len(intensities) - 1):
            prev_change = intensities[i] - intensities[i-1]
            next_change = intensities[i+1] - intensities[i]
            
            # 方向改变且变化幅度足够大
            if abs(prev_change) > 1.0 and abs(next_change) > 1.0:
                if (prev_change > 0 and next_change < 0) or (prev_change < 0 and next_change > 0):
                    turning_points.append(chapters[i])
        
        return turning_points
    
    def _identify_shape(
        self, 
        segments: List[TrajectorySegment], 
        intensities: List[float]
    ) -> Tuple[TrajectoryShape, float]:
        """识别故事形状"""
        if not segments:
            return TrajectoryShape.FLAT, 0.5
        
        # 提取片段方向序列
        directions = [seg.direction for seg in segments]
        
        # 计算整体趋势
        overall_change = intensities[-1] - intensities[0]
        
        # 计算波动次数（方向改变次数）
        direction_changes = sum(1 for i in range(len(directions)-1) 
                               if directions[i] != directions[i+1])
        
        # 形状匹配逻辑
        shape_scores = {}
        
        # 1. 上升型 (Rags to Riches)
        if overall_change > 2.0 and directions.count('rising') > len(directions) * 0.6:
            shape_scores[TrajectoryShape.RAGS_TO_RICHES] = 0.8 + min(0.2, overall_change / 10)
        
        # 2. 下降型 (Riches to Rags)
        if overall_change < -2.0 and directions.count('falling') > len(directions) * 0.6:
            shape_scores[TrajectoryShape.RICHES_TO_RAGS] = 0.8 + min(0.2, abs(overall_change) / 10)
        
        # 3. V型 (Man in Hole)
        if direction_changes >= 1 and 'falling' in directions[:len(directions)//2] and 'rising' in directions[len(directions)//2:]:
            shape_scores[TrajectoryShape.MAN_IN_HOLE] = 0.7 + min(0.3, direction_changes / 5)
        
        # 4. 倒V型 (Icarus)
        if direction_changes >= 1 and 'rising' in directions[:len(directions)//2] and 'falling' in directions[len(directions)//2:]:
            shape_scores[TrajectoryShape.ICARUS] = 0.7 + min(0.3, direction_changes / 5)
        
        # 5. 波浪型 (Cinderella)
        if direction_changes >= 3:
            shape_scores[TrajectoryShape.CINDERELLA] = 0.6 + min(0.4, direction_changes / 10)
        
        # 6. 复杂型 (Oedipus)
        if direction_changes >= 2 and len(segments) >= 3:
            # 先升后降再升的模式
            if directions[0] == 'rising' and 'falling' in directions[1:-1] and directions[-1] == 'rising':
                shape_scores[TrajectoryShape.OEDIPUS] = 0.75
        
        # 7. 平稳型 (Flat)
        if directions.count('stable') > len(directions) * 0.7 or abs(overall_change) < 1.0:
            shape_scores[TrajectoryShape.FLAT] = 0.6
        
        # 选择最高分的形状
        if shape_scores:
            best_shape = max(shape_scores.items(), key=lambda x: x[1])
            return best_shape[0], best_shape[1]
        
        # 默认返回平稳型
        return TrajectoryShape.FLAT, 0.5
    
    def _generate_description(
        self, 
        shape: TrajectoryShape, 
        segments: List[TrajectorySegment],
        avg_intensity: float,
        volatility: float
    ) -> str:
        """生成轨迹描述"""
        shape_descriptions = {
            TrajectoryShape.RAGS_TO_RICHES: "故事呈现上升型轨迹，情感从低谷逐渐走向高潮，给读者带来积极向上的阅读体验。",
            TrajectoryShape.RICHES_TO_RAGS: "故事呈现下降型轨迹，情感从高峰逐渐走向低谷，营造出悲剧性的氛围。",
            TrajectoryShape.MAN_IN_HOLE: "故事呈现V型轨迹，主角经历低谷后重新崛起，符合经典的'英雄之旅'模式。",
            TrajectoryShape.ICARUS: "故事呈现倒V型轨迹，主角从高峰跌落，具有强烈的戏剧张力。",
            TrajectoryShape.CINDERELLA: "故事呈现波浪型轨迹，情感起伏多次，情节跌宕起伏，扣人心弦。",
            TrajectoryShape.OEDIPUS: "故事呈现复杂型轨迹，情感变化丰富，层次分明，具有深刻的主题表达。",
            TrajectoryShape.FLAT: "故事呈现平稳型轨迹，情感变化较小，适合日常向或治愈系作品。",
        }
        
        desc = shape_descriptions.get(shape, "")
        
        # 添加统计信息
        desc += f" 平均情感强度为 {avg_intensity:.1f}/10"
        
        if volatility > 2.0:
            desc += "，情感波动剧烈"
        elif volatility > 1.0:
            desc += "，情感波动适中"
        else:
            desc += "，情感波动平缓"
        
        desc += f"。全文共 {len(segments)} 个主要情节段落。"
        
        return desc
    
    def _generate_recommendations(
        self, 
        shape: TrajectoryShape, 
        segments: List[TrajectorySegment],
        volatility: float
    ) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 基于形状的建议
        if shape == TrajectoryShape.FLAT:
            recommendations.append("建议增加情节冲突和情感起伏，避免故事过于平淡")
            recommendations.append("可以添加转折点或意外事件来提升戏剧张力")
        
        elif shape == TrajectoryShape.RAGS_TO_RICHES:
            recommendations.append("上升型故事需要注意节奏，避免过快或过慢")
            recommendations.append("建议在上升过程中加入小的挫折，增加真实感")
        
        elif shape == TrajectoryShape.RICHES_TO_RAGS:
            recommendations.append("下降型故事需要给读者希望，避免过于压抑")
            recommendations.append("可以在结尾留下一丝光明或反思空间")
        
        elif shape == TrajectoryShape.MAN_IN_HOLE:
            recommendations.append("V型故事的低谷部分需要足够深刻，才能让后续的上升更有力量")
            recommendations.append("注意低谷和上升的转折点要合理且有说服力")
        
        elif shape == TrajectoryShape.ICARUS:
            recommendations.append("倒V型故事的下降需要有充分的铺垫和原因")
            recommendations.append("可以在结尾加入反思或教训，提升主题深度")
        
        elif shape == TrajectoryShape.CINDERELLA:
            recommendations.append("波浪型故事需要注意每次起伏的合理性")
            recommendations.append("避免情节过于重复，每次起伏都应有新的内容")
        
        # 基于波动性的建议
        if volatility < 0.8:
            recommendations.append("情感波动较小，建议增加情节冲突和情感张力")
        elif volatility > 3.0:
            recommendations.append("情感波动过于剧烈，建议适当平衡，给读者喘息空间")
        
        # 基于片段的建议
        if len(segments) < 3:
            recommendations.append("故事结构较为简单，可以考虑增加更多的情节层次")
        
        return recommendations
    
    def _create_insufficient_data_result(self, chapter_count: int) -> TrajectoryAnalysis:
        """创建数据不足时的结果"""
        return TrajectoryAnalysis(
            shape=TrajectoryShape.FLAT,
            shape_confidence=0.0,
            total_chapters=chapter_count,
            avg_intensity=5.0,
            intensity_range=(5.0, 5.0),
            volatility=0.0,
            segments=[],
            peak_chapters=[],
            valley_chapters=[],
            turning_points=[],
            description=f"当前仅有 {chapter_count} 章，数据不足以进行完整的轨迹分析。建议至少完成 {self.min_chapters_for_analysis} 章后再进行分析。",
            recommendations=["继续创作更多章节", "保持情节的连贯性和情感的变化"]
        )


# 导出函数
def analyze_story_trajectory(emotion_points: List[Dict]) -> Dict:
    """
    故事轨迹分析函数
    
    Args:
        emotion_points: 情感点列表
        
    Returns:
        Dict: 轨迹分析结果字典
    """
    analyzer = StoryTrajectoryAnalyzer()
    result = analyzer.analyze_trajectory(emotion_points)
    
    return {
        'shape': result.shape.value,
        'shape_confidence': result.shape_confidence,
        'total_chapters': result.total_chapters,
        'avg_intensity': result.avg_intensity,
        'intensity_range': result.intensity_range,
        'volatility': result.volatility,
        'segments': [
            {
                'start_chapter': seg.start_chapter,
                'end_chapter': seg.end_chapter,
                'direction': seg.direction,
                'intensity_change': seg.intensity_change,
                'avg_intensity': seg.avg_intensity,
            }
            for seg in result.segments
        ],
        'peak_chapters': result.peak_chapters,
        'valley_chapters': result.valley_chapters,
        'turning_points': result.turning_points,
        'description': result.description,
        'recommendations': result.recommendations,
    }
