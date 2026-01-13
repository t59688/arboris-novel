<!-- AIMETA P=增强章节工作区_增强版编辑界面|R=增强编辑功能|NR=不含基础功能|E=component:ChapterWorkspaceEnhanced|X=internal|A=增强工作区|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <!-- 章节头部 -->
    <div v-if="chapterOutline" class="mb-6">
      <h2 class="text-xl font-bold text-gray-800">
        第{{ chapterOutline.chapter_number }}章: {{ chapterOutline.title }}
      </h2>
      <p class="text-gray-600 mt-2">{{ chapterOutline.summary }}</p>
    </div>

    <!-- 无选择状态 -->
    <div v-if="!chapterOutline" class="text-center py-12 text-gray-500">
      请从左侧选择一个章节开始工作
    </div>

    <!-- 已完成的章节 -->
    <div v-else-if="chapter && chapter.content" class="space-y-6">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-800">已发布内容</h3>
        <div class="flex gap-2">
          <!-- 分层优化按钮 -->
          <button
            @click="showOptimizer = true"
            class="px-4 py-2 bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors flex items-center gap-2"
          >
            <span>✨</span>
            <span>分层优化</span>
          </button>
          <button
            @click="confirmRegenerate"
            class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition-colors"
          >
            重新生成版本
          </button>
        </div>
      </div>

      <!-- 内容显示区域 -->
      <div class="prose max-w-none p-4 bg-gray-50 rounded-lg border relative">
        <!-- 优化对比视图 -->
        <div v-if="showComparison" class="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-yellow-800">优化预览</span>
            <div class="flex gap-2">
              <button
                @click="applyOptimization"
                class="px-3 py-1 bg-green-500 text-white text-sm rounded hover:bg-green-600"
              >
                应用优化
              </button>
              <button
                @click="cancelOptimization"
                class="px-3 py-1 bg-gray-300 text-gray-700 text-sm rounded hover:bg-gray-400"
              >
                取消
              </button>
            </div>
          </div>
          <p class="text-xs text-yellow-700">{{ optimizationNotes }}</p>
        </div>

        <!-- 内容 -->
        <div class="whitespace-pre-wrap">{{ displayContent }}</div>
      </div>

      <!-- 字数统计 -->
      <div class="text-right text-sm text-gray-500">
        字数：{{ wordCount }}
      </div>
    </div>

    <!-- 生成结果选择 -->
    <div v-else-if="generationResult" class="space-y-6">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-800">选择版本</h3>
        <button
          @click="confirmRegenerate"
          class="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
        >
          重新生成
        </button>
      </div>

      <!-- AI评估 -->
      <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
        <h4 class="font-medium text-blue-800 mb-2">AI评估建议</h4>
        <p class="text-blue-700 text-sm">{{ generationResult.evaluation }}</p>
      </div>

      <!-- 版本选择 -->
      <div class="space-y-4">
        <div
          v-for="(version, index) in generationResult.versions"
          :key="index"
          class="border rounded-lg p-4 hover:bg-gray-50 transition-colors cursor-pointer"
          @click="$emit('selectVersion', index)"
        >
          <div class="flex justify-between items-start mb-3">
            <h4 class="font-medium text-gray-800">版本 {{ index + 1 }}</h4>
            <button
              @click.stop="$emit('selectVersion', index)"
              class="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors text-sm"
            >
              选择此版本
            </button>
          </div>
          <div class="prose max-w-none text-sm text-gray-700 whitespace-pre-wrap">
            {{ version }}
          </div>
        </div>
      </div>
    </div>

    <!-- 等待生成状态 -->
    <div v-else class="text-center py-12">
      <div class="text-gray-500 mb-4">点击左侧的"生成"按钮开始创作这一章</div>
      <button
        @click="confirmRegenerate"
        class="px-6 py-3 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors"
      >
        开始生成
      </button>
    </div>

    <!-- 分层优化弹窗 -->
    <Teleport to="body">
      <div
        v-if="showOptimizer"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="showOptimizer = false"
      >
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto m-4">
          <div class="p-6">
            <LayeredOptimizer
              ref="optimizerRef"
              :chapter-content="chapter?.content || ''"
              :optimization-history="optimizationHistory"
              @optimize="handleOptimize"
              @cancel="showOptimizer = false"
              @revert="handleRevert"
            />
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 优化进度提示 -->
    <Teleport to="body">
      <div
        v-if="isOptimizing"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg p-8 text-center">
          <div class="animate-spin w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p class="text-gray-700 font-medium">正在优化中...</p>
          <p class="text-gray-500 text-sm mt-2">AI正在对{{ currentOptimizeDimension }}进行深度优化</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { globalAlert } from '@/composables/useAlert'
