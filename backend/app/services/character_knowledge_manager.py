# AIMETA P=角色知识管理_主角认知建模|R=知识库_角色出场_认知约束|NR=不含内容生成|E=CharacterKnowledgeManager|X=internal|A=管理器类|D=none|S=none|RD=./README.ai
"""
主角认知建模和角色出场管理模块
实现主角视角约束和角色自然引入
"""
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class KnowledgeType(Enum):
    """知识类型"""
    WORLD_SETTING = "world_setting"  # 世界观设定
    CHARACTER_INFO = "character_info"  # 角色信息
    PLOT_SECRET = "plot_secret"  # 剧情秘密
    LOCATION = "location"  # 地点信息
    FACTION = "faction"  # 势力信息
    SKILL = "skill"  # 技能知识
    HISTORY = "history"  # 历史背景


class AcquisitionMethod(Enum):
    """知识获取方式"""
    INNATE = "innate"  # 天生就知道（常识、成长背景）
    TOLD = "told"  # 被告知（对话、讲述）
    OBSERVED = "observed"  # 亲眼所见
    INVESTIGATED = "investigated"  # 调查得知
    EXPERIENCED = "experienced"  # 亲身经历
    DEDUCED = "deduced"  # 推理得出
    READ = "read"  # 阅读获得（书籍、文档）


@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    content: str  # 知识内容描述
    type: KnowledgeType
    is_known: bool = False  # 主角是否已知
    acquisition_method: Optional[AcquisitionMethod] = None
    acquired_chapter: Optional[int] = None  # 在哪一章获得
    trigger_condition: Optional[str] = None  # 获取条件（如"进入XX地点"、"与XX对话"）
    related_characters: List[str] = field(default_factory=list)  # 相关角色
    importance: str = "medium"  # low, medium, high, critical


@dataclass
class CharacterInfo:
    """角色信息"""
    id: str
    name: str
    role: str  # protagonist, antagonist, ally, mentor, etc.
    
    # 出场信息
    is_introduced: bool = False  # 是否已出场
    first_mentioned_chapter: Optional[int] = None  # 首次被提及
    first_appeared_chapter: Optional[int] = None  # 首次正式出场
    introduction_method: Optional[str] = None  # 引入方式
    
    # 关系信息
    relationship_to_protagonist: str = "unknown"  # 与主角的关系
    known_by_protagonist: bool = False  # 主角是否认识
    
    # 背景信息（分层揭示）
    basic_info: str = ""  # 基本信息（首次出场时揭示）
    background_info: str = ""  # 背景故事（逐步揭示）
    secrets: List[str] = field(default_factory=list)  # 秘密（后期揭示）
    
    # 出场触发条件
    appearance_trigger: Optional[str] = None
    appearance_priority: int = 0  # 出场优先级（数字越小越早出场）


