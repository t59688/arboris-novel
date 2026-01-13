<!-- AIMETA P=写作台工作区_主编辑区域|R=章节编辑_生成|NR=不含侧边栏|E=component:WDWorkspace|X=ui|A=工作区|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="flex-1 min-w-0 h-full">
    <div class="bg-white rounded-2xl shadow-lg border border-gray-100 h-full flex flex-col">
      <!-- 章节工作区头部 -->
      <div v-if="selectedChapterNumber" class="border-b border-gray-100 p-6 flex-shrink-0">
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <h2 class="text-xl font-bold text-gray-900">第{{ selectedChapterNumber }}章</h2>
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  isChapterCompleted(selectedChapterNumber)
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-600'
                ]"
              >
                {{ isChapterCompleted(selectedChapterNumber) ? '已完成' : '未完成' }}
              </span>
            </div>
            <h3 class="text-lg text-gray-700 mb-1">{{ selectedChapterOutline?.title || '未知标题' }}</h3>
            <p class="text-sm text-gray-600">{{ selectedChapterOutline?.summary || '暂无章节描述' }}</p>
          </div>

          <div class="flex items-center gap-2">
            <button
              v-if="isChapterCompleted(selectedChapterNumber)"
              @click="openEditModal"
              class="px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-lg transition-colors flex items-center gap-2 whitespace-nowrap"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
              </svg>
              手动编辑
            </button>
            <button
              @click="confirmRegenerateChapter"
              :disabled="generatingChapter === selectedChapterNumber"
              class="px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2 whitespace-nowrap"
            >
              <svg v-if="generatingChapter === selectedChapterNumber" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
              </svg>
              {{ generatingChapter === selectedChapterNumber ? '生成中...' : '重新生成' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 章节内容展示区 -->
      <div class="flex-1 p-6 overflow-y-auto">
        <component
          :is="currentComponent"
          v-bind="currentComponentProps"
          @hideVersionSelector="$emit('hideVersionSelector')"
          @update:selectedVersionIndex="$emit('update:selectedVersionIndex', $event)"
          @showVersionDetail="$emit('showVersionDetail', $event)"
          @confirmVersionSelection="$emit('confirmVersionSelection')"
          @generateChapter="$emit('generateChapter', $event)"
          @showVersionSelector="$emit('showVersionSelector')"
          @regenerateChapter="$emit('regenerateChapter')"
          @evaluateChapter="$emit('evaluateChapter')"
          @showEvaluationDetail="$emit('showEvaluationDetail')"
        />
      </div>
    </div>

    <!-- 编辑章节内容模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full h-full flex flex-col">
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 class="text-lg font-semibold text-gray-900">
            编辑第{{ selectedChapterNumber }}章内容
          </h3>
          <button
            @click="closeEditModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>

        <!-- 模态框内容 -->
        <div class="flex-1 p-6 overflow-hidden">
          <div class="flex flex-col h-full">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              章节内容
            </label>
            <textarea
              v-model="editingContent"
              class="flex-1 w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
              placeholder="请输入章节内容..."
              :disabled="isSaving"
            ></textarea>
            <div class="text-sm text-gray-500 mt-2">
              字数统计: {{ editingContent.length }}
            </div>
          </div>
        </div>

        <!-- 模态框底部 -->
        <div class="flex items-center justify-end gap-3 p-6 border-t border-gray-200">
          <button
            @click="closeEditModal"
            :disabled="isSaving"
            class="px-4 py-2 text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors disabled:opacity-50"
          >
            取消
          </button>
          <button
            @click="saveEditedContent"
            :disabled="isSaving || !editingContent.trim()"
            class="px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <svg v-if="isSaving" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
            </svg>
            {{ isSaving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { globalAlert } from '@/composables/useAlert'
import type { Chapter, ChapterOutline, ChapterGenerationResponse, ChapterVersion, NovelProject } from '@/api/novel'
import WorkspaceInitial from './workspace/WorkspaceInitial.vue'
import ChapterGenerating from './workspace/ChapterGenerating.vue'
import VersionSelector from './workspace/VersionSelector.vue'
import ChapterContent from './workspace/ChapterContent.vue'
import ChapterFailed from './workspace/ChapterFailed.vue'
import ChapterEmpty from './workspace/ChapterEmpty.vue'

interface Props {
  project: NovelProject | null
  selectedChapterNumber: number | null
  generatingChapter: number | null
  evaluatingChapter: number | null
  showVersionSelector: boolean
  chapterGenerationResult: ChapterGenerationResponse | null
  selectedVersionIndex: number
  availableVersions: ChapterVersion[]
  isSelectingVersion?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits([
  'regenerateChapter',
  'evaluateChapter',
  'hideVersionSelector',
  'update:selectedVersionIndex',
  'showVersionDetail',
  'confirmVersionSelection',
  'generateChapter',
  'showVersionSelector',
  'showEvaluationDetail',
  'fetchChapterStatus',
  'editChapter'
])

const confirmRegenerateChapter = async () => {
  const confirmed = await globalAlert.showConfirm('重新生成会覆盖当前章节的现有内容，确定继续吗？', '重新生成确认')
  if (confirmed) {
    emit('regenerateChapter')
  }
}

// 编辑模态框状态
const showEditModal = ref(false)
const editingContent = ref('')
const isSaving = ref(false)

// 清理版本内容的辅助函数
const cleanVersionContent = (content: string): string => {
  if (!content) return ''
  try {
    const parsed = JSON.parse(content)
    if (parsed && typeof parsed === 'object' && parsed.content) {
      content = parsed.content
    }
  } catch (error) {
    // not a json
  }
  let cleaned = content.replace(/^"|"$/g, '')
  cleaned = cleaned.replace(/\\n/g, '\n')
  cleaned = cleaned.replace(/\\"/g, '"')
  cleaned = cleaned.replace(/\\t/g, '\t')
  cleaned = cleaned.replace(/\\\\/g, '\\')
  return cleaned
}

const openEditModal = () => {
  if (selectedChapter.value?.content) {
    editingContent.value = cleanVersionContent(selectedChapter.value.content)
    showEditModal.value = true
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  editingContent.value = ''
  isSaving.value = false
}

const saveEditedContent = async () => {
  if (!props.selectedChapterNumber || !editingContent.value.trim()) return
  
  isSaving.value = true
  try {
    emit('editChapter', {
      chapterNumber: props.selectedChapterNumber,
      content: editingContent.value
    })
    closeEditModal()
  } catch (error) {
    console.error('保存章节内容失败:', error)
  } finally {
    isSaving.value = false
  }
}

const selectedChapter = computed(() => {
  if (!props.project || props.selectedChapterNumber === null) return null
  return props.project.chapters.find(ch => ch.chapter_number === props.selectedChapterNumber) || null
})

const selectedChapterOutline = computed(() => {
  if (!props.project?.blueprint?.chapter_outline || props.selectedChapterNumber === null) return null
  return props.project.blueprint.chapter_outline.find(ch => ch.chapter_number === props.selectedChapterNumber) || null
})

const isChapterCompleted = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'successful'
}

const isChapterGenerating = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'generating'
}

const isChapterFailed = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'failed'
}

const isChapterEvaluationFailed = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'evaluation_failed'
}

const canGenerateChapter = (chapterNumber: number | null) => {
  if (chapterNumber === null || !props.project?.blueprint?.chapter_outline) return false

  const outlines = props.project.blueprint.chapter_outline.sort((a, b) => a.chapter_number - b.chapter_number)
  
  for (const outline of outlines) {
    if (outline.chapter_number >= chapterNumber) break
    
    const chapter = props.project?.chapters.find(ch => ch.chapter_number === outline.chapter_number)
    if (!chapter || chapter.generation_status !== 'successful') {
      return false
    }
  }

  const currentChapter = props.project?.chapters.find(ch => ch.chapter_number === chapterNumber)
  if (currentChapter && currentChapter.generation_status === 'successful') {
    return true
  }

  return true
}

const currentComponent = computed(() => {
  if (!props.selectedChapterNumber) {
    return WorkspaceInitial
  }

  const status = selectedChapter.value?.generation_status
  if (status === 'generating' || status === 'evaluating' || status === 'selecting') {
    return ChapterGenerating // Use a generic "in-progress" component
  }

  if (status === 'waiting_for_confirm' || status === 'evaluation_failed') {
    return VersionSelector
  }

  if (selectedChapter.value?.content) {
    return ChapterContent
  }
  if (isChapterFailed(props.selectedChapterNumber)) {
    return ChapterFailed
  }
  return ChapterEmpty
})

// Polling for chapter status updates
const pollingTimer = ref<number | null>(null)

const startPolling = () => {
  stopPolling()
  pollingTimer.value = window.setInterval(() => {
    emit('fetchChapterStatus')
  }, 10000)
}

const stopPolling = () => {
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value)
    pollingTimer.value = null
  }
}

watch(
  () => [selectedChapter.value?.generation_status, props.evaluatingChapter, props.isSelectingVersion, props.selectedChapterNumber],
  ([status, evaluating, selecting, chapterNumber]) => {
    if (chapterNumber === null) {
      stopPolling()
      return
    }

    const isEvaluating = evaluating === chapterNumber
    // Poll when generating, evaluating, or selecting a version
    const needsPolling = status === 'generating' || status === 'evaluating' || status === 'selecting'

    if (needsPolling) {
      startPolling()
    } else {
      stopPolling()
    }
  },
  { immediate: true }
)

onUnmounted(() => {
  stopPolling()
})

const currentComponentProps = computed(() => {
  if (!props.selectedChapterNumber) {
    return {}
  }
  const status = selectedChapter.value?.generation_status
  if (status === 'generating' || status === 'evaluating' || status === 'selecting') {
    return {
      chapterNumber: props.selectedChapterNumber,
      status: status
    }
  }

  if (status === 'waiting_for_confirm' || status === 'evaluation_failed') {
    return {
      selectedChapter: selectedChapter.value,
      chapterGenerationResult: props.chapterGenerationResult,
      availableVersions: props.availableVersions,
      selectedVersionIndex: props.selectedVersionIndex,
      isSelectingVersion: props.isSelectingVersion,
      evaluatingChapter: props.evaluatingChapter,
      isEvaluationFailed: isChapterEvaluationFailed(props.selectedChapterNumber)
    }
  }
  if (selectedChapter.value?.content) {
    return { 
      selectedChapter: selectedChapter.value,
      projectId: props.project?.id
    }
  }
  if (isChapterFailed(props.selectedChapterNumber)) {
    return {
      chapterNumber: props.selectedChapterNumber,
      generatingChapter: props.generatingChapter
    }
  }
  return {
    chapterNumber: props.selectedChapterNumber,
    generatingChapter: props.generatingChapter,
    canGenerate: canGenerateChapter(props.selectedChapterNumber)
  }
})
</script>
