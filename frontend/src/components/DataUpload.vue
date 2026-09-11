<template>
  <div class="data-upload">
    <el-upload
      drag
      :auto-upload="true"
      :http-request="handleUpload"
      accept=".npy,.wav"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">拖拽 .npy / .wav 文件到此处，或<em>点击上传</em></div>
      <template #tip>
        <div class="el-upload__tip">支持 IQ 数据集格式：.npy / .wav</div>
      </template>
    </el-upload>
    <el-divider>或选择内置数据集</el-divider>
    <el-select v-model="selectedBuiltin" placeholder="选择内置数据集" @change="handleBuiltinSelect">
      <el-option label="RadioML 2018.01a 样本" value="radioml-sample" />
      <el-option label="BPSK 测试信号" value="bpsk-test" />
      <el-option label="16QAM 测试信号" value="16qam-test" />
    </el-select>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadDataset } from '@/api/dataset'
import { useRecognitionStore } from '@/stores/recognition'

const recognitionStore = useRecognitionStore()
const selectedBuiltin = ref('')

async function handleUpload(options: any) {
  try {
    const res = await uploadDataset(options.file)
    recognitionStore.setDataset((res as any).id)
    ElMessage.success('数据集上传成功')
  } catch {
    ElMessage.error('数据集上传失败')
  }
}

function handleBuiltinSelect(value: string) {
  recognitionStore.setDataset(value)
  ElMessage.info(`已选择内置数据集: ${value}`)
}
</script>

<style scoped>
.data-upload {
  padding: 16px;
}
.el-divider {
  margin: 16px 0;
}
</style>