import type { Chapter, ChapterOutline, ChapterGenerationResponse } from '@/api/novel'
import LayeredOptimizer from './LayeredOptimizer.vue'

interface OptimizationRecord {
  dimension: string
  timestamp: string
  originalContent: string
}

interface Props {
  chapter: Chapter | null
  chapterOutline: ChapterOutline | null
  generationResult: ChapterGenerationResponse | null
  projectId: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  selectVersion: [versionIndex: number]
  regenerate: []
  optimize: [params: { dimension: string; additionalNotes: string; projectId: string; chapterNumber: number }]
  applyOptimization: [content: string]
}>()

// 状态
const showOptimizer = ref(false)
const isOptimizing = ref(false)
const currentOptimizeDimension = ref('')
const optimizedContent = ref('')
const optimizationNotes = ref('')
const showComparison = ref(false)
const optimizationHistory = ref<OptimizationRecord[]>([])
const optimizerRef = ref<InstanceType<typeof LayeredOptimizer> | null>(null)

// 计算属性
const displayContent = computed(() => {
  if (showComparison.value && optimizedContent.value) {
    return optimizedContent.value
  }
  return props.chapter?.content || ''
})

const wordCount = computed(() => {
  const content = displayContent.value
  if (!content) return 0
  // 中文字符计数
  const chineseChars = (content.match(/[\u4e00-\u9fa5]/g) || []).length
  // 英文单词计数
  const englishWords = (content.match(/[a-zA-Z]+/g) || []).length
  return chineseChars + englishWords
})

// 维度名称映射
const dimensionNames: Record<string, string> = {
  dialogue: '对话',
  environment: '环境描写',
  psychology: '心理活动',
  rhythm: '节奏韵律'
}

// 方法
const confirmRegenerate = async () => {
  const confirmed = await globalAlert.showConfirm('重新生成会覆盖当前章节的现有结果，确定继续吗？', '重新生成确认')
  if (confirmed) {
    emit('regenerate')
  }
}

const handleOptimize = async (params: { dimension: string; additionalNotes: string; originalContent: string }) => {
  if (!props.chapter || !props.chapterOutline) return
  
  isOptimizing.value = true
  currentOptimizeDimension.value = dimensionNames[params.dimension] || params.dimension
  showOptimizer.value = false
  
  // 保存原始内容到历史
  optimizationHistory.value.unshift({
    dimension: params.dimension,
    timestamp: new Date().toLocaleString(),
    originalContent: params.originalContent
  })
  
  // 触发优化事件，由父组件处理API调用
  emit('optimize', {
    dimension: params.dimension,
    additionalNotes: params.additionalNotes,
    projectId: props.projectId,
    chapterNumber: props.chapterOutline.chapter_number
  })
}

const handleRevert = (record: OptimizationRecord) => {
  if (record.originalContent) {
    emit('applyOptimization', record.originalContent)
    globalAlert.showSuccess('已回退到之前的版本')
  }
}

const applyOptimization = () => {
  if (optimizedContent.value) {
    emit('applyOptimization', optimizedContent.value)
    showComparison.value = false
    optimizedContent.value = ''
    optimizationNotes.value = ''
    globalAlert.showSuccess('优化内容已应用')
  }
}

const cancelOptimization = () => {
  showComparison.value = false
  optimizedContent.value = ''
  optimizationNotes.value = ''
}

// 暴露方法供父组件调用
defineExpose({
  setOptimizationResult: (content: string, notes: string) => {
    optimizedContent.value = content
    optimizationNotes.value = notes
    showComparison.value = true
    isOptimizing.value = false
    if (optimizerRef.value) {
      optimizerRef.value.setOptimizing(false)
    }
  },
  setOptimizing: (value: boolean) => {
    isOptimizing.value = value
  }
})

// 监听章节变化，重置状态
watch(() => props.chapter?.chapter_number, () => {
  showComparison.value = false
  optimizedContent.value = ''
  optimizationNotes.value = ''
  optimizationHistory.value = []
})
</script>
