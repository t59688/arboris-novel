<!-- AIMETA P=用户管理_用户列表管理|R=用户CRUD_权限|NR=不含认证功能|E=component:UserManagement|X=ui|A=用户组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-card :bordered="false" class="admin-card">
    <template #header>
      <div class="card-header">
        <span class="card-title">用户管理</span>
        <n-space :size="12">
          <n-input
            v-model:value="keyword"
            clearable
            round
            placeholder="搜索用户名或邮箱"
            @update:value="handleSearch"
            class="search-input"
          />
          <n-button type="primary" size="small" @click="handleAdd">
            新建用户
          </n-button>
          <n-button quaternary size="small" @click="fetchUsers" :loading="loading">
            刷新
          </n-button>
        </n-space>
      </div>
    </template>

    <n-space vertical size="large">
      <n-alert v-if="error" type="error" closable @close="error = null">
        {{ error }}
      </n-alert>

      <n-spin :show="loading">
        <n-data-table
          :columns="columns"
          :data="filteredUsers"
          :bordered="false"
          :pagination="pagination"
          :row-key="rowKey"
          class="user-table"
        />
      </n-spin>
    </n-space>

    <!-- Create/Edit User Modal -->
    <n-modal v-model:show="showModal" preset="card" :title="modalTitle" style="width: 500px">
      <n-form
        ref="formRef"
        :model="formModel"
        :rules="rules"
        label-placement="left"
        label-width="80"
        require-mark-placement="right-hanging"
      >
        <n-form-item label="用户名" path="username">
          <n-input
            v-model:value="formModel.username"
            placeholder="请输入用户名"
            :input-props="{ autocomplete: 'off' }"
          />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input
            v-model:value="formModel.email"
            placeholder="请输入邮箱（可选）"
            :input-props="{ autocomplete: 'off' }"
          />
        </n-form-item>
        <n-form-item
          label="密码"
          path="password"
          :rule="isEditMode ? [{ min: 6, message: '密码至少 6 个字符', trigger: 'blur' }] : passwordRules"
        >
          <n-input
            v-model:value="formModel.password"
            type="password"
            show-password-on="click"
            :placeholder="isEditMode ? '不修改请留空' : '请输入密码'"
            :input-props="{ autocomplete: 'new-password' }"
          />
        </n-form-item>
        <n-form-item label="权限" path="is_admin">
          <n-switch v-model:value="formModel.is_admin" :disabled="!isEditMode">
            <template #checked>管理员</template>
            <template #unchecked>普通用户</template>
          </n-switch>
        </n-form-item>
        <n-form-item label="状态" path="is_active">
          <n-switch v-model:value="formModel.is_active">
            <template #checked>激活</template>
            <template #unchecked>禁用</template>
          </n-switch>
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showModal = false">取消</n-button>
          <n-button type="primary" :loading="submitting" @click="handleSubmit">
            确认
          </n-button>
        </n-space>
      </template>
    </n-modal>
  </n-card>
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
  NModal,
  NPopconfirm,
  NSpin,
  NSwitch,
  NTag,
  NSpace,
  useMessage,
  type DataTableColumns,
  type FormInst,
  type FormRules,
  type FormItemRule
} from 'naive-ui'

import { AdminAPI, type AdminUser, type UserCreatePayload } from '@/api/admin'

