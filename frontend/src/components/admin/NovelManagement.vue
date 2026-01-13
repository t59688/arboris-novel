<!-- AIMETA P=小说管理_管理员小说列表管理|R=小说列表_删除_统计|NR=不含普通用户功能|E=component:NovelManagement|X=ui|A=管理组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <n-card class="novel-management-card" size="large" :bordered="false">
    <template #header>
      <div class="card-header">
        <span class="card-title">小说管理</span>
        <n-tag size="small" type="primary" round>共 {{ novels.length }} 项</n-tag>
      </div>
    </template>

    <n-space vertical size="large">
      <n-alert v-if="error" type="error" closable @close="error = null">
        {{ error }}
      </n-alert>

      <n-spin :show="loading">
        <template #default>
          <n-empty
            v-if="!novels.length && !loading"
            description="暂无小说项目"
            class="empty-state"
          />
          <div v-else>
            <n-space v-if="isMobile" vertical size="large">
              <n-card
                v-for="novel in novels"
                :key="novel.id"
                size="small"
                embedded
                class="novel-card"
              >
                <template #header>
                  <div class="mobile-card-header">
                    <span class="mobile-card-title">{{ novel.title }}</span>
                    <n-tag size="small" type="info" round>{{ novel.genre || '未分类' }}</n-tag>
                  </div>
                </template>
                <div class="mobile-meta">
                  <span class="mobile-label">编号</span>
                  <span class="mobile-value">{{ novel.id }}</span>
                </div>
                <div class="mobile-meta">
                  <span class="mobile-label">创作者</span>
                  <span class="mobile-value">{{ novel.owner_username }}</span>
                </div>
                <div class="mobile-meta">
                  <span class="mobile-label">进度</span>
                  <span class="mobile-value">{{ formatProgress(novel) }}</span>
                </div>
                <div class="mobile-meta">
                  <span class="mobile-label">最近更新</span>
                  <span class="mobile-value">{{ formatDate(novel.last_edited) }}</span>
                </div>
                <template #footer>
                  <n-button type="primary" size="small" block @click="viewDetails(novel.id)">
                    查看详情
                  </n-button>
                </template>
              </n-card>
            </n-space>
            <n-data-table
              v-else
              :columns="columns"
              :data="novels"
              :pagination="pagination"
              :bordered="false"
              size="small"
              class="novel-table"
            />
          </div>
        </template>
      </n-spin>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { h, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  NAlert,
  NButton,
  NCard,
  NDataTable,
  NEmpty,
  NSpin,
  NTag,
  NSpace,
  type DataTableColumns
} from 'naive-ui'

import { AdminAPI } from '@/api/admin'
import type { AdminNovelSummary } from '@/api/admin'

const novels = ref<AdminNovelSummary[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const isMobile = ref(false)
const router = useRouter()

const pagination = {
  pageSize: 8,
  showSizePicker: false
}

const updateLayout = () => {
  isMobile.value = window.innerWidth < 768
}

const formatDate = (value: string | null | undefined) => {
  if (!value) return '未记录'
  try {
    const date = new Date(value)
    if (isNaN(date.getTime())) return '未记录'
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${year}年${month}月${day}日 ${hours}:${minutes}`
  } catch (error) {
    return '未记录'
  }
}

const formatProgress = (novel: Pick<AdminNovelSummary, 'completed_chapters' | 'total_chapters'>) => {
  const total = novel.total_chapters || 0
  const completed = novel.completed_chapters || 0
  return `${completed} / ${total}`
}

const viewDetails = (novelId: string) => {
  router.push(`/admin/novel/${novelId}`)
}

const columns: DataTableColumns<AdminNovelSummary> = [
  {
    title: '项目',
    key: 'title',
    ellipsis: { tooltip: true },
    render(row) {
      return h('div', { class: 'table-title-cell' }, [
        h('div', { class: 'table-title' }, row.title),
        h('div', { class: 'table-subtitle' }, row.id)
      ])
    }
  },
  {
    title: '类型',
    key: 'genre',
    render(row) {
      return h(
        NTag,
        { type: 'info', size: 'small', round: true, bordered: false },
        { default: () => row.genre || '未分类' }
      )
    }
  },
  {
    title: '创作者',
    key: 'owner_username',
    render(row) {
      return h('span', { class: 'table-owner' }, row.owner_username)
    }
  },
  {
    title: '进度',
    key: 'progress',
    render(row) {
      return h('span', { class: 'table-progress' }, formatProgress(row))
    }
  },
  {
    title: '最近更新',
    key: 'last_edited',
    render(row) {
      return h('span', { class: 'table-date' }, formatDate(row.last_edited))
    }
  },
  {
    title: '操作',
    key: 'actions',
    align: 'center',
    render(row) {
      return h(
        NButton,
        {
          size: 'small',
          type: 'primary',
          tertiary: true,
          onClick: () => viewDetails(row.id)
        },
        { default: () => '详情' }
      )
    }
  }
]

const fetchNovels = async () => {
  loading.value = true
  error.value = null
  try {
    novels.value = await AdminAPI.listNovels()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '获取小说数据失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  updateLayout()
  window.addEventListener('resize', updateLayout)
  fetchNovels()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayout)
})
</script>

<style scoped>
.novel-management-card {
  width: 100%;
  box-sizing: border-box;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.novel-table {
  width: 100%;
}

.table-title-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.table-title {
  font-weight: 600;
  color: #111827;
}

.table-subtitle {
  font-size: 0.75rem;
  color: #6b7280;
  word-break: break-all;
}

.table-owner,
.table-progress,
.table-date {
  color: #374151;
}

.novel-card {
  border-radius: 16px;
}

.mobile-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.mobile-card-title {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.mobile-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  font-size: 0.875rem;
  color: #4b5563;
  word-break: break-word;
}

.mobile-label {
  color: #6b7280;
}

.mobile-value {
  color: #111827;
  font-weight: 500;
  text-align: right;
  margin-left: 12px;
}

.empty-state {
  padding: 48px 0;
}

@media (max-width: 767px) {
  .card-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .card-title {
    font-size: 1.125rem;
  }
}
</style>
