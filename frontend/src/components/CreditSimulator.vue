<template>
  <div class="credit-simulator">
    <div class="slider-section">
      <span>里程碑进度: {{ (progress * 100).toFixed(0) }}%</span>
      <el-slider v-model="progressPercent" :max="100" @change="simulate" />
    </div>

    <el-row :gutter="12" v-if="result" style="margin-top: 16px">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="基础额度" :value="result.base_amount" :precision="0" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="进度系数" :value="result.progress_factor" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="风险系数" :value="result.risk_factor" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="最终授信额度" :value="result.final_amount" :precision="0" />
        </el-card>
      </el-col>
    </el-row>

    <el-alert
      v-if="result"
      style="margin-top: 12px"
      type="info"
      :closable="false"
      title="授信公式"
      description="最终额度 = 基础额度 × 里程碑进度系数 × 风险评估系数"
    />

    <div v-if="history.length" style="margin-top: 16px">
      <el-divider>授信模拟历史</el-divider>
      <el-table :data="history.slice(0, 5)" size="small" stripe>
        <el-table-column label="时间" width="170">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="基础额度" width="120">
          <template #default="{ row }">{{ row.base_amount.toFixed(0) }}</template>
        </el-table-column>
        <el-table-column label="进度系数" width="100">
          <template #default="{ row }">{{ row.progress_factor.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="风险系数" width="100">
          <template #default="{ row }">{{ row.risk_factor.toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="最终授信" width="120">
          <template #default="{ row }">
            <span style="color: #F5D488; font-weight: 600">{{ row.final_amount.toFixed(0) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { simulateCredit, getCreditHistory, type CreditResult } from '@/api/credit'

const props = defineProps<{ enterpriseId: string }>()
const progressPercent = ref(50)
const progress = ref(0.5)
const result = ref<CreditResult | null>(null)
const history = ref<any[]>([])

async function simulate() {
  progress.value = progressPercent.value / 100
  try {
    result.value = await simulateCredit(props.enterpriseId, progress.value) as any
    await loadHistory()
  } catch {}
}

async function loadHistory() {
  try { history.value = await getCreditHistory(props.enterpriseId) as any } catch {}
}

function formatTime(iso: string): string {
  return iso?.replace('T', ' ').slice(0, 19) || ''
}

watch(() => props.enterpriseId, () => { simulate(); loadHistory() }, { immediate: true })
</script>

<style scoped>
.credit-simulator { padding: 12px; }
.slider-section { margin-bottom: 8px; }
</style>
