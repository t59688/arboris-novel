// AIMETA P=LLM_API客户端_模型配置接口|R=LLM配置CRUD|NR=不含UI逻辑|E=api:llm|X=internal|A=llmApi对象|D=axios|S=net|RD=./README.ai
import { useAuthStore } from '@/stores/auth';

const API_PREFIX = '/api';
const LLM_BASE = `${API_PREFIX}/llm-config`;

export interface LLMConfig {
  user_id: number;
  llm_provider_url: string | null;
  llm_provider_api_key: string | null;
  llm_provider_model: string | null;
}

export interface LLMConfigCreate {
  llm_provider_url?: string;
  llm_provider_api_key?: string;
  llm_provider_model?: string;
}

const getHeaders = () => {
  const authStore = useAuthStore();
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authStore.token}`,
  };
};

export const getLLMConfig = async (): Promise<LLMConfig | null> => {
  const response = await fetch(LLM_BASE, {
    method: 'GET',
    headers: getHeaders(),
  });
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error('Failed to fetch LLM config');
  }
  return response.json();
};

export const createOrUpdateLLMConfig = async (config: LLMConfigCreate): Promise<LLMConfig> => {
  const response = await fetch(LLM_BASE, {
    method: 'PUT',
    headers: getHeaders(),
    body: JSON.stringify(config),
  });
  if (!response.ok) {
    throw new Error('Failed to save LLM config');
  }
  return response.json();
};

export const deleteLLMConfig = async (): Promise<void> => {
  const response = await fetch(LLM_BASE, {
    method: 'DELETE',
    headers: getHeaders(),
  });
  if (!response.ok) {
    throw new Error('Failed to delete LLM config');
  }
};
