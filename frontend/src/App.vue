<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-title">频谱智瞳 · 无线信号智能识别平台</div>
      <nav class="header-nav">
        <router-link to="/">首页</router-link>
        <router-link to="/datasets">数据集管理</router-link>
        <router-link to="/history">识别历史</router-link>
      </nav>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 56px;
  background: #1a1a2e;
  color: #fff;
}
.header-title {
  font-size: 18px;
  font-weight: 600;
}
.header-nav {
  display: flex;
  gap: 24px;
}
.header-nav a {
  color: #ccc;
  text-decoration: none;
  font-size: 14px;
}
.header-nav a.router-link-active {
  color: #409eff;
}
.app-main {
  flex: 1;
  overflow: hidden;
}
</style>
