<template>
  <div class="h-screen flex flex-col overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/40">
    <!-- Header -->
    <header class="sticky top-0 z-40 bg-white/90 backdrop-blur-lg border-b border-slate-200/60 shadow-sm">
      <div class="max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <!-- Left: Title & Info -->
          <div class="flex items-center gap-3 flex-1 min-w-0">
            <button
              class="lg:hidden flex-shrink-0 p-2 text-slate-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-all duration-200"
              @click="toggleSidebar"
              aria-label="Toggle sidebar"
            >
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div class="flex-1 min-w-0">
              <h1 class="text-xl sm:text-2xl lg:text-3xl font-bold text-slate-900 truncate">
                {{ formattedTitle }}
              </h1>
              <p v-if="overviewMeta.updated_at" class="text-xs sm:text-sm text-slate-500 mt-0.5">
                最近更新：{{ overviewMeta.updated_at }}
              </p>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <button
              class="px-3 py-2 sm:px-4 text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg transition-all duration-200 hover:shadow-md"
              @click="goBack"
            >
              <span class="hidden sm:inline">返回列表</span>
              <span class="sm:hidden">返回</span>
            </button>
            <button
              v-if="!isAdmin"
              class="px-3 py-2 sm:px-4 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
              @click="goToWritingDesk"
            >
              <span class="hidden sm:inline">开始创作</span>
              <span class="sm:hidden">创作</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex max-w-[1800px] mx-auto w-full flex-1 min-h-0 overflow-hidden">
      <!-- Sidebar -->
      <aside
        class="fixed left-0 top-[73px] bottom-0 z-30 w-72 bg-white/95 backdrop-blur-lg border-r border-slate-200/60 shadow-2xl transform transition-transform duration-300 ease-out lg:translate-x-0"
        :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
      >
        <!-- Sidebar Header -->
        <div class="hidden lg:flex items-center justify-between px-6 py-5 border-b border-slate-200/60">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500"></div>
            <span class="text-sm font-semibold text-slate-700 uppercase tracking-wide">
              {{ isAdmin ? '内容视图' : '蓝图导航' }}
            </span>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="px-4 py-6 space-y-1.5 overflow-y-auto h-[calc(100%-5rem)] lg:h-[calc(100%-5rem)]">
          <button
            v-for="section in sections"
            :key="section.key"
            type="button"
            @click="switchSection(section.key)"
            :class="[
              'w-full group flex items-center gap-3 rounded-xl px-4 py-3.5 text-sm font-medium transition-all duration-200',
              activeSection === section.key
                ? 'bg-gradient-to-r from-indigo-50 to-indigo-100/80 text-indigo-700 shadow-sm ring-1 ring-indigo-200/50'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            ]"
          >
            <span
              class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg transition-all duration-200"
              :class="activeSection === section.key
                ? 'bg-gradient-to-br from-indigo-500 to-indigo-600 text-white shadow-md'
                : 'bg-slate-100 text-slate-500 group-hover:bg-slate-200'"
            >
              <component :is="getSectionIcon(section.key)" class="w-5 h-5" />
            </span>
            <span class="text-left flex-1">
              <span class="block font-semibold">{{ section.label }}</span>
              <span class="text-xs font-normal opacity-70">{{ section.description }}</span>
            </span>
          </button>
        </nav>
      </aside>

      <!-- Sidebar Overlay (Mobile) -->
      <transition
        enter-active-class="transition-opacity duration-300"
        leave-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isSidebarOpen"
          class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-20 lg:hidden"
          @click="toggleSidebar"
        ></div>
      </transition>

      <!-- Main Content Area -->
      <div class="flex-1 lg:ml-72 min-h-0 flex flex-col h-full">
        <div class="flex-1 min-h-0 h-full px-4 sm:px-6 lg:px-8 xl:px-12 py-6 sm:py-8 flex flex-col overflow-hidden box-border">
          <div class="flex-1 flex flex-col min-h-0 h-full">
            <!-- Content Card -->
            <div class="flex-1 h-full bg-white/95 backdrop-blur-sm rounded-2xl border border-slate-200/60 shadow-xl p-6 sm:p-8 lg:p-10 min-h-[20rem] transition-shadow duration-300 hover:shadow-2xl flex flex-col box-border" :class="contentCardClass">
              <!-- Loading State -->
              <div v-if="isSectionLoading" class="flex flex-col items-center justify-center py-20 sm:py-28">
                <div class="relative">
                  <div class="w-12 h-12 border-4 border-indigo-100 rounded-full"></div>
                  <div class="absolute top-0 left-0 w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <p class="mt-4 text-sm text-slate-500">加载中...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="currentError" class="flex flex-col items-center justify-center py-20 sm:py-28 space-y-4">
                <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center">
                  <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p class="text-slate-600 text-center">{{ currentError }}</p>
                <button
                  class="px-6 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
                  @click="reloadSection(activeSection, true)"
                >
                  重试
                </button>
              </div>

              <!-- Content -->
              <component
                v-else
                :is="currentComponent"
                v-bind="componentProps"
                :class="componentContainerClass"
                @edit="handleSectionEdit"
                @add="startAddChapter"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Blueprint Edit Modal -->
    <BlueprintEditModal
      v-if="!isAdmin"
      :show="isModalOpen"
      :title="modalTitle"
      :content="modalContent"
      :field="modalField"
      @close="isModalOpen = false"
      @save="handleSave"
    />

    <!-- Add Chapter Modal -->
    <transition
      enter-active-class="transition-all duration-300"
      leave-active-class="transition-all duration-300"
      enter-from-class="opacity-0 scale-95"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="isAddChapterModalOpen && !isAdmin" class="fixed inset-0 z-50 flex items-center justify-center px-4">
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="cancelNewChapter"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl border border-slate-200 p-6 sm:p-8 w-full max-w-lg transform transition-all" @click.stop>
          <h3 class="text-xl font-bold text-slate-900 mb-6">新增章节大纲</h3>
          <div class="space-y-5">
            <div>
              <label for="new-chapter-title" class="block text-sm font-semibold text-slate-700 mb-2">
                章节标题
              </label>
              <input
                id="new-chapter-title"
                v-model="newChapterTitle"
                type="text"
                class="block w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200"
                placeholder="例如：意外的相遇"
              >
            </div>
            <div>
              <label for="new-chapter-summary" class="block text-sm font-semibold text-slate-700 mb-2">
                章节摘要
              </label>
              <textarea
                id="new-chapter-summary"
                v-model="newChapterSummary"
                rows="4"
                class="block w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all duration-200 resize-none"
                placeholder="简要描述本章发生的主要事件"
              ></textarea>
            </div>
          </div>
          <div class="mt-8 flex justify-end gap-3">
            <button
              type="button"
              class="px-5 py-2.5 text-sm font-medium text-slate-600 bg-white hover:bg-slate-50 border border-slate-200 rounded-lg transition-all duration-200"
              @click="cancelNewChapter"
            >
              取消
            </button>
            <button
              type="button"
              class="px-5 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
              @click="saveNewChapter"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNovelStore } from '@/stores/novel'
