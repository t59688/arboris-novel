# AIMETA P=优化提示模板_系统规约和生成模板|R=系统消息_章节生成_大纲生成|NR=不含模型调用|E=SYSTEM_MESSAGE_NOVELIST_generate_chapter_prompt|X=internal|A=模板函数|D=none|S=none|RD=./README.ai
"""
优化的小说生成 Prompt 模板系统
实现 5 大优化：
1. 移除显式标签（结构提示隐化为自然叙事）
2. 节奏建模与情绪曲线控制
3. 避免主角全知问题（主角视角约束）
4. 角色出场自然性
5. Prompt 结构优化与算法自检
"""

# ==================== 系统消息：写作规约 ====================

SYSTEM_MESSAGE_NOVELIST = """你是一位富有经验的小说家，擅长创作引人入胜的故事。你的写作风格自然流畅，注重细节描写和人物刻画。

## 核心写作规约

### 1. 叙事风格
- **禁止输出任何大纲标签或特殊标记**（如【三次递进挑战】、【双方势力】等）
- 所有结构要素必须通过自然叙事展现：对话、动作、环境描写、内心独白
- 输出内容应当像人类作家的作品，而非剧情大纲或提纲要点
- 使用生动的文学表述，避免列表式或说明性语言

### 2. 节奏控制
- **保持故事节奏张弛有度**，交替紧张与舒缓场景
- 高潮冲突场景后，必须跟随角色反应/过渡场景（Scene & Sequel）
- 避免持续高强度情节，给读者和角色"喘息"的空间
- 根据情绪强度参数调整句式：
  * 高强度（8-10）：短促有力的句子，快节奏动作描写
  * 中强度（4-7）：平衡的叙事节奏，动作与心理交织
  * 低强度（1-3）：舒缓细腻的句子，详尽的环境和心理描写

### 3. 视角限制
- **主角仅知其所知**，避免全知叙述
- 采用主角有限视角（第一人称或第三人称有限视角）
- 只描述主角感知到的事物，对未见未闻之事不做描述
- 主角可能犯错或持有偏见，随后通过情节发展修正认知
- 不以全知口吻描写场景（除非明确采用全知叙事风格）

### 4. 角色引入
- **新角色需先有铺垫**，出场时给出必要介绍
- 避免同时引入过多新角色
- 角色关系应逐步揭示，而非一开始就全盘托出
- 通过对话、回忆或情节自然引入角色背景
- 角色出场应符合剧情逻辑和社交逻辑

### 5. 逻辑自洽
- 保持人物行为和世界规则的逻辑一致性
- 角色动机应当合理，行为符合其性格设定
- 世界观设定应前后一致，不自相矛盾
- 情节发展应有因果关系，避免突兀的转折

### 6. 语言风格
- 使用生动形象的语言，富有画面感
- 对话要符合角色身份和性格
- 描写要有层次感：从宏观到微观，从外在到内心
- 善用修辞手法，但不过度堆砌

## 创作流程

1. **内部规划**：先在心中构思本章节的结构要点和情节走向
2. **自然转写**：将规划转化为流畅的小说文本，不暴露结构标签
3. **节奏调控**：根据情绪强度参数调整叙事节奏和句式
4. **视角检查**：确保未超出主角认知范围
5. **质量把关**：检查逻辑、语言和节奏是否符合规约

记住：你的目标是创作一部让读者沉浸其中的小说，而非展示你的创作提纲。"""


# ==================== 章节生成 Prompt 模板 ====================

