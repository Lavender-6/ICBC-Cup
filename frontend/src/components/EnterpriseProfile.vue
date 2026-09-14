<template>
  <div class="enterprise-profile">
    <el-descriptions :column="2" border size="small" v-if="enterprise">
      <el-descriptions-item label="企业名称">{{ enterprise.name }}</el-descriptions-item>
      <el-descriptions-item label="行业">
        <el-tag>{{ enterprise.industry }}</el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="研发阶段">{{ enterprise.stage }}</el-descriptions-item>
      <el-descriptions-item label="成立年份">{{ enterprise.founded_year || '-' }}</el-descriptions-item>
      <el-descriptions-item label="员工人数">{{ enterprise.employee_count || '-' }}</el-descriptions-item>
      <el-descriptions-item label="研发占比">{{ ((enterprise.rd_ratio || 0) * 100).toFixed(0) }}%</el-descriptions-item>
    </el-descriptions>

    <el-divider>AI 估值结果</el-divider>

    <el-row :gutter="12" v-if="valuation">
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="基础估值" :value="valuation.base_valuation" :precision="0" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="当前估值" :value="valuation.current_valuation" :precision="0" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="风险评分" :value="valuation.risk_score * 100" :precision="1" suffix="%" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="12" style="margin-top: 12px" v-if="valuation">
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="专利数量" :value="valuation.patent_count" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="平均专利质量" :value="valuation.avg_patent_quality * 100" :precision="1" suffix="%" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <el-statistic title="团队评分" :value="valuation.team_score * 100" :precision="1" suffix="%" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { getValuation, type Enterprise, type Valuation } from '@/api/enterprise'

const props = defineProps<{ enterprise: Enterprise | null }>()
const valuation = ref<Valuation | null>(null)

async function loadValuation(id: string) {
  try {
    valuation.value = await getValuation(id) as any
  } catch {}
}

watch(() => props.enterprise, (ep) => {
  if (ep) loadValuation(ep.id)
}, { immediate: true })
</script>

<style scoped>
.enterprise-profile { padding: 12px; }
</style>
