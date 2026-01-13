<!-- AIMETA P=根组件_应用根节点|R=全局布局_RouterView|NR=不含页面逻辑|E=component:App|X=ui|A=RouterView|D=vue-router|S=dom|RD=./README.ai -->
<script setup lang="ts">
import { RouterView } from 'vue-router'
import { NMessageProvider } from 'naive-ui'
import CustomAlert from '@/components/CustomAlert.vue'
import { globalAlert } from '@/composables/useAlert'
</script>

<template>
  <n-message-provider>
    <div>
      <RouterView />

      <!-- 全局提示框 -->
      <CustomAlert
        v-for="alert in globalAlert.alerts.value"
        :key="alert.id"
        :visible="alert.visible"
        :type="alert.type"
        :title="alert.title"
        :message="alert.message"
        :show-cancel="alert.showCancel"
        :confirm-text="alert.confirmText"
        :cancel-text="alert.cancelText"
        @confirm="globalAlert.closeAlert(alert.id, true)"
        @cancel="globalAlert.closeAlert(alert.id, false)"
        @close="globalAlert.closeAlert(alert.id, false)"
      />
    </div>
  </n-message-provider>
</template>

<style scoped>
</style>
