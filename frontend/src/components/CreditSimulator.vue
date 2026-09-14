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
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { simulateCredit, type CreditResult } from '@/api/credit'

const props = defineProps<{ enterpriseId: string }>()
const progressPercent = ref(50)
const progress = ref(0.5)
const result = ref<CreditResult | null>(null)

async function simulate() {
  progress.value = progressPercent.value / 100
  try { result.value = await simulateCredit(props.enterpriseId, progress.value) as any } catch {}
}

watch(() => props.enterpriseId, simulate, { immediate: true })
</script>

<style scoped>
.credit-simulator { padding: 12px; }
.slider-section { margin-bottom: 8px; }
</style>
