// AIMETA P=日期工具_日期格式化函数|R=日期格式化_相对时间|NR=不含业务逻辑|E=formatDate|X=internal|A=formatDate函数|D=none|S=none|RD=./README.ai
/**
 * 日期时间格式化工具函数
 */

/**
 * 将 ISO 8601 格式的时间字符串转换为友好的中文格式
 * @param isoString ISO 8601 格式的时间字符串，如 "2026-01-11T09:42:54.539359"
 * @returns 格式化后的时间字符串，如 "2026年01月11日 09:42"
 */
export function formatDateTime(isoString: string | null | undefined): string {
  if (!isoString) return '-'
  
  try {
    const date = new Date(isoString)
    
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return isoString
    }
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    
    return `${year}年${month}月${day}日 ${hours}:${minutes}`
  } catch (error) {
    console.error('日期格式化错误:', error)
    return isoString
  }
}

/**
 * 将 ISO 8601 格式的时间字符串转换为仅日期的中文格式
 * @param isoString ISO 8601 格式的时间字符串
 * @returns 格式化后的日期字符串，如 "2026年01月11日"
 */
export function formatDate(isoString: string | null | undefined): string {
  if (!isoString) return '-'
  
  try {
    const date = new Date(isoString)
    
    if (isNaN(date.getTime())) {
      return isoString
    }
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    
    return `${year}年${month}月${day}日`
  } catch (error) {
    console.error('日期格式化错误:', error)
    return isoString
  }
}

/**
 * 将 ISO 8601 格式的时间字符串转换为相对时间描述
 * @param isoString ISO 8601 格式的时间字符串
 * @returns 相对时间描述，如 "刚刚"、"5分钟前"、"2小时前"、"3天前"
 */
export function formatRelativeTime(isoString: string | null | undefined): string {
  if (!isoString) return '-'
  
  try {
    const date = new Date(isoString)
    const now = new Date()
    
    if (isNaN(date.getTime())) {
      return isoString
    }
    
    const diffMs = now.getTime() - date.getTime()
    const diffSeconds = Math.floor(diffMs / 1000)
    const diffMinutes = Math.floor(diffSeconds / 60)
    const diffHours = Math.floor(diffMinutes / 60)
    const diffDays = Math.floor(diffHours / 24)
    
    if (diffSeconds < 60) {
      return '刚刚'
    } else if (diffMinutes < 60) {
      return `${diffMinutes}分钟前`
    } else if (diffHours < 24) {
      return `${diffHours}小时前`
    } else if (diffDays < 7) {
      return `${diffDays}天前`
    } else {
      return formatDateTime(isoString)
    }
  } catch (error) {
    console.error('相对时间格式化错误:', error)
    return isoString
  }
}