import { NovelAPI } from '@/api/novel'
import { AdminAPI } from '@/api/admin'
import type { NovelProject, NovelSectionResponse, NovelSectionType } from '@/api/novel'
import BlueprintEditModal from '@/components/BlueprintEditModal.vue'
import OverviewSection from '@/components/novel-detail/OverviewSection.vue'
import WorldSettingSection from '@/components/novel-detail/WorldSettingSection.vue'
import CharactersSection from '@/components/novel-detail/CharactersSection.vue'
import RelationshipsSection from '@/components/novel-detail/RelationshipsSection.vue'
import ChapterOutlineSection from '@/components/novel-detail/ChapterOutlineSection.vue'
import ChaptersSection from '@/components/novel-detail/ChaptersSection.vue'

interface Props {
  isAdmin?: boolean
}

type SectionKey = NovelSectionType

const props = withDefaults(defineProps<Props>(), {
  isAdmin: false
})

const route = useRoute()
const router = useRouter()
const novelStore = useNovelStore()

const projectId = route.params.id as string
const isSidebarOpen = ref(typeof window !== 'undefined' ? window.innerWidth >= 1024 : true)

const sections: Array<{ key: SectionKey; label: string; description: string }> = [
  { key: 'overview', label: '项目概览', description: '定位与整体梗概' },
  { key: 'world_setting', label: '世界设定', description: '规则、地点与阵营' },
  { key: 'characters', label: '主要角色', description: '人物性格与目标' },
  { key: 'relationships', label: '人物关系', description: '角色之间的联系' },
  { key: 'chapter_outline', label: '章节大纲', description: props.isAdmin ? '故事章节规划' : '故事结构规划' },
  { key: 'chapters', label: '章节内容', description: props.isAdmin ? '生成章节与正文' : '生成状态与摘要' }
]

const sectionComponents: Record<SectionKey, any> = {
  overview: OverviewSection,
  world_setting: WorldSettingSection,
  characters: CharactersSection,
  relationships: RelationshipsSection,
  chapter_outline: ChapterOutlineSection,
  chapters: ChaptersSection
}

