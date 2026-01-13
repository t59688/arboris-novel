<!-- AIMETA P=蓝图卡片_小说蓝图展示|R=蓝图信息展示|NR=不含编辑功能|E=component:BlueprintCard|X=internal|A=卡片组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">小说蓝图</h3>

    <div v-if="!blueprint" class="text-gray-500 text-center py-8">
      暂无蓝图信息
    </div>

    <div v-else class="space-y-4">
      <!-- 基本信息 -->
      <div class="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span class="font-medium text-gray-600">类型：</span>
          <span class="text-gray-800">{{ blueprint.genre || '未指定' }}</span>
        </div>
        <div>
          <span class="font-medium text-gray-600">风格：</span>
          <span class="text-gray-800">{{ blueprint.style || '未指定' }}</span>
        </div>
        <div>
          <span class="font-medium text-gray-600">基调：</span>
          <span class="text-gray-800">{{ blueprint.tone || '未指定' }}</span>
        </div>
        <div>
          <span class="font-medium text-gray-600">目标读者：</span>
          <span class="text-gray-800">{{ blueprint.target_audience || '未指定' }}</span>
        </div>
      </div>

      <!-- 一句话总结 -->
      <div v-if="blueprint.one_sentence_summary">
        <h4 class="font-medium text-gray-600 mb-2">一句话总结</h4>
        <p class="text-gray-800 text-sm">{{ blueprint.one_sentence_summary }}</p>
      </div>

      <!-- 主要角色 -->
      <div v-if="blueprint.characters && blueprint.characters.length > 0">
        <h4 class="font-medium text-gray-600 mb-2">主要角色</h4>
        <div class="space-y-2">
          <div
            v-for="character in blueprint.characters"
            :key="character.name"
            class="text-sm"
          >
            <span class="font-medium text-gray-800">{{ character.name }}:</span>
            <span class="text-gray-600 ml-1">{{ character.description }}</span>
          </div>
        </div>
      </div>

      <!-- 展开按钮 -->
      <button
        @click="showDetails = !showDetails"
        class="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
      >
        {{ showDetails ? '收起详情' : '查看详情' }}
      </button>

      <!-- 详细信息 -->
      <div v-if="showDetails" class="space-y-4 pt-4 border-t">
        <div v-if="blueprint.full_synopsis">
          <h4 class="font-medium text-gray-600 mb-2">完整简介</h4>
          <p class="text-gray-800 text-sm leading-relaxed">{{ blueprint.full_synopsis }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Blueprint } from '@/api/novel'

interface Props {
  blueprint: Blueprint | undefined
}

defineProps<Props>()

const showDetails = ref(false)
</script>