def generate_chapter_prompt(
    project_info: dict,
    chapter_number: int,
    outline: str,
    previous_summary: str = "",
    emotion_intensity_target: float = 5.0,
    character_knowledge: dict = None,
    active_characters: list = None,
    world_knowledge: dict = None,
) -> str:
    """
    生成章节内容的 Prompt
    
    Args:
        project_info: 项目基本信息（标题、类型、世界观等）
        chapter_number: 章节编号
        outline: 本章大纲要点（内部规划用，不直接输出）
        previous_summary: 前文摘要
        emotion_intensity_target: 目标情绪强度（1-10）
        character_knowledge: 主角当前已知的知识
        active_characters: 已登场的角色列表
        world_knowledge: 世界观信息（标注主角是否知晓）
    """
    
    # 情绪强度描述
    intensity_desc = _get_intensity_description(emotion_intensity_target)
    
    # 主角认知约束
    knowledge_constraint = ""
    if character_knowledge:
        known_facts = character_knowledge.get('known_facts', [])
        unknown_facts = character_knowledge.get('unknown_facts', [])
        
        if known_facts:
            knowledge_constraint += f"\n\n**主角当前已知信息**：\n"
            for fact in known_facts:
                knowledge_constraint += f"- {fact}\n"
        
        if unknown_facts:
            knowledge_constraint += f"\n**主角当前未知信息**（不可在叙事中透露）：\n"
            for fact in unknown_facts:
                knowledge_constraint += f"- {fact}\n"
    
    # 角色出场约束
    character_constraint = ""
    if active_characters:
        character_constraint = f"\n\n**已登场角色**：{', '.join(active_characters)}\n"
        character_constraint += "如需引入新角色，请先通过对话或场景铺垫，再正式出场并介绍。"
    
    prompt = f"""## 创作任务

请为小说《{project_info.get('title', '未命名')}》创作第 {chapter_number} 章的正文内容。

### 项目信息
- **类型**：{project_info.get('genre', '未指定')}
- **风格**：{project_info.get('style', '未指定')}
- **世界观**：{project_info.get('worldview', '未设定')}

### 前情提要
{previous_summary if previous_summary else '（本章为开篇章节）'}

### 本章剧情要点（内部规划参考，不要以列表形式输出）
{outline}

### 创作要求

#### 1. 情绪强度目标
本章目标情绪强度：**{emotion_intensity_target:.1f}/10** - {intensity_desc}

{_get_pacing_guidance(emotion_intensity_target)}

#### 2. 视角与认知约束
- 采用主角有限视角，紧跟主角的感知和认知
- 主角只能知道其经历过或被告知的信息
- 对于主角未知的事物，可以通过其疑惑、推测来表现，但不要直接揭示答案
{knowledge_constraint}

#### 3. 角色管理
{character_constraint if character_constraint else '本章可能是主角首次登场，请自然地介绍主角的基本信息。'}

#### 4. 结构要求
- 将剧情要点融入自然叙事，通过对话、动作、环境描写展现
- 不要使用【】标记或列表式表述
- 确保情节有起承转合，但不要标注"起承转合"等字样

#### 5. 字数要求
正文字数：{project_info.get('chapter_length', 3000)} 字左右

### 输出格式
直接输出小说正文，无需任何标题、标签或说明。以自然的叙事开始，以自然的叙事结束。

---

现在开始创作："""
    
    return prompt


def _get_intensity_description(intensity: float) -> str:
    """根据情绪强度返回描述"""
    if intensity >= 9.0:
        return "极高强度，高潮场景，紧张刺激"
    elif intensity >= 7.0:
        return "高强度，冲突升级，节奏加快"
    elif intensity >= 5.0:
        return "中等强度，情节推进，张弛有度"
    elif intensity >= 3.0:
        return "低强度，过渡场景，舒缓平静"
    else:
        return "极低强度，铺垫场景，细腻描写"


def _get_pacing_guidance(intensity: float) -> str:
    """根据情绪强度返回节奏指导"""
    if intensity >= 8.0:
        return """**节奏指导**：
- 使用短促有力的句子，营造紧张感
- 快速推进动作场景，减少环境描写
- 对话简短直接，冲突激烈
- 适当使用感叹句和短句增强节奏感"""
    elif intensity >= 6.0:
        return """**节奏指导**：
- 平衡动作与心理描写
- 适度的环境渲染，烘托氛围
- 对话与叙述交织，推进情节
- 句式长短结合，保持阅读流畅性"""
    elif intensity >= 4.0:
        return """**节奏指导**：
- 注重心理活动和人物互动
- 细致的环境描写，营造氛围
- 对话深入，展现人物性格
- 使用较长的句子，节奏舒缓"""
    else:
        return """**节奏指导**：
- 详尽的环境和心理描写
- 慢节奏叙事，给读者喘息空间
- 深入人物内心，展现细腻情感
- 使用长句和复杂句式，营造沉思氛围
- 这是高潮后的缓冲，或下一波高潮前的铺垫"""


# ==================== 大纲生成 Prompt 模板 ====================

def generate_outline_prompt(
    project_info: dict,
    total_chapters: int,
    story_structure: str = "three_act",
) -> str:
    """
    生成整体大纲的 Prompt
    
    Args:
        project_info: 项目基本信息
        total_chapters: 总章节数
        story_structure: 故事结构（three_act, hero_journey, etc.）
    """
    
    structure_guide = _get_structure_guidance(story_structure, total_chapters)
    
    prompt = f"""## 大纲规划任务

请为小说《{project_info.get('title', '未命名')}》规划完整的章节大纲。

### 项目信息
- **类型**：{project_info.get('genre', '未指定')}
- **风格**：{project_info.get('style', '未指定')}
- **世界观**：{project_info.get('worldview', '未设定')}
- **主要角色**：{project_info.get('characters', '未设定')}
- **核心冲突**：{project_info.get('conflict', '未设定')}

### 规划要求

#### 1. 故事结构
{structure_guide}

#### 2. 情绪曲线设计
- 规划整体情绪曲线，呈现**起伏有致**的节奏
- 避免持续高能或持续平淡
- 设计多个小高潮，逐步升级至最终高潮
- 高潮后安排缓冲章节，再逐步攀向下一高潮
- 为每章标注预期情绪强度（1-10）

#### 3. 主角认知路径
- 规划主角的知识获取路径
- 明确每章主角会了解哪些新信息
- 设计信息揭示的节奏和方式（对话、调查、亲历等）
- 可以安排主角的错误认知，后续再纠正

#### 4. 角色出场规划
- 规划主要角色的出场时机和方式
- 先出场核心角色，逐步扩展到次要角色
- 为重要角色设计出场前的铺垫（提及、传闻等）
- 避免同时引入过多角色

#### 5. 输出格式
为每一章输出以下信息（JSON 格式）：
- chapter_number: 章节编号
- title: 章节标题
- plot_points: 剧情要点（3-5个关键事件）
- emotion_intensity: 情绪强度（1-10）
- narrative_phase: 叙事阶段（exposition/rising_action/climax/falling_action/resolution）
- new_characters: 本章新登场的角色
- knowledge_revealed: 主角在本章获得的新知识
- foreshadowing: 本章埋下的伏笔

### 特别注意
- 剧情要点应当是内部规划用的，不会直接出现在最终文本中
- 使用自然语言描述，而非标签式列表
- 确保整体逻辑连贯，前后呼应

---

现在开始规划："""
    
    return prompt


