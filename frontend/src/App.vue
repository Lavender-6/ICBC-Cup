<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-title">工银科创桥 · 硬科技企业投贷联动平台</div>
    </header>
    <div class="app-body">
      <aside class="app-sidebar">
        <el-menu :default-active="activeMenu" @select="handleMenuSelect" class="sidebar-menu">
          <el-menu-item index="/">
            <el-icon><List /></el-icon>
            <span>企业列表</span>
          </el-menu-item>
          <template v-if="inEnterpriseDetail">
            <el-menu-item-group title="企业详情">
              <el-menu-item index="profile"><span>企业画像</span></el-menu-item>
              <el-menu-item index="patents"><span>专利分析</span></el-menu-item>
              <el-menu-item index="team"><span>研发团队</span></el-menu-item>
              <el-menu-item index="milestone"><span>里程碑看板</span></el-menu-item>
              <el-menu-item index="credit"><span>授信模拟器</span></el-menu-item>
              <el-menu-item index="risk"><span>风控预警</span></el-menu-item>
            </el-menu-item-group>
          </template>
        </el-menu>
      </aside>
      <main class="app-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { List } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const inEnterpriseDetail = computed(() => route.name === 'enterprise-detail')
const activeMenu = computed(() => route.path)

function handleMenuSelect(index: string) {
  if (index === '/') {
    router.push('/')
  } else if (inEnterpriseDetail.value) {
    const el = document.querySelector(`[data-section="${index}"]`)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}
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
  padding: 0 24px;
  height: 56px;
  background: linear-gradient(90deg, #0A1730, #0E2145);
  color: #fff;
  border-bottom: 2px solid;
  border-image: linear-gradient(90deg, #C7000B, #E8B34B) 1;
}
.header-title {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 2px;
}
.header-title::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 18px;
  background: #C7000B;
  margin-right: 10px;
  vertical-align: middle;
  border-radius: 2px;
}
.app-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.app-sidebar {
  width: 200px;
  background: rgba(10, 23, 48, 0.8);
  border-right: 1px solid rgba(91, 125, 187, 0.15);
  overflow-y: auto;
  backdrop-filter: blur(8px);
}
.sidebar-menu {
  border-right: none;
}
.app-main {
  flex: 1;
  overflow-y: auto;
  background: #0A1730;
}
</style>
