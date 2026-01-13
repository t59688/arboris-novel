<!-- AIMETA P=世界观区_世界设定展示|R=世界观信息|NR=不含编辑功能|E=component:WorldSettingSection|X=ui|A=世界观组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="space-y-6">
    <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-6">
      <div class="flex items-start justify-between gap-4 mb-4">
        <h3 class="text-lg font-semibold text-slate-900">核心规则</h3>
        <button
          v-if="editable"
          type="button"
          class="text-gray-400 hover:text-indigo-600 transition-colors"
          @click="emitEdit('world_setting.core_rules', '核心规则', worldSetting.core_rules)">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
            <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <p class="text-slate-600 leading-7 whitespace-pre-line">{{ worldSetting.core_rules || '暂无' }}</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center text-slate-900 font-semibold">
            <svg class="mr-2 text-indigo-500" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18"/><path d="M6 18H4a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h2v7Z"/><path d="M18 18h2a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2h-2v7Z"/></svg>
            <span>关键地点</span>
          </div>
          <button
            v-if="editable"
            type="button"
            class="text-gray-400 hover:text-indigo-600 transition-colors"
            @click="emitEdit('world_setting.key_locations', '关键地点', worldSetting.key_locations)">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
              <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <ul class="space-y-4 text-sm text-slate-600">
          <li v-for="(item, index) in locations" :key="index" class="bg-slate-50 border border-slate-100 rounded-xl p-4">
            <strong class="block text-slate-800 mb-1">{{ item.title }}</strong>
            <span class="text-xs text-slate-500 leading-5">{{ item.description }}</span>
          </li>
          <li v-if="!locations.length" class="text-slate-400 text-sm">暂无数据</li>
        </ul>
      </div>

      <div class="bg-white/95 rounded-2xl shadow-sm border border-slate-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center text-slate-900 font-semibold">
            <svg class="mr-2 text-indigo-500" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span>主要阵营</span>
          </div>
          <button
            v-if="editable"
            type="button"
            class="text-gray-400 hover:text-indigo-600 transition-colors"
            @click="emitEdit('world_setting.factions', '主要阵营', worldSetting.factions)">
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
              <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <ul class="space-y-4 text-sm text-slate-600">
          <li v-for="(item, index) in factions" :key="index" class="bg-slate-50 border border-slate-100 rounded-xl p-4">
            <strong class="block text-slate-800 mb-1">{{ item.title }}</strong>
            <span class="text-xs text-slate-500 leading-5">{{ item.description }}</span>
          </li>
          <li v-if="!factions.length" class="text-slate-400 text-sm">暂无数据</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineEmits, defineProps } from 'vue'

interface ListItem {
  title: string
  description: string
}

const props = defineProps<{
  data: Record<string, any> | null
  editable?: boolean
}>()

const emit = defineEmits<{
  (e: 'edit', payload: { field: string; title: string; value: any }): void
}>()

const worldSetting = computed(() => props.data?.world_setting || {})

const normalizeList = (source: any): ListItem[] => {
  if (!source) return []
  if (Array.isArray(source)) {
    return source.map((item: any) => {
      if (typeof item === 'string') {
        const [title, ...rest] = item.split('：')
        return {
          title: title || item,
          description: rest.join('：') || '暂无描述'
        }
      }
      return {
        title: item?.name || '未命名',
        description: item?.description || item?.details || '暂无描述'
      }
    })
  }
  return []
}

const locations = computed(() => normalizeList(worldSetting.value?.key_locations))
const factions = computed(() => normalizeList(worldSetting.value?.factions))

const emitEdit = (field: string, title: string, value: any) => {
  if (!props.editable) return
  emit('edit', { field, title, value })
}
</script>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'WorldSettingSection'
})
</script>
