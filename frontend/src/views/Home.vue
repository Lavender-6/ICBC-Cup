<template>
  <div class="home-view">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>硬科技企业列表</span>
          <el-tag type="info">工银科创桥</el-tag>
        </div>
      </template>
      <EnterpriseList />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import EnterpriseList from '@/components/EnterpriseList.vue'
</script>

<style scoped>
.home-view { padding: 16px; }
</style>
