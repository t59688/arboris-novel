<!-- AIMETA P=设置管理_系统设置界面|R=系统配置表单|NR=不含用户设置|E=component:SettingsManagement|X=ui|A=设置组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-space vertical size="large" class="admin-settings">
    <n-card :bordered="false">
      <template #header>
        <div class="card-header">
          <span class="card-title">每日请求额度</span>
          <n-button quaternary size="small" @click="fetchDailyLimit" :loading="dailyLimitLoading">
            刷新
          </n-button>
        </div>
      </template>
      <n-spin :show="dailyLimitLoading">
        <n-alert v-if="dailyLimitError" type="error" closable @close="dailyLimitError = null">
          {{ dailyLimitError }}
        </n-alert>
        <n-form label-placement="top" class="limit-form">
          <n-form-item label="未配置 API Key 的用户每日可用请求次数">
            <n-input-number
              v-model:value="dailyLimit"
              :min="0"
              :step="10"
              placeholder="请输入每日请求上限"
            />
          </n-form-item>
          <n-space justify="end">
            <n-button type="primary" :loading="dailyLimitSaving" @click="saveDailyLimit">
              保存设置
            </n-button>
          </n-space>
        </n-form>
      </n-spin>
    </n-card>

    <n-card :bordered="false">
      <template #header>
        <div class="card-header">
          <span class="card-title">系统配置</span>
          <n-button type="primary" size="small" @click="openCreateModal">
            新增配置
          </n-button>
        </div>
      </template>

      <n-spin :show="configLoading">
        <n-alert v-if="configError" type="error" closable @close="configError = null">
          {{ configError }}
        </n-alert>

        <n-data-table
          :columns="columns"
          :data="configs"
          :loading="configLoading"
          :bordered="false"
          :row-key="rowKey"
          class="config-table"
        />
      </n-spin>
    </n-card>
  </n-space>

  <n-modal
    v-model:show="configModalVisible"
    preset="card"
    :title="modalTitle"
    class="config-modal"
    :style="{ width: '520px', maxWidth: '92vw' }"
  >
    <n-form label-placement="top" :model="configForm">
      <n-form-item label="Key">
        <n-input
          v-model:value="configForm.key"
          :disabled="!isCreateMode"
          placeholder="请输入唯一 Key"
        />
      </n-form-item>
      <n-form-item label="值">
        <n-input v-model:value="configForm.value" placeholder="配置的具体值" />
      </n-form-item>
      <n-form-item label="描述">
        <n-input v-model:value="configForm.description" placeholder="配置项的用途说明，可选" />
      </n-form-item>
    </n-form>
    <template #footer>
      <n-space justify="end">
        <n-button quaternary @click="closeConfigModal">取消</n-button>
        <n-button type="primary" :loading="configSaving" @click="submitConfig">
          保存
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { computed, h, onMounted, reactive, ref } from 'vue'
import {
  NAlert,
  NButton,
  NCard,
  NDataTable,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NModal,
  NPopconfirm,
  NSpace,
  NSpin,
  type DataTableColumns
} from 'naive-ui'

import {
  AdminAPI,
  type DailyRequestLimit,
  type SystemConfig,
  type SystemConfigUpdatePayload,
  type SystemConfigUpsertPayload
} from '@/api/admin'
import { useAlert } from '@/composables/useAlert'

const { showAlert } = useAlert()

const dailyLimit = ref<number | null>(null)
const dailyLimitLoading = ref(false)
const dailyLimitSaving = ref(false)
const dailyLimitError = ref<string | null>(null)

const configs = ref<SystemConfig[]>([])
const configLoading = ref(false)
const configSaving = ref(false)
const configError = ref<string | null>(null)

const configModalVisible = ref(false)
const isCreateMode = ref(true)
const configForm = reactive<SystemConfig>({
  key: '',
  value: '',
  description: ''
})

const rowKey = (row: SystemConfig) => row.key

const modalTitle = computed(() => (isCreateMode.value ? '新增配置项' : '编辑配置项'))

const fetchDailyLimit = async () => {
  dailyLimitLoading.value = true
  dailyLimitError.value = null
  try {
    const result = await AdminAPI.getDailyRequestLimit()
    dailyLimit.value = result.limit
  } catch (err) {
    dailyLimitError.value = err instanceof Error ? err.message : '加载每日限制失败'
  } finally {
    dailyLimitLoading.value = false
  }
}

