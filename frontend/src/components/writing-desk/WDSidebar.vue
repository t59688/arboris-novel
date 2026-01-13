<!-- AIMETA P=写作台侧边栏_章节目录|R=章节列表_导航|NR=不含内容编辑|E=component:WDSidebar|X=ui|A=侧边栏|D=vue|S=dom|RD=./README.ai -->
<template>
  <div>
    <!-- 侧边栏遮罩 (移动端) -->
    <div
      v-if="sidebarOpen"
      @click="$emit('closeSidebar')"
      class="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
    ></div>

    <!-- 左侧：蓝图和章节列表 -->
    <div
      :class="[
        'bg-white rounded-2xl shadow-lg border border-gray-100 transition-all duration-300 h-full',
        'lg:relative lg:translate-x-0 lg:w-80 lg:flex-shrink-0',
        sidebarOpen
          ? 'fixed left-4 top-20 bottom-4 w-80 z-50 translate-x-0'
          : 'lg:w-80 lg:flex-shrink-0 -translate-x-full absolute lg:relative'
      ]"
    >
      <div class="h-full flex flex-col">
        <!-- 蓝图预览卡片 -->
        <div class="p-6 border-b border-gray-100 flex-shrink-0">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-gray-900">故事蓝图</h2>
              <p class="text-sm text-gray-600">{{ project.blueprint?.style || '未设定风格' }}</p>
            </div>
          </div>

          <div class="space-y-3">
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-3">
              <h3 class="text-sm font-semibold text-blue-900 mb-1">故事概要</h3>
              <Tooltip :text="project.blueprint?.one_sentence_summary">
                <p class="text-xs text-blue-700 line-clamp-3">{{ project.blueprint?.one_sentence_summary || '暂无概要' }}</p>
              </Tooltip>
            </div>
            <div class="grid grid-cols-2 gap-2 text-xs">
              <div class="bg-purple-50 rounded-lg p-2 text-center">
                <div class="font-semibold text-purple-800">{{ characterCount }}</div>
                <div class="text-purple-600">角色</div>
              </div>
              <div class="bg-green-50 rounded-lg p-2 text-center">
                <div class="font-semibold text-green-800">{{ relationshipCount }}</div>
                <div class="text-green-600">关系</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 章节列表 -->
        <div ref="listContainer" class="flex-1 overflow-y-auto">
          <div class="p-6 pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-gray-900">章节大纲</h3>
              <div class="flex items-center gap-2">
                <button
                  v-if="hasIncompleteChapters"
                  @click.stop="scrollToFirstIncompleteChapter"
                  class="px-3 py-1 text-xs font-medium text-indigo-600 bg-indigo-50 rounded-full hover:bg-indigo-100 transition-colors"
                >
                  定位到未完成
                </button>
                <span class="bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full text-xs font-medium">
                  {{ totalChapters }} 章
                </span>
              </div>
            </div>
          </div>

          <div class="px-6 pb-6">
            <div v-if="project.blueprint?.chapter_outline?.length" class="space-y-2">
              <div
                v-for="chapter in project.blueprint.chapter_outline"
                :key="chapter.chapter_number"
                :ref="el => setChapterRef(chapter.chapter_number, el)"
                @click="$emit('selectChapter', chapter.chapter_number)"
                :class="[
                  'group cursor-pointer rounded-lg border-2 p-4 transition-all duration-200',
                  selectedForDeletion.includes(chapter.chapter_number)
                    ? 'border-red-300 bg-red-50'
                    : selectedChapterNumber === chapter.chapter_number
                    ? 'border-indigo-300 bg-indigo-50 shadow-md'
                    : 'border-gray-200 hover:border-indigo-200 hover:bg-gray-50'
                ]"
              >
                <div class="flex items-start gap-3">
                  <div class="flex-shrink-0 pt-1">
                    <input
                      type="checkbox"
                      :disabled="isChapterCompleted(chapter.chapter_number)"
                      :checked="selectedForDeletion.includes(chapter.chapter_number)"
                      @click.stop="toggleSelection(chapter.chapter_number)"
                      class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 disabled:opacity-50"
                    />
                  </div>
                  <div
                    :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0',
                      isChapterCompleted(chapter.chapter_number)
                        ? 'bg-green-500 text-white'
                        : isChapterGenerating(chapter.chapter_number) || isChapterEvaluating(chapter.chapter_number) || isChapterSelecting(chapter.chapter_number)
                        ? 'bg-blue-500 text-white animate-pulse'
                        : isChapterFailed(chapter.chapter_number)
                        ? 'bg-red-500 text-white'
                        : selectedChapterNumber === chapter.chapter_number
                        ? 'bg-indigo-500 text-white'
                        : 'bg-gray-200 text-gray-600'
                    ]"
                  >
                    <svg v-if="isChapterCompleted(chapter.chapter_number)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    <svg v-else-if="isChapterGenerating(chapter.chapter_number) || isChapterSelecting(chapter.chapter_number)" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                    </svg>
                    <svg v-else-if="isChapterEvaluating(chapter.chapter_number)" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 2a6 6 0 00-6 6v3.586l-1.707 1.707A1 1 0 003 15v1a1 1 0 001 1h12a1 1 0 001-1v-1a1 1 0 00-.293-.707L16 11.586V8a6 6 0 00-6-6zM8.05 17a2 2 0 103.9 0H8.05z"></path>
                    </svg>
                    <svg v-else-if="isChapterFailed(chapter.chapter_number)" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    <span v-else>{{ chapter.chapter_number }}</span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <Tooltip :text="chapter.title">
                      <h4 class="font-semibold text-gray-900 text-sm mb-1 line-clamp-1">{{ chapter.title }}</h4>
                    </Tooltip>
                    <Tooltip :text="chapter.summary">
                      <p class="text-xs text-gray-600 line-clamp-2 leading-relaxed">{{ chapter.summary }}</p>
                    </Tooltip>

                    <!-- 章节状态 -->
                    <div class="mt-2 flex items-center gap-2">
                      <span v-if="isChapterCompleted(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        已完成
                      </span>
                      <span v-else-if="isChapterGenerating(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 animate-pulse">
                        生成中...
                      </span>
                      <span v-else-if="isChapterSelecting(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 animate-pulse">
                        选择中...
                      </span>
                      <span v-else-if="isChapterEvaluating(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 animate-pulse">
                        评审中...
                      </span>
                      <span v-else-if="isChapterFailed(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                        生成失败
                      </span>
                      <span v-else-if="hasChapterInProgress(chapter.chapter_number)" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800">
                        待选择版本
                      </span>
                      <span v-else class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                        未开始
                      </span>
                    </div>
                  </div>

                  <!-- 章节操作按钮 -->
                  <div class="flex items-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <button
                      v-if="!isChapterCompleted(chapter.chapter_number)"
                      @click.stop="$emit('editChapter', chapter)"
                      class="p-1.5 text-gray-500 hover:bg-gray-100 rounded-md transition-colors"
                      title="编辑大纲"
                    >
                      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z"></path>
                        <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd"></path>
                      </svg>
                    </button>
                    <button
                      v-if="canGenerateChapter(chapter.chapter_number) || isChapterFailed(chapter.chapter_number) || hasChapterInProgress(chapter.chapter_number)"
                      @click.stop="confirmGenerateChapter(chapter.chapter_number)"
                      :disabled="generatingChapter === chapter.chapter_number || isChapterGenerating(chapter.chapter_number)"
                      class="p-1.5 text-indigo-600 hover:bg-indigo-100 rounded-md transition-colors disabled:opacity-50"
                      :title="isChapterCompleted(chapter.chapter_number) ? '重新生成' : isChapterFailed(chapter.chapter_number) ? '重试' : hasChapterInProgress(chapter.chapter_number) ? '重新生成版本' : '开始创作'"
                    >
                      <svg v-if="generatingChapter === chapter.chapter_number || isChapterGenerating(chapter.chapter_number)" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                      </svg>
                      <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                      </svg>
                    </button>
                    <!-- Batch delete replaces the single delete button -->
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-3 opacity-50" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4zM18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9z"></path>
              </svg>
              <p>暂无章节大纲</p>
            </div>
            <div v-if="selectedForDeletion.length > 0" class="mt-4">
              <button
                @click="handleDeleteSelected"
                class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v6a1 1 0 11-2 0V8z" clip-rule="evenodd"></path>
                </svg>
                <span>删除选中的 {{ selectedForDeletion.length }} 章</span>
              </button>
            </div>
            <div class="mt-4">
              <button
                @click="$emit('generateOutline')"
                :disabled="props.isGeneratingOutline"
                class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg v-if="props.isGeneratingOutline" class="w-5 h-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
                </svg>
                <span>{{ props.isGeneratingOutline ? '生成中...' : '生成后续大纲' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, nextTick } from 'vue'
import type { ComponentPublicInstance } from 'vue'
import { globalAlert } from '@/composables/useAlert'
import type { NovelProject } from '@/api/novel'
import Tooltip from '@/components/Tooltip.vue'

interface Props {
  project: NovelProject
  sidebarOpen: boolean
  selectedChapterNumber: number | null
  generatingChapter: number | null
  evaluatingChapter: number | null
  isGeneratingOutline: boolean
}

const props = defineProps<Props>()

const emit = defineEmits(['closeSidebar', 'selectChapter', 'generateChapter', 'editChapter', 'deleteChapter', 'generateOutline'])

const selectedForDeletion = ref<number[]>([])
const listContainer = ref<HTMLElement | null>(null)
const chapterRefs = ref<Record<number, HTMLElement | null>>({})

const characterCount = computed(() => {
  return props.project?.blueprint?.characters?.length || 0
})

const relationshipCount = computed(() => {
  return props.project?.blueprint?.relationships?.length || 0
})

const lastChapterNumber = computed(() => {
  if (!props.project?.blueprint?.chapter_outline || props.project.blueprint.chapter_outline.length === 0) {
    return null
  }
  return Math.max(...props.project.blueprint.chapter_outline.map(ch => ch.chapter_number))
})

const totalChapters = computed(() => {
  return props.project?.blueprint?.chapter_outline?.length || 0
})

const hasIncompleteChapters = computed(() => {
  if (!props.project?.blueprint?.chapter_outline) return false
  return props.project.blueprint.chapter_outline.some(ch => !isChapterCompleted(ch.chapter_number))
})

function toggleSelection(chapterNumber: number) {
  if (isChapterCompleted(chapterNumber)) return
  const index = selectedForDeletion.value.indexOf(chapterNumber)
  if (index > -1) {
    selectedForDeletion.value.splice(index, 1)
  } else {
    selectedForDeletion.value.push(chapterNumber)
  }
}

function handleDeleteSelected() {
  if (selectedForDeletion.value.length === 0) return

  const sortedSelection = [...selectedForDeletion.value].sort((a, b) => a - b)

  if (!lastChapterNumber.value || !sortedSelection.includes(lastChapterNumber.value)) {
    alert('批量删除必须包含最后一章。')
    return
  }

  const isContinuous = sortedSelection.every((num, i) => {
    return i === 0 || num === sortedSelection[i - 1] + 1
  })
  if (!isContinuous) {
    alert('只能删除连续的章节块。')
    return
  }

  emit('deleteChapter', sortedSelection)
  selectedForDeletion.value = []
}

async function confirmGenerateChapter(chapterNumber: number) {
  const confirmed = await globalAlert.showConfirm('重新生成会覆盖当前章节的生成结果，确定继续吗？', '重新生成确认')
  if (confirmed) {
    emit('generateChapter', chapterNumber)
  }
}

function setChapterRef(chapterNumber: number, el: Element | ComponentPublicInstance | null) {
  if (!el) {
    delete chapterRefs.value[chapterNumber]
    return
  }

  const element = el instanceof Element ? el : (el.$el instanceof Element ? el.$el : null)

  if (element) {
    chapterRefs.value[chapterNumber] = element as HTMLElement
  }
}

const scrollToFirstIncompleteChapter = async () => {
  if (!props.project?.blueprint?.chapter_outline) return
  const sorted = [...props.project.blueprint.chapter_outline].sort((a, b) => a.chapter_number - b.chapter_number)
  const target = sorted.find(chapter => !isChapterCompleted(chapter.chapter_number))
  if (!target) return
  await nextTick()
  const element = chapterRefs.value[target.chapter_number]
  if (!element) return
  const container = listContainer.value
  if (container) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' })
  } else {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

// 章节状态检查
const isChapterCompleted = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'successful'
}

const hasChapterInProgress = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'waiting_for_confirm'
}

const isChapterGenerating = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'generating'
}

const isChapterEvaluating = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'evaluating'
}

const isChapterFailed = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'failed'
}

const isChapterSelecting = (chapterNumber: number) => {
  if (!props.project?.chapters) return false
  const chapter = props.project.chapters.find(ch => ch.chapter_number === chapterNumber)
  return chapter && chapter.generation_status === 'selecting'
}

const canGenerateChapter = (chapterNumber: number) => {
  if (!props.project?.blueprint?.chapter_outline) return false

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
</script>
