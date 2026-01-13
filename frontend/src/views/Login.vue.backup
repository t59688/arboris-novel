<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4">
    <div class="mb-12">
      <TypewriterEffect text="拯 救 小 说 家" />
    </div>
    <div class="w-full max-w-sm p-8 space-y-8 bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl">
      <div>
        <h2 class="text-2xl font-bold text-center text-gray-800">
          欢迎回来
        </h2>
        <p class="mt-2 text-sm text-center text-gray-500">
          登录以继续您的创作之旅
        </p>
      </div>
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label for="username" class="sr-only">用户名</label>
            <input v-model="username" id="username" name="username" type="text" required
              class="w-full px-4 py-3 text-gray-700 bg-gray-100 border-2 border-gray-200 rounded-lg focus:outline-none focus:bg-white focus:border-blue-500 transition-all duration-300"
              placeholder="用户名" />
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

        <div>
          <button type="submit"
            :disabled="isLoading"
            class="w-full px-4 py-3 text-sm font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-60 transition-all duration-300">
            <span v-if="isLoading">正在登录...</span>
            <span v-else>登录</span>
          </button>
        </div>
      </form>

      <div class="relative flex items-center justify-center my-6">
        <div class="w-full border-t border-gray-200"></div>
        <span class="absolute px-3 text-sm text-gray-400 bg-white">或</span>
      </div>

      <div v-if="enableLinuxdoLogin">
        <a href="/api/auth/linuxdo/login"
          class="flex items-center justify-center w-full px-4 py-3 text-sm font-bold text-gray-700 bg-white border-2 border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-4 focus:ring-gray-200 transition-all duration-300">
          <svg class="w-5 h-5 mr-2" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="linux" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><path fill="currentColor" d="M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.5 0-200-89.5-200-200S137.5 56 248 56s200 89.5 200 200-89.5 200-200 200z"></path></svg>
          使用 Linux DO 登录
        </a>
      </div>
      
      <p v-if="allowRegistration" class="mt-8 text-sm text-center text-gray-500">
        还没有账户？
        <router-link to="/register" class="font-medium text-blue-600 hover:underline">
          立即注册
        </router-link>
      </p>
    </div>
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