class CharacterKnowledgeManager:
    """主角认知和角色出场管理器"""
    
    def __init__(self, protagonist_name: str = "主角"):
        self.protagonist_name = protagonist_name
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.characters: Dict[str, CharacterInfo] = {}
        self.current_chapter = 0
        
        # 主角的错误认知（用于制造悬念和转折）
        self.false_beliefs: List[Dict] = []
    
    def add_knowledge(
        self,
        knowledge_id: str,
        content: str,
        knowledge_type: KnowledgeType,
        is_initially_known: bool = False,
        trigger_condition: Optional[str] = None,
        importance: str = "medium",
    ) -> None:
        """
        添加知识条目到知识库
        
        Args:
            knowledge_id: 知识ID
            content: 知识内容
            knowledge_type: 知识类型
            is_initially_known: 主角是否一开始就知道
            trigger_condition: 获取条件
            importance: 重要性
        """
        item = KnowledgeItem(
            id=knowledge_id,
            content=content,
            type=knowledge_type,
            is_known=is_initially_known,
            trigger_condition=trigger_condition,
            importance=importance,
        )
        
        if is_initially_known:
            item.acquisition_method = AcquisitionMethod.INNATE
            item.acquired_chapter = 0
        
        self.knowledge_base[knowledge_id] = item
    
    def reveal_knowledge(
        self,
        knowledge_id: str,
        chapter_number: int,
        method: AcquisitionMethod,
    ) -> Dict:
        """
        揭示知识给主角
        
        Returns:
            包含知识内容和获取方式的字典
        """
        if knowledge_id not in self.knowledge_base:
            raise ValueError(f"知识ID {knowledge_id} 不存在")
        
        item = self.knowledge_base[knowledge_id]
        
        if item.is_known:
            return {
                'already_known': True,
                'content': item.content,
                'acquired_chapter': item.acquired_chapter,
            }
        
        item.is_known = True
        item.acquisition_method = method
        item.acquired_chapter = chapter_number
        
        return {
            'already_known': False,
            'content': item.content,
            'method': method.value,
            'chapter': chapter_number,
            'importance': item.importance,
        }
    
    def get_known_knowledge(
        self,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> List[KnowledgeItem]:
        """获取主角已知的知识"""
        known = [item for item in self.knowledge_base.values() if item.is_known]
        
        if knowledge_type:
            known = [item for item in known if item.type == knowledge_type]
        
        return known
    
    def get_unknown_knowledge(
        self,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> List[KnowledgeItem]:
        """获取主角未知的知识"""
        unknown = [item for item in self.knowledge_base.values() if not item.is_known]
        
        if knowledge_type:
            unknown = [item for item in unknown if item.type == knowledge_type]
        
        return unknown
    
    def check_knowledge_triggers(self, chapter_number: int, context: Dict) -> List[str]:
        """
        检查是否有知识的触发条件满足
        
        Args:
            chapter_number: 当前章节
            context: 上下文信息（如当前地点、对话角色等）
        
        Returns:
            应当揭示的知识ID列表
        """
        triggered = []
        
        for knowledge_id, item in self.knowledge_base.items():
            if item.is_known or not item.trigger_condition:
                continue
            
            # 简单的触发条件匹配（实际应用中可以更复杂）
            if self._check_trigger(item.trigger_condition, context):
                triggered.append(knowledge_id)
        
        return triggered
    
    def _check_trigger(self, trigger: str, context: Dict) -> bool:
        """检查触发条件是否满足"""
        # 简化的触发检查逻辑
        # 实际应用中可以实现更复杂的条件解析
        
        if "location:" in trigger:
            required_location = trigger.split("location:")[1].strip()
            return context.get("current_location") == required_location
        
        if "character:" in trigger:
            required_character = trigger.split("character:")[1].strip()
            return required_character in context.get("present_characters", [])
        
        if "event:" in trigger:
            required_event = trigger.split("event:")[1].strip()
            return required_event in context.get("events", [])
        
        return False
    
    def add_false_belief(
        self,
        belief_content: str,
        truth_content: str,
        correction_chapter: int,
    ) -> None:
        """
        添加主角的错误认知
        
        Args:
            belief_content: 主角错误地相信的内容
            truth_content: 真相
            correction_chapter: 在哪一章纠正认知
        """
        self.false_beliefs.append({
            'belief': belief_content,
            'truth': truth_content,
            'correction_chapter': correction_chapter,
            'is_corrected': False,
        })
    
    def get_current_beliefs(self, chapter_number: int) -> Dict:
        """
        获取主角当前的认知状态（包括错误认知）
        
        Returns:
            包含正确认知和错误认知的字典
        """
        active_false_beliefs = [
            fb for fb in self.false_beliefs
            if not fb['is_corrected'] and chapter_number < fb['correction_chapter']
        ]
        
        return {
            'known_truths': [item.content for item in self.get_known_knowledge()],
            'false_beliefs': [fb['belief'] for fb in active_false_beliefs],
        }
    
    # ==================== 角色管理 ====================
    
    def add_character(
        self,
        character_id: str,
        name: str,
        role: str,
        relationship: str = "unknown",
        basic_info: str = "",
        background_info: str = "",
        secrets: List[str] = None,
        appearance_trigger: Optional[str] = None,
        appearance_priority: int = 0,
    ) -> None:
        """添加角色到角色库"""
        character = CharacterInfo(
            id=character_id,
            name=name,
            role=role,
            relationship_to_protagonist=relationship,
            basic_info=basic_info,
            background_info=background_info,
            secrets=secrets or [],
            appearance_trigger=appearance_trigger,
            appearance_priority=appearance_priority,
        )
        
        self.characters[character_id] = character
    
    def mention_character(
        self,
        character_id: str,
        chapter_number: int,
        mention_context: str = "",
    ) -> Dict:
        """
        提及角色（在正式出场前）
        
        Args:
            character_id: 角色ID
            chapter_number: 章节编号
            mention_context: 提及的上下文（如"酒客谈论"、"传闻"）
        
        Returns:
            提及信息
        """
        if character_id not in self.characters:
            raise ValueError(f"角色ID {character_id} 不存在")
        
        character = self.characters[character_id]
        
        if character.first_mentioned_chapter is None:
            character.first_mentioned_chapter = chapter_number
        
        return {
            'character_name': character.name,
            'is_introduced': character.is_introduced,
            'mention_type': 'foreshadowing' if not character.is_introduced else 'reference',
            'context': mention_context,
        }
    
    def introduce_character(
        self,
        character_id: str,
        chapter_number: int,
        introduction_method: str = "direct_encounter",
    ) -> Dict:
        """
        正式引入角色
        
        Args:
            character_id: 角色ID
            chapter_number: 章节编号
            introduction_method: 引入方式（direct_encounter, introduced_by_other, etc.）
        
        Returns:
            角色引入信息
        """
        if character_id not in self.characters:
            raise ValueError(f"角色ID {character_id} 不存在")
        
        character = self.characters[character_id]
        
        if character.is_introduced:
            return {
                'already_introduced': True,
                'first_appeared_chapter': character.first_appeared_chapter,
            }
        
        character.is_introduced = True
        character.first_appeared_chapter = chapter_number
        character.introduction_method = introduction_method
        character.known_by_protagonist = True
        
        # 判断是否有提前铺垫
        has_foreshadowing = character.first_mentioned_chapter is not None and \
                          character.first_mentioned_chapter < chapter_number
        
        return {
            'already_introduced': False,
            'character_name': character.name,
            'role': character.role,
            'basic_info': character.basic_info,
            'introduction_method': introduction_method,
            'has_foreshadowing': has_foreshadowing,
            'foreshadowing_chapter': character.first_mentioned_chapter,
            'relationship': character.relationship_to_protagonist,
        }
    
    def get_introduced_characters(self) -> List[CharacterInfo]:
        """获取已出场的角色列表"""
        return [char for char in self.characters.values() if char.is_introduced]
    
    def get_pending_characters(self, chapter_number: int) -> List[CharacterInfo]:
        """获取待出场的角色列表（按优先级排序）"""
        pending = [
            char for char in self.characters.values()
            if not char.is_introduced
        ]
        
        # 按优先级排序
        pending.sort(key=lambda x: x.appearance_priority)
        
        return pending
    
    def suggest_character_introduction(
        self,
        chapter_number: int,
        context: Dict,
        max_new_characters: int = 2,
    ) -> List[Dict]:
        """
        建议在本章引入哪些角色
        
        Args:
            chapter_number: 当前章节
            context: 上下文信息
            max_new_characters: 最多引入几个新角色
        
        Returns:
            建议引入的角色列表
        """
        pending = self.get_pending_characters(chapter_number)
        suggestions = []
        
        for character in pending[:max_new_characters * 2]:  # 多取一些候选
            # 检查触发条件
            if character.appearance_trigger:
                if not self._check_trigger(character.appearance_trigger, context):
                    continue
            
            # 检查是否已有足够的铺垫
            has_foreshadowing = character.first_mentioned_chapter is not None
            
            suggestions.append({
                'character_id': character.id,
                'character_name': character.name,
                'role': character.role,
                'priority': character.appearance_priority,
                'has_foreshadowing': has_foreshadowing,
                'suggested_method': self._suggest_introduction_method(character, context),
            })
            
            if len(suggestions) >= max_new_characters:
                break
        
        return suggestions
    
    def _suggest_introduction_method(
        self,
        character: CharacterInfo,
        context: Dict,
    ) -> str:
        """建议角色引入方式"""
        # 根据角色类型和上下文建议引入方式
        if character.role == "mentor":
            return "主角遇到困难时，导师出现给予指引"
        elif character.role == "antagonist":
            return "通过冲突事件引入，展现对立关系"
        elif character.role == "ally":
            if character.first_mentioned_chapter:
                return "主角终于见到之前听说过的盟友"
            else:
                return "通过共同经历的事件自然相识"
        else:
            return "根据剧情需要自然出场"
    
    def get_character_relationship_graph(self) -> Dict:
        """
        获取角色关系图谱
        
        Returns:
            角色关系的图结构
        """
        graph = {
            'nodes': [],
            'edges': [],
        }
        
        # 添加主角节点
        graph['nodes'].append({
            'id': 'protagonist',
            'name': self.protagonist_name,
            'type': 'protagonist',
        })
        
        # 添加其他角色节点
        for char_id, char in self.characters.items():
            graph['nodes'].append({
                'id': char_id,
                'name': char.name,
                'type': char.role,
                'is_introduced': char.is_introduced,
            })
            
            # 添加与主角的关系边
            if char.known_by_protagonist:
                graph['edges'].append({
                    'source': 'protagonist',
                    'target': char_id,
                    'relationship': char.relationship_to_protagonist,
                })
        
        return graph
    
    def export_knowledge_state(self, chapter_number: int) -> Dict:
        """
        导出主角在指定章节的完整认知状态
        
        用于生成 Prompt 时的上下文
        """
        return {
            'chapter_number': chapter_number,
            'protagonist_name': self.protagonist_name,
            'known_knowledge': {
                'world_setting': [
                    item.content for item in self.get_known_knowledge(KnowledgeType.WORLD_SETTING)
                ],
                'characters': [
                    item.content for item in self.get_known_knowledge(KnowledgeType.CHARACTER_INFO)
                ],
                'plot_secrets': [
                    item.content for item in self.get_known_knowledge(KnowledgeType.PLOT_SECRET)
                ],
                'locations': [
                    item.content for item in self.get_known_knowledge(KnowledgeType.LOCATION)
                ],
            },
            'unknown_knowledge': {
                'world_setting': [
                    item.content for item in self.get_unknown_knowledge(KnowledgeType.WORLD_SETTING)
                ],
                'plot_secrets': [
                    item.content for item in self.get_unknown_knowledge(KnowledgeType.PLOT_SECRET)
                ],
            },
            'false_beliefs': [
                fb['belief'] for fb in self.false_beliefs
                if not fb['is_corrected'] and chapter_number < fb['correction_chapter']
            ],
            'introduced_characters': [
                char.name for char in self.get_introduced_characters()
            ],
            'pending_characters': [
                char.name for char in self.get_pending_characters(chapter_number)[:5]
            ],
        }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 创建管理器
    manager = CharacterKnowledgeManager(protagonist_name="林枫")
    
    # 添加知识
    manager.add_knowledge(
        "world_001",
        "这个世界分为修仙界和凡人界两个层面",
        KnowledgeType.WORLD_SETTING,
        is_initially_known=True,
    )
    
    manager.add_knowledge(
        "secret_001",
        "修仙界的真正统治者是上古魔神的转世",
        KnowledgeType.PLOT_SECRET,
        is_initially_known=False,
        trigger_condition="location:天机阁",
        importance="critical",
    )
    
    # 添加角色
    manager.add_character(
        "char_001",
        "苏婉儿",
        "ally",
        relationship="青梅竹马",
        basic_info="林枫的青梅竹马，温柔善良",
        background_info="实际上是天机阁少主的女儿",
        secrets=["她的真实身份", "她一直在暗中保护林枫"],
        appearance_priority=1,
    )
    
    manager.add_character(
        "char_002",
        "剑圣",
        "mentor",
        relationship="师父",
        basic_info="隐居的剑道宗师",
        appearance_trigger="event:林枫遇到生死危机",
        appearance_priority=2,
    )
    
    # 提及角色（铺垫）
    mention_result = manager.mention_character("char_002", 3, "村民闲聊中提到山中有位剑圣")
    print(f"第3章提及剑圣：{mention_result}")
    
    # 引入角色
    intro_result = manager.introduce_character("char_001", 1, "childhood_friend")
    print(f"\n第1章引入苏婉儿：{intro_result}")
    
    # 揭示知识
    reveal_result = manager.reveal_knowledge("secret_001", 15, AcquisitionMethod.INVESTIGATED)
    print(f"\n第15章揭示秘密：{reveal_result}")
    
    # 导出认知状态
    state = manager.export_knowledge_state(10)
    print(f"\n第10章主角认知状态：")
    print(f"  已知角色：{state['introduced_characters']}")
    print(f"  已知世界观：{state['known_knowledge']['world_setting']}")
    print(f"  未知秘密：{state['unknown_knowledge']['plot_secrets']}")
