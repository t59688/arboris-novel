<!-- AIMETA P=写作台头部_顶部导航栏|R=导航_操作按钮|NR=不含内容区域|E=component:WDHeader|X=ui|A=头部组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="flex-shrink-0 z-30 bg-white/80 backdrop-blur-lg border-b border-gray-200 shadow-sm">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- 左侧：项目信息 -->
        <div class="flex items-center gap-2 sm:gap-4 min-w-0">
          <button
            @click="$emit('goBack')"
            class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors flex-shrink-0"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L4.414 9H17a1 1 0 110 2H4.414l5.293 5.293a1 1 0 010 1.414z" clip-rule="evenodd"></path>
            </svg>
          </button>
          <div class="min-w-0">
            <h1 class="text-base sm:text-lg font-bold text-gray-900 truncate">{{ project?.title || '加载中...' }}</h1>
            <div class="hidden sm:flex items-center gap-2 md:gap-4 text-xs md:text-sm text-gray-600">
              <span>{{ project?.blueprint?.genre || '--' }}</span>
              <span class="hidden md:inline">•</span>
              <span class="hidden md:inline">{{ progress }}% 完成</span>
              <span class="hidden lg:inline">•</span>
              <span class="hidden lg:inline">{{ completedChapters }}/{{ totalChapters }} 章</span>
            </div>
          </div>
        </div>

        <!-- 右侧：操作按钮 -->
        <div class="flex items-center gap-1 sm:gap-2">
          <button
            @click="$emit('viewProjectDetail')"
            class="p-2 sm:px-3 sm:py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
            </svg>
            <span class="hidden md:inline text-sm">项目详情</span>
          </button>
          <div class="w-px h-6 bg-gray-300 hidden sm:block"></div>
          <button
            @click="handleLogout"
            class="p-2 sm:px-3 sm:py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="hidden md:inline text-sm">退出登录</span>
          </button>
          <button
            @click="$emit('toggleSidebar')"
            class="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors lg:hidden"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { NovelProject } from '@/api/novel'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

interface Props {
  project: NovelProject | null
  progress: number
  completedChapters: number
  totalChapters: number
}

defineProps<Props>()

defineEmits(['goBack', 'viewProjectDetail', 'toggleSidebar'])
</script>
