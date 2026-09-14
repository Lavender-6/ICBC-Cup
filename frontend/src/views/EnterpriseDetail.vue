<template>
  <div class="enterprise-detail" v-loading="loading">
    <el-row :gutter="16">
      <el-col :span="10">
        <el-card shadow="never">
          <template #header>企业画像</template>
          <EnterpriseProfile :enterprise="enterprise" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <template #header>研发团队画像</template>
          <TeamPortrait :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <template #header>风控预警</template>
          <RiskWarning :enterpriseId="enterpriseId" />
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card shadow="never">
          <template #header>专利引用网络</template>
          <PatentNetworkGraph :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <template #header>里程碑看板</template>
          <MilestoneBoard :enterpriseId="enterpriseId" />
        </el-card>
        <el-card shadow="never" style="margin-top: 12px">
          <template #header>授信模拟器</template>
          <CreditSimulator :enterpriseId="enterpriseId" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getEnterprise, type Enterprise } from '@/api/enterprise'
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

async function loadData() {
  loading.value = true
  try { enterprise.value = await getEnterprise(enterpriseId) as any } finally { loading.value = false }
}

onMounted(loadData)
</script>

<style scoped>
.enterprise-detail { padding: 12px; }
</style>
