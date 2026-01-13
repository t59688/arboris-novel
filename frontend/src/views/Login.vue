<!-- AIMETA P=登录页_用户登录|R=登录表单_认证|NR=不含注册功能|E=route:/login#component:Login|X=ui|A=登录表单|D=vue|S=dom,net,storage|RD=./README.ai -->
<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4 md-surface-dim">
    <!-- Logo / Title -->
    <div class="mb-10">
      <TypewriterEffect text="拯 救 小 说 家" />
    </div>

    <!-- Material 3 Card -->
    <div class="md-card md-card-elevated w-full max-w-md p-8" style="border-radius: var(--md-radius-xl);">
      <!-- Header -->
      <div class="text-center mb-8">
        <h2 class="md-headline-medium" style="color: var(--md-on-surface);">
          欢迎回来
        </h2>
        <p class="md-body-medium mt-2" style="color: var(--md-on-surface-variant);">
          登录以继续您的创作之旅
        </p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Username Field -->
        <div class="md-text-field">
          <label for="username" class="md-text-field-label">用户名</label>
          <input 
            v-model="username" 
            id="username" 
            name="username" 
            type="text" 
            required
            class="md-text-field-input"
            placeholder="请输入用户名"
          />
        </div>

        <!-- Password Field -->
        <div class="md-text-field">
          <label for="password" class="md-text-field-label">密码</label>
          <input 
            v-model="password" 
            id="password" 
            name="password" 
            type="password" 
            required
            class="md-text-field-input"
            placeholder="请输入密码"
          />
        </div>

        <!-- Error Message -->
        <div v-if="error" class="flex items-center gap-2 p-3 rounded-lg" style="background-color: var(--md-error-container);">
          <svg class="w-5 h-5 flex-shrink-0" style="color: var(--md-error);" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="md-body-medium" style="color: var(--md-on-error-container);">{{ error }}</span>
        </div>

        <!-- Submit Button -->
        <button 
          type="submit"
          :disabled="isLoading"
          class="md-btn md-btn-filled md-ripple w-full h-12"
        >
          <svg v-if="isLoading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-if="isLoading">正在登录...</span>
          <span v-else>登录</span>
        </button>
      </form>

      <!-- Divider -->
      <div class="relative flex items-center justify-center my-8">
        <div class="w-full" style="height: 1px; background-color: var(--md-outline-variant);"></div>
        <span class="absolute px-4 md-body-small md-surface" style="color: var(--md-on-surface-variant);">或</span>
      </div>

      <!-- Linux DO Login -->
      <div v-if="enableLinuxdoLogin">
        <a 
          href="/api/auth/linuxdo/login"
          class="md-btn md-btn-outlined md-ripple w-full h-12"
        >
          <svg class="w-5 h-5" aria-hidden="true" viewBox="0 0 496 512">
            <path fill="currentColor" d="M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.5 0-200-89.5-200-200S137.5 56 248 56s200 89.5 200 200-89.5 200-200 200z"></path>
          </svg>
          使用 Linux DO 登录
        </a>
      </div>
      
      <!-- Register Link -->
      <p v-if="allowRegistration" class="mt-8 text-center md-body-medium" style="color: var(--md-on-surface-variant);">
        还没有账户？
        <router-link to="/register" class="md-label-large" style="color: var(--md-primary);">
          立即注册
        </router-link>
      </p>
    </div>

    <!-- Footer -->
    <p class="mt-8 md-body-small" style="color: var(--md-on-surface-variant);">
      Powered by AI · Material Design 3
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import TypewriterEffect from '@/components/TypewriterEffect.vue';

const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);
const router = useRouter();
const authStore = useAuthStore();
const allowRegistration = computed(() => authStore.allowRegistration);
const enableLinuxdoLogin = computed(() => authStore.enableLinuxdoLogin);

// 首屏自动拉取认证配置，确保登录页动态展示开关
onMounted(() => {
  authStore.fetchAuthOptions().catch((error) => {
    console.error('初始化认证配置失败', error);
  });
});

const handleLogin = async () => {
  error.value = '';
  isLoading.value = true;
  try {
    const mustChange = await authStore.login(username.value, password.value);
    const user = authStore.user;
    if (user?.is_admin && (authStore.mustChangePassword || mustChange)) {
      router.push({ name: 'admin', query: { tab: 'password' } });
    } else {
      router.push('/');
    }
  } catch (err) {
    error.value = '登录失败，请检查您的用户名和密码。';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
};
</script>
