<!-- AIMETA P=编辑章节弹窗_章节信息编辑|R=章节编辑表单|NR=不含内容生成|E=component:WDEditChapterModal|X=ui|A=编辑弹窗|D=vue|S=dom|RD=./README.ai -->
<template>
  <div v-if="show" class="fixed inset-0 bg-black/30 z-50 flex justify-center items-center" @click.self="$emit('close')">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg mx-4 p-8 transform transition-all duration-300 ease-out" :class="show ? 'scale-100 opacity-100' : 'scale-95 opacity-0'">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">编辑章节大纲</h2>
        <button @click="$emit('close')" class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>

      <div v-if="editableChapter" class="space-y-6">
        <div>
          <label for="chapter-title" class="block text-sm font-medium text-gray-700 mb-2">章节标题</label>
          <input
            type="text"
            id="chapter-title"
            v-model="editableChapter.title"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            placeholder="请输入章节标题"
          />
        </div>
        <div>
          <label for="chapter-summary" class="block text-sm font-medium text-gray-700 mb-2">章节摘要</label>
          <textarea
            id="chapter-summary"
            v-model="editableChapter.summary"
            rows="5"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            placeholder="请输入章节摘要"
          ></textarea>
        </div>
      </div>

      <div class="mt-8 flex justify-end gap-4">
        <button @click="$emit('close')" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
          取消
        </button>
        <button @click="saveChanges" class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50" :disabled="!isChanged">
          保存更改
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import type { ChapterOutline } from '@/api/novel'

interface Props {
  show: boolean
  chapter: ChapterOutline | null
}

const props = defineProps<Props>()
const emit = defineEmits(['close', 'save'])

const editableChapter = ref<ChapterOutline | null>(null)

watch(() => props.chapter, (newChapter) => {
  if (newChapter) {
    editableChapter.value = { ...newChapter }
  } else {
    editableChapter.value = null
  }
}, { deep: true, immediate: true })

const isChanged = computed(() => {
  if (!props.chapter || !editableChapter.value) {
    return false
  }
  return props.chapter.title !== editableChapter.value.title || props.chapter.summary !== editableChapter.value.summary
})

const saveChanges = () => {
  if (editableChapter.value && isChanged.value) {
    emit('save', editableChapter.value)
  }
}
</script>
