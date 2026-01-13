<!-- AIMETA P=灵感模式_AI对话创作|R=对话创作界面|NR=不含写作台功能|E=route:/inspiration#component:InspirationMode|X=ui|A=对话界面|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-6xl mx-auto">
      <!-- 灵感模式入口界面 -->
      <div v-if="!conversationStarted" class="text-center p-8 bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg fade-in">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-800">小说家的新篇章</h1>
        <p class="text-lg text-gray-600 mt-4 mb-8">
          准备好释放你的创造力了吗？让AI引导你，一步步构建出独一无二的故事世界。
        </p>
        <button
          @click="startConversation"
          :disabled="novelStore.isLoading"
          class="bg-indigo-500 text-white font-bold py-3 px-8 rounded-full hover:bg-indigo-600 transition-all duration-300 transform hover:scale-105 shadow-lg focus:outline-none focus:ring-4 focus:ring-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ novelStore.isLoading ? '正在准备...' : '开启灵感模式' }}
        </button>
        <button
          @click="goBack"
          class="mt-4 block mx-auto text-gray-500 hover:text-gray-800 transition-colors"
        >
          返回
        </button>
      </div>

      <!-- 灵感模式交互界面 -->
      <div
        v-else-if="!showBlueprintConfirmation && !showBlueprint"
        class="h-[90vh] max-h-[950px] flex flex-col bg-white rounded-2xl shadow-2xl overflow-hidden fade-in"
      >
        <!-- 头部 -->
        <div class="p-4 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-2">
              <span class="relative flex h-3 w-3">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-indigo-500"></span>
              </span>
              <span class="text-sm font-medium text-indigo-600">与“文思”对话中...</span>
            </div>
            <div class="flex items-center gap-4">
              <span v-if="currentTurn > 0" class="text-sm font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-md">
                第 {{ currentTurn }} 轮
              </span>
              <button
                @click="handleRestart"
                title="重新开始"
                class="text-gray-400 hover:text-indigo-600 transition-colors"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
                </svg>
              </button>
              <button
                @click="exitConversation"
                title="返回首页"
                class="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 聊天区域 -->
        <div class="flex-1 p-6 overflow-y-auto space-y-6 relative" ref="chatArea">
          <transition name="fade">
            <InspirationLoading v-if="isInitialLoading" />
          </transition>
          <ChatBubble
            v-for="(message, index) in chatMessages"
            :key="index"
            :message="message.content"
            :type="message.type"
          />
        </div>

        <!-- 输入区域 -->
        <div class="p-4 border-t border-gray-200 bg-gray-50">
          <ConversationInput
            :ui-control="currentUIControl"
            :loading="novelStore.isLoading"
            @submit="handleUserInput"
          />
        </div>
      </div>

      <!-- 蓝图确认界面 -->
      <BlueprintConfirmation
        v-if="showBlueprintConfirmation"
        :ai-message="confirmationMessage"
        @blueprint-generated="handleBlueprintGenerated"
        @back="backToConversation"
      />

      <!-- 大纲展示界面 -->
      <BlueprintDisplay
        v-if="showBlueprint"
        :blueprint="completedBlueprint"
        :ai-message="blueprintMessage"
        @confirm="handleConfirmBlueprint"
        @regenerate="handleRegenerateBlueprint"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useNovelStore } from '@/stores/novel'
import type { UIControl, Blueprint } from '@/api/novel'
import ChatBubble from '@/components/ChatBubble.vue'
import ConversationInput from '@/components/ConversationInput.vue'
import BlueprintConfirmation from '@/components/BlueprintConfirmation.vue'
import BlueprintDisplay from '@/components/BlueprintDisplay.vue'
import InspirationLoading from '@/components/InspirationLoading.vue'
import { globalAlert } from '@/composables/useAlert'

interface ChatMessage {
  content: string
  type: 'user' | 'ai'
}

const router = useRouter()
const route = useRoute()
const novelStore = useNovelStore()

const conversationStarted = ref(false)
const isInitialLoading = ref(false)
const showBlueprintConfirmation = ref(false)
const showBlueprint = ref(false)
const chatMessages = ref<ChatMessage[]>([])
const currentUIControl = ref<UIControl | null>(null)
const currentTurn = ref(0)
const completedBlueprint = ref<Blueprint | null>(null)
const confirmationMessage = ref('')
const blueprintMessage = ref('')
const chatArea = ref<HTMLElement>()

const goBack = () => {
  router.push('/')
}

// 清空所有状态，开始新的灵感对话
const resetInspirationMode = () => {
  conversationStarted.value = false
  isInitialLoading.value = false
  showBlueprintConfirmation.value = false
  showBlueprint.value = false
  chatMessages.value = []
  currentUIControl.value = null
  currentTurn.value = 0
  completedBlueprint.value = null
  confirmationMessage.value = ''
  blueprintMessage.value = ''
  
  // 清空 store 中的当前项目和对话状态
  novelStore.setCurrentProject(null)
  novelStore.currentConversationState = {}
}

const exitConversation = async () => {
  const confirmed = await globalAlert.showConfirm('确定要退出灵感模式吗？当前进度可能会丢失。', '退出确认')
  if (confirmed) {
    resetInspirationMode()
    router.push('/')
  }
}

const handleRestart = async () => {
  const confirmed = await globalAlert.showConfirm('确定要重新开始吗？当前对话内容将会丢失。', '重新开始确认')
  if (confirmed) {
    await startConversation()
  }
}

const backToConversation = () => {
  showBlueprintConfirmation.value = false
}

