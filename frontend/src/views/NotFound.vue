<template>
  <div class="not-found">
    <div class="error-code">404</div>
    <div class="error-msg">页面不存在</div>
    <el-button type="primary" round @click="router.push('/')">返回首页</el-button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0A1730 0%, #0E2145 50%, #143061 100%);
}
.error-code {
  font-size: 96px;
  font-weight: 700;
  color: #C7000B;
  letter-spacing: 4px;
}
.error-msg {
  font-size: 20px;
  color: #9FB4DA;
  margin: 16px 0 32px;
  letter-spacing: 2px;
}
</style>
