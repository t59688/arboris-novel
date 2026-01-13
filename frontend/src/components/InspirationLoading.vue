<!-- AIMETA P=灵感加载_加载动画组件|R=加载动画|NR=不含业务逻辑|E=component:InspirationLoading|X=internal|A=加载组件|D=vue|S=dom|RD=./README.ai -->
<template>
  <div class="absolute inset-0 bg-white flex flex-col items-center justify-center text-center p-8 transition-opacity duration-500">
    <div class="relative mb-8">
      <div class="w-24 h-24 bg-gradient-to-r from-indigo-400 to-purple-500 rounded-full mx-auto flex items-center justify-center animate-pulse shadow-lg">
        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707"></path>
        </svg>
      </div>
      <div class="absolute inset-0 w-24 h-24 bg-gradient-to-r from-indigo-400 to-purple-500 rounded-full mx-auto animate-ping opacity-30"></div>
    </div>
    <h2 class="text-2xl font-bold text-gray-800 mb-3">正在为你准备灵感空间...</h2>
    <div class="space-y-2 text-gray-600">
      <p class="animate-pulse" style="animation-delay: 0.2s">✨ 连接文思泉涌的AI...</p>
      <p class="animate-pulse" style="animation-delay: 0.6s">🎨 铺开创意的画卷...</p>
      <p class="animate-pulse" style="animation-delay: 1s;">🚀 准备开启灵感之旅！</p>
    </div>
  </div>
</template>

<script setup lang="ts">
// This is a purely presentational component.
</script>
