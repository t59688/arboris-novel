<!-- AIMETA P=生成大纲弹窗_大纲生成界面|R=大纲生成表单|NR=不含生成逻辑|E=component:WDGenerateOutlineModal|X=ui|A=生成弹窗|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <TransitionRoot as="template" :show="show">
    <Dialog as="div" class="relative z-50" @close="$emit('close')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-6 sm:w-full sm:max-w-lg">
              <div class="bg-white px-5 pt-6 pb-5 sm:px-6 sm:pt-6 sm:pb-5">
                <div class="flex flex-col gap-4 sm:flex-row sm:items-start">
                  <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-indigo-100 sm:mx-0 sm:h-12 sm:w-12">
                    <svg class="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
                    </svg>
                  </div>
                  <div class="text-center sm:flex-1 sm:text-left">
                    <DialogTitle as="h3" class="text-xl font-semibold leading-7 text-gray-900">生成后续大纲</DialogTitle>
                    <div class="mt-2">
                      <p class="text-base text-gray-500">请输入或选择要生成的后续章节数量。</p>
                    </div>
                  </div>
                </div>
                <div class="mt-6">
                  <label for="numChapters" class="block text-base font-medium text-gray-700">生成数量</label>
                  <input type="number" name="numChapters" id="numChapters" v-model.number="numChapters" class="mt-2 block w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-lg shadow-sm focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500" min="1" max="20">
                  <div class="mt-5 flex flex-wrap justify-center gap-3">
                    <button v-for="count in [1, 2, 5, 10]" :key="count" @click="setNumChapters(count)"
                      :class="['px-5 py-2 text-base rounded-full transition-colors duration-150', numChapters === count ? 'bg-indigo-600 text-white shadow-md' : 'bg-gray-200 text-gray-700 hover:bg-gray-300']">
                      {{ count }} 章
                    </button>
                  </div>
                </div>
              </div>
              <div class="bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse sm:px-8">
                <button type="button" class="inline-flex w-full justify-center rounded-lg border border-transparent bg-indigo-600 px-5 py-3 text-base font-semibold text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:ml-3 sm:w-auto" @click="handleGenerate">生成</button>
                <button type="button" class="mt-3 inline-flex w-full justify-center rounded-lg border border-gray-300 bg-white px-5 py-3 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:mt-0 sm:ml-3 sm:w-auto" @click="$emit('close')">取消</button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'

interface Props {
  show: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['close', 'generate'])

const numChapters = ref(5)

const setNumChapters = (count: number) => {
  numChapters.value = count
}

const handleGenerate = () => {
  if (numChapters.value > 0) {
    emit('generate', numChapters.value)
    emit('close')
  }
}
</script>
