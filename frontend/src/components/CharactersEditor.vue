<!-- AIMETA P=角色编辑器_角色信息编辑|R=角色CRUD|NR=不含关系编辑|E=component:CharactersEditor|X=internal|A=编辑器|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="space-y-4 max-h-96 overflow-y-auto p-1">
    <div v-for="(character, index) in localCharacters" :key="index" class="p-4 border border-gray-200 rounded-lg bg-gray-50 relative">
      <button @click="removeCharacter(index)" class="absolute top-2 right-2 text-red-400 hover:text-red-600 transition-colors p-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm4 0a1 1 0 012 0v6a1 1 0 11-2 0V8z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">姓名</label>
          <input type="text" v-model="character.name" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">身份</label>
          <input type="text" v-model="character.identity" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">性格</label>
          <input type="text" v-model="character.personality" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">目标</label>
          <input type="text" v-model="character.goals" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">能力</label>
          <input type="text" v-model="character.abilities" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">与主角关系</label>
          <input type="text" v-model="character.relationship_to_protagonist" class="w-full p-1 border-b-2 border-gray-300 focus:border-indigo-500 outline-none transition bg-transparent" />
        </div>
      </div>
    </div>
    <button @click="addCharacter" class="w-full mt-4 px-4 py-2 text-sm font-medium text-indigo-600 bg-indigo-50 border border-indigo-200 rounded-md hover:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
      + 添加新角色
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, nextTick } from 'vue';

interface Character {
  name: string;
  identity: string;
  personality: string;
  goals: string;
  abilities: string;
  relationship_to_protagonist: string;
}

const props = defineProps({
  modelValue: {
    type: Array as () => Character[],
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue']);

const localCharacters = ref<Character[]>([]);
let syncing = false;

watch(() => props.modelValue, (newVal) => {
  syncing = true;
  localCharacters.value = JSON.parse(JSON.stringify(newVal || []));
  nextTick(() => {
    syncing = false;
  });
}, { immediate: true });

watch(localCharacters, (newVal) => {
  if (syncing) return;
  emit('update:modelValue', JSON.parse(JSON.stringify(newVal)));
}, { deep: true });

const addCharacter = () => {
  localCharacters.value.push({ 
    name: '', 
    identity: '', 
    personality: '', 
    goals: '', 
    abilities: '', 
    relationship_to_protagonist: '' 
  });
};

const removeCharacter = (index: number) => {
  localCharacters.value.splice(index, 1);
};
</script>
