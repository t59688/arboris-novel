<!-- AIMETA P=概览区_小说基本信息|R=基本信息展示|NR=不含编辑功能|E=component:OverviewSection|X=ui|A=概览组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="space-y-6">
    <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-6">
      <div class="flex items-start justify-between gap-4 mb-3">
        <div>
          <h3 class="text-sm font-semibold text-indigo-600 uppercase tracking-wide">核心摘要</h3>
          <p class="text-gray-500 text-xs">快速了解项目的定位与调性</p>
        </div>
        <button
          v-if="editable"
          type="button"
          class="text-gray-400 hover:text-indigo-600 transition-colors"
          @click="emitEdit('one_sentence_summary', '核心摘要', data?.one_sentence_summary)">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
            <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <p class="text-slate-800 text-lg leading-relaxed min-h-[2.5rem]">{{ data?.one_sentence_summary || '暂无' }}</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-4">
        <h4 class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">目标受众</h4>
        <p class="text-base font-medium text-slate-800 min-h-[1.5rem]">{{ data?.target_audience || '暂无' }}</p>
      </div>
      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-4">
        <h4 class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">类型</h4>
        <p class="text-base font-medium text-slate-800 min-h-[1.5rem]">{{ data?.genre || '暂无' }}</p>
      </div>
      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-4">
        <h4 class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">风格</h4>
        <p class="text-base font-medium text-slate-800 min-h-[1.5rem]">{{ data?.style || '暂无' }}</p>
      </div>
      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-4">
        <h4 class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-2">基调</h4>
        <p class="text-base font-medium text-slate-800 min-h-[1.5rem]">{{ data?.tone || '暂无' }}</p>
      </div>
    </div>

    <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-6">
      <div class="flex items-start justify-between gap-4 mb-4">
        <h3 class="text-lg font-semibold text-slate-900">完整剧情梗概</h3>
        <button
          v-if="editable"
          type="button"
          class="text-gray-400 hover:text-indigo-600 transition-colors"
          @click="emitEdit('full_synopsis', '完整剧情梗概', data?.full_synopsis)">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
            <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <div class="prose prose-sm max-w-none text-slate-600 leading-7 whitespace-pre-line">
        <p>{{ data?.full_synopsis || '暂无' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue'

interface OverviewData {
  one_sentence_summary?: string | null
  target_audience?: string | null
  genre?: string | null
  style?: string | null
  tone?: string | null
  full_synopsis?: string | null
}

const props = defineProps<{
  data: OverviewData | null
  editable?: boolean
}>()

const emit = defineEmits<{
  (e: 'edit', payload: { field: string; title: string; value: any }): void
}>()

const emitEdit = (field: string, title: string, value: any) => {
  if (!props.editable) return
  emit('edit', { field, title, value })
}
</script>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OverviewSection'
})
</script>
