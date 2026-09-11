<template>
  <div class="dataset-management-view">
    <el-card>
      <template #header>数据集管理</template>
      <DatasetManager />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import DatasetManager from '@/components/DatasetManager.vue'
</script>

<style scoped>
.dataset-management-view {
  padding: 16px;
}
</style>
