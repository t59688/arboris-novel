# AI小说创作提示词体系集成方案

## 一、集成原则

1. **零侵入性**：不修改现有数据库表结构，利用现有的JSON字段扩展
2. **向后兼容**：所有新功能都是可选的，不影响现有用户的使用习惯
3. **渐进增强**：用户可以选择使用新功能，也可以继续使用原有流程
4. **提示词驱动**：主要通过增强提示词来实现功能，减少代码改动

## 二、功能模块设计

### 模块1：角色DNA档案（Character DNA Profile）

**目标**：让用户能够为角色建立更深层的背景档案，使AI生成更立体的人物

**实现方式**：
- 利用 `BlueprintCharacter.extra` JSON字段存储扩展信息
- 前端增加"深层档案"展开面板
- 提示词中自动提取并格式化DNA信息

**扩展字段结构**：
```json
{
  "dna_profile": {
    "childhood_trauma": "童年经历/创伤事件",
    "core_fear": "核心恐惧",
    "inner_desire": "内心渴望",
    "speech_habits": "说话习惯/口头禅",
    "body_language": "身体语言/紧张时的小动作",
    "thinking_pattern": "思维模式（理性/感性/乐观/悲观）",
    "decision_style": "决策方式",
    "hidden_secret": "隐藏的秘密"
  }
}
```

### 模块2：情绪节拍控制（Emotion Beat Control）

**目标**：让用户能够为每个章节设定情绪目标，控制读者的阅读体验

**实现方式**：
- 利用 `ChapterOutline.summary` 字段的扩展，或在 `writing_notes` 中传递
- 创建新的提示词模板 `writing_enhanced.md`
- 前端在章节生成时增加情绪设置面板

**情绪节拍参数**：
```json
{
  "emotion_beat": {
    "primary_emotion": "悬疑紧张|温暖感动|愤怒不甘|好奇期待|忧伤惆怅",
    "intensity": 1-10,
    "curve": {
      "start": 3,
      "peak": 8,
      "end": 5
    },
    "turning_point": "情绪转折点描述"
  }
}
```

### 模块3：分层优化系统（Layered Optimization）

**目标**：支持对生成内容进行多维度的分层优化

**实现方式**：
- 创建新的提示词模板用于各维度优化
- 在章节版本选择后，提供"深度优化"选项
- 每次优化专注一个维度

**优化维度**：
1. `optimize_dialogue.md` - 对话优化
2. `optimize_environment.md` - 环境描写优化
3. `optimize_psychology.md` - 心理活动优化
4. `optimize_rhythm.md` - 节奏韵律优化

## 三、文件修改清单

### 新增文件

1. **后端提示词**：
   - `backend/prompts/writing_enhanced.md` - 增强版写作提示词
   - `backend/prompts/character_dna_guide.md` - 角色DNA构建指南
   - `backend/prompts/optimize_dialogue.md` - 对话优化提示词
   - `backend/prompts/optimize_environment.md` - 环境描写优化提示词
   - `backend/prompts/optimize_psychology.md` - 心理活动优化提示词

2. **前端组件**：
   - `frontend/src/components/CharacterDNAEditor.vue` - 角色DNA编辑器
   - `frontend/src/components/EmotionBeatSelector.vue` - 情绪节拍选择器
   - `frontend/src/components/LayeredOptimizer.vue` - 分层优化面板

### 修改文件

1. **后端**：
   - `backend/app/api/routers/writer.py` - 添加优化API端点
   - `backend/app/schemas/novel.py` - 添加新的请求/响应模型

2. **前端**：
   - `frontend/src/components/CharactersEditor.vue` - 集成DNA编辑器
   - `frontend/src/components/ChapterWorkspace.vue` - 集成情绪设置和优化面板

## 四、实现优先级

### 第一优先级（核心功能）
1. ✅ 增强版写作提示词 `writing_enhanced.md`
2. ✅ 角色DNA档案扩展

### 第二优先级（体验优化）
3. ✅ 情绪节拍控制
4. ✅ 前端角色DNA编辑器

### 第三优先级（高级功能）
5. ⬜ 分层优化系统
6. ⬜ 优化效果对比

## 五、向后兼容策略

1. **提示词选择**：系统保留原有的 `writing.md`，新增 `writing_enhanced.md`
2. **字段可选**：所有新增的JSON字段都是可选的，不填写时使用默认行为
3. **渐进迁移**：用户可以逐步为角色添加DNA信息，无需一次性完成
4. **功能开关**：可通过系统配置控制是否启用增强功能

## 六、预期效果

1. **角色更立体**：通过DNA档案，AI能生成更有深度的角色行为和对话
2. **情绪更可控**：通过情绪节拍，作者能精确控制读者的阅读体验
3. **质量更高**：通过分层优化，内容质量能够逐步提升
4. **审核更易过**：更人性化的内容更容易通过平台审核
