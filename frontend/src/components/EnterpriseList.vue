<template>
  <div class="enterprise-list">
    <el-table :data="enterprises" stripe @row-click="handleClick" v-loading="loading">
      <el-table-column prop="name" label="企业名称" min-width="120" />
      <el-table-column prop="industry" label="行业" width="100" />
      <el-table-column prop="stage" label="研发阶段" width="100" />
      <el-table-column label="当前估值" width="120">
        <template #default="{ row }">{{ formatMoney(row.current_valuation) }}</template>
      </el-table-column>
      <el-table-column label="风险评分" width="100">
        <template #default="{ row }">
          <el-tag :type="riskType(row.risk_score)">{{ (row.risk_score * 100).toFixed(1) }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="80" fixed="right">
        <template #default="{ row }">
          <el-button type="danger" size="small" link @click.stop="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getEnterprises, deleteEnterprise, type Enterprise } from '@/api/enterprise'

const router = useRouter()
const enterprises = ref<Enterprise[]>([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await getEnterprises()
    enterprises.value = res as any
  } finally {
    loading.value = false
  }
}

function handleClick(row: Enterprise) {
  router.push(`/enterprise/${row.id}`)
}

async function handleDelete(row: Enterprise) {
  try {
    await ElMessageBox.confirm(`确认删除企业「${row.name}」？`, '提示', { type: 'warning' })
    await deleteEnterprise(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {}
}

function formatMoney(val: number): string {
  if (val >= 10000) return (val / 10000).toFixed(2) + ' 万'
  return val.toFixed(2)
}

function riskType(score: number): string {
  if (score < 0.3) return 'success'
  if (score < 0.6) return 'warning'
  return 'danger'
}

onMounted(loadData)
</script>

<style scoped>
.enterprise-list { padding: 8px; }
</style>
