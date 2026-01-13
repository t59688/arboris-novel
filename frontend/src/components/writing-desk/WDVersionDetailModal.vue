<!-- AIMETA P=版本详情弹窗_版本信息展示|R=版本对比_历史|NR=不含版本管理|E=component:WDVersionDetailModal|X=ui|A=版本弹窗|D=vue|S=dom|RD=./README.ai -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
    <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden">
      <!-- 弹窗头部 -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div>
          <h3 class="text-xl font-bold text-gray-900">版本详情</h3>
          <p class="text-sm text-gray-600 mt-1">
            版本 {{ detailVersionIndex + 1 }}
            <span class="text-gray-400">•</span>
            {{ version?.style || '标准' }}风格
            <span class="text-gray-400">•</span>
            约 {{ Math.round(cleanVersionContent(version?.content || '').length / 100) * 100 }} 字
          </p>
        </div>
        <button
          @click="$emit('close')"
          class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>

      <!-- 弹窗内容 -->
      <div class="p-6 overflow-y-auto max-h-[60vh]">
        <div class="prose max-w-none">
          <div class="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {{ cleanVersionContent(version?.content || '') }}
          </div>
        </div>
      </div>

      <!-- 弹窗底部操作按钮 -->
      <div class="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
        <div class="text-sm text-gray-500">
          <span v-if="isCurrent" class="inline-flex items-center px-2 py-1 rounded-full bg-green-100 text-green-800 font-medium">
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            当前选中版本
          </span>
          <span v-else class="text-gray-400">未选中版本</span>
        </div>

        <div class="flex gap-3">
          <button
            @click="$emit('close')"
            class="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded-lg transition-colors"
          >
            关闭
          </button>
          <button
            v-if="!isCurrent"
            @click="$emit('selectVersion')"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            选择此版本
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ChapterVersion } from '@/api/novel'
import { computed } from 'vue'

interface Props {
  show: boolean
  detailVersionIndex: number
  version: ChapterVersion | null
  isCurrent: boolean
}

const props = defineProps<Props>()

defineEmits(['close', 'selectVersion'])

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
</script>