const message = useMessage()
const users = ref<AdminUser[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const keyword = ref('')

const showModal = ref(false)
const submitting = ref(false)
const isEditMode = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInst | null>(null)

const formModel = reactive({
  username: '',
  email: '',
  password: '',
  is_admin: false,
  is_active: true
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, message: '用户名至少 2 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const passwordRules: FormItemRule[] = [
  { required: true, message: '请输入密码', trigger: 'blur' },
  { min: 6, message: '密码至少 6 个字符', trigger: 'blur' }
]

const pagination = reactive({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
})

const columns: DataTableColumns<AdminUser> = [
  {
    title: 'ID',
    key: 'id',
    sorter: (a, b) => a.id - b.id,
    width: 80
  },
  {
    title: '用户名',
    key: 'username',
    ellipsis: { tooltip: true }
  },
  {
    title: '邮箱',
    key: 'email',
    ellipsis: { tooltip: true },
    render(row) {
      return row.email || '—'
    }
  },
  {
    title: '权限',
    key: 'is_admin',
    align: 'center',
    render(row) {
      return h(
        NTag,
        {
          type: row.is_admin ? 'success' : 'default',
          bordered: false,
          size: 'small'
        },
        { default: () => (row.is_admin ? '管理员' : '普通用户') }
      )
    }
  },
  {
    title: '状态',
    key: 'is_active',
    align: 'center',
    render(row) {
      return h(
        NTag,
        {
          type: row.is_active ? 'success' : 'error',
          bordered: false,
          size: 'small'
        },
        { default: () => (row.is_active ? '激活' : '禁用') }
      )
    }
  },
  {
    title: '操作',
    key: 'actions',
    align: 'center',
    render(row) {
      return h(NSpace, { justify: 'center', size: 'small' }, {
        default: () => [
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              secondary: true,
              onClick: () => handleEdit(row)
            },
            { default: () => '编辑' }
          ),
          h(
            NPopconfirm,
            {
              onPositiveClick: () => handleDelete(row.id)
            },
            {
              trigger: () => h(
                NButton,
                {
                  size: 'small',
                  type: 'error',
                  secondary: true,
                  disabled: row.is_admin
                },
                { default: () => '删除' }
              ),
              default: () => '确定要删除该用户吗？'
            }
          )
        ]
      })
    }
  }
]

const filteredUsers = computed(() => {
  if (!keyword.value.trim()) {
    return users.value
  }
  const q = keyword.value.trim().toLowerCase()
  return users.value.filter(
    (user) =>
      user.username.toLowerCase().includes(q) ||
      (user.email && user.email.toLowerCase().includes(q))
  )
})

const modalTitle = computed(() => isEditMode.value ? '编辑用户' : '新建用户')

const rowKey = (row: AdminUser) => row.id

const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    users.value = await AdminAPI.listUsers()
  } catch (err) {
    error.value = err instanceof Error ? err.message : '获取用户数据失败'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
}

const handleAdd = () => {
  isEditMode.value = false
  editingId.value = null
  // 清空表单数据
  formModel.username = ''
  formModel.email = ''
  formModel.password = ''
  formModel.is_admin = false
  formModel.is_active = true
  
  showModal.value = true
}

const handleEdit = (row: AdminUser) => {
  isEditMode.value = true
  editingId.value = row.id
  formModel.username = row.username
  formModel.email = row.email || ''
  formModel.password = '' // 密码留空表示不修改
  formModel.is_admin = row.is_admin
  formModel.is_active = row.is_active
  showModal.value = true
}

const handleDelete = async (id: number) => {
  try {
    await AdminAPI.deleteUser(id)
    message.success('删除成功')
    await fetchUsers()
  } catch (err) {
    message.error(err instanceof Error ? err.message : '删除失败')
  }
}

const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (errors) return

    submitting.value = true
    try {
      if (isEditMode.value && editingId.value) {
        const payload: any = {
          username: formModel.username,
          is_admin: formModel.is_admin,
          is_active: formModel.is_active
        }
        if (formModel.email) payload.email = formModel.email
        if (formModel.password) payload.password = formModel.password
        
        await AdminAPI.updateUser(editingId.value, payload)
        message.success('更新成功')
      } else {
        const payload: UserCreatePayload = {
          username: formModel.username,
          password: formModel.password,
          is_admin: formModel.is_admin,
          is_active: formModel.is_active
        }
        if (formModel.email) payload.email = formModel.email
        
        await AdminAPI.createUser(payload)
        message.success('创建成功')
      }
      showModal.value = false
      await fetchUsers()
    } catch (err) {
      message.error(err instanceof Error ? err.message : '操作失败')
    } finally {
      submitting.value = false
    }
  })
}

onMounted(fetchUsers)
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

.search-input {
  width: min(230px, 60vw);
}

@media (max-width: 767px) {
  .card-header {
    flex-direction: column;
    align-items: stretch;
  }

  .card-title {
    font-size: 1.125rem;
  }

  .search-input {
    width: 100%;
  }
}
</style>
