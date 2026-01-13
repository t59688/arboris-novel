<!-- AIMETA P=生成失败_生成错误状态|R=错误提示_重试|NR=不含生成逻辑|E=component:ChapterFailed|X=internal|A=错误状态|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="h-full flex items-center justify-center">
    <div class="text-center max-w-md">
      <div class="w-24 h-24 bg-red-100 rounded-full mx-auto flex items-center justify-center mb-6 shadow-lg">
        <svg class="w-12 h-12 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
      </div>
      <h3 class="text-2xl font-bold text-gray-800 mb-3">第{{ chapterNumber }}章生成失败</h3>
      <p class="text-gray-600 mb-6">很抱歉，AI在生成这个章节时遇到了问题。请点击重试按钮重新生成。</p>
      <button
        @click="$emit('generateChapter', chapterNumber)"
        :disabled="generatingChapter === chapterNumber"
        class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-2 mx-auto"
      >
        <svg v-if="generatingChapter === chapterNumber" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
        </svg>
        <svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
        </svg>
        {{ generatingChapter === chapterNumber ? '重试中...' : '重试生成' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  chapterNumber: number
  generatingChapter: number | null
}

defineProps<Props>()

defineEmits(['generateChapter'])
</script>