const startConversation = async () => {
  // 重置所有状态，开始全新的对话
  resetInspirationMode()
  conversationStarted.value = true
  isInitialLoading.value = true
  
  try {
    await novelStore.createProject('未命名灵感', '开始灵感模式')
    
    // 发起第一次对话
    await handleUserInput(null)
  } catch (error) {
    console.error('启动灵感模式失败:', error)
    globalAlert.showError(`无法开始灵感模式: ${error instanceof Error ? error.message : '未知错误'}`, '启动失败')
    resetInspirationMode() // 失败时重置回初始状态
  }
}

const restoreConversation = async (projectId: string) => {
  try {
    await novelStore.loadProject(projectId)
    const project = novelStore.currentProject
    if (project && project.conversation_history) {
      conversationStarted.value = true
      chatMessages.value = project.conversation_history.map((item): ChatMessage | null => {
        if (item.role === 'user') {
          try {
            const userInput = JSON.parse(item.content)
            return { content: userInput.value, type: 'user' }
          } catch {
            return { content: item.content, type: 'user' }
          }
        } else { // assistant
          try {
            const assistantOutput = JSON.parse(item.content)
            return { content: assistantOutput.ai_message, type: 'ai' }
          } catch {
            return { content: item.content, type: 'ai' }
          }
        }
      }).filter((msg): msg is ChatMessage => msg !== null && msg.content !== null) // 过滤掉空的 user message

      const lastAssistantMsgStr = project.conversation_history.filter(m => m.role === 'assistant').pop()?.content
      if (lastAssistantMsgStr) {
        const lastAssistantMsg = JSON.parse(lastAssistantMsgStr)
        
        if (lastAssistantMsg.is_complete) {
          // 如果对话已完成，直接显示蓝图确认界面
          confirmationMessage.value = lastAssistantMsg.ai_message
          showBlueprintConfirmation.value = true
        } else {
          // 否则，恢复对话
          currentUIControl.value = lastAssistantMsg.ui_control
        }
      }
      // 计算当前轮次
      currentTurn.value = project.conversation_history.filter(m => m.role === 'assistant').length
      await scrollToBottom()
    }
  } catch (error) {
    console.error('恢复对话失败:', error)
    globalAlert.showError(`无法恢复对话: ${error instanceof Error ? error.message : '未知错误'}`, '加载失败')
    resetInspirationMode()
  }
}

const handleUserInput = async (userInput: any) => {
  try {
    // 如果有用户输入，添加到聊天记录
    if (userInput && userInput.value) {
      chatMessages.value.push({
        content: userInput.value,
        type: 'user'
      })
      await scrollToBottom()
    }

    const response = await novelStore.sendConversation(userInput)

    // 首次加载完成后，关闭加载动画
    if (isInitialLoading.value) {
      isInitialLoading.value = false
    }

    // 添加AI回复到聊天记录
    chatMessages.value.push({
      content: response.ai_message,
      type: 'ai'
    })
    currentTurn.value++

    await scrollToBottom()

    if (response.is_complete && response.ready_for_blueprint) {
      // 对话完成，显示蓝图确认界面
      confirmationMessage.value = response.ai_message
      showBlueprintConfirmation.value = true
    } else if (response.is_complete) {
      // 向后兼容：直接生成蓝图（如果后端还没更新）
      await handleGenerateBlueprint()
    } else {
      // 继续对话
      currentUIControl.value = response.ui_control
    }
  } catch (error) {
    console.error('对话失败:', error)
    // 确保在出错时也停止初始加载状态
    if (isInitialLoading.value) {
      isInitialLoading.value = false
    }
    globalAlert.showError(`抱歉，与AI连接时遇到问题: ${error instanceof Error ? error.message : '未知错误'}`, '通信失败')
    // 停止加载并返回初始界面
    resetInspirationMode()
  }
}

const handleGenerateBlueprint = async () => {
  try {
    const response = await novelStore.generateBlueprint()
    handleBlueprintGenerated(response)
  } catch (error) {
    console.error('生成蓝图失败:', error)
    globalAlert.showError(`生成蓝图失败: ${error instanceof Error ? error.message : '未知错误'}`, '生成失败')
  }
}

const handleBlueprintGenerated = (response: any) => {
  console.log('收到蓝图生成完成事件:', response)
  completedBlueprint.value = response.blueprint
  blueprintMessage.value = response.ai_message
  showBlueprintConfirmation.value = false
  showBlueprint.value = true
}

const handleRegenerateBlueprint = () => {
  showBlueprint.value = false
  showBlueprintConfirmation.value = true
}

const handleConfirmBlueprint = async () => {
  if (!completedBlueprint.value) {
    globalAlert.showError('蓝图数据缺失，请重新生成或稍后重试。', '保存失败')
    return
  }
  try {
    await novelStore.saveBlueprint(completedBlueprint.value)
    // 跳转到写作工作台
    if (novelStore.currentProject) {
      router.push(`/novel/${novelStore.currentProject.id}`)
    }
  } catch (error) {
    console.error('保存蓝图失败:', error)
    globalAlert.showError(`保存蓝图失败: ${error instanceof Error ? error.message : '未知错误'}`, '保存失败')
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatArea.value) {
    chatArea.value.scrollTop = chatArea.value.scrollHeight
  }
}

onMounted(() => {
  const projectId = route.query.project_id as string
  if (projectId) {
    restoreConversation(projectId)
  } else {
    // 每次进入灵感模式都重置状态，确保没有缓存
    resetInspirationMode()
  }
})
</script>
