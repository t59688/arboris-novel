<!-- AIMETA P=项目卡片_小说项目展示|R=项目信息卡片|NR=不含编辑功能|E=component:ProjectCard|X=internal|A=卡片组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div
    class="md-card md-card-elevated group p-5 flex flex-col justify-between transition-all duration-300 hover:scale-[1.01]"
    style="border-radius: var(--md-radius-lg);"
  >
    <div>
      <!-- Header: Icon + Title -->
      <div class="flex items-center gap-4 mb-4">
        <div 
          class="w-12 h-12 rounded-full flex items-center justify-center"
          :style="{ backgroundColor: themeColors.container, color: themeColors.onContainer }"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
            />
          </svg>
        </div>
        <div class="flex-1 cursor-pointer" @click="$emit('detail', project.id)">
          <h3 class="md-title-medium hover:opacity-80 transition-opacity" style="color: var(--md-on-surface);">
            {{ project.title }}
          </h3>
          <p class="md-body-small" style="color: var(--md-on-surface-variant);">
            {{ project.genre || '未知类型' }} · {{ getStatusText }}
          </p>
          <p class="md-label-small mt-1" style="color: var(--md-on-surface-variant);">
            最后编辑: {{ formatDateTime(project.last_edited) }}
          </p>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="flex justify-between mb-2">
          <span class="md-label-medium" style="color: var(--md-on-surface-variant);">完成进度</span>
          <span class="md-label-medium" style="color: var(--md-on-surface);">{{ progress }}%</span>
        </div>
        <div class="md-progress-linear">
          <div 
            class="md-progress-linear-bar" 
            :style="{ width: `${progress}%`, backgroundColor: themeColors.primary }"
          ></div>
        </div>
      </div>

      <!-- Material 3 Chips -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span 
          v-if="project.genre"
          class="md-chip md-chip-filter selected"
          :style="{ backgroundColor: themeColors.container, color: themeColors.onContainer }"
        >
          {{ project.genre }}
        </span>
        <span 
          v-if="chapterCount > 0"
          class="md-chip md-chip-assist"
        >
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          {{ chapterCount }} 章节
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-2 group-hover:translate-y-0">
      <button
        @click.stop="$emit('detail', project.id)"
        class="md-btn md-btn-tonal md-ripple flex-1"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        查看
      </button>
      <button
        @click.stop="handleDelete"
        class="md-icon-btn md-ripple"
        style="color: var(--md-error);"
        title="删除项目"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
      <button
        @click.stop="$emit('continue', project)"
        class="md-btn md-btn-filled md-ripple flex-1"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
        创作
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { NovelProjectSummary } from '@/api/novel'
import { formatDateTime } from '@/utils/date'

interface Props {
  project: NovelProjectSummary
}

const props = defineProps<Props>()

const emit = defineEmits<{
  (e: 'click', id: string): void
  (e: 'detail', id: string): void
  (e: 'continue', project: NovelProjectSummary): void
  (e: 'delete', id: string): void
}>()

// Material 3 Color Theming based on genre
const themeColors = computed(() => {
  const genre = props.project.genre || ''
  
  // Google 4-color palette mapping
  if (genre.includes('科幻') || genre.includes('悬疑')) {
    return {
      primary: 'var(--md-google-blue)',
      container: 'var(--md-primary-container)',
      onContainer: 'var(--md-on-primary-container)'
    }
  } else if (genre.includes('奇幻') || genre.includes('冒险')) {
    return {
      primary: 'var(--md-google-green)',
      container: 'var(--md-success-container)',
      onContainer: 'var(--md-on-success-container)'
    }
  } else if (genre.includes('穿越') || genre.includes('言情')) {
    return {
      primary: 'var(--md-google-red)',
      container: 'var(--md-error-container)',
      onContainer: 'var(--md-on-error-container)'
    }
  } else if (genre.includes('东方') || genre.includes('武侠')) {
    return {
      primary: 'var(--md-google-yellow)',
      container: 'var(--md-warning-container)',
      onContainer: 'var(--md-on-warning-container)'
    }
  }
  
  return {
    primary: 'var(--md-primary)',
    container: 'var(--md-secondary-container)',
    onContainer: 'var(--md-on-secondary-container)'
  }
})

// 使用后端预计算的进度数据
const progress = computed(() => {
  const { completed_chapters, total_chapters } = props.project
  return total_chapters > 0 ? Math.round((completed_chapters / total_chapters) * 100) : 0
})

const getStatusText = computed(() => {
  const { completed_chapters, total_chapters } = props.project
  
  if (completed_chapters > 0) {
    return `已完成 ${completed_chapters}/${total_chapters} 章`
  } else if (total_chapters > 0) {
    return '准备创作'
  } else {
    return '蓝图完成'
  }
})

// 使用后端返回的预计算数据
const chapterCount = computed(() => {
  return props.project.total_chapters
})

const handleDelete = () => {
  emit('delete', props.project.id)
}
</script>
