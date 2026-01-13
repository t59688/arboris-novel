# AIMETA P=节奏控制器_情绪曲线规划|R=三幕结构_英雄之旅_曲线验证|NR=不含内容生成|E=PacingController|X=internal|A=控制器类|D=none|S=none|RD=./README.ai
"""
节奏控制器和情绪曲线规划模块
实现起伏有致的叙事节奏，避免持续高能或平淡
"""
from typing import List, Dict, Tuple, Optional
import math


class PacingController:
    """节奏控制器 - 规划和调控故事情绪曲线"""
    
    def __init__(self, total_chapters: int, story_structure: str = "three_act"):
        """
        初始化节奏控制器
        
        Args:
            total_chapters: 总章节数
            story_structure: 故事结构类型（three_act, hero_journey, custom）
        """
        self.total_chapters = total_chapters
        self.story_structure = story_structure
        self.emotion_curve = []
    
    def plan_emotion_curve(
        self,
        min_intensity: float = 2.0,
        max_intensity: float = 9.5,
        num_peaks: int = None,
    ) -> List[Dict]:
        """
        规划整体情绪曲线
        
        Args:
            min_intensity: 最低情绪强度
            max_intensity: 最高情绪强度
            num_peaks: 高潮数量（None 则自动计算）
        
        Returns:
            每章的情绪强度和叙事阶段
        """
        if num_peaks is None:
            # 根据章节数自动计算高潮数量
            if self.total_chapters <= 10:
                num_peaks = 1
            elif self.total_chapters <= 30:
                num_peaks = 2
            elif self.total_chapters <= 50:
                num_peaks = 3
            else:
                num_peaks = 4
        
        if self.story_structure == "three_act":
            curve = self._plan_three_act_curve(min_intensity, max_intensity, num_peaks)
        elif self.story_structure == "hero_journey":
            curve = self._plan_hero_journey_curve(min_intensity, max_intensity)
        else:
            curve = self._plan_wave_curve(min_intensity, max_intensity, num_peaks)
        
        self.emotion_curve = curve
        return curve
    
    def _plan_three_act_curve(
        self,
        min_intensity: float,
        max_intensity: float,
        num_peaks: int,
    ) -> List[Dict]:
        """规划三幕结构的情绪曲线"""
        curve = []
        
        # 三幕分界点
        act1_end = int(self.total_chapters * 0.25)
        act2_end = int(self.total_chapters * 0.75)
        
        for chapter in range(1, self.total_chapters + 1):
            if chapter <= act1_end:
                # 第一幕：铺垫与设定，逐步上升
                progress = chapter / act1_end
                intensity = min_intensity + (5.0 - min_intensity) * progress
                phase = "exposition" if chapter <= act1_end // 2 else "rising_action"
                
            elif chapter <= act2_end:
                # 第二幕：发展与冲突，波浪式上升
                act2_progress = (chapter - act1_end) / (act2_end - act1_end)
                
                # 使用正弦波叠加线性增长，创造起伏
                base_intensity = 5.0 + (7.5 - 5.0) * act2_progress
                wave_amplitude = 1.5
                wave_frequency = num_peaks * math.pi
                wave = wave_amplitude * math.sin(act2_progress * wave_frequency)
                
                intensity = base_intensity + wave
                
                # 中点设置一个明显的转折
                midpoint = act1_end + (act2_end - act1_end) // 2
                if abs(chapter - midpoint) <= 1:
                    intensity = max(intensity, 7.5)
                
                phase = "rising_action"
                
            else:
                # 第三幕：高潮与解决
                act3_progress = (chapter - act2_end) / (self.total_chapters - act2_end)
                
                if act3_progress < 0.4:
                    # 前40%：冲向最终高潮
                    intensity = 7.5 + (max_intensity - 7.5) * (act3_progress / 0.4)
                    phase = "climax"
                elif act3_progress < 0.7:
                    # 中30%：最终高潮
                    intensity = max_intensity
                    phase = "climax"
                else:
                    # 后30%：回落至结局
                    falloff = (act3_progress - 0.7) / 0.3
                    intensity = max_intensity - (max_intensity - 4.0) * falloff
                    phase = "falling_action" if act3_progress < 0.9 else "resolution"
            
            # 限制范围
            intensity = max(min_intensity, min(max_intensity, intensity))
            
            curve.append({
                'chapter_number': chapter,
                'emotion_intensity': round(intensity, 1),
                'narrative_phase': phase,
                'is_peak': intensity >= 8.0,
                'is_valley': intensity <= 3.5,
            })
        
        return curve
    
    def _plan_hero_journey_curve(
        self,
        min_intensity: float,
        max_intensity: float,
    ) -> List[Dict]:
        """规划英雄之旅结构的情绪曲线"""
        curve = []
        
        # 英雄之旅的12个阶段及其情绪强度特征
        stages = [
            ('ordinary_world', 0.00, 0.10, 3.0, 'exposition'),
            ('call_to_adventure', 0.10, 0.20, 5.5, 'rising_action'),
            ('refusal_of_call', 0.20, 0.25, 4.0, 'rising_action'),
            ('meeting_mentor', 0.25, 0.30, 5.0, 'rising_action'),
            ('crossing_threshold', 0.30, 0.40, 6.5, 'rising_action'),
            ('tests_allies_enemies', 0.40, 0.60, 6.0, 'rising_action'),  # 波动段
            ('approach_cave', 0.60, 0.70, 7.0, 'rising_action'),
            ('ordeal', 0.70, 0.85, 9.0, 'climax'),
            ('reward', 0.85, 0.90, 7.5, 'falling_action'),
            ('road_back', 0.90, 0.93, 6.0, 'falling_action'),
            ('resurrection', 0.93, 0.97, 8.5, 'climax'),
            ('return_with_elixir', 0.97, 1.00, 4.5, 'resolution'),
        ]
        
        for chapter in range(1, self.total_chapters + 1):
            progress = (chapter - 1) / (self.total_chapters - 1)
            
            # 找到当前所在阶段
            current_stage = None
            for stage_name, start, end, base_intensity, phase in stages:
                if start <= progress < end:
                    current_stage = (stage_name, start, end, base_intensity, phase)
                    break
            
            if current_stage is None:
                current_stage = stages[-1]
            
            stage_name, start, end, base_intensity, phase = current_stage
            
            # 在阶段内部添加微小波动
            stage_progress = (progress - start) / (end - start) if end > start else 0
            micro_wave = 0.3 * math.sin(stage_progress * 2 * math.pi)
            
            # 特殊处理"试炼、盟友与敌人"阶段，增加波动
            if stage_name == 'tests_allies_enemies':
                wave_amplitude = 1.0
                wave_frequency = 3 * math.pi
                macro_wave = wave_amplitude * math.sin(stage_progress * wave_frequency)
                intensity = base_intensity + macro_wave + micro_wave
            else:
                intensity = base_intensity + micro_wave
            
            # 限制范围
            intensity = max(min_intensity, min(max_intensity, intensity))
            
            curve.append({
                'chapter_number': chapter,
                'emotion_intensity': round(intensity, 1),
                'narrative_phase': phase,
                'hero_journey_stage': stage_name,
                'is_peak': intensity >= 8.0,
                'is_valley': intensity <= 3.5,
            })
        
        return curve
    
    def _plan_wave_curve(
        self,
        min_intensity: float,
        max_intensity: float,
        num_peaks: int,
    ) -> List[Dict]:
        """规划波浪式上升的情绪曲线"""
        curve = []
        
        for chapter in range(1, self.total_chapters + 1):
            progress = (chapter - 1) / (self.total_chapters - 1)
            
            # 基础线性增长
            base_intensity = min_intensity + (max_intensity - min_intensity) * progress
            
            # 叠加正弦波创造起伏
            wave_amplitude = (max_intensity - min_intensity) * 0.2
            wave_frequency = num_peaks * math.pi
            wave = wave_amplitude * math.sin(progress * wave_frequency)
            
            intensity = base_intensity + wave
            
            # 限制范围
            intensity = max(min_intensity, min(max_intensity, intensity))
            
            # 判断叙事阶段
            if progress < 0.15:
                phase = "exposition"
            elif progress < 0.75:
                phase = "rising_action"
            elif progress < 0.90:
                phase = "climax"
            else:
                phase = "resolution"
            
            curve.append({
                'chapter_number': chapter,
                'emotion_intensity': round(intensity, 1),
                'narrative_phase': phase,
                'is_peak': intensity >= 8.0,
                'is_valley': intensity <= 3.5,
            })
        
        return curve
    
    def get_chapter_pacing(self, chapter_number: int) -> Dict:
        """
        获取指定章节的节奏信息
        
        Returns:
            包含情绪强度、叙事阶段、节奏建议等信息
        """
        if not self.emotion_curve:
            raise ValueError("请先调用 plan_emotion_curve() 规划情绪曲线")
        
        if chapter_number < 1 or chapter_number > self.total_chapters:
            raise ValueError(f"章节编号 {chapter_number} 超出范围")
        
        chapter_data = self.emotion_curve[chapter_number - 1]
        
        # 获取前后章节的强度，用于判断趋势
        prev_intensity = self.emotion_curve[chapter_number - 2]['emotion_intensity'] if chapter_number > 1 else chapter_data['emotion_intensity']
        next_intensity = self.emotion_curve[chapter_number]['emotion_intensity'] if chapter_number < self.total_chapters else chapter_data['emotion_intensity']
        
        current_intensity = chapter_data['emotion_intensity']
        
        # 判断趋势
        if next_intensity > current_intensity + 0.5:
            trend = "rising"
        elif next_intensity < current_intensity - 0.5:
            trend = "falling"
        else:
            trend = "stable"
        
        # 生成节奏建议
        pacing_advice = self._generate_pacing_advice(
            current_intensity,
            prev_intensity,
            trend,
            chapter_data['narrative_phase']
        )
        
        return {
            **chapter_data,
            'trend': trend,
            'prev_intensity': prev_intensity,
            'next_intensity': next_intensity,
            'pacing_advice': pacing_advice,
        }
    
    def _generate_pacing_advice(
        self,
        current_intensity: float,
        prev_intensity: float,
        trend: str,
        phase: str,
    ) -> List[str]:
        """生成节奏建议"""
        advice = []
        
        # 基于当前强度的建议
        if current_intensity >= 8.0:
            advice.append("本章为高潮场景，使用短促有力的句子，快节奏推进")
            advice.append("减少环境描写，聚焦于动作和冲突")
        elif current_intensity >= 6.0:
            advice.append("本章情节紧张，平衡动作与心理描写")
            advice.append("适度的环境渲染，烘托紧张氛围")
        elif current_intensity >= 4.0:
            advice.append("本章节奏平稳，注重人物互动和心理活动")
            advice.append("细致的环境描写，营造氛围")
        else:
            advice.append("本章为过渡场景，详尽的环境和心理描写")
            advice.append("慢节奏叙事，给读者和角色喘息空间")
        
        # 基于趋势的建议
        if trend == "rising":
            advice.append("情节逐步升级，为下一章的高潮做铺垫")
        elif trend == "falling":
            advice.append("高潮后的缓冲，角色反思和情绪沉淀")
        
        # 基于前后对比的建议
        if prev_intensity >= 7.0 and current_intensity < 5.0:
            advice.append("⚠️ 重要：上一章为高潮，本章必须包含角色反应和过渡（Scene & Sequel）")
            advice.append("展现角色对前一章事件的情绪反应和思考")
        
        if current_intensity >= 8.0 and prev_intensity < 6.0:
            advice.append("⚠️ 注意：情绪强度急剧上升，需要合理的触发事件")
        
        return advice
    
    def validate_curve(self) -> Dict:
        """
        验证情绪曲线是否符合规范
        
        Returns:
            验证结果和改进建议
        """
        if not self.emotion_curve:
            return {'valid': False, 'error': '未规划情绪曲线'}
        
        issues = []
        
        # 检查1：是否有足够的起伏
        intensities = [point['emotion_intensity'] for point in self.emotion_curve]
        intensity_range = max(intensities) - min(intensities)
        
        if intensity_range < 3.0:
            issues.append({
                'type': 'insufficient_variation',
                'severity': 'high',
                'description': f'情绪强度变化范围过小（{intensity_range:.1f}），故事可能过于平淡',
                'suggestion': '增加情绪强度的起伏，设计更多的冲突和转折'
            })
        
        # 检查2：是否有持续高能段落
        consecutive_high = 0
        max_consecutive_high = 0
        
        for point in self.emotion_curve:
            if point['emotion_intensity'] >= 7.5:
                consecutive_high += 1
                max_consecutive_high = max(max_consecutive_high, consecutive_high)
            else:
                consecutive_high = 0
        
        if max_consecutive_high > 5:
            issues.append({
                'type': 'sustained_high_intensity',
                'severity': 'medium',
                'description': f'存在连续{max_consecutive_high}章的高强度情节，可能导致读者疲劳',
                'suggestion': '在高潮章节之间插入缓冲章节，给读者喘息空间'
            })
        
        # 检查3：是否有过长的平淡段落
        consecutive_low = 0
        max_consecutive_low = 0
        
        for point in self.emotion_curve:
            if point['emotion_intensity'] <= 4.0:
                consecutive_low += 1
                max_consecutive_low = max(max_consecutive_low, consecutive_low)
            else:
                consecutive_low = 0
        
        if max_consecutive_low > 6:
            issues.append({
                'type': 'sustained_low_intensity',
                'severity': 'medium',
                'description': f'存在连续{max_consecutive_low}章的低强度情节，可能导致读者失去兴趣',
                'suggestion': '在平缓段落中增加小冲突或转折，保持读者的注意力'
            })
        
        # 检查4：高潮是否在合适的位置
        climax_chapters = [p['chapter_number'] for p in self.emotion_curve if p['narrative_phase'] == 'climax']
        
        if climax_chapters:
            first_climax = min(climax_chapters)
            last_climax = max(climax_chapters)
            
            if first_climax < self.total_chapters * 0.5:
                issues.append({
                    'type': 'early_climax',
                    'severity': 'low',
                    'description': f'高潮出现较早（第{first_climax}章），可能导致后续情节乏力',
                    'suggestion': '考虑将主要高潮推迟，或在后期设计更强的高潮'
                })
            
            if last_climax > self.total_chapters * 0.95:
                issues.append({
                    'type': 'late_climax',
                    'severity': 'low',
                    'description': f'高潮出现过晚（第{last_climax}章），可能缺少足够的解决空间',
                    'suggestion': '适当提前高潮位置，为结局留出更多空间'
                })
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'summary': {
                'total_chapters': self.total_chapters,
                'intensity_range': intensity_range,
                'max_consecutive_high': max_consecutive_high,
                'max_consecutive_low': max_consecutive_low,
                'num_peaks': len([p for p in self.emotion_curve if p['is_peak']]),
                'num_valleys': len([p for p in self.emotion_curve if p['is_valley']]),
            }
        }
    
    def export_curve(self) -> List[Dict]:
        """导出完整的情绪曲线数据"""
        return self.emotion_curve


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建节奏控制器
    controller = PacingController(total_chapters=30, story_structure="three_act")
    
    # 规划情绪曲线
    curve = controller.plan_emotion_curve(min_intensity=2.0, max_intensity=9.5, num_peaks=3)
    
    # 打印前5章的信息
    print("前5章的情绪曲线：")
    for i in range(5):
        pacing = controller.get_chapter_pacing(i + 1)
        print(f"\n第{pacing['chapter_number']}章：")
        print(f"  情绪强度：{pacing['emotion_intensity']}/10")
        print(f"  叙事阶段：{pacing['narrative_phase']}")
        print(f"  趋势：{pacing['trend']}")
        print(f"  节奏建议：")
        for advice in pacing['pacing_advice']:
            print(f"    - {advice}")
    
    # 验证曲线
    validation = controller.validate_curve()
    print(f"\n曲线验证：{'通过' if validation['valid'] else '存在问题'}")
    if validation['issues']:
        print("问题列表：")
        for issue in validation['issues']:
            print(f"  - [{issue['severity']}] {issue['description']}")
            print(f"    建议：{issue['suggestion']}")
