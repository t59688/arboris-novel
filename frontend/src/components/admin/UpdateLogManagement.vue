<!-- AIMETA P=更新日志管理_系统更新记录|R=日志CRUD|NR=不含系统更新|E=component:UpdateLogManagement|X=ui|A=日志组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-card :bordered="false" class="admin-card">
    <template #header>
      <div class="card-header">
        <span class="card-title">更新日志管理</span>
        <n-button quaternary size="small" @click="fetchLogs" :loading="loading">
          刷新
        </n-button>
      </div>
    </template>

    <n-space vertical size="large">
      <n-alert v-if="error" type="error" closable @close="error = null">
        {{ error }}
      </n-alert>

      <n-card size="small" class="form-card">
        <n-form :model="form" label-placement="top">
          <n-form-item label="更新内容">
            <n-input
              v-model:value="form.content"
              type="textarea"
              :autosize="{ minRows: 3, maxRows: 10 }"
              placeholder="输入新的更新日志..."
            />
          </n-form-item>
          <n-form-item label="置顶">
            <n-switch v-model:value="form.isPinned" />
          </n-form-item>
          <n-space justify="end">
            <n-button type="primary" :loading="submitting" @click="addLog" :disabled="!form.content.trim()">
              发布日志
            </n-button>
          </n-space>
        </n-form>
      </n-card>

      <n-spin :show="loading">
        <n-empty v-if="!logs.length && !loading" description="目前还没有更新记录" />
        <n-space v-else vertical size="large">
          <n-card
            v-for="log in orderedLogs"
            :key="log.id"
            :bordered="false"
            size="small"
            class="log-card"
          >
            <div class="log-header">
              <n-space align="center" size="small">
                <n-tag v-if="log.is_pinned" type="warning" :bordered="false">置顶</n-tag>
                <span class="log-date">{{ formatDate(log.created_at) }}</span>
                <span v-if="log.created_by" class="log-author">by {{ log.created_by }}</span>
              </n-space>
              <n-space size="small">
                <n-switch
                  :value="log.is_pinned"
                  size="small"
                  :loading="togglingId === log.id"
                  @update:value="(value) => togglePin(log, value)"
                >
                  <template #checked>置顶</template>
                  <template #unchecked>置顶</template>
                </n-switch>
                <n-popconfirm
                  placement="left"
                  positive-text="删除"
                  negative-text="取消"
                  type="error"
                  @positive-click="() => deleteLog(log.id)"
                >
                  <template #trigger>
                    <n-button quaternary type="error" size="small" :loading="deletingId === log.id">
                      删除
                    </n-button>
                  </template>
                  确认删除该更新日志？
                </n-popconfirm>
              </n-space>
            </div>
            <div class="log-content">
              {{ log.content }}
            </div>
          </n-card>
        </n-space>
      </n-spin>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import {
  NAlert,
  NButton,
  NCard,
  NEmpty,
  NForm,
  NFormItem,
  NInput,
  NPopconfirm,
  NSpace,
  NSpin,
  NSwitch,
  NTag
} from 'naive-ui'

import { AdminAPI, type UpdateLog } from '@/api/admin'
import { useAlert } from '@/composables/useAlert'

const { showAlert } = useAlert()

const logs = ref<UpdateLog[]>([])
const loading = ref(false)
const submitting = ref(false)
const deletingId = ref<number | null>(null)
const togglingId = ref<number | null>(null)
const error = ref<string | null>(null)

const form = ref({
  content: '',
  isPinned: false
})

const orderedLogs = computed(() => {
  return [...logs.value].sort((a, b) => {
    if (a.is_pinned && !b.is_pinned) return -1
    if (!a.is_pinned && b.is_pinned) return 1
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  })
})

const fetchLogs = async () => {
  loading.value = true
  error.value = null
  try {
    logs.value = await AdminAPI.listUpdateLogs()
  } catch (err) {
    error.value = err instanceof Error ? err.message : '获取更新日志失败'
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value.content = ''
  form.value.isPinned = false
}

const addLog = async () => {
  if (!form.value.content.trim()) return
  submitting.value = true
  try {
    const created = await AdminAPI.createUpdateLog({
      content: form.value.content.trim(),
      is_pinned: form.value.isPinned
    })
    logs.value.unshift(created)
    resetForm()
    showAlert('更新日志发布成功', 'success')
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '发布失败', 'error')
  } finally {
    submitting.value = false
  }
}

const deleteLog = async (id: number) => {
  deletingId.value = id
  try {
    await AdminAPI.deleteUpdateLog(id)
    logs.value = logs.value.filter((item) => item.id !== id)
    showAlert('删除成功', 'success')
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '删除失败', 'error')
  } finally {
    deletingId.value = null
  }
}

const togglePin = async (log: UpdateLog, value: boolean) => {
  togglingId.value = log.id
  try {
    const updated = await AdminAPI.updateUpdateLog(log.id, { is_pinned: value })
    const index = logs.value.findIndex((item) => item.id === log.id)
    if (index !== -1) {
      logs.value.splice(index, 1, updated)
    }
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '更新失败', 'error')
  } finally {
    togglingId.value = null
  }
}

const formatDate = (date: string) => {
  try {
    const d = new Date(date)
    if (isNaN(d.getTime())) return date
    
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const hours = String(d.getHours()).padStart(2, '0')
    const minutes = String(d.getMinutes()).padStart(2, '0')
    
    return `${year}年${month}月${day}日 ${hours}:${minutes}`
  } catch (error) {
    return date
  }
}

onMounted(fetchLogs)
</script>

<style scoped>
.admin-card {
  width: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.form-card {
  border-radius: 16px;
}

.log-card {
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(15, 118, 110, 0.06), rgba(15, 118, 110, 0));
}

.log-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 10px;
}

.log-date {
  font-size: 0.85rem;
  color: #4b5563;
}

.log-author {
  font-size: 0.85rem;
  color: #6b7280;
}

.log-content {
  font-size: 0.95rem;
  color: #1f2937;
  line-height: 1.6;
  white-space: pre-wrap;
}

@media (max-width: 767px) {
  .card-title {
    font-size: 1.125rem;
  }
}
</style>
