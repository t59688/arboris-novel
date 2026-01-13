<!-- AIMETA P=蓝图编辑_蓝图编辑弹窗|R=蓝图编辑表单|NR=不含展示功能|E=component:BlueprintEditModal|X=internal|A=编辑弹窗|D=vue|S=dom|RD=./README.ai -->
<template>
  <transition
    enter-active-class="transition-opacity duration-200"
    leave-active-class="transition-opacity duration-200"
    enter-from-class="opacity-0"
    leave-to-class="opacity-0"
  >
    <div v-if="show" class="md-dialog-overlay" @click.self="$emit('close')">
      <transition
        enter-active-class="transition-all duration-300"
        leave-active-class="transition-all duration-200"
        enter-from-class="opacity-0 scale-95"
        leave-to-class="opacity-0 scale-95"
      >
        <div class="md-dialog w-full max-w-2xl mx-4 max-h-[90vh] flex flex-col">
          <!-- Material 3 Dialog Header -->
          <div class="md-dialog-header flex items-center justify-between">
            <h3 class="md-dialog-title">编辑 {{ title }}</h3>
            <button 
              @click="$emit('close')" 
              class="md-icon-btn md-ripple"
              aria-label="关闭"
            >
              <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Dialog Content -->
          <div class="md-dialog-content flex-1 overflow-y-auto py-4">
            <ChapterOutlineEditor v-if="props.field === 'chapter_outline'" v-model="editableContent" />
            <KeyLocationsEditor v-else-if="props.field === 'world_setting.key_locations'" v-model="editableContent" />
            <CharactersEditor v-else-if="props.field === 'characters'" v-model="editableContent" />
            <RelationshipsEditor v-else-if="props.field === 'relationships'" v-model="editableContent" />
            <FactionsEditor v-else-if="props.field === 'world_setting.factions'" v-model="editableContent" />
            <div v-else class="md-text-field">
              <textarea 
                v-model="editableContent" 
                class="md-textarea w-full"
                style="min-height: 256px;"
                placeholder="请输入内容..."
              ></textarea>
            </div>
          </div>

          <!-- Material 3 Dialog Actions -->
          <div class="md-dialog-actions" style="border-top: 1px solid var(--md-outline-variant);">
            <button 
              @click="$emit('close')" 
              class="md-btn md-btn-text md-ripple"
            >
              取消
            </button>
            <button 
              @click="saveChanges" 
              class="md-btn md-btn-filled md-ripple"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              保存
            </button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
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
    try {
      editableContent.value = JSON.parse(JSON.stringify(props.content || ''));
    } catch (e) {
      editableContent.value = props.content || '';
    }
  }
}, { immediate: true });

const saveChanges = () => {
  emit('save', { field: props.field, content: editableContent.value });
};
</script>