// Section icons as functional components
const getSectionIcon = (key: SectionKey) => {
  const icons: Record<SectionKey, any> = {
    overview: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('rect', { x: 3, y: 3, width: 18, height: 18, rx: 2 }),
      h('line', { x1: 3, y1: 9, x2: 21, y2: 9 }),
      h('line', { x1: 9, y1: 21, x2: 9, y2: 9 })
    ]),
    world_setting: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('circle', { cx: 12, cy: 12, r: 10 }),
      h('path', { d: 'M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z' })
    ]),
    characters: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('path', { d: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2' }),
      h('circle', { cx: 9, cy: 7, r: 4 }),
      h('path', { d: 'M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75' })
    ]),
    relationships: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('path', { d: 'M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2' }),
      h('circle', { cx: 9, cy: 7, r: 4 }),
      h('path', { d: 'M22 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75' })
    ]),
    chapter_outline: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('line', { x1: 8, y1: 6, x2: 21, y2: 6 }),
      h('line', { x1: 8, y1: 12, x2: 21, y2: 12 }),
      h('line', { x1: 8, y1: 18, x2: 21, y2: 18 }),
      h('line', { x1: 3, y1: 6, x2: 3.01, y2: 6 }),
      h('line', { x1: 3, y1: 12, x2: 3.01, y2: 12 }),
      h('line', { x1: 3, y1: 18, x2: 3.01, y2: 18 })
    ]),
    chapters: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2 }, [
      h('path', { d: 'M4 19.5A2.5 2.5 0 016.5 17H20' }),
      h('path', { d: 'M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z' })
    ])
  }
  return icons[key]
}

const sectionData = reactive<Partial<Record<SectionKey, any>>>({})
const sectionLoading = reactive<Record<SectionKey, boolean>>({
  overview: false,
  world_setting: false,
  characters: false,
  relationships: false,
  chapter_outline: false,
  chapters: false
})
const sectionError = reactive<Record<SectionKey, string | null>>({
  overview: null,
  world_setting: null,
  characters: null,
  relationships: null,
  chapter_outline: null,
  chapters: null
})

const overviewMeta = reactive<{ title: string; updated_at: string | null }>({
  title: '加载中...',
  updated_at: null
})

const activeSection = ref<SectionKey>('overview')

// Modal state (user mode only)
const isModalOpen = ref(false)
const modalTitle = ref('')
const modalContent = ref<any>('')
const modalField = ref('')

// Add chapter modal state (user mode only)
const isAddChapterModalOpen = ref(false)
const newChapterTitle = ref('')
const newChapterSummary = ref('')
const originalBodyOverflow = ref('')

const novel = computed(() => !props.isAdmin ? novelStore.currentProject as NovelProject | null : null)

const formattedTitle = computed(() => {
  const title = overviewMeta.title || '加载中...'
  return title.startsWith('《') && title.endsWith('》') ? title : `《${title}》`
})

const componentContainerClass = computed(() => {
  const fillSections: SectionKey[] = ['chapters']
  return fillSections.includes(activeSection.value)
    ? 'flex-1 min-h-0 h-full flex flex-col overflow-hidden'
    : 'overflow-y-auto'
})

const contentCardClass = computed(() => {
  const fillSections: SectionKey[] = ['chapters']
  return fillSections.includes(activeSection.value)
    ? 'overflow-hidden'
    : 'overflow-visible'
})

// 懒加载完整项目（仅在需要编辑时）
const ensureProjectLoaded = async () => {
  if (props.isAdmin || !projectId) return
  if (novel.value) return // 已加载
  await novelStore.loadProject(projectId)
}

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const handleResize = () => {
  if (typeof window === 'undefined') return
  isSidebarOpen.value = window.innerWidth >= 1024
}

const loadSection = async (section: SectionKey, force = false) => {
  if (!projectId) return
  if (!force && sectionData[section]) {
    return
  }

  sectionLoading[section] = true
  sectionError[section] = null
  try {
    const response: NovelSectionResponse = props.isAdmin
      ? await AdminAPI.getNovelSection(projectId, section)
      : await NovelAPI.getSection(projectId, section)
    sectionData[section] = response.data
    if (section === 'overview') {
      overviewMeta.title = response.data?.title || overviewMeta.title
      overviewMeta.updated_at = response.data?.updated_at || null
    }
  } catch (error) {
    console.error('加载模块失败:', error)
    sectionError[section] = error instanceof Error ? error.message : '加载失败'
  } finally {
    sectionLoading[section] = false
  }
}

const reloadSection = (section: SectionKey, force = false) => {
  loadSection(section, force)
}

const switchSection = (section: SectionKey) => {
  activeSection.value = section
  if (typeof window !== 'undefined' && window.innerWidth < 1024) {
    isSidebarOpen.value = false
  }
  loadSection(section)
}

const goBack = () => router.push(props.isAdmin ? '/admin' : '/workspace')

