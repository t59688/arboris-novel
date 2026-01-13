<!-- AIMETA P=工具提示_悬浮提示组件|R=提示信息|NR=不含业务逻辑|E=component:Tooltip|X=internal|A=提示组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div ref="triggerRef" class="inline-block" @mouseenter="onMouseEnter" @mouseleave="onMouseLeave">
    <slot></slot>
    <Teleport to="body">
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div
          v-if="showTooltip && text"
          ref="tooltipRef"
          :style="tooltipStyle"
          class="fixed z-50 p-3 text-sm leading-tight text-white bg-gray-800 rounded-lg shadow-lg max-w-xs"
          @mouseenter="onTooltipEnter"
          @mouseleave="onTooltipLeave"
        >
          {{ text }}
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from 'vue'

interface Props {
  text?: string
}

const props = defineProps<Props>()

const showTooltip = ref(false)
const triggerRef = ref<HTMLElement | null>(null)
const tooltipRef = ref<HTMLElement | null>(null)
const tooltipPosition = ref({ top: 0, left: 0 })

const tooltipStyle = computed(() => ({
  top: `${tooltipPosition.value.top}px`,
  left: `${tooltipPosition.value.left}px`,
}))

let leaveTimeout: NodeJS.Timeout
let enterTimeout: NodeJS.Timeout

const onMouseEnter = () => {
  clearTimeout(leaveTimeout)
  enterTimeout = setTimeout(async () => {
    showTooltip.value = true
    await nextTick()
    updatePosition()
  }, 1000) // 延迟1秒显示
}

const onMouseLeave = () => {
  clearTimeout(enterTimeout) // 清除进入的计时器
  leaveTimeout = setTimeout(() => {
    showTooltip.value = false
  }, 200) // 增加延时以便鼠标可以移动到 tooltip 上
}

const onTooltipEnter = () => {
  clearTimeout(leaveTimeout)
}

const onTooltipLeave = () => {
  showTooltip.value = false
}

const updatePosition = () => {
  if (!triggerRef.value || !tooltipRef.value) return

  const triggerRect = triggerRef.value.getBoundingClientRect()
  const tooltipRect = tooltipRef.value.getBoundingClientRect()

  let top = triggerRect.top - tooltipRect.height - 8 // 默认在上方，留 8px 间距
  let left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2)

  // 如果上方空间不足，则显示在下方
  if (top < 0) {
    top = triggerRect.bottom + 8
  }

  // 如果左侧超出屏幕，则向右对齐
  if (left < 0) {
    left = 8
  }

  // 如果右侧超出屏幕，则向左对齐
  if (left + tooltipRect.width > window.innerWidth) {
    left = window.innerWidth - tooltipRect.width - 8
  }

  tooltipPosition.value = { top, left }
}
</script>
