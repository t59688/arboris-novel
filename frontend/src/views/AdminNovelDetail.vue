<!-- AIMETA P=管理员小说详情_管理员查看小说|R=小说详情_管理操作|NR=不含普通用户功能|E=route:/admin/novel/:id#component:AdminNovelDetail|X=ui|A=详情展示_管理|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <NovelDetailShell :is-admin="true" />
</template>

<script setup lang="ts">
import NovelDetailShell from '@/components/shared/NovelDetailShell.vue'
</script>
