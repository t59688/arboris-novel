// AIMETA P=提示组合函数_全局提示消息管理|R=showAlert_hideAlert|NR=不含UI组件|E=compose:useAlert|X=internal|A=useAlert函数|D=vue|S=dom|RD=./README.ai
import { ref } from 'vue'

type AlertType = 'success' | 'error' | 'info' | 'confirmation'

interface Alert {
  id: number
  visible: boolean
  type: AlertType
  title: string
  message: string
  showCancel: boolean
  confirmText: string
  cancelText: string
  onConfirm: (result: boolean) => void
}

const alerts = ref<Alert[]>([])
let alertId = 0

const closeAlert = (id: number, result: boolean) => {
  const index = alerts.value.findIndex((a) => a.id === id)
  if (index !== -1) {
    // First, call the onConfirm callback to resolve the promise.
    alerts.value[index].onConfirm(result)
    // Then, remove the alert from the array to hide it.
    alerts.value.splice(index, 1)
  }
}

const showAlert = (
  message: string,
  type: AlertType = 'info',
  title: string = '',
  options: Partial<Omit<Alert, 'id' | 'visible' | 'message' | 'type' | 'title'>> = {}
) => {
  return new Promise<boolean>((resolve) => {
    const id = alertId++

    const newAlert: Alert = {
      id,
      visible: true,
      type,
      title: title || (type === 'success' ? '成功' : type === 'error' ? '错误' : '提示'),
      message,
      showCancel: options.showCancel || false,
      confirmText: options.confirmText || '确定',
      cancelText: options.cancelText || '取消',
      // The onConfirm callback is simply the resolve function of the promise.
      // This breaks the recursive loop.
      onConfirm: resolve,
    }
    alerts.value.push(newAlert)

    // For simple notifications (not confirmation dialogs), auto-close after 3 seconds.
    if ((type === 'success' || type === 'info') && !newAlert.showCancel) {
      setTimeout(() => {
        closeAlert(id, false) // Auto-close and resolve promise with false
      }, 3000)
    }
  })
}

const showSuccess = (message: string, title: string = '成功') => {
  return showAlert(message, 'success', title);
};

const showError = (message: string, title: string = '错误') => {
  return showAlert(message, 'error', title);
};

const showConfirm = (message: string, title: string = '请确认') => {
  return showAlert(message, 'confirmation', title, { showCancel: true });
};

export const globalAlert = {
  alerts,
  showAlert,
  closeAlert,
  showSuccess,
  showError,
  showConfirm,
}

export function useAlert() {
  return {
    showAlert: globalAlert.showAlert,
  }
}
