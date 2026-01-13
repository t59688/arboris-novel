<!-- AIMETA P=工作区入口_应用主入口|R=入口导航|NR=不含具体功能|E=route:/#component:WorkspaceEntry|X=ui|A=入口页|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="flex items-center justify-center min-h-screen p-4 relative md-surface-dim">
    <!-- Material 3 Update Log Modal -->
    <div v-if="showModal" class="md-dialog-overlay" @click.self="closeModal">
      <div class="md-dialog w-full max-w-4xl mx-4 max-h-[90vh] flex flex-col">
        <!-- Header -->
        <div class="md-dialog-header border-b" style="border-color: var(--md-outline-variant);">
          <h1 class="md-headline-medium text-center" style="color: var(--md-on-surface);">更新日志</h1>
        </div>
        
        <!-- Community Section -->
        <div v-if="communityLog" class="px-6 pt-6">
          <div class="p-4 rounded-lg" style="background-color: var(--md-primary-container);">
            <div class="prose max-w-none prose-sm" style="color: var(--md-on-primary-container);" v-html="renderMarkdown(communityLog.content)"></div>
          </div>
        </div>

        <!-- Timeline Content -->
        <div class="px-6 py-6 overflow-y-auto flex-1">
          <div class="flow-root">
            <ul role="list" class="-mb-8">
              <li v-for="(log, index) in filteredUpdateLogs" :key="log.id">
                <div class="relative pb-8">
                  <!-- Connector Line -->
                  <span 
                    v-if="index < filteredUpdateLogs.length - 1" 
                    class="absolute left-2.5 top-4 -ml-px h-full w-0.5" 
                    style="background-color: var(--md-outline-variant);"
                    aria-hidden="true"
                  ></span>
                  <div class="relative flex items-start space-x-4">
                    <!-- Timeline Dot -->
                    <div 
                      class="h-5 w-5 rounded-full flex items-center justify-center ring-8 mt-1"
                      style="background-color: var(--md-primary); ring-color: var(--md-surface);"
                    ></div>
                    <!-- Card Content -->
                    <div class="min-w-0 flex-1">
                      <div class="md-card md-card-outlined p-4">
                        <time class="md-label-large" style="color: var(--md-on-surface-variant);">
                          {{ new Date(log.created_at).toLocaleDateString() }}
                        </time>
                        <div class="mt-3 prose max-w-none prose-sm" style="color: var(--md-on-surface);" v-html="renderMarkdown(log.content)"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- Footer Actions -->
        <div class="md-dialog-actions border-t" style="border-color: var(--md-outline-variant); background-color: var(--md-surface-container-low);">
          <button @click="hideModalToday" class="md-btn md-btn-text md-ripple">
            今日不再显示
          </button>
          <button @click="closeModal" class="md-btn md-btn-filled md-ripple">
            关闭
          </button>
        </div>
      </div>
    </div>

    <!-- Top Right Actions -->
    <div class="absolute top-4 right-4 flex space-x-2">
      <router-link
        to="/settings"
        class="md-btn md-btn-text md-ripple"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        设置
      </router-link>
      <button
        @click="handleLogout"
        class="md-btn md-btn-text md-ripple"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        退出登录
      </button>
    </div>

    <!-- Main Content -->
    <div class="w-full max-w-4xl mx-auto">
      <div class="text-center p-8 fade-in">
        <!-- Title -->
        <h1 class="md-display-small mb-4" style="color: var(--md-on-surface);">
          拯救小说家：创作中心
        </h1>
        <p class="md-body-large mb-12" style="color: var(--md-on-surface-variant);">
          从一个新灵感开始，或继续打磨你的世界。
        </p>

        <!-- Mode Selection Cards -->
        <div class="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto">
          <!-- Inspiration Mode Card -->
          <div
            @click="goToInspiration"
            class="md-card md-card-elevated group p-8 cursor-pointer transition-all duration-300 hover:scale-[1.02]"
            style="border-radius: var(--md-radius-xl);"
          >
            <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: var(--md-primary-container);">
              <svg class="w-8 h-8" style="color: var(--md-on-primary-container);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h2 class="md-title-large mb-2" style="color: var(--md-primary);">灵感模式</h2>
            <p class="md-body-medium" style="color: var(--md-on-surface-variant);">
              没有头绪？让AI通过对话式引导，帮你构建故事的雏形。
            </p>
          </div>

          <!-- Novel Workspace Card -->
          <div
            @click="goToWorkspace"
            class="md-card md-card-elevated group p-8 cursor-pointer transition-all duration-300 hover:scale-[1.02]"
            style="border-radius: var(--md-radius-xl);"
          >
            <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center" style="background-color: var(--md-success-container);">
              <svg class="w-8 h-8" style="color: var(--md-on-success-container);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <h2 class="md-title-large mb-2" style="color: var(--md-success);">小说工作台</h2>
            <p class="md-body-medium" style="color: var(--md-on-surface-variant);">
              查看、编辑和管理你所有的小说项目工程。
            </p>
          </div>
        </div>

        <!-- Google Colors Accent Bar -->
        <div class="flex justify-center gap-2 mt-12">
          <div class="w-12 h-1 rounded-full" style="background-color: var(--md-google-blue);"></div>
          <div class="w-12 h-1 rounded-full" style="background-color: var(--md-google-red);"></div>
          <div class="w-12 h-1 rounded-full" style="background-color: var(--md-google-yellow);"></div>
          <div class="w-12 h-1 rounded-full" style="background-color: var(--md-google-green);"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { marked } from 'marked'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { getLatestUpdates } from '../api/updates'
import type { UpdateLog } from '../api/updates'

marked.setOptions({
  gfm: true,
  breaks: true
})

const renderMarkdown = (md: string) => marked.parse(md)

const router = useRouter()
const authStore = useAuthStore()

const showModal = ref(false)
const updateLogs = ref<UpdateLog[]>([])

// 查找包含"交流群"的日志
const communityLog = computed(() => {
  return updateLogs.value.find(log => /交流群/.test(log.content))
})

// 过滤掉包含"交流群"的日志，用于时间线显示
const filteredUpdateLogs = computed(() => {
  if (!communityLog.value) {
    return updateLogs.value
  }
  return updateLogs.value.filter(log => log.id !== communityLog.value!.id)
})

onMounted(async () => {
  const hideUntil = localStorage.getItem('hideAnnouncement')
  if (hideUntil !== new Date().toDateString()) {
    try {
      updateLogs.value = await getLatestUpdates()
      if (updateLogs.value.length > 0) {
        showModal.value = true
      }
    } catch (error) {
      console.error('Failed to fetch update logs:', error)
    }
  }
})

const closeModal = () => {
  showModal.value = false
}

const hideModalToday = () => {
  localStorage.setItem('hideAnnouncement', new Date().toDateString())
  closeModal()
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const goToInspiration = () => {
  router.push('/inspiration')
}

const goToWorkspace = () => {
  router.push('/workspace')
}
</script>
