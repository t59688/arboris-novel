<!-- AIMETA P=统计面板_系统使用统计|R=统计图表|NR=不含数据修改|E=component:Statistics|X=ui|A=统计组件|D=vue,chart.js|S=dom,net|RD=./README.ai -->
<template>
  <n-card :bordered="false" class="admin-card">
    <template #header>
      <div class="card-header">
        <span class="card-title">数据总览</span>
        <n-button quaternary size="small" @click="fetchStats" :loading="loading">
          刷新
        </n-button>
      </div>
    </template>

    <n-space vertical size="large">
      <n-alert v-if="error" type="error" closable @close="error = null">
        {{ error }}
      </n-alert>

      <n-spin :show="loading">
        <n-grid :cols="gridCols" :x-gap="16" :y-gap="16">
          <n-gi>
            <n-card class="stat-card" :bordered="false">
              <div class="stat-icon">📚</div>
              <n-statistic label="小说总数" :value="stats?.novel_count ?? 0" show-separator>
                <template #suffix>部</template>
              </n-statistic>
            </n-card>
          </n-gi>
          <n-gi>
            <n-card class="stat-card" :bordered="false">
              <div class="stat-icon">👥</div>
              <n-statistic label="用户总数" :value="stats?.user_count ?? 0" show-separator>
                <template #suffix>人</template>
              </n-statistic>
            </n-card>
          </n-gi>
          <n-gi>
            <n-card class="stat-card" :bordered="false">
              <div class="stat-icon">⚡</div>
              <n-statistic label="API 请求总数" :value="stats?.api_request_count ?? 0" show-separator>
                <template #suffix>次</template>
              </n-statistic>
            </n-card>
          </n-gi>
        </n-grid>
      </n-spin>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import {
  NAlert,
  NButton,
  NCard,
  NGi,
  NGrid,
  NSpin,
  NStatistic,
  NSpace
} from 'naive-ui'

import { AdminAPI, type Statistics } from '@/api/admin'

const stats = ref<Statistics | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const isMobile = ref(false)

const updateLayout = () => {
  isMobile.value = window.innerWidth < 768
}

const gridCols = computed(() => (isMobile.value ? 1 : 3))

const fetchStats = async () => {
  loading.value = true
  error.value = null
  try {
    stats.value = await AdminAPI.getStatistics()
  } catch (err) {
    error.value = err instanceof Error ? err.message : '获取统计数据失败'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  updateLayout()
  window.addEventListener('resize', updateLayout)
  fetchStats()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayout)
})
</script>

<style scoped>
.admin-card {
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

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.08), rgba(79, 70, 229, 0));
}

.stat-icon {
  font-size: 28px;
  line-height: 1;
}

@media (max-width: 767px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .card-title {
    font-size: 1.125rem;
  }

  .stat-card {
    padding: 16px;
  }
}
</style>
