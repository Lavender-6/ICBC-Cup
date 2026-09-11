<template>
  <div class="recognition-history-view">
    <el-card>
      <template #header>识别历史</template>
      <el-table :data="history" stripe v-loading="loading">
        <el-table-column prop="datasetId" label="数据集ID" min-width="120" />
        <el-table-column prop="modulation" label="调制方式" width="100" />
        <el-table-column prop="confidence" label="置信度" width="100">
          <template #default="{ row }">{{ row.confidence }}%</template>
        </el-table-column>
        <el-table-column prop="snr" label="SNR (dB)" width="100" />
        <el-table-column prop="createdAt" label="识别时间" min-width="150" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRecognitionHistory, type RecognitionResult } from '@/api/recognition'

const history = ref<RecognitionResult[]>([])
const loading = ref(false)

async function loadHistory() {
  loading.value = true
  try {
    const res = await getRecognitionHistory()
    history.value = res as any
  } catch {
    ElMessage.error('加载历史记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(loadHistory)
</script>

<style scoped>
.recognition-history-view {
  padding: 16px;
}
</style>