def _get_structure_guidance(structure: str, total_chapters: int) -> str:
    """根据故事结构类型返回指导"""
    if structure == "three_act":
        act1_end = int(total_chapters * 0.25)
        act2_end = int(total_chapters * 0.75)
        
        return f"""采用**三幕结构**：
- **第一幕（第1-{act1_end}章）**：铺垫与设定，介绍主角、世界观和核心冲突，情绪强度逐步上升（3-6）
- **第二幕（第{act1_end+1}-{act2_end}章）**：发展与冲突，主角面对挑战，多次起伏，情绪强度波动（4-8），中点设置一次重要转折
- **第三幕（第{act2_end+1}-{total_chapters}章）**：高潮与解决，最终对决，情绪强度达到顶峰（8-10），然后逐步回落至结局（3-5）"""
    
    elif structure == "hero_journey":
        return f"""采用**英雄之旅结构**（共{total_chapters}章）：
1. 平凡世界（10%）：主角的日常生活
2. 冒险召唤（10%）：事件打破平静
3. 拒绝召唤（5%）：主角犹豫不决
4. 遇见导师（5%）：获得指引
5. 跨越第一道门槛（10%）：正式踏上旅程
6. 试炼、盟友与敌人（20%）：多次挑战和成长
7. 深入洞穴（10%）：接近核心目标
8. 磨难考验（15%）：最大危机和考验
9. 奖赏（5%）：获得成果
10. 回归之路（5%）：返回起点
11. 复活（3%）：最终蜕变
12. 带着灵药归来（2%）：圆满结局

为每个阶段分配合适的章节数，并设计相应的情绪强度。"""
    
    else:  # 自由结构
        return f"""采用**自由结构**（共{total_chapters}章）：
- 设计清晰的故事弧线，有明确的起点、发展、高潮和结局
- 规划3-5个主要情节段落，每个段落包含起承转合
- 确保情绪曲线呈现波浪式上升，而非单调递增或平直
- 在关键节点设置转折点，推动情节发展"""


# ==================== 后处理过滤 Prompt ====================

POST_PROCESS_FILTER_PROMPT = """## 文本后处理任务

请检查并优化以下小说文本，移除任何不符合规范的内容：

### 检查项目
1. **移除显式标签**：删除所有【】标记和结构化标签（如【三次递进挑战】、【双方势力】等）
2. **转换列表式表述**：将"一、二、三"或"首先、其次、然后"等列表式表述改写为自然叙事
3. **检查视角一致性**：确保没有超出主角认知范围的全知描述
4. **优化节奏**：检查是否有过长的平淡段落或过于紧绷的情节，适当调整
5. **语言润色**：提升文学性，使用更生动形象的语言

### 输出要求
直接输出优化后的文本，无需说明修改内容。

---

原文：
{original_text}

---

优化后的文本："""


# ==================== 自检 Prompt ====================

SELF_CHECK_PROMPT = """## 质量自检任务

请对以下小说章节进行质量检查，找出可能存在的问题：

### 检查维度
1. **节奏问题**：是否存在节奏单一（持续高能或持续平淡）的情况？
2. **视角问题**：主角是否表现出全知视角，知道不该知道的信息？
3. **角色问题**：新角色出场是否突兀，缺乏铺垫或介绍？
4. **逻辑问题**：情节发展是否合理，有无前后矛盾？
5. **语言问题**：是否存在大纲式表述或标签残留？

### 输出格式
以 JSON 格式输出检查结果：
{{
    "has_issues": true/false,
    "issues": [
        {{
            "type": "pacing/perspective/character/logic/language",
            "severity": "critical/high/medium/low",
            "description": "问题描述",
            "location": "问题位置（章节段落）",
            "suggestion": "修改建议"
        }}
    ],
    "overall_quality": "excellent/good/fair/poor",
    "suggestions": ["总体改进建议1", "总体改进建议2"]
}}

---

待检查文本：
{text_to_check}

---

检查结果："""


# ==================== 导出所有模板 ====================

PROMPT_TEMPLATES = {
    'system_message': SYSTEM_MESSAGE_NOVELIST,
    'generate_chapter': generate_chapter_prompt,
    'generate_outline': generate_outline_prompt,
    'post_process_filter': POST_PROCESS_FILTER_PROMPT,
    'self_check': SELF_CHECK_PROMPT,
}
