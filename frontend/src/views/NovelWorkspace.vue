<!-- AIMETA P=小说工作区_小说列表管理|R=小说列表_创建|NR=不含章节编辑|E=route:/workspace#component:NovelWorkspace|X=ui|A=工作区|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="flex items-center justify-center min-h-screen p-4 md-surface-dim">
    <!-- Material 3 Snackbar for delete message -->
    <transition
      enter-active-class="transition-all duration-300"
      leave-active-class="transition-all duration-300"
      enter-from-class="opacity-0 translate-y-4"
      leave-to-class="opacity-0 translate-y-4"
    >
      <div v-if="deleteMessage" class="md-snackbar">
        <svg 
          v-if="deleteMessage.type === 'success'" 
          class="w-5 h-5" 
          style="color: var(--md-success);"
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
        <svg 
          v-else 
          class="w-5 h-5" 
          style="color: var(--md-error);"
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="md-snackbar-text">{{ deleteMessage.text }}</span>
      </div>
    </transition>
    
    <div class="w-full max-w-7xl mx-auto">
      <div class="md-card md-card-elevated p-8 fade-in" style="border-radius: var(--md-radius-xl);">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
          <div class="flex items-center gap-4">
            <h2 class="md-headline-medium" style="color: var(--md-on-surface);">我的小说项目</h2>
            <router-link 
              v-if="authStore.user?.is_admin" 
              to="/admin" 
              class="md-chip md-chip-assist"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              管理后台
            </router-link>
          </div>
          <button
            @click="goBack"
            class="md-btn md-btn-text md-ripple"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            返回
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="novelStore.isLoading" class="flex flex-col items-center justify-center py-16">
          <div class="md-spinner"></div>
          <p class="mt-4 md-body-medium" style="color: var(--md-on-surface-variant);">加载中...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="novelStore.error" class="flex flex-col items-center justify-center py-16">
          <div class="w-16 h-16 rounded-full flex items-center justify-center mb-4" style="background-color: var(--md-error-container);">
            <svg class="w-8 h-8" style="color: var(--md-error);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="md-body-large mb-4" style="color: var(--md-error);">{{ novelStore.error }}</p>
          <button
            @click="loadProjects"
            class="md-btn md-btn-filled md-ripple"
          >
            重试
          </button>
        </div>

        <!-- Project Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Empty State -->
          <div v-if="novelStore.projects.length === 0" class="col-span-full flex flex-col items-center justify-center py-16">
            <div class="w-20 h-20 rounded-full flex items-center justify-center mb-4" style="background-color: var(--md-primary-container);">
              <svg class="w-10 h-10" style="color: var(--md-on-primary-container);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <p class="md-body-large mb-2" style="color: var(--md-on-surface);">还没有项目</p>
            <p class="md-body-medium mb-6" style="color: var(--md-on-surface-variant);">快去开启灵感模式创建一个吧！</p>
            <button
              @click="goToInspiration"
              class="md-btn md-btn-filled md-ripple"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              开始创作
            </button>
          </div>

          <!-- Project Cards -->
          <ProjectCard
            v-for="project in novelStore.projects"
            :key="project.id"
            :project="project"
            @click="enterProject(project)"
            @detail="viewProjectDetail"
            @continue="enterProject"
            @delete="handleDeleteProject"
          />

          <!-- Create New Project Card -->
          <div
            @click="goToInspiration"
            class="md-card md-card-outlined flex items-center justify-center p-5 cursor-pointer group min-h-[180px] transition-all duration-300 hover:border-2"
            style="border-radius: var(--md-radius-lg); border-style: dashed;"
            :style="{ borderColor: 'var(--md-outline)' }"
          >
            <div class="text-center transition-colors" style="color: var(--md-on-surface-variant);">
              <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center transition-colors" style="background-color: var(--md-primary-container);">
                <svg class="w-6 h-6" style="color: var(--md-on-primary-container);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
              </div>
              <span class="md-label-large">创建新项目</span>
            </div>
          </div>

          <!-- Import Project Card -->
          <div
            @click="triggerImport"
            class="md-card md-card-outlined flex items-center justify-center p-5 cursor-pointer group min-h-[180px] transition-all duration-300 hover:border-2"
            style="border-radius: var(--md-radius-lg); border-style: dashed;"
            :style="{ borderColor: 'var(--md-outline)' }"
          >
            <div class="text-center transition-colors" style="color: var(--md-on-surface-variant);">
              <div v-if="isImporting" class="flex flex-col items-center">
                <div class="md-spinner w-8 h-8 mb-3"></div>
                <span class="md-label-large">正在导入并分析...</span>
              </div>
              <div v-else>
                <div class="w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center transition-colors" style="background-color: var(--md-success-container);">
                  <svg class="w-6 h-6" style="color: var(--md-on-success-container);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                  </svg>
                </div>
                <span class="md-label-large">导入小说文件</span>
              </div>
            </div>
          </div>
          <input
            type="file"
            ref="fileInput"
            accept=".txt"
            class="hidden"
            @change="handleFileImport"
          />
        </div>
      </div>
    </div>

    <!-- Material 3 Delete Confirmation Dialog -->
    <transition
      enter-active-class="transition-opacity duration-200"
      leave-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div v-if="showDeleteDialog" class="md-dialog-overlay">
        <transition
          enter-active-class="transition-all duration-300"
          leave-active-class="transition-all duration-200"
          enter-from-class="opacity-0 scale-95"
          leave-to-class="opacity-0 scale-95"
        >
          <div class="md-dialog max-w-md w-full mx-4">
            <div class="md-dialog-header flex items-center gap-4">
              <div class="w-12 h-12 rounded-full flex items-center justify-center" style="background-color: var(--md-error-container);">
                <svg class="w-6 h-6" style="color: var(--md-error);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <div>
                <h3 class="md-dialog-title">确认删除</h3>
                <p class="md-body-small" style="color: var(--md-on-surface-variant);">此操作无法撤销</p>
              </div>
            </div>
            
            <div class="md-dialog-content">
              <p class="md-body-large" style="color: var(--md-on-surface);">
                确定要删除项目 "<strong>{{ projectToDelete?.title }}</strong>" 吗？所有相关数据将被永久删除。
              </p>
            </div>
            
            <div class="md-dialog-actions">
              <button
                @click="cancelDelete"
                class="md-btn md-btn-text md-ripple"
              >
                取消
              </button>
              <button
                @click="confirmDelete"
                :disabled="isDeleting"
                class="md-btn md-btn-filled md-ripple"
                style="background-color: var(--md-error); color: var(--md-on-error);"
              >
                <svg v-if="isDeleting" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isDeleting ? '删除中...' : '确认删除' }}
              </button>
            </div>
          </div>
        </transition>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNovelStore } from '@/stores/novel'
