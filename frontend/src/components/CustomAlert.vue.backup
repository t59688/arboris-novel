<template>
  <Teleport to="body">
    <div
      v-if="visible"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="handleClose"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl max-w-md w-full transform transition-all duration-300 ease-out"
        :class="visible ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
      >
        <!-- 头部 -->
        <div
          class="flex items-center p-6 pb-4"
          :class="headerColorClass"
        >
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center mr-4"
            :class="iconBgClass"
          >
            <!-- 错误图标 -->
            <svg
              v-if="type === 'error'"
              class="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <!-- 成功图标 -->
            <svg
              v-else-if="type === 'success'"
              class="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
            </svg>
            <!-- 警告图标 -->
            <svg
              v-else-if="type === 'warning'"
              class="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
            <!-- 确认图标 -->
            <svg
              v-else-if="type === 'confirmation'"
              class="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
            <!-- 信息图标 -->
            <svg
              v-else
              class="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800">{{ titleText }}</h3>
          </div>
        </div>

        <!-- 内容 -->
        <div class="px-6 pb-4">
          <p class="text-gray-600 leading-relaxed">{{ message }}</p>
        </div>

        <!-- 底部按钮 -->
        <div class="flex justify-end gap-3 p-6 pt-4 bg-gray-50 rounded-b-2xl">
          <button
            v-if="showCancel"
            @click="handleCancel"
            class="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition-colors duration-200"
          >
            {{ cancelText }}
          </button>
          <button
            @click="handleConfirm"
            class="px-6 py-2 rounded-lg font-medium transition-all duration-200 transform hover:scale-105"
            :class="confirmButtonClass"
          >
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  visible: boolean
  type?: 'success' | 'error' | 'warning' | 'info' | 'confirmation'
  title?: string
  message: string
  showCancel?: boolean
  confirmText?: string
  cancelText?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  title: '',
  showCancel: false,
  confirmText: '确定',
  cancelText: '取消'
})

const emit = defineEmits<{
  confirm: []
  cancel: []
  close: []
}>()

const titleText = computed(() => {
  if (props.title) return props.title

  switch (props.type) {
    case 'success': return '操作成功'
    case 'error': return '出现错误'
    case 'warning': return '警告提示'
    case 'confirmation': return '请确认'
    default: return '提示信息'
  }
})

const headerColorClass = computed(() => {
  switch (props.type) {
    case 'success': return ''
    case 'error': return ''
    case 'warning': return ''
    default: return ''
  }
})

const iconBgClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bg-green-500'
    case 'error': return 'bg-red-500'
    case 'warning': return 'bg-amber-500'
    case 'confirmation': return 'bg-gray-500'
    default: return 'bg-blue-500'
  }
})

const confirmButtonClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bg-green-500 hover:bg-green-600 text-white shadow-lg hover:shadow-green-200'
    case 'error': return 'bg-red-500 hover:bg-red-600 text-white shadow-lg hover:shadow-red-200'
    case 'warning': return 'bg-amber-500 hover:bg-amber-600 text-white shadow-lg hover:shadow-amber-200'
    case 'confirmation': return 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg hover:shadow-indigo-200'
    default: return 'bg-blue-500 hover:bg-blue-600 text-white shadow-lg hover:shadow-blue-200'
  }
})

const handleConfirm = () => {
  emit('confirm')
  emit('close')
}

const handleCancel = () => {
  emit('cancel')
  emit('close')
}

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
/* 自定义动画 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.transform {
  animation: slideIn 0.3s ease-out;
}
</style>
