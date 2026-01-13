<!-- AIMETA P=自定义提示_提示消息组件|R=提示弹窗|NR=不含业务逻辑|E=component:CustomAlert|X=internal|A=提示组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <Teleport to="body">
    <transition
      enter-active-class="transition-opacity duration-200"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="visible"
        class="md-dialog-overlay"
        @click.self="handleClose"
      >
        <transition
          enter-active-class="transition-all duration-300"
          leave-active-class="transition-all duration-200"
          enter-from-class="opacity-0 scale-95"
          leave-to-class="opacity-0 scale-95"
        >
          <div class="md-dialog max-w-md w-full mx-4">
            <!-- Material 3 Dialog Header -->
            <div class="md-dialog-header flex items-center gap-4">
              <!-- Icon -->
              <div
                class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0"
                :style="iconContainerStyle"
              >
                <!-- Error Icon -->
                <svg
                  v-if="type === 'error'"
                  class="w-6 h-6"
                  :style="{ color: iconColor }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <!-- Success Icon -->
                <svg
                  v-else-if="type === 'success'"
                  class="w-6 h-6"
                  :style="{ color: iconColor }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <!-- Warning Icon -->
                <svg
                  v-else-if="type === 'warning'"
                  class="w-6 h-6"
                  :style="{ color: iconColor }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <!-- Confirmation Icon -->
                <svg
                  v-else-if="type === 'confirmation'"
                  class="w-6 h-6"
                  :style="{ color: iconColor }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <!-- Info Icon -->
                <svg
                  v-else
                  class="w-6 h-6"
                  :style="{ color: iconColor }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="md-dialog-title">{{ titleText }}</h3>
              </div>
            </div>

            <!-- Content -->
            <div class="md-dialog-content">
              <p class="md-body-large" style="color: var(--md-on-surface-variant);">{{ message }}</p>
            </div>

            <!-- Material 3 Dialog Actions -->
            <div class="md-dialog-actions">
              <button
                v-if="showCancel"
                @click="handleCancel"
                class="md-btn md-btn-text md-ripple"
              >
                {{ cancelText }}
              </button>
              <button
                @click="handleConfirm"
                class="md-btn md-ripple"
                :class="confirmButtonClass"
              >
                {{ confirmText }}
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
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

// Material 3 Color Theming
const iconContainerStyle = computed(() => {
  switch (props.type) {
    case 'success': 
      return { backgroundColor: 'var(--md-success-container)' }
    case 'error': 
      return { backgroundColor: 'var(--md-error-container)' }
    case 'warning': 
      return { backgroundColor: 'var(--md-warning-container)' }
    case 'confirmation': 
      return { backgroundColor: 'var(--md-secondary-container)' }
    default: 
      return { backgroundColor: 'var(--md-primary-container)' }
  }
})

const iconColor = computed(() => {
  switch (props.type) {
    case 'success': return 'var(--md-success)'
    case 'error': return 'var(--md-error)'
    case 'warning': return 'var(--md-warning)'
    case 'confirmation': return 'var(--md-secondary)'
    default: return 'var(--md-primary)'
  }
})

const confirmButtonClass = computed(() => {
  switch (props.type) {
    case 'error': 
      return 'md-btn-filled'
    default: 
      return 'md-btn-filled'
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
