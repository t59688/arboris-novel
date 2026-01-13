<!-- AIMETA P=章节列表_章节目录展示|R=章节列表渲染|NR=不含章节编辑|E=component:ChapterList|X=internal|A=列表组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">章节列表</h3>

    <div v-if="chapterOutline.length === 0" class="text-gray-500 text-center py-8">
      暂无章节大纲
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="outline in chapterOutline"
        :key="outline.chapter_number"
        class="border rounded-lg p-3 hover:bg-gray-50 transition-colors"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <h4 class="font-medium text-gray-800">
              第{{ outline.chapter_number }}章: {{ outline.title }}
            </h4>
            <p class="text-sm text-gray-600 mt-1">{{ outline.summary }}</p>

            <!-- 章节状态 -->
            <div class="mt-2">
              <span
                :class="getChapterStatusClass(outline.chapter_number)"
                class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
              >
                {{ getChapterStatus(outline.chapter_number) }}
              </span>
            </div>
          </div>

          <div class="flex flex-col gap-2 ml-4">
            <!-- 查看按钮 -->
            <button
              v-if="isChapterCompleted(outline.chapter_number)"
              @click="$emit('selectChapter', outline.chapter_number)"
              class="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors text-sm"
            >
              查看
            </button>

            <!-- 生成按钮 -->
            <button
              v-if="!isChapterCompleted(outline.chapter_number)"
              @click="$emit('generateChapter', outline.chapter_number)"
              class="px-3 py-1 bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors text-sm"
            >
              生成
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Chapter, ChapterOutline } from '@/api/novel'

interface Props {
  chapters: Chapter[]
  chapterOutline: ChapterOutline[]
}

const props = defineProps<Props>()

defineEmits<{
  selectChapter: [chapterNumber: number]
  generateChapter: [chapterNumber: number]
}>()

const isChapterCompleted = (chapterNumber: number) => {
  return props.chapters.some(ch => ch.chapter_number === chapterNumber && ch.content)
}

const getChapterStatus = (chapterNumber: number) => {
  const chapter = props.chapters.find(ch => ch.chapter_number === chapterNumber)
  if (!chapter) return '未开始'
  if (chapter.content) return '已完成'
  if (chapter.versions && chapter.versions.length > 0) return '待选择'
  return '未开始'
}

const getChapterStatusClass = (chapterNumber: number) => {
  const status = getChapterStatus(chapterNumber)
  switch (status) {
    case '已完成':
      return 'bg-green-100 text-green-800'
    case '待选择':
      return 'bg-yellow-100 text-yellow-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>