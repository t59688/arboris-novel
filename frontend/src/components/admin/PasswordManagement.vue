<!-- AIMETA P=密码管理_管理员密码修改|R=密码修改表单|NR=不含用户管理|E=component:PasswordManagement|X=ui|A=密码组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-space vertical size="large" class="password-container">
    <n-card :bordered="false" class="password-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">管理员密码修改</span>
        </div>
      </template>

      <n-alert v-if="mustReset" type="warning" class="mb-4">
        为保障安全，请先更新默认密码后再继续使用管理后台。
      </n-alert>

      <n-alert v-if="error" type="error" closable @close="error = null" class="mb-4">
        {{ error }}
      </n-alert>

      <n-spin :show="submitting">
        <n-form class="password-form" label-placement="top" @submit.prevent="handleSubmit">
          <n-form-item label="当前密码">
            <n-input
              v-model:value="form.oldPassword"
              type="password"
              show-password-on="click"
              placeholder="请输入当前管理员密码"
              autocomplete="current-password"
            />
          </n-form-item>

          <n-form-item label="新密码">
            <n-input
              v-model:value="form.newPassword"
              type="password"
              show-password-on="click"
              placeholder="请输入至少 8 位新密码"
              autocomplete="new-password"
            />
          </n-form-item>

          <n-form-item label="确认新密码">
            <n-input
              v-model:value="form.confirmPassword"
              type="password"
              show-password-on="click"
              placeholder="请再次输入新密码"
              autocomplete="new-password"
            />
          </n-form-item>

          <n-space justify="end">
            <n-button type="primary" :loading="submitting" @click="handleSubmit">
              保存新密码
            </n-button>
          </n-space>
        </n-form>
      </n-spin>
    </n-card>
  </n-space>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { NAlert, NButton, NCard, NForm, NFormItem, NInput, NSpace, NSpin } from 'naive-ui'

import { AdminAPI } from '@/api/admin'
import { useAlert } from '@/composables/useAlert'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { showAlert } = useAlert()

const form = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const submitting = ref(false)
const error = ref<string | null>(null)

const mustReset = computed(() => authStore.mustChangePassword && authStore.user?.is_admin)

const resetForm = () => {
  form.oldPassword = ''
  form.newPassword = ''
  form.confirmPassword = ''
}

const handleSubmit = async () => {
  error.value = null

  if (!form.oldPassword.trim() || !form.newPassword.trim()) {
    error.value = '请填写完整的密码信息'
    return
  }

  if (form.newPassword.length < 8) {
    error.value = '新密码长度需至少 8 位'
    return
  }

  if (form.newPassword === form.oldPassword) {
    error.value = '新密码不能与当前密码相同'
    return
  }

  if (form.newPassword !== form.confirmPassword) {
    error.value = '两次输入的新密码不一致'
    return
  }

  submitting.value = true
  try {
    await AdminAPI.changePassword(form.oldPassword, form.newPassword)
    await authStore.fetchUser()
    resetForm()
    await showAlert('密码已更新，请使用新密码继续操作', 'success')
  } catch (err) {
    error.value = err instanceof Error ? err.message : '密码更新失败'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.password-container {
  max-width: 520px;
  margin: 0 auto;
}

.password-card {
  border-radius: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1f2937;
}

.password-form {
  max-width: 420px;
}

.mb-4 {
  margin-bottom: 16px;
}
</style>
