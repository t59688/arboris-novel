<!-- AIMETA P=小说详情_小说信息展示|R=详情展示_分析|NR=不含编辑功能|E=route:/detail/:id#component:NovelDetail|X=ui|A=详情页|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <NovelDetailShell :is-admin="false" />
</template>

<script setup lang="ts">
import NovelDetailShell from '@/components/shared/NovelDetailShell.vue'
</script>
