<!-- AIMETA P=章节工作区_章节编辑界面|R=章节编辑|NR=不含列表功能|E=component:ChapterWorkspace|X=internal|A=工作区|D=vue|S=dom,net|RD=./README.ai -->
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
        <button
          @click="confirmRegenerate"
          class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition-colors"
        >
          重新生成版本
        </button>
      </div>

      <div class="prose max-w-none p-4 bg-gray-50 rounded-lg border">
        <div class="whitespace-pre-wrap">{{ chapter.content }}</div>
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
  </div>
</template>

<script setup lang="ts">
import { globalAlert } from '@/composables/useAlert'
import type { Chapter, ChapterOutline, ChapterGenerationResponse } from '@/api/novel'

interface Props {
  chapter: Chapter | null
  chapterOutline: ChapterOutline | null
  generationResult: ChapterGenerationResponse | null
}

defineProps<Props>()

const emit = defineEmits<{
  selectVersion: [versionIndex: number]
  regenerate: []
}>()

const confirmRegenerate = async () => {
  const confirmed = await globalAlert.showConfirm('重新生成会覆盖当前章节的现有结果，确定继续吗？', '重新生成确认')
  if (confirmed) {
    emit('regenerate')
  }
}
</script>