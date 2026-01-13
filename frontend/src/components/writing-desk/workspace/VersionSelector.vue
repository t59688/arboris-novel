<!-- AIMETA P=版本选择器_章节版本切换|R=版本列表_切换|NR=不含版本管理|E=component:VersionSelector|X=internal|A=选择器|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="space-y-6">
    <!-- AI 评审提示 -->
    <div v-if="isEvaluationFailed" class="bg-red-50 border border-red-200 rounded-xl p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div>
            <h4 class="font-bold text-red-900">AI 评审失败</h4>
            <p class="text-sm text-red-700">AI 评审时遇到问题，请重试。</p>
          </div>
        </div>
        <button
          @click="$emit('evaluateChapter')"
          :disabled="evaluatingChapter === selectedChapter?.chapter_number"
          class="px-4 py-2 bg-red-600 text-white hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2 whitespace-nowrap"
        >
          <svg v-if="evaluatingChapter === selectedChapter?.chapter_number" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          {{ evaluatingChapter === selectedChapter?.chapter_number ? '重试中...' : '重新评审' }}
        </button>
      </div>
    </div>
    <div v-else-if="selectedChapter?.evaluation" class="bg-purple-50 border border-purple-200 rounded-xl p-4">
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 2a6 6 0 00-6 6v3.586l-1.707 1.707A1 1 0 003 15v1a1 1 0 001 1h12a1 1 0 001-1v-1a1 1 0 00-.293-.707L16 11.586V8a6 6 0 00-6-6zM8.05 17a2 2 0 103.9 0H8.05z"></path>
                    </svg>
                </div>
                <div>
                    <h4 class="font-bold text-purple-900">AI 评审已完成</h4>
                    <p class="text-sm text-purple-700">AI 已对所有版本进行评估，点击查看详细结果。</p>
                </div>
            </div>
            <button @click="$emit('showEvaluationDetail')" class="px-4 py-2 bg-purple-600 text-white hover:bg-purple-700 rounded-lg transition-colors flex items-center gap-2 whitespace-nowrap">
                查看 AI 评审
            </button>
        </div>
    </div>

    <!-- AI消息 (仅对新生成的内容显示) -->
    <div v-if="chapterGenerationResult?.ai_message" class="bg-blue-50 border border-blue-200 rounded-xl p-4">
      <div class="flex items-start gap-3">
        <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
          </svg>
        </div>
        <div class="flex-1">
          <div 
            class="prose prose-sm max-w-none prose-headings:mt-2 prose-headings:mb-1 prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0 text-blue-800"
            v-html="parseMarkdown(chapterGenerationResult.ai_message)"
          ></div>
        </div>
      </div>
    </div>

    <!-- 状态提示 -->
    <div v-if="selectedChapter?.content" class="bg-amber-50 border border-amber-200 rounded-xl p-4">
      <div class="flex items-center gap-2 text-amber-800">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <span class="font-medium">您可以查看所有版本并选择不同的版本</span>
      </div>
    </div>

    <div v-else class="bg-blue-50 border border-blue-200 rounded-xl p-4">
      <div class="flex items-center gap-2 text-blue-800">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
        </svg>
        <span class="font-medium">请选择一个版本来完成这个章节</span>
      </div>
    </div>

    <!-- 版本选择器 -->
    <div class="bg-gray-50 rounded-xl p-4">
      <div class="flex items-center justify-between mb-4">
        <h4 class="font-semibold text-gray-800">
          {{ availableVersions.length > 1 ? '选择版本' : '生成内容' }}
          <span class="text-sm font-normal text-gray-600 ml-2">({{ availableVersions.length }} 个版本)</span>
        </h4>
        <!-- <button
          @click="$emit('confirmVersionSelection')"
          :disabled="!availableVersions?.[selectedVersionIndex]?.content || isCurrentVersion(selectedVersionIndex) || isSelectingVersion"
          class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg v-if="isSelectingVersion" class="w-5 h-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          <span v-else>
            {{ isCurrentVersion(selectedVersionIndex) ? '当前版本' : '确认选择此版本' }}
          </span>
        </button> -->
      </div>

      <div class="grid gap-3">
        <div
          v-for="(version, index) in availableVersions"
          :key="index"
          @click="$emit('update:selectedVersionIndex', index)"
          :class="[
            'cursor-pointer border-2 rounded-lg p-4 transition-all duration-200',
            selectedVersionIndex === index
              ? 'border-indigo-300 bg-indigo-50 shadow-md'
              : isCurrentVersion(index)
              ? 'border-green-300 bg-green-50'
              : 'border-gray-200 hover:border-indigo-200 hover:bg-white'
          ]"
        >
          <div class="flex items-start gap-3">
            <div
              :class="[
                'w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0',
                selectedVersionIndex === index
                  ? 'bg-indigo-500 text-white'
                  : isCurrentVersion(index)
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-300 text-gray-600'
              ]"
            >
              <svg v-if="isCurrentVersion(index)" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div class="flex-1">
              <p class="text-sm text-gray-700 line-clamp-3">
                {{ cleanVersionContent(version.content).substring(0, 150) }}...
              </p>
              <div class="mt-2 flex items-center gap-2 text-xs text-gray-500">
                <span>约 {{ Math.round(cleanVersionContent(version.content).length / 100) * 100 }} 字</span>
                <span>•</span>
                <span>{{ version.style || '标准' }}风格</span>
                <span v-if="isCurrentVersion(index)" class="text-green-600 font-medium">• 当前选中</span>
              </div>
              <div class="mt-2">
                <button
                  @click.stop="$emit('showVersionDetail', index)"
                  class="text-xs text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1"
                >
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
                  </svg>
                  查看详情
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 flex justify-end items-center gap-4">
        <button
          @click="$emit('evaluateChapter')"
          :disabled="evaluatingChapter === selectedChapter?.chapter_number || availableVersions.length < 2"
          class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <svg v-if="evaluatingChapter === selectedChapter?.chapter_number" class="w-4 h-4 animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          {{ evaluatingChapter === selectedChapter?.chapter_number ? '评审中...' : 'AI 评审' }}
        </button>
        <button
          @click="$emit('confirmVersionSelection')"
          :disabled="!availableVersions?.[selectedVersionIndex]?.content || isCurrentVersion(selectedVersionIndex) || isSelectingVersion"
          class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          <svg v-if="isSelectingVersion" class="w-5 h-5 animate-spin" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"></path>
          </svg>
          <span v-else>
            {{ isCurrentVersion(selectedVersionIndex) ? '当前版本' : '确认选择此版本' }}
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Chapter, ChapterGenerationResponse, ChapterVersion } from '@/api/novel'

