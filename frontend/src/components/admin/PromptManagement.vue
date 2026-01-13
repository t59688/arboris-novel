<!-- AIMETA P=提示词管理_AI提示模板管理|R=提示词CRUD|NR=不含模型调用|E=component:PromptManagement|X=ui|A=管理组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-card :bordered="false" class="admin-card">
    <template #header>
      <div class="card-header">
        <span class="card-title">提示词管理</span>
        <n-space :size="12">
          <n-button quaternary size="small" @click="fetchPrompts" :loading="loading">
            刷新
          </n-button>
          <n-button type="primary" size="small" @click="openCreateModal">
            新建 Prompt
          </n-button>
        </n-space>
      </div>
    </template>

    <n-space vertical size="large">
      <n-alert v-if="error" type="error" closable @close="error = null">
        {{ error }}
      </n-alert>

      <n-spin :show="loading">
        <div :class="['prompt-layout', { mobile: isMobile }]">
          <div class="prompt-sidebar">
            <n-scrollbar class="prompt-scroll">
              <n-empty v-if="!prompts.length && !loading" description="暂无提示词" />
              <n-space v-else vertical size="small">
                <n-button
                  v-for="prompt in prompts"
                  :key="prompt.id"
                  type="primary"
                  :ghost="selectedPrompt?.id !== prompt.id"
                  quaternary
                  block
                  @click="selectPrompt(prompt)"
                >
                  <div class="prompt-item">
                    <span class="prompt-name">{{ prompt.title || prompt.name }}</span>
                    <n-tag v-if="prompt.tags?.length" size="tiny" type="info">
                      {{ prompt.tags.length }}
                    </n-tag>
                  </div>
                </n-button>
              </n-space>
            </n-scrollbar>
          </div>

          <div class="prompt-editor">
            <div v-if="!selectedPrompt" class="empty-editor">
              <n-empty description="请选择一个提示词以编辑" />
            </div>
            <div v-else class="editor-content">
              <n-form label-placement="top" :model="editForm">
                <n-form-item label="唯一标识">
                  <n-input v-model:value="editForm.name" disabled />
                </n-form-item>
                <n-form-item label="标题">
                  <n-input
                    v-model:value="editForm.title"
                    placeholder="用于后台识别的标题，可为空"
                  />
                </n-form-item>
                <n-form-item label="标签">
                  <n-dynamic-tags
                    v-model:value="editForm.tags"
                    size="small"
                    placeholder="输入标签后回车"
                  />
                </n-form-item>
                <n-form-item label="提示词内容">
                  <n-input
                    v-model:value="editForm.content"
                    type="textarea"
                    :autosize="{ minRows: isMobile ? 8 : 16, maxRows: 40 }"
                    placeholder="请输入完整的提示词内容..."
                    class="prompt-textarea"
                  />
                </n-form-item>
              </n-form>
              <n-space justify="end">
                <n-popconfirm
                  v-if="selectedPrompt"
                  placement="bottom"
                  positive-text="删除"
                  negative-text="取消"
                  type="error"
                  @positive-click="deletePrompt"
                >
                  <template #trigger>
                    <n-button type="error" quaternary :loading="deleting">
                      删除
                    </n-button>
                  </template>
                  确认删除该 Prompt？
                </n-popconfirm>
                <n-button type="primary" :loading="saving" @click="savePrompt">
                  保存修改
                </n-button>
              </n-space>
            </div>
          </div>
        </div>
      </n-spin>
    </n-space>
  </n-card>

  <n-modal v-model:show="createModalVisible" preset="card" title="新建 Prompt" class="prompt-modal">
    <n-form label-placement="top" :model="createForm">
      <n-form-item label="唯一标识（必填）">
        <n-input v-model:value="createForm.name" placeholder="例如 concept / outline" />
      </n-form-item>
      <n-form-item label="标题">
        <n-input v-model:value="createForm.title" placeholder="可选，用于后台展示" />
      </n-form-item>
      <n-form-item label="标签">
        <n-dynamic-tags
          v-model:value="createForm.tags"
          size="small"
          placeholder="输入标签后回车"
        />
      </n-form-item>
      <n-form-item label="内容">
        <n-input
          v-model:value="createForm.content"
          type="textarea"
          :autosize="{ minRows: 10, maxRows: 30 }"
          placeholder="输入提示词内容..."
        />
      </n-form-item>
    </n-form>
    <template #footer>
      <n-space justify="end">
        <n-button quaternary @click="closeCreateModal">取消</n-button>
        <n-button type="primary" :loading="creating" @click="createPrompt">创建</n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import {
  NAlert,
  NButton,
  NCard,
  NDynamicTags,
  NEmpty,
  NForm,
  NFormItem,
  NInput,
  NModal,
  NPopconfirm,
  NScrollbar,
  NSpace,
  NSpin,
  NTag
} from 'naive-ui'

import { AdminAPI, type PromptCreatePayload, type PromptItem } from '@/api/admin'
import { useAlert } from '@/composables/useAlert'

