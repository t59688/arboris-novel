# AIMETA P=大纲转写器_标签移除和后处理|R=标签移除_列表转换_视角验证|NR=不含内容生成|E=OutlineRewriter_PostProcessor|X=internal|A=转写器类|D=none|S=none|RD=./README.ai
"""
大纲转写器和后处理过滤模块
将结构化大纲转化为自然叙事，移除显式标签
"""
import re
from typing import List, Dict, Tuple, Optional


class OutlineRewriter:
    """大纲转写器 - 将结构化大纲转化为自然叙事指导"""
    
    # 需要移除或转换的标签模式
    TAG_PATTERNS = [
        r'【[^】]+】',  # 【标签】
        r'\[[^\]]+\]',  # [标签]
        r'<[^>]+>',     # <标签>
        r'##+\s*',      # Markdown标题标记
    ]
    
    # 列表式表述模式
    LIST_PATTERNS = [
        r'^\s*[一二三四五六七八九十]+[、，。]',  # 中文序号
        r'^\s*\d+[、，。]',                      # 数字序号
        r'^\s*[①②③④⑤⑥⑦⑧⑨⑩]',                # 圆圈数字
        r'^\s*[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽]',                # 括号数字
        r'^\s*首先[，、]',                        # 首先、其次、然后
        r'^\s*其次[，、]',
        r'^\s*然后[，、]',
        r'^\s*最后[，、]',
        r'^\s*第一[，、]',
        r'^\s*第二[，、]',
        r'^\s*第三[，、]',
    ]
    
    @staticmethod
    def remove_explicit_tags(text: str) -> str:
        """
        移除文本中的显式标签
        
        Args:
            text: 原始文本
        
        Returns:
            移除标签后的文本
        """
        cleaned = text
        
        for pattern in OutlineRewriter.TAG_PATTERNS:
            cleaned = re.sub(pattern, '', cleaned)
        
        # 移除多余的空行
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        return cleaned.strip()
    
    @staticmethod
    def convert_list_to_narrative(text: str) -> str:
        """
        将列表式表述转换为自然叙事
        
        Args:
            text: 原始文本
        
        Returns:
            转换后的文本
        """
        lines = text.split('\n')
        converted_lines = []
        
        in_list = False
        list_items = []
        
        for line in lines:
            is_list_item = False
            
            for pattern in OutlineRewriter.LIST_PATTERNS:
                if re.match(pattern, line):
                    is_list_item = True
                    # 移除序号标记
                    cleaned_line = re.sub(pattern, '', line).strip()
                    list_items.append(cleaned_line)
                    in_list = True
                    break
            
            if not is_list_item:
                if in_list and list_items:
                    # 将列表项转换为自然叙事
                    narrative = OutlineRewriter._list_items_to_narrative(list_items)
                    converted_lines.append(narrative)
                    list_items = []
                    in_list = False
                
                converted_lines.append(line)
        
        # 处理最后的列表
        if list_items:
            narrative = OutlineRewriter._list_items_to_narrative(list_items)
            converted_lines.append(narrative)
        
        return '\n'.join(converted_lines)
    
    @staticmethod
    def _list_items_to_narrative(items: List[str]) -> str:
        """将列表项转换为自然叙事"""
        if len(items) == 0:
            return ""
        elif len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return f"{items[0]}，接着{items[1]}"
        else:
            # 多个项目，使用连接词
            narrative = items[0]
            for i in range(1, len(items) - 1):
                narrative += f"，随后{items[i]}"
            narrative += f"，最终{items[-1]}"
            return narrative
    
    @staticmethod
    def rewrite_outline_to_guidance(outline: str) -> str:
        """
        将大纲重写为叙事指导
        
        将结构化的大纲要点转换为自然语言的创作指导，
        而不是直接可输出的文本
        
        Args:
            outline: 原始大纲
        
        Returns:
            叙事指导
        """
        # 1. 移除显式标签
        text = OutlineRewriter.remove_explicit_tags(outline)
        
        # 2. 转换列表式表述
        text = OutlineRewriter.convert_list_to_narrative(text)
        
        # 3. 添加叙事指导性语言
        text = OutlineRewriter._add_narrative_guidance(text)
        
        return text
    
    @staticmethod
    def _add_narrative_guidance(text: str) -> str:
        """为大纲要点添加叙事指导性语言"""
        # 在段落前添加指导性前缀
        guidance_prefixes = [
            "本章应当展现",
            "通过场景描写",
            "可以通过对话揭示",
            "用动作和心理描写表现",
        ]
        
        lines = text.split('\n')
        guided_lines = []
        
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith(('本章', '通过', '可以', '用')):
                # 随机选择一个指导性前缀（实际应用中可以更智能）
                prefix_index = i % len(guidance_prefixes)
                guided_lines.append(f"{guidance_prefixes[prefix_index]}{line}")
            else:
                guided_lines.append(line)
        
        return '\n'.join(guided_lines)


