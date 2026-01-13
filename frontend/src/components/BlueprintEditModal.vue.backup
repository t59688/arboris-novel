<template>
  <div v-if="show" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex justify-center items-center" @click.self="$emit('close')">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-2xl mx-4">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-xl font-semibold text-gray-800">编辑 {{ title }}</h3>
      </div>
      <div class="p-6">
        <ChapterOutlineEditor v-if="props.field === 'chapter_outline'" v-model="editableContent" />
        <KeyLocationsEditor v-else-if="props.field === 'world_setting.key_locations'" v-model="editableContent" />
        <CharactersEditor v-else-if="props.field === 'characters'" v-model="editableContent" />
        <RelationshipsEditor v-else-if="props.field === 'relationships'" v-model="editableContent" />
        <FactionsEditor v-else-if="props.field === 'world_setting.factions'" v-model="editableContent" />
        <textarea 
          v-else
          v-model="editableContent" 
          class="w-full h-64 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-150 ease-in-out"
          placeholder="请输入内容..."
        ></textarea>
      </div>
      <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end space-x-3">
        <button @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          取消
        </button>
        <button @click="saveChanges" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          保存
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import ChapterOutlineEditor from './ChapterOutlineEditor.vue';
import KeyLocationsEditor from './KeyLocationsEditor.vue';
import CharactersEditor from './CharactersEditorEnhanced.vue';
import RelationshipsEditor from './RelationshipsEditor.vue';
import FactionsEditor from './FactionsEditor.vue';
import type { ChapterOutline } from '@/api/novel';

const props = defineProps({
  show: Boolean,
  title: String,
  content: {
    type: [String, Object, Array],
    default: ''
  },
  field: String
});

const emit = defineEmits(['close', 'save']);

const editableContent = ref<any>('');

watch(() => props.show, (isVisible) => {
  if (isVisible) {
    // 当模态框显示时，进行一次性的深克隆，创建一个独立的、可编辑的副本。
    // 这会切断与外部的响应式链接，避免编辑时的大规模更新。
    // 我们在这里恢复使用 JSON.parse(JSON.stringify(...))，因为它的性能开销
    // 在“一次性”操作中是可接受的，并且是实现深克隆和响应式隔离的最简单方法。
    try {
      editableContent.value = JSON.parse(JSON.stringify(props.content || ''));
    } catch (e) {
      // 对于无法序列化的简单类型，直接赋值
      editableContent.value = props.content || '';
    }
  }
}, { immediate: true });

const saveChanges = () => {
  emit('save', { field: props.field, content: editableContent.value });
};
</script>
