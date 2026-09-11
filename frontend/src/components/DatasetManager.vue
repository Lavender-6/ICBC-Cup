<template>
  <div class="dataset-manager">
    <el-table :data="datasets" stripe size="small" v-loading="loading">
      <el-table-column prop="name" label="名称" min-width="120" />
      <el-table-column prop="format" label="格式" width="80" />
      <el-table-column prop="size" label="大小" width="80">
        <template #default="{ row }">{{ formatSize(row.size) }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80" />
      <el-table-column prop="createdAt" label="上传时间" min-width="120" />
      <el-table-column label="操作" width="80">
        <template #default="{ row }">
          <el-button type="danger" size="small" link @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getDatasets, deleteDataset, type Dataset } from '@/api/dataset'

const datasets = ref<Dataset[]>([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await getDatasets()
    datasets.value = res as any
  } catch {
    ElMessage.error('加载数据集列表失败')
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: string) {
  try {
    await deleteDataset(id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    ElMessage.error('删除失败')
  }
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(loadData)
</script>

<style scoped>
.dataset-manager {
  padding: 8px;
}
</style>