class PostProcessor:
    """后处理器 - 对生成的文本进行质量检查和优化"""
    
    @staticmethod
    def filter_and_clean(text: str) -> Tuple[str, List[Dict]]:
        """
        过滤和清理文本
        
        Args:
            text: 原始生成的文本
        
        Returns:
            (清理后的文本, 发现的问题列表)
        """
        issues = []
        cleaned = text
        
        # 1. 检查并移除显式标签
        tag_matches = []
        for pattern in OutlineRewriter.TAG_PATTERNS:
            matches = re.findall(pattern, cleaned)
            tag_matches.extend(matches)
        
        if tag_matches:
            issues.append({
                'type': 'explicit_tags',
                'severity': 'high',
                'description': f'发现显式标签：{", ".join(set(tag_matches))}',
                'action': '已自动移除',
            })
            cleaned = OutlineRewriter.remove_explicit_tags(cleaned)
        
        # 2. 检查列表式表述
        list_matches = []
        for line in cleaned.split('\n'):
            for pattern in OutlineRewriter.LIST_PATTERNS:
                if re.match(pattern, line):
                    list_matches.append(line.strip())
                    break
        
        if list_matches:
            issues.append({
                'type': 'list_format',
                'severity': 'medium',
                'description': f'发现列表式表述（{len(list_matches)}处）',
                'action': '已自动转换为自然叙事',
            })
            cleaned = OutlineRewriter.convert_list_to_narrative(cleaned)
        
        # 3. 检查全知视角标记
        omniscient_patterns = [
            r'与此同时[，。]',
            r'此时此刻[，。]',
            r'在.*不知道的情况下',
            r'殊不知[，。]',
            r'实际上[，。]',  # 在某些上下文中可能是全知
        ]
        
        omniscient_matches = []
        for pattern in omniscient_patterns:
            matches = re.findall(pattern, cleaned)
            omniscient_matches.extend(matches)
        
        if omniscient_matches:
            issues.append({
                'type': 'omniscient_perspective',
                'severity': 'medium',
                'description': f'可能存在全知视角表述：{", ".join(set(omniscient_matches))}',
                'action': '需要人工检查',
            })
        
        # 4. 检查过长的段落
        paragraphs = cleaned.split('\n\n')
        long_paragraphs = [
            (i, len(p)) for i, p in enumerate(paragraphs)
            if len(p) > 500
        ]
        
        if long_paragraphs:
            issues.append({
                'type': 'long_paragraph',
                'severity': 'low',
                'description': f'发现{len(long_paragraphs)}个过长段落（>500字）',
                'action': '建议拆分段落以提高可读性',
            })
        
        # 5. 检查对话格式
        dialogue_issues = PostProcessor._check_dialogue_format(cleaned)
        if dialogue_issues:
            issues.extend(dialogue_issues)
        
        return cleaned, issues
    
    @staticmethod
    def _check_dialogue_format(text: str) -> List[Dict]:
        """检查对话格式是否规范"""
        issues = []
        
        # 检查是否有未闭合的引号
        quote_count = text.count('"') + text.count('"')
        if quote_count % 2 != 0:
            issues.append({
                'type': 'dialogue_format',
                'severity': 'medium',
                'description': '对话引号未成对出现',
                'action': '需要检查对话格式',
            })
        
        return issues
    
    @staticmethod
    def enhance_language(text: str) -> str:
        """
        提升文本的文学性
        
        这是一个简化版本，实际应用中可以使用更复杂的NLP技术
        或调用LLM进行润色
        """
        enhanced = text
        
        # 简单的替换示例（实际应用中应该更智能）
        replacements = {
            '很': '十分',
            '非常': '极为',
            '走': '行',
            '看': '望',
        }
        
        # 注意：这里的替换非常简单，实际应用中需要考虑上下文
        # 建议使用LLM进行更智能的润色
        
        return enhanced
    
    @staticmethod
    def validate_perspective(text: str, protagonist_knowledge: Dict) -> List[Dict]:
        """
        验证视角一致性
        
        Args:
            text: 文本内容
            protagonist_knowledge: 主角的认知状态
        
        Returns:
            视角问题列表
        """
        issues = []
        
        # 检查是否提及了主角不应知道的信息
        unknown_facts = protagonist_knowledge.get('unknown_knowledge', {})
        
        for category, facts in unknown_facts.items():
            for fact in facts:
                # 简化的检查：看是否直接提及
                if fact.lower() in text.lower():
                    issues.append({
                        'type': 'knowledge_leak',
                        'severity': 'critical',
                        'description': f'文本中提及了主角不应知道的信息：{fact}',
                        'action': '需要修改或删除相关内容',
                    })
        
        return issues
    
    @staticmethod
    def suggest_improvements(text: str, emotion_intensity: float) -> List[str]:
        """
        根据文本和目标情绪强度提供改进建议
        
        Args:
            text: 文本内容
            emotion_intensity: 目标情绪强度（1-10）
        
        Returns:
            改进建议列表
        """
        suggestions = []
        
        # 分析句子长度
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return suggestions
        
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
        
        # 根据情绪强度和句子长度给出建议
        if emotion_intensity >= 8.0:
            if avg_sentence_length > 30:
                suggestions.append("高强度场景建议使用更短的句子（平均<25字），增强紧张感")
        elif emotion_intensity <= 4.0:
            if avg_sentence_length < 20:
                suggestions.append("低强度场景可以使用更长的句子（平均>25字），营造舒缓氛围")
        
        # 检查对话比例
        dialogue_lines = len(re.findall(r'[""].*?[""]', text))
        total_lines = len(sentences)
        dialogue_ratio = dialogue_lines / total_lines if total_lines > 0 else 0
        
        if emotion_intensity >= 7.0 and dialogue_ratio < 0.3:
            suggestions.append("高强度场景建议增加对话，使冲突更直接")
        elif emotion_intensity <= 4.0 and dialogue_ratio > 0.5:
            suggestions.append("低强度场景可以减少对话，增加环境和心理描写")
        
        # 检查动作词密度
        action_verbs = ['冲', '跑', '打', '击', '砍', '刺', '躲', '闪', '跳', '飞']
        action_count = sum(text.count(verb) for verb in action_verbs)
        
        if emotion_intensity >= 8.0 and action_count < 5:
            suggestions.append("高强度场景建议增加动作描写，提升画面感")
        
        return suggestions


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例1：移除显式标签
    text_with_tags = """
    【三次递进挑战】
    主角面对三个挑战：
    一、击败守门人
    二、破解机关阵
    三、通过心魔考验
    
    【双方势力】
    正派和邪派展开对决。
    """
    
    print("原文：")
    print(text_with_tags)
    print("\n" + "="*50 + "\n")
    
    cleaned = OutlineRewriter.remove_explicit_tags(text_with_tags)
    print("移除标签后：")
    print(cleaned)
    print("\n" + "="*50 + "\n")
    
    # 示例2：转换列表式表述
    converted = OutlineRewriter.convert_list_to_narrative(cleaned)
    print("转换列表后：")
    print(converted)
    print("\n" + "="*50 + "\n")
    
    # 示例3：后处理过滤
    generated_text = """
    【场景】林枫来到山洞。
    
    与此同时，反派正在密谋。殊不知，林枫已经察觉。
    
    "我一定要找到宝藏！"林枫说道。
    
    首先，他检查了洞口。其次，他点燃火把。最后，他走进深处。
    """
    
    print("原始生成文本：")
    print(generated_text)
    print("\n" + "="*50 + "\n")
    
    cleaned, issues = PostProcessor.filter_and_clean(generated_text)
    print("清理后的文本：")
    print(cleaned)
    print("\n发现的问题：")
    for issue in issues:
        print(f"  [{issue['severity']}] {issue['description']}")
        print(f"    处理：{issue['action']}")
    print("\n" + "="*50 + "\n")
    
    # 示例4：改进建议
    suggestions = PostProcessor.suggest_improvements(cleaned, emotion_intensity=8.5)
    print("改进建议：")
    for suggestion in suggestions:
        print(f"  - {suggestion}")
