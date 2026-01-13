<!-- AIMETA P=注册页_用户注册|R=注册表单|NR=不含登录功能|E=route:/register#component:Register|X=ui|A=注册表单|D=vue|S=dom,net|RD=./README.ai -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4">
    <div class="mb-12">
      <TypewriterEffect text="拯救小说家" />
    </div>
    <div v-if="allowRegistration" class="w-full max-w-md p-8 space-y-8 bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl">
      <div>
        <h2 class="text-2xl font-bold text-center text-gray-800">
          加入我们
        </h2>
        <p class="mt-2 text-sm text-center text-gray-500">
          开启您的创作新篇章
        </p>
      </div>
      <form @submit.prevent="handleRegister" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label for="username" class="sr-only">用户名</label>
            <input v-model="username" id="username" name="username" type="text" required
              class="w-full px-4 py-3 text-gray-700 bg-gray-100 border-2 border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-blue-500 transition-all duration-300"
              placeholder="用户名" />
          </div>
          <div>
            <label for="email" class="sr-only">邮箱</label>
            <input v-model="email" id="email" name="email" type="email" required
              class="w-full px-4 py-3 text-gray-700 bg-gray-100 border-2 border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-blue-500 transition-all duration-300"
              placeholder="邮箱" />
          </div>
          <div class="flex space-x-2 items-center">
            <input v-model="verificationCode" id="verificationCode" name="verificationCode" type="text" required
              class="flex-1 px-4 py-3 text-gray-700 bg-gray-100 border-2 border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-blue-500 transition-all duration-300"
              placeholder="验证码" />
            <button type="button" @click="sendCode" :disabled="countdown > 0 || sending"
              class="px-4 py-3 text-sm font-bold text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-4 focus:ring-green-300 disabled:opacity-60 transition-all duration-300">
              <span v-if="sending">发送中...</span>
              <span v-else>{{ countdown > 0 ? countdown + '秒后重试' : '发送验证码' }}</span>
            </button>
          </div>
          <div>
            <label for="password" class="sr-only">密码</label>
            <input v-model="password" id="password" name="password" type="password" required
              class="w-full px-4 py-3 text-gray-700 bg-gray-100 border-2 border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-blue-500 transition-all duration-300"
              placeholder="密码" />
          </div>
        </div>

        <div v-if="error" class="text-sm font-medium text-center text-red-500">
          {{ error }}
        </div>
        <div v-if="success" class="text-sm font-medium text-center text-green-500">
          {{ success }}
        </div>

        <div>
          <button type="submit"
            class="w-full px-4 py-3 text-sm font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-60 transition-all duration-300">
            注册
          </button>
        </div>
      </form>
      
      <p class="mt-8 text-sm text-center text-gray-500">
        已有账户？
        <router-link to="/login" class="font-medium text-blue-600 hover:underline">
          立即登录
        </router-link>
      </p>
    </div>

    <div v-else class="w-full max-w-md p-8 space-y-6 text-center bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl">
      <h2 class="text-xl font-bold text-gray-800">暂未开放注册</h2>
      <p class="text-sm text-gray-500">请联系管理员或稍后再试。</p>
      <router-link to="/login" class="inline-block px-4 py-2 text-sm font-medium text-blue-600 hover:underline">
        返回登录
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import TypewriterEffect from '@/components/TypewriterEffect.vue';

const username = ref('');
const email = ref('');
const verificationCode = ref('');
const password = ref('');
const countdown = ref(0);
const sending = ref(false);
const error = ref('');
const success = ref('');
const router = useRouter();
const authStore = useAuthStore();
const allowRegistration = computed(() => authStore.allowRegistration);

// 进入页面即拉取认证开关，避免展示无效注册表单
onMounted(async () => {
  try {
    await authStore.fetchAuthOptions();
  } catch (error) {
    console.error('加载认证开关失败', error);
  }
  if (!allowRegistration.value) {
    success.value = '';
    error.value = '当前已关闭注册，请稍后再试。';
  }
});

const validateInput = () => {
  // Password validation
  if (password.value.length < 8) {
    return '密码必须至少8个字符';
  }

  // Username validation
  const usernameVal = username.value;
  const hasChinese = /[\u4e00-\u9fa5]/.test(usernameVal);
  const isNumeric = /^\d+$/.test(usernameVal);
  const isAlphanumeric = /^[a-zA-Z0-9]+$/.test(usernameVal);

  if (isNumeric) {
    return '用户名不能是纯数字';
  }

  if (hasChinese && usernameVal.length <= 1) {
    return '户名长度必须大于2个汉字';
  }

  if (isAlphanumeric && !hasChinese && usernameVal.length <= 6) {
    return '用户名长度必须大于6个字母或数字';
  }
  
  return null; // No validation errors
};

const sendCode = async () => {
  error.value = '';
  success.value = '';

  if (!allowRegistration.value) {
    error.value = '当前已关闭注册，请联系管理员。';
    return;
  }

  if (!email.value) {
    error.value = '请输入邮箱';
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    error.value = '邮箱格式不正确';
    return;
  }

  sending.value = true;
  try {
    const res = await fetch(`/api/auth/send-code?email=${encodeURIComponent(email.value)}`, {
      method: 'POST'
    });
    if (!res.ok) {
      const errMsg = await res.json();
      throw new Error(errMsg.detail || '发送验证码失败');
    }
    success.value = '验证码已发送，请查收邮箱';
    // 等接口返回成功后再开始倒计时
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) clearInterval(timer);
    }, 1000);
  } catch (err: any) {
    error.value = err.message;
  } finally {
    sending.value = false;
  }
};

const handleRegister = async () => {
  error.value = '';
  success.value = '';

  const validationError = validateInput();
  if (validationError) {
    error.value = validationError;
    return;
  }

  if (!allowRegistration.value) {
    error.value = '当前已关闭注册，请联系管理员。';
    return;
  }

  try {
    const res = await fetch('/api/auth/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        verification_code: verificationCode.value
      })
    });
    if (!res.ok) {
      const errMsg = await res.json();
      throw new Error(errMsg.detail || '注册失败');
    }
    success.value = '注册成功！正在跳转到登录页面...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err: any) {
    error.value = err.message || '注册失败，请稍后再试。';
    console.error(err);
  }
};
</script>