import { useAuthStore } from '@/stores/auth'
import ProjectCard from '@/components/ProjectCard.vue'
import type { NovelProject, NovelProjectSummary } from '@/api/novel'
import { NovelAPI } from '@/api/novel'

const router = useRouter()
const novelStore = useNovelStore()
const authStore = useAuthStore()

// 导入相关状态
const fileInput = ref<HTMLInputElement | null>(null)
const isImporting = ref(false)

// 删除相关状态
const showDeleteDialog = ref(false)
const projectToDelete = ref<NovelProjectSummary | null>(null)
const isDeleting = ref(false)
const deleteMessage = ref<{type: 'success' | 'error', text: string} | null>(null)

const goBack = () => {
  router.push('/')
}

const goToInspiration = () => {
  router.push('/inspiration')
}

const viewProjectDetail = (projectId: string) => {
  router.push(`/detail/${projectId}`)
}

const enterProject = (project: NovelProjectSummary) => {
  if (project.title === '未命名灵感') {
    router.push(`/inspiration?project_id=${project.id}`)
  } else {
    router.push(`/novel/${project.id}`)
  }
}

const loadProjects = async () => {
  await novelStore.loadProjects()
}

// 导入相关方法
const triggerImport = () => {
  if (isImporting.value) return
  fileInput.value?.click()
}

const handleFileImport = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return

  const file = target.files[0]
  if (!file.name.endsWith('.txt')) {
    alert('请上传 .txt 格式的文件')
    return
  }

  isImporting.value = true
  try {
    const response = await NovelAPI.importNovel(file)
    await loadProjects()
    router.push(`/novel/${response.id}`)
  } catch (error: any) {
    console.error('导入失败:', error)
    alert(error.message || '导入失败，请重试')
  } finally {
    isImporting.value = false
    target.value = ''
  }
}

// 删除相关方法
const handleDeleteProject = (projectId: string) => {
  const project = novelStore.projects.find(p => p.id === projectId)
  if (project) {
    projectToDelete.value = project
    showDeleteDialog.value = true
  }
}

const cancelDelete = () => {
  showDeleteDialog.value = false
  projectToDelete.value = null
}

const confirmDelete = async () => {
  if (!projectToDelete.value) return
  
  isDeleting.value = true
  try {
    await novelStore.deleteProjects([projectToDelete.value.id])
    deleteMessage.value = { type: 'success', text: `项目 "${projectToDelete.value.title}" 已成功删除` }
    showDeleteDialog.value = false
    projectToDelete.value = null
    
    setTimeout(() => {
      deleteMessage.value = null
    }, 3000)
  } catch (error) {
    console.error('删除项目失败:', error)
    deleteMessage.value = { type: 'error', text: '删除项目失败，请重试' }
    
    setTimeout(() => {
      deleteMessage.value = null
    }, 3000)
  } finally {
    isDeleting.value = false
  }
}

onMounted(() => {
  loadProjects()
})
</script>
