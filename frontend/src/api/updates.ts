// AIMETA P=更新API客户端_更新日志接口|R=更新日志查询|NR=不含UI逻辑|E=api:updates|X=internal|A=updatesApi对象|D=axios|S=net|RD=./README.ai
// Using a relative path to avoid potential alias issues
import { API_BASE_URL } from './admin';

// A simplified request function for public endpoints that don't require authentication.
const publicRequest = async (url: string, options: RequestInit = {}) => {
  const response = await fetch(url, { ...options });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed, status code: ${response.status}`);
  }

  // For DELETE requests which might not have a body
  if (response.status === 204) {
    return;
  }

  return response.json();
};

export interface UpdateLog {
  id: number;
  content: string;
  created_at: string;
}

export const getLatestUpdates = (): Promise<UpdateLog[]> => {
  return publicRequest(`${API_BASE_URL}/api/updates/latest`);
};