const saveDailyLimit = async () => {
  if (dailyLimit.value === null || dailyLimit.value < 0) {
    showAlert('请设置有效的每日额度', 'error')
    return
  }
  dailyLimitSaving.value = true
  try {
    await AdminAPI.setDailyRequestLimit(dailyLimit.value)
    showAlert('每日额度已更新', 'success')
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '保存失败', 'error')
  } finally {
    dailyLimitSaving.value = false
  }
}

const fetchConfigs = async () => {
  configLoading.value = true
  configError.value = null
  try {
    configs.value = await AdminAPI.listSystemConfigs()
  } catch (err) {
    configError.value = err instanceof Error ? err.message : '加载配置失败'
  } finally {
    configLoading.value = false
  }
}

const openCreateModal = () => {
  isCreateMode.value = true
  configForm.key = ''
  configForm.value = ''
  configForm.description = ''
  configModalVisible.value = true
}

const openEditModal = (config: SystemConfig) => {
  isCreateMode.value = false
  configForm.key = config.key
  configForm.value = config.value
  configForm.description = config.description || ''
  configModalVisible.value = true
}

const closeConfigModal = () => {
  configModalVisible.value = false
  configSaving.value = false
}

const submitConfig = async () => {
  if (!configForm.key.trim() || !configForm.value.trim()) {
    showAlert('Key 与 Value 均为必填项', 'error')
    return
  }
  configSaving.value = true
  try {
    let updated: SystemConfig
    if (isCreateMode.value) {
      updated = await AdminAPI.upsertSystemConfig(configForm.key.trim(), {
        value: configForm.value,
        description: configForm.description || undefined
      })
      configs.value.unshift(updated)
    } else {
      updated = await AdminAPI.patchSystemConfig(configForm.key, {
        value: configForm.value,
        description: configForm.description || undefined
      } as SystemConfigUpdatePayload)
      const index = configs.value.findIndex((item) => item.key === updated.key)
      if (index !== -1) {
        configs.value.splice(index, 1, updated)
      }
    }
    showAlert('配置已保存', 'success')
    closeConfigModal()
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '保存失败', 'error')
  } finally {
    configSaving.value = false
  }
}

const deleteConfig = async (key: string) => {
  try {
    await AdminAPI.deleteSystemConfig(key)
    configs.value = configs.value.filter((item) => item.key !== key)
    showAlert('配置已删除', 'success')
  } catch (err) {
    showAlert(err instanceof Error ? err.message : '删除失败', 'error')
  }
}

const columns: DataTableColumns<SystemConfig> = [
  {
    title: 'Key',
    key: 'key',
    width: 220,
    ellipsis: { tooltip: true }
  },
  {
    title: '值',
    key: 'value',
    ellipsis: { tooltip: true }
  },
  {
    title: '描述',
    key: 'description',
    ellipsis: { tooltip: true },
    render(row) {
      return row.description || '—'
    }
  },
  {
    title: '操作',
    key: 'actions',
    align: 'center',
    width: 160,
    render(row) {
      return h(
        NSpace,
        { justify: 'center', size: 'small' },
        {
          default: () => [
            h(
              NButton,
              {
                size: 'small',
                type: 'primary',
                tertiary: true,
                onClick: () => openEditModal(row)
              },
              { default: () => '编辑' }
            ),
            h(
              NPopconfirm,
              {
                'positive-text': '删除',
                'negative-text': '取消',
                type: 'error',
                placement: 'left',
                onPositiveClick: () => deleteConfig(row.key)
              },
              {
                default: () => '确认删除该配置项？',
                trigger: () =>
                  h(
                    NButton,
                    { size: 'small', type: 'error', quaternary: true },
                    { default: () => '删除' }
                  )
              }
            )
          ]
        }
      )
    }
  }
]

onMounted(() => {
  fetchDailyLimit()
  fetchConfigs()
})
</script>

<style scoped>
.admin-settings {
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

.limit-form {
  max-width: 360px;
}

.config-modal {
  max-width: min(640px, 92vw);
}

@media (max-width: 767px) {
  .card-title {
    font-size: 1.125rem;
  }
}
</style>