const { showAlert } = useAlert()

const prompts = ref<PromptItem[]>([])
const selectedPrompt = ref<PromptItem | null>(null)
const loading = ref(false)
const saving = ref(false)
const deleting = ref(false)
const creating = ref(false)
const error = ref<string | null>(null)
const editForm = reactive({
  name: '',
  title: '',
  content: '',
  tags: [] as string[]
})

const createModalVisible = ref(false)
const createForm = reactive<PromptCreatePayload>({
  name: '',
  title: '',
  content: '',
  tags: []
})

const isMobile = ref(false)

const updateLayout = () => {
  isMobile.value = window.innerWidth < 920
}

const fetchPrompts = async () => {
  loading.value = true
  error.value = null
  try {
    prompts.value = await AdminAPI.listPrompts()
    if (selectedPrompt.value) {
      const refreshed = prompts.value.find((item) => item.id === selectedPrompt.value?.id)
      if (refreshed) {
        selectPrompt(refreshed)
      } else {
        resetSelection()
      }
    } else if (prompts.value.length) {
      selectPrompt(prompts.value[0])
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : '获取提示词列表失败'
  } finally {
    loading.value = false
  }
}

const resetSelection = () => {
  selectedPrompt.value = null
  editForm.name = ''
  editForm.title = ''
  editForm.content = ''
  editForm.tags = []
}

const selectPrompt = (prompt: PromptItem) => {
  selectedPrompt.value = prompt
  editForm.name = prompt.name
  editForm.title = prompt.title || ''
  editForm.content = prompt.content
  editForm.tags = prompt.tags ? [...prompt.tags] : []
}

const savePrompt = async () => {
  if (!selectedPrompt.value) return
  if (!editForm.content.trim()) {
    showAlert('提示词内容不能为空', 'error')
    return
  }
  saving.value = true
  try {
    const updated = await AdminAPI.updatePrompt(selectedPrompt.value.id, {
      title: editForm.title || undefined,
      content: editForm.content,
      tags: editForm.tags
    })
    selectPrompt(updated)
    const index = prompts.value.findIndex((item) => item.id === updated.id)
    if (index !== -1) {
      prompts.value.splice(index, 1, updated)
    }
    showAlert('保存成功', 'success')
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '保存失败', 'error')
  } finally {
    saving.value = false
  }
}

const deletePrompt = async () => {
  if (!selectedPrompt.value) return
  deleting.value = true
  try {
    await AdminAPI.deletePrompt(selectedPrompt.value.id)
    showAlert('删除成功', 'success')
    prompts.value = prompts.value.filter((item) => item.id !== selectedPrompt.value?.id)
    resetSelection()
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '删除失败', 'error')
  } finally {
    deleting.value = false
  }
}

const openCreateModal = () => {
  createModalVisible.value = true
}

const closeCreateModal = () => {
  createModalVisible.value = false
  createForm.name = ''
  createForm.title = ''
  createForm.content = ''
  createForm.tags = []
}

const createPrompt = async () => {
  if (!createForm.name.trim() || !createForm.content.trim()) {
    showAlert('名称与内容均为必填项', 'error')
    return
  }
  creating.value = true
  try {
    const created = await AdminAPI.createPrompt({
      name: createForm.name.trim(),
      title: createForm.title?.trim() || undefined,
      content: createForm.content,
      tags: createForm.tags?.length ? [...createForm.tags] : undefined
    })
    prompts.value.unshift(created)
    selectPrompt(created)
    showAlert('创建成功', 'success')
    closeCreateModal()
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '创建失败', 'error')
  } finally {
    creating.value = false
  }
}

onMounted(() => {
  updateLayout()
  window.addEventListener('resize', updateLayout)
  fetchPrompts()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayout)
})
</script>

<style scoped>
.admin-card {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.prompt-layout {
  display: flex;
  align-items: stretch;
  gap: 20px;
  min-height: 420px;
}

.prompt-layout.mobile {
  flex-direction: column;
}

.prompt-sidebar {
  width: 260px;
  flex-shrink: 0;
}

.prompt-layout.mobile .prompt-sidebar {
  width: 100%;
  max-height: 220px;
}

.prompt-scroll {
  max-height: 520px;
}

.prompt-layout.mobile .prompt-scroll {
  max-height: 200px;
}

.prompt-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  font-weight: 500;
}

.prompt-name {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-right: 8px;
}

.prompt-editor {
  flex: 1;
  min-width: 0;
}

.empty-editor {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
}

.editor-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.prompt-textarea :deep(textarea) {
  font-family: 'Fira Code', 'JetBrains Mono', 'SFMono-Regular', Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
  line-height: 1.5;
}

.prompt-modal {
  max-width: min(720px, 90vw);
}

@media (max-width: 1023px) {
  .prompt-sidebar {
    width: 220px;
  }
}

@media (max-width: 767px) {
  .card-title {
    font-size: 1.125rem;
  }
}
</style>
