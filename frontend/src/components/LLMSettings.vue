<!-- AIMETA P=LLM设置_模型配置界面|R=LLM配置表单|NR=不含模型调用|E=component:LLMSettings|X=internal|A=设置组件|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="bg-white/70 backdrop-blur-xl rounded-2xl shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">LLM 配置</h2>
    <h5 class="text-1xl font-bold text-gray-800 mb-6">建议使用自己的中转API和KEY</h5>
    <form @submit.prevent="handleSave" class="space-y-6">
      <div>
        <label for="url" class="block text-sm font-medium text-gray-700">API URL</label>
        <div class="relative mt-1">
          <input
            type="text"
            id="url"
            v-model="config.llm_provider_url"
            class="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="https://api.example.com/v1"
          >
          <button
            type="button"
            @click="clearApiUrl"
            class="absolute inset-y-0 right-2 flex items-center px-2 text-gray-400 hover:text-gray-600"
            aria-label="清空 API URL"
          >
            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      <div>
        <label for="key" class="block text-sm font-medium text-gray-700">API Key</label>
        <div class="relative mt-1">
          <input
            :type="showApiKey ? 'text' : 'password'"
            id="key"
            v-model="config.llm_provider_api_key"
            class="block w-full px-3 py-2 pr-24 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="留空则使用默认Key"
          >
          <button
            type="button"
            @click="clearApiKey"
            class="absolute inset-y-0 right-2 flex items-center px-2 text-gray-400 hover:text-gray-600"
            aria-label="清空 API Key"
          >
            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
          <button
            type="button"
            @click="toggleApiKeyVisibility"
            class="absolute inset-y-0 right-10 flex items-center px-2 text-gray-400 hover:text-gray-600"
            :aria-label="showApiKey ? '隐藏 API Key' : '显示 API Key'"
          >
            <svg v-if="showApiKey" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 5c-4.478 0-8.268 2.943-9.542 7C1.732 16.057 5.522 19 10 19s8.268-2.943 9.542-7C18.268 7.943 14.478 5 10 5zm0 10a5 5 0 110-10 5 5 0 010 10z" fill-opacity="0.2" />
              <path d="M10 7a3 3 0 100 6 3 3 0 000-6z" />
            </svg>
            <svg v-else class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zm13.707 0a4.167 4.167 0 11-8.334 0 4.167 4.167 0 018.334 0z" clip-rule="evenodd" />
              <path d="M10 8a2 2 0 100 4 2 2 0 000-4z" />
            </svg>
          </button>
        </div>
      </div>
      <div>
        <label for="model" class="block text-sm font-medium text-gray-700">Model</label>
        <div class="relative mt-1">
          <input
            type="text"
            id="model"
            v-model="config.llm_provider_model"
            class="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="留空则使用默认模型"
          >
          <button
            type="button"
            @click="clearApiModel"
            class="absolute inset-y-0 right-2 flex items-center px-2 text-gray-400 hover:text-gray-600"
            aria-label="清空模型名称"
          >
            <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      <div class="flex justify-end space-x-4 pt-4">
        <button type="button" @click="handleDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">删除配置</button>
        <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">保存</button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getLLMConfig, createOrUpdateLLMConfig, deleteLLMConfig, type LLMConfigCreate } from '@/api/llm';

const config = ref<LLMConfigCreate>({
  llm_provider_url: '',
  llm_provider_api_key: '',
  llm_provider_model: '',
});

const showApiKey = ref(false);

onMounted(async () => {
  const existingConfig = await getLLMConfig();
  if (existingConfig) {
    config.value = {
      llm_provider_url: existingConfig.llm_provider_url || '',
      llm_provider_api_key: existingConfig.llm_provider_api_key || '',
      llm_provider_model: existingConfig.llm_provider_model || '',
    };
  }
});

const handleSave = async () => {
  await createOrUpdateLLMConfig(config.value);
  alert('设置已保存！');
};

const handleDelete = async () => {
  if (confirm('确定要删除您的自定义LLM配置吗？删除后将恢复为默认配置。')) {
    await deleteLLMConfig();
    config.value = {
      llm_provider_url: '',
      llm_provider_api_key: '',
      llm_provider_model: '',
    };
    alert('配置已删除！');
  }
};

const toggleApiKeyVisibility = () => {
  showApiKey.value = !showApiKey.value;
};

const clearApiKey = () => {
  config.value.llm_provider_api_key = '';
};

const clearApiUrl = () => {
  config.value.llm_provider_url = '';
};

const clearApiModel = () => {
  config.value.llm_provider_model = '';
};
</script>
