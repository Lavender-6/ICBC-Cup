<template>
  <div class="result-card">
    <el-card shadow="hover">
      <template #header>识别结果</template>
      <div v-if="!result" class="empty-tip">暂无识别结果，请上传数据集并启动识别</div>
      <div v-else class="result-content">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="调制方式">
            <el-tag type="success">{{ result.modulation }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="置信度">
            <el-progress :percentage="result.confidence" :stroke-width="14" />
          </el-descriptions-item>
          <el-descriptions-item label="SNR">{{ result.snr }} dB</el-descriptions-item>
          <el-descriptions-item label="符号率" v-if="result.symbolRate">
            {{ result.symbolRate }} Hz
          </el-descriptions-item>
          <el-descriptions-item label="频偏" v-if="result.freqOffset">
            {{ result.freqOffset }} Hz
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRecognitionStore } from '@/stores/recognition'

const recognitionStore = useRecognitionStore()
const result = computed(() => recognitionStore.recognitionResult)
</script>

<style scoped>
.result-card {
  padding: 8px;
}
.empty-tip {
  color: #999;
  text-align: center;
  padding: 20px;
}
</style>
