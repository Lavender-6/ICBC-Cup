<template>
  <div class="enterprise-detail" v-loading="loading">
    <template v-if="loading">
      <el-skeleton :rows="8" animated />
      <el-skeleton :rows="6" animated style="margin-top: 16px" />
    </template>
    <template v-else>
    <div class="detail-toolbar">
      <el-button type="primary" @click="handleExport" :loading="exporting">导出数据</el-button>
    </div>
    <el-row :gutter="16">
      <el-col :span="10">
        <el-card shadow="never" data-section="profile">
          <template #header>企业画像</template>
          <EnterpriseProfile :enterprise="enterprise" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px" data-section="team">
          <template #header>研发团队画像</template>
          <TeamPortrait :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px" data-section="risk">
          <template #header>风控预警</template>
          <RiskWarning :enterpriseId="enterpriseId" />
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card shadow="never" data-section="patents">
          <template #header>专利引用趋势</template>
          <PatentNetworkGraph :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px" data-section="milestone">
          <template #header>里程碑看板</template>
          <MilestoneBoard :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px" data-section="credit">
          <template #header>授信模拟器</template>
          <CreditSimulator :enterpriseId="enterpriseId" />
        </el-card>
      </el-col>
    </el-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getEnterprise, exportEnterprise, type Enterprise } from '@/api/enterprise'
import EnterpriseProfile from '@/components/EnterpriseProfile.vue'
import TeamPortrait from '@/components/TeamPortrait.vue'
import RiskWarning from '@/components/RiskWarning.vue'
import PatentNetworkGraph from '@/components/PatentNetworkGraph.vue'
import MilestoneBoard from '@/components/MilestoneBoard.vue'
import CreditSimulator from '@/components/CreditSimulator.vue'

const route = useRoute()
const enterpriseId = route.params.id as string
const enterprise = ref<Enterprise | null>(null)
const loading = ref(false)
const exporting = ref(false)

async function loadData() {
  loading.value = true
  try { enterprise.value = await getEnterprise(enterpriseId) as any } finally { loading.value = false }
}

async function handleExport() {
  exporting.value = true
  try {
    const res = await exportEnterprise(enterpriseId) as any
    const blob = new Blob([res], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${enterprise.value?.name || '企业'}_数据导出.csv`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch {
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.enterprise-detail {
  padding: 16px;
  min-height: 100%;
  background: linear-gradient(180deg, #0A1730 0%, #0E2145 100%);
}
.detail-toolbar { margin-bottom: 12px; }
@media (max-width: 1024px) {
  .enterprise-detail :deep(.el-col-10),
  .enterprise-detail :deep(.el-col-14) {
    max-width: 100%;
    flex: 0 0 100%;
  }
}
</style>