interface Props {
  selectedChapter: Chapter | null
  chapterGenerationResult: ChapterGenerationResponse | null
  availableVersions: ChapterVersion[]
  selectedVersionIndex: number
  evaluatingChapter: number | null
  isSelectingVersion?: boolean
  isEvaluationFailed?: boolean
}

const props = defineProps<Props>()

defineEmits(['hideVersionSelector', 'update:selectedVersionIndex', 'showVersionDetail', 'confirmVersionSelection', 'evaluateChapter', 'showEvaluationDetail'])


const isCurrentVersion = (versionIndex: number) => {
  if (!props.selectedChapter?.content || !props.availableVersions?.[versionIndex]?.content) return false
  const cleanCurrentContent = cleanVersionContent(props.selectedChapter.content)
  const cleanVersionContentStr = cleanVersionContent(props.availableVersions[versionIndex].content)
  return cleanCurrentContent === cleanVersionContentStr
}

const cleanVersionContent = (content: string): string => {
  if (!content) return ''
  try {
    const parsed = JSON.parse(content)
    if (parsed && typeof parsed === 'object' && parsed.content) {
      content = parsed.content
    }
  } catch (error) {
    // not a json
  }
  let cleaned = content.replace(/^"|"$/g, '')
  cleaned = cleaned.replace(/\\n/g, '\n')
  cleaned = cleaned.replace(/\\"/g, '"')
  cleaned = cleaned.replace(/\\t/g, '\t')
  cleaned = cleaned.replace(/\\\\/g, '\\')
  return cleaned
}

const parseMarkdown = (text: string): string => {
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
