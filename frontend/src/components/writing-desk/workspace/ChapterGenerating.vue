<!-- AIMETA P=生成中_章节生成进度|R=进度展示_流式输出|NR=不含生成逻辑|E=component:ChapterGenerating|X=internal|A=生成状态|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="h-full flex items-center justify-center">
    <div class="text-center max-w-md">
      <div class="relative mb-8">
        <div class="w-24 h-24 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-full mx-auto flex items-center justify-center animate-pulse shadow-lg">
          <svg class="w-12 h-12 text-white animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="absolute inset-0 w-24 h-24 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-full mx-auto animate-ping opacity-20"></div>
      </div>
      <h3 class="text-2xl font-bold text-gray-800 mb-3">{{ statusText.title }}</h3>
      <div class="space-y-2 text-gray-600 mb-6">
        <p class="animate-pulse">{{ statusText.line1 }}</p>
        <p class="animate-pulse" style="animation-delay: 0.5s">{{ statusText.line2 }}</p>
        <p class="animate-pulse" style="animation-delay: 1s">🎨 描绘生动场景...</p>
      </div>
      <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <p class="text-blue-800 text-sm">
          <svg class="w-4 h-4 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
          </svg>
          生成过程通常需要2分钟以上，请耐心等待。您可以随时离开此页面，生成完成后再回来查看。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Chapter } from '@/api/novel'

interface Props {
  chapterNumber: number | null
  status: Chapter['generation_status'] | null
}

const props = defineProps<Props>()

const statusText = computed(() => {
  switch (props.status) {
    case 'generating':
      return {
        title: `AI 正在为您创作第${props.chapterNumber}章`,
        line1: '✨ 构思情节发展...',
        line2: '📝 编织精彩对话...'
      }
    case 'evaluating':
      return {
        title: `AI 正在评审第${props.chapterNumber}章的多个版本`,
        line1: '🧐 分析故事结构...',
        line2: '⚖️ 比较版本优劣...'
      }
    case 'selecting':
      return {
        title: `正在确认第${props.chapterNumber}章的最终版本`,
        line1: '💾 保存您的选择...',
        line2: '✍️ 生成最终摘要...'
      }
    default:
      return {
        title: '请稍候...',
        line1: '正在处理您的请求...',
        line2: '...'
      }
  }
})
</script>
