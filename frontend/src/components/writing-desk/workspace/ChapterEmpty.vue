<!-- AIMETA P=空章节_未选择章节状态|R=空状态提示|NR=不含内容展示|E=component:ChapterEmpty|X=internal|A=空状态|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="h-full flex items-center justify-center">
    <div class="text-center">
      <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
      </svg>
      <h3 class="text-lg font-semibold text-gray-700 mb-2">开始创作</h3>

      <div v-if="canGenerate">
        <p class="text-gray-500 mb-4">点击"开始创作"按钮生成这个章节</p>
        <button
          @click="$emit('generateChapter', chapterNumber)"
          :disabled="generatingChapter === chapterNumber"
          class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 flex items-center gap-2 mx-auto"
        >
          <svg v-if="generatingChapter === chapterNumber" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
          </svg>
          {{ generatingChapter === chapterNumber ? '生成中...' : '开始创作' }}
        </button>
      </div>

      <div v-else>
        <p class="text-gray-500 mb-4">请先完成前面的章节，才能生成此章节</p>
        <div class="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-600 rounded-lg">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"></path>
          </svg>
          按顺序生成
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  chapterNumber: number
  generatingChapter: number | null
  canGenerate: boolean
}

defineProps<Props>()

defineEmits(['generateChapter'])
</script>
