<!-- AIMETA P=评审详情弹窗_章节评审展示|R=评审结果展示|NR=不含评审逻辑|E=component:WDEvaluationDetailModal|X=ui|A=评审弹窗|D=vue|S=dom|RD=./README.ai -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
    <div class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden flex flex-col">
      <!-- 弹窗头部 -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a6 6 0 00-6 6v3.586l-1.707 1.707A1 1 0 003 15v1a1 1 0 001 1h12a1 1 0 001-1v-1a1 1 0 00-.293-.707L16 11.586V8a6 6 0 00-6-6zM8.05 17a2 2 0 103.9 0H8.05z"></path>
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-900">AI 评审详情</h3>
        </div>
        <button
          @click="$emit('close')"
          class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
          </svg>
        </button>
      </div>

      <!-- 弹窗内容 -->
      <div class="p-6 overflow-y-auto max-h-[calc(80vh-130px)]">
        <div v-if="parsedEvaluation" class="space-y-6 text-sm">
            <div class="bg-purple-50 border border-purple-200 rounded-xl p-4">
              <p class="font-semibold text-purple-800 text-base">🏆 最佳选择：版本 {{ parsedEvaluation.best_choice }}</p>
              <p class="text-purple-700 mt-2">{{ parsedEvaluation.reason_for_choice }}</p>
            </div>
            <div class="space-y-4">
              <div v-for="(evalResult, versionName) in parsedEvaluation.evaluation" :key="versionName" class="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <h5 class="font-bold text-gray-800 text-lg mb-2">版本 {{ String(versionName).replace('version', '') }} 评估</h5>
                <div class="prose prose-sm max-w-none text-gray-700 space-y-3">
                  <div>
                    <p class="font-semibold text-gray-800">综合评价:</p>
                    <p>{{ evalResult.overall_review }}</p>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-800">优点:</p>
                    <ul class="list-disc pl-5 space-y-1">
                      <li v-for="(pro, i) in evalResult.pros" :key="`pro-${i}`">{{ pro }}</li>
                    </ul>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-800">缺点:</p>
                    <ul class="list-disc pl-5 space-y-1">
                      <li v-for="(con, i) in evalResult.cons" :key="`con-${i}`">{{ con }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div 
            v-else
            class="prose prose-sm max-w-none prose-headings:mt-2 prose-headings:mb-1 prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0 text-gray-800"
            v-html="parseMarkdown(evaluation)"
          ></div>
      </div>

      <!-- 弹窗底部操作按钮 -->
      <div class="flex items-center justify-end p-6 border-t border-gray-200 bg-gray-50">
        <button
            @click="$emit('close')"
            class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
        >
            关闭
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  evaluation: string | null
}

const props = defineProps<Props>()

defineEmits(['close'])

const parsedEvaluation = computed(() => {
  if (!props.evaluation) return null
  try {
    // First, try to parse the whole string as JSON
    let data = JSON.parse(props.evaluation);
    // If successful and it's a string, parse it again (for double-encoded JSON)
    if (typeof data === 'string') {
      data = JSON.parse(data);
    }
    return data;
  } catch (error) {
    console.error('Failed to parse evaluation JSON:', error)
    return null
  }
})

const parseMarkdown = (text: string | null): string => {
  if (!text) return ''
  let parsed = text
    .replace(/\\n/g, '\n')
    .replace(/\\"/g, '"')
    .replace(/\\'/g, "'")
    .replace(/\\\\/g, '\\')
  parsed = parsed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  parsed = parsed.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>')
  parsed = parsed.replace(/^([A-Z])\)\s*\*\*(.*?)\*\*(.*)/gm, '<div class="mb-2"><span class="inline-flex items-center justify-center w-6 h-6 bg-indigo-100 text-indigo-600 text-sm font-bold rounded-full mr-2">$1</span><strong>$2</strong>$3</div>')
  parsed = parsed.replace(/\n/g, '<br>')
  parsed = parsed.replace(/(<br\s*\/?>\s*){2,}/g, '</p><p class="mt-2">')
  if (!parsed.includes('<p>')) {
    parsed = `<p>${parsed}</p>`
  }
  return parsed
}
</script>
