<template>
  <div class="home-view">
    <el-row :gutter="16" class="full-height">
      <el-col :span="6" class="left-panel">
        <el-card shadow="never">
          <template #header>数据上传</template>
          <DataUpload />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <template #header>数据集管理</template>
          <DatasetManager />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <ResultCard />
        </el-card>
      </el-col>
      <el-col :span="18" class="right-panel">
        <div class="waterfall-container">
          <WaterfallPlot />
        </div>
        <div class="constellation-container">
          <ConstellationDiagram />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import DataUpload from '@/components/DataUpload.vue'
import DatasetManager from '@/components/DatasetManager.vue'
import ResultCard from '@/components/ResultCard.vue'
import WaterfallPlot from '@/components/WaterfallPlot.vue'
import ConstellationDiagram from '@/components/ConstellationDiagram.vue'
</script>

<style scoped>
.home-view {
  height: 100%;
  padding: 12px;
  overflow: hidden;
}
.full-height {
  height: 100%;
}
.left-panel {
  height: 100%;
  overflow-y: auto;
}
.right-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.waterfall-container {
  flex: 3;
  background: #fff;
  border-radius: 4px;
  padding: 8px;
}
.constellation-container {
  flex: 2;
  background: #fff;
  border-radius: 4px;
  padding: 8px;
}
</style>
