// AIMETA P=管理员API客户端_管理接口调用|R=用户管理_系统配置_统计|NR=不含UI逻辑|E=api:admin|X=internal|A=adminApi对象|D=axios|S=net|RD=./README.ai
import { useAuthStore } from '@/stores/auth'
import router from '@/router'
import type { NovelSectionResponse, NovelSectionType } from '@/api/novel'

// API 配置
export const API_BASE_URL = import.meta.env.MODE === 'production' ? '' : 'http://127.0.0.1:8000'
export const ADMIN_API_PREFIX = '/api/admin'

// 统一请求封装
const request = async (url: string, options: RequestInit = {}) => {
  const authStore = useAuthStore()
  const headers = new Headers({
    'Content-Type': 'application/json',
    ...options.headers
  })

  if (authStore.isAuthenticated && authStore.token) {
    headers.set('Authorization', `Bearer ${authStore.token}`)
  }

  const response = await fetch(url, { ...options, headers })

  if (response.status === 401) {
    authStore.logout()
    router.push('/login')
    throw new Error('会话已过期，请重新登录')
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `请求失败，状态码: ${response.status}`)
  }

  if (response.status === 204) {
    return
  }

  return response.json()
}

const adminRequest = (path: string, options: RequestInit = {}) =>
  request(`${API_BASE_URL}${ADMIN_API_PREFIX}${path}`, options)

// 类型定义
export interface Statistics {
  novel_count: number
  user_count: number
  api_request_count: number
}

export interface AdminUser {
  id: number
  username: string
  email?: string | null
  is_admin: boolean
  is_active: boolean
}

export interface UserCreatePayload {
  username: string
  email?: string
  password: string
  is_admin?: boolean
  is_active?: boolean
}

export interface UserUpdatePayload {
  username?: string
  email?: string
  password?: string
  is_admin?: boolean
  is_active?: boolean
}

export interface NovelProjectSummary {
  id: string
  title: string
  genre: string
  last_edited: string
  completed_chapters: number
  total_chapters: number
}

export interface AdminNovelSummary extends NovelProjectSummary {
  owner_id: number
  owner_username: string
}

export interface Chapter {
  chapter_number: number
  title: string
  summary: string
  content?: string | null
  status?: string
  version_id?: string | number | null
  versions?: any[]
  word_count?: number
}

export interface NovelProject {
  id: string
  user_id: number
  title: string
  initial_prompt: string
  conversation_history: any[]
  blueprint?: any
  chapters: Chapter[]
}

export interface PromptItem {
  id: number
  name: string
  title?: string | null
  content: string
  tags?: string[] | null
}

export interface PromptCreatePayload {
  name: string
  content: string
  title?: string
  tags?: string[]
}

export type PromptUpdatePayload = Partial<Omit<PromptCreatePayload, 'name'>>

export interface UpdateLog {
  id: number
  content: string
  created_at: string
  created_by?: string | null
  is_pinned: boolean
}

export interface UpdateLogPayload {
  content?: string
  is_pinned?: boolean
}

export interface DailyRequestLimit {
  limit: number
}

export interface SystemConfig {
  key: string
  value: string
  description?: string | null
}

export interface SystemConfigUpsertPayload {
  value: string
  description?: string | null
}

export type SystemConfigUpdatePayload = Partial<SystemConfigUpsertPayload>

export class AdminAPI {
  private static request(path: string, options: RequestInit = {}) {
    return adminRequest(path, options)
  }

  // Overview
  static getStatistics(): Promise<Statistics> {
    return this.request('/stats')
  }

  // Users
  static listUsers(): Promise<AdminUser[]> {
    return this.request('/users')
  }

  static createUser(payload: UserCreatePayload): Promise<AdminUser> {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  }

  static getUser(id: number): Promise<AdminUser> {
    return this.request(`/users/${id}`)
  }

  static updateUser(id: number, payload: UserUpdatePayload): Promise<AdminUser> {
    return this.request(`/users/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
  }

  static deleteUser(id: number): Promise<void> {
    return this.request(`/users/${id}`, {
      method: 'DELETE'
    })
  }

  // Novels
  static listNovels(): Promise<AdminNovelSummary[]> {
    return this.request('/novel-projects')
  }

  static getNovelDetails(projectId: string): Promise<NovelProject> {
    return this.request(`/novel-projects/${projectId}`)
  }

  static getNovelSection(projectId: string, section: NovelSectionType): Promise<NovelSectionResponse> {
    return this.request(`/novel-projects/${projectId}/sections/${section}`)
  }

  static getNovelChapter(projectId: string, chapterNumber: number): Promise<Chapter> {
    return this.request(`/novel-projects/${projectId}/chapters/${chapterNumber}`)
  }

  // Prompts
  static listPrompts(): Promise<PromptItem[]> {
    return this.request('/prompts')
  }

  static createPrompt(payload: PromptCreatePayload): Promise<PromptItem> {
    return this.request('/prompts', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  }

  static getPrompt(id: number): Promise<PromptItem> {
    return this.request(`/prompts/${id}`)
  }

  static updatePrompt(id: number, payload: PromptUpdatePayload): Promise<PromptItem> {
    return this.request(`/prompts/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
  }

  static deletePrompt(id: number): Promise<void> {
    return this.request(`/prompts/${id}`, {
      method: 'DELETE'
    })
  }

  // Update logs
  static listUpdateLogs(): Promise<UpdateLog[]> {
    return this.request('/update-logs')
  }

  static createUpdateLog(payload: UpdateLogPayload & { content: string }): Promise<UpdateLog> {
    return this.request('/update-logs', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  }

  static updateUpdateLog(id: number, payload: UpdateLogPayload): Promise<UpdateLog> {
    return this.request(`/update-logs/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
  }

  static deleteUpdateLog(id: number): Promise<void> {
    return this.request(`/update-logs/${id}`, {
      method: 'DELETE'
    })
  }

  // Settings
  static getDailyRequestLimit(): Promise<DailyRequestLimit> {
    return this.request('/settings/daily-request-limit')
  }

  static setDailyRequestLimit(limit: number): Promise<DailyRequestLimit> {
    return this.request('/settings/daily-request-limit', {
      method: 'PUT',
      body: JSON.stringify({ limit })
    })
  }

  static listSystemConfigs(): Promise<SystemConfig[]> {
    return this.request('/system-configs')
  }

  static upsertSystemConfig(key: string, payload: SystemConfigUpsertPayload): Promise<SystemConfig> {
    return this.request(`/system-configs/${key}`, {
      method: 'PUT',
      body: JSON.stringify({ key, ...payload })
    })
  }

  static patchSystemConfig(key: string, payload: SystemConfigUpdatePayload): Promise<SystemConfig> {
    return this.request(`/system-configs/${key}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
  }

  static deleteSystemConfig(key: string): Promise<void> {
    return this.request(`/system-configs/${key}`, {
      method: 'DELETE'
    })
  }

  static changePassword(oldPassword: string, newPassword: string): Promise<void> {
    return this.request('/password', {
      method: 'POST',
      body: JSON.stringify({
        old_password: oldPassword,
        new_password: newPassword
      })
    })
  }
}