const goToWritingDesk = async () => {
  await ensureProjectLoaded()
  const project = novel.value
  if (!project) return
  const path = project.title === '未命名灵感' ? `/inspiration?project_id=${project.id}` : `/novel/${project.id}`
  router.push(path)
}

const currentComponent = computed(() => sectionComponents[activeSection.value])
const isSectionLoading = computed(() => sectionLoading[activeSection.value])
const currentError = computed(() => sectionError[activeSection.value])

const componentProps = computed(() => {
  const data = sectionData[activeSection.value]
  const editable = !props.isAdmin

  switch (activeSection.value) {
    case 'overview':
      return { data: data || null, editable }
    case 'world_setting':
      return { data: data || null, editable }
    case 'characters':
      return { data: data || null, editable }
    case 'relationships':
      return { data: data || null, editable }
    case 'chapter_outline':
      return { outline: data?.chapter_outline || [], editable }
    case 'chapters':
      return { chapters: data?.chapters || [], isAdmin: props.isAdmin }
    default:
      return {}
  }
})

const handleSectionEdit = (payload: { field: string; title: string; value: any }) => {
  if (props.isAdmin) return
  modalField.value = payload.field
  modalTitle.value = payload.title
  modalContent.value = payload.value
  isModalOpen.value = true
}

const resolveSectionKey = (field: string): SectionKey => {
  if (field.startsWith('world_setting')) return 'world_setting'
  if (field.startsWith('characters')) return 'characters'
  if (field.startsWith('relationships')) return 'relationships'
  if (field.startsWith('chapter_outline')) return 'chapter_outline'
  return 'overview'
}

const handleSave = async (data: { field: string; content: any }) => {
  if (props.isAdmin) return
  await ensureProjectLoaded()
  const project = novel.value
  if (!project) return

  const { field, content } = data
  const payload: Record<string, any> = {}

  if (field.includes('.')) {
    const [parentField, childField] = field.split('.')
    payload[parentField] = {
      ...(project.blueprint?.[parentField as keyof typeof project.blueprint] as Record<string, any> | undefined),
      [childField]: content
    }
  } else {
    payload[field] = content
  }

  try {
    const updatedProject = await NovelAPI.updateBlueprint(project.id, payload)
    novelStore.setCurrentProject(updatedProject)
    const sectionToReload = resolveSectionKey(field)
    await loadSection(sectionToReload, true)
    if (sectionToReload !== 'overview') {
      await loadSection('overview', true)
    }
    isModalOpen.value = false
  } catch (error) {
    console.error('保存变更失败:', error)
  }
}

const startAddChapter = async () => {
  if (props.isAdmin) return
  await ensureProjectLoaded()
  const outline = sectionData.chapter_outline?.chapter_outline || novel.value?.blueprint?.chapter_outline || []
  const nextNumber = outline.length > 0 ? Math.max(...outline.map((item: any) => item.chapter_number)) + 1 : 1
  newChapterTitle.value = `新章节 ${nextNumber}`
  newChapterSummary.value = ''
  isAddChapterModalOpen.value = true
}

const cancelNewChapter = () => {
  isAddChapterModalOpen.value = false
}

const saveNewChapter = async () => {
  if (props.isAdmin) return
  await ensureProjectLoaded()
  const project = novel.value
  if (!project) return
  if (!newChapterTitle.value.trim()) {
    alert('章节标题不能为空')
    return
  }

  const existingOutline = project.blueprint?.chapter_outline || []
  const nextNumber = existingOutline.length > 0 ? Math.max(...existingOutline.map(ch => ch.chapter_number)) + 1 : 1
  const newOutline = [...existingOutline, {
    chapter_number: nextNumber,
    title: newChapterTitle.value,
    summary: newChapterSummary.value
  }]

  try {
    const updatedProject = await NovelAPI.updateBlueprint(project.id, { chapter_outline: newOutline })
    novelStore.setCurrentProject(updatedProject)
    await loadSection('chapter_outline', true)
    isAddChapterModalOpen.value = false
  } catch (error) {
    console.error('新增章节失败:', error)
  }
}

onMounted(async () => {
  if (typeof window !== 'undefined') {
    window.addEventListener('resize', handleResize)
  }
  if (typeof document !== 'undefined') {
    originalBodyOverflow.value = document.body.style.overflow
    document.body.style.overflow = 'hidden'
  }

  // 只加载必要的 section 数据，不预加载完整项目
  await loadSection('overview', true)
  loadSection('world_setting')
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
  }
  if (typeof document !== 'undefined') {
    document.body.style.overflow = originalBodyOverflow.value || ''
  }
})
</script>

<style scoped>
/* Smooth scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
