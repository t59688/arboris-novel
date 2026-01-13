<template>
  <div class="flex items-center justify-center min-h-screen p-4 relative">
    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-slate-900/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm" @click.self="closeModal">
      <div class="w-full max-w-4xl bg-white rounded-2xl shadow-xl overflow-hidden transform transition-all duration-300 flex flex-col max-h-[90vh]">
        <div class="p-8 sm:p-10 pb-4">
            <!-- 头部标题 -->
            <header class="text-center mb-6">
                <h1 class="text-2xl sm:text-3xl font-bold text-slate-800">更新日志</h1>
            </header>
            
            <!-- 加入交流群部分 (动态) -->
            <div v-if="communityLog" class="bg-slate-50 border border-slate-200 rounded-xl p-4">
                <div v-html="renderMarkdown(communityLog.content)"></div>
            </div>
        </div>
        <div class="px-8 sm:px-10 pb-8 sm:pb-10 overflow-y-auto flex-1">
            <!-- 日志条目列表 - 时间线样式 -->
            <div class="flow-root">
                <ul role="list" class="-mb-8">
                    
                    <!-- Timeline Item -->
                    <li v-for="(log, index) in filteredUpdateLogs" :key="log.id">
                        <div class="relative pb-8">
                            <!-- 连接线 (除了最后一个) -->
                            <span v-if="index < filteredUpdateLogs.length - 1" class="absolute left-2.5 top-4 -ml-px h-full w-0.5 bg-slate-200" aria-hidden="true"></span>
                            <div class="relative flex items-start space-x-4">
                                <!-- 时间线上的圆点 -->
                                <div class="h-5 w-5 bg-blue-500 rounded-full flex items-center justify-center ring-8 ring-white mt-1"></div>
                                <!-- 卡片内容 -->
                                <div class="min-w-0 flex-1">
                                    <div class="bg-slate-50/80 border border-slate-200/80 rounded-xl p-4">
                                        <time class="text-sm font-semibold text-slate-600">{{ new Date(log.created_at).toLocaleDateString() }}</time>
                                        <div class="mt-3 prose max-w-none prose-sm prose-slate" v-html="renderMarkdown(log.content)"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        
        <!-- 底部操作按钮 -->
        <footer class="bg-slate-50/70 px-8 py-4 border-t border-slate-200 mt-auto">
            <div class="flex justify-end items-center space-x-4">
                <button @click="hideModalToday" class="px-5 py-2 text-sm font-semibold text-slate-600 bg-transparent rounded-lg hover:bg-slate-200 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400">
                    今日不再显示
                </button>
                <button @click="closeModal" class="px-5 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-sm">
                    关闭
                </button>
            </div>
        </footer>
      </div>
    </div>
    <div class="absolute top-4 right-4 flex space-x-2">
        <router-link
          to="/settings"
          class="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2 cursor-pointer"
        >
          设置
        </router-link>
        <button
          @click="handleLogout"
          class="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-2 cursor-pointer"
        >
          退出登录
        </button>
    </div>
    <div class="w-full max-w-4xl mx-auto">
      <div class="text-center p-8 fade-in">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-4">拯救小说家：创作中心</h1>
        <p class="text-lg text-gray-600 mb-12">从一个新灵感开始，或继续打磨你的世界。</p>

        <div class="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          <!-- 灵感模式卡片 -->
          <div
            @click="goToInspiration"
            class="group p-8 bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer"
          >
            <h2 class="text-2xl font-bold text-indigo-600 mb-3">灵感模式</h2>
            <p class="text-gray-600">没有头绪？让AI通过对话式引导，帮你构建故事的雏形。</p>
          </div>

          <!-- 小说工作台卡片 -->
          <div
            @click="goToWorkspace"
            class="group p-8 bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 cursor-pointer"
          >
            <h2 class="text-2xl font-bold text-teal-600 mb-3">小说工作台</h2>
            <p class="text-gray-600">查看、编辑和管理你所有的小说项目工程。</p>
          </div>
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
  gfm: true,           // 启用 GitHub 风格语法（表格/任务列表/自动链接 等）
  breaks: true         // 将单个换行视为 <br>（常见于后端返回的段落）
})

const renderMarkdown = (md: string) => marked.parse(md)

const router = useRouter()
const authStore = useAuthStore()

const showModal = ref(false)
const updateLogs = ref<UpdateLog[]>([])

// 查找包含“交流群”的日志
const communityLog = computed(() => {
  return updateLogs.value.find(log => /交流群/.test(log.content))
})

// 过滤掉包含“交流群”的日志，用于时间线显示
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
