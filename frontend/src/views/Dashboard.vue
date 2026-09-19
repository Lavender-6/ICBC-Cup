<template>
  <div class="dashboard">
    <div class="dash-header">
      <h2>数据大屏</h2>
    </div>
    <template v-if="!stats">
      <el-skeleton :rows="4" animated />
      <el-skeleton :rows="8" animated style="margin-top: 16px" />
    </template>
    <template v-else>
    <div class="dash-cards">
      <el-card shadow="hover" v-for="c in cards" :key="c.title">
        <el-statistic :title="c.title" :value="c.value" :precision="c.precision || 0" :suffix="c.suffix || ''" />
      </el-card>
    </div>
    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>行业分布</template>
          <div ref="industryChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>研发阶段分布</template>
          <div ref="stageChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>风险等级分布</template>
          <div ref="riskChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>里程碑状态统计</template>
          <div ref="msChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, type DashboardStats } from '@/api/stats'

const stats = ref<DashboardStats | null>(null)
const industryChart = ref<HTMLElement>()
const stageChart = ref<HTMLElement>()
const riskChart = ref<HTMLElement>()
const msChart = ref<HTMLElement>()
let charts: echarts.ECharts[] = []

const cards = ref<{ title: string; value: number; precision?: number; suffix?: string }[]>([])

const axisStyle = {
  axisLabel: { color: '#9FB4DA' },
  nameTextStyle: { color: '#9FB4DA' },
  splitLine: { lineStyle: { color: 'rgba(91,125,187,0.15)' } },
}

function renderCharts() {
  if (!stats.value) return
  const s = stats.value

  cards.value = [
    { title: '企业总数', value: s.total_enterprises },
    { title: '平均估值', value: s.avg_valuation, precision: 0, suffix: '万元' },
    { title: '专利总数', value: s.total_patents },
    { title: '研发人员', value: s.total_members },
  ]

  if (industryChart.value) {
    const c = echarts.init(industryChart.value)
    c.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, textStyle: { color: '#9FB4DA' } },
      series: [{
        type: 'pie', radius: ['40%', '70%'],
        data: Object.entries(s.industry_dist).map(([name, value]) => ({ name, value })),
        label: { color: '#E0E6F0' },
        itemStyle: { borderColor: '#0A1730', borderWidth: 2 },
      }],
      color: ['#C7000B', '#2A5298', '#E8B34B', '#FF5A4E', '#5B7DBB', '#F9D488'],
    })
    charts.push(c)
  }

  if (stageChart.value) {
    const c = echarts.init(stageChart.value)
    c.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, textStyle: { color: '#9FB4DA' } },
      series: [{
        type: 'pie', radius: ['40%', '70%'],
        data: Object.entries(s.stage_dist).map(([name, value]) => ({ name, value })),
        label: { color: '#E0E6F0' },
        itemStyle: { borderColor: '#0A1730', borderWidth: 2 },
      }],
      color: ['#E8B34B', '#C7000B', '#5B7DBB', '#FF5A4E', '#143061'],
    })
    charts.push(c)
  }

  if (riskChart.value) {
    const c = echarts.init(riskChart.value)
    c.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['低风险', '中风险', '高风险'], ...axisStyle },
      yAxis: { type: 'value', ...axisStyle },
      series: [{
        type: 'bar', data: [s.risk_levels.low, s.risk_levels.medium, s.risk_levels.high],
        itemStyle: { color: '#E8B34B' },
        barWidth: '40%',
      }],
    })
    charts.push(c)
  }

  if (msChart.value) {
    const c = echarts.init(msChart.value)
    c.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['已完成', '进行中', '待启动'], ...axisStyle },
      yAxis: { type: 'value', ...axisStyle },
      series: [{
        type: 'bar', data: [s.milestone_stats.completed, s.milestone_stats.in_progress, s.milestone_stats.pending],
        itemStyle: { color: '#C7000B' },
        barWidth: '40%',
      }],
    })
    charts.push(c)
  }
}

onMounted(async () => {
  try {
    stats.value = await getDashboardStats() as any
    await nextTick()
    renderCharts()
  } catch {}
})

onUnmounted(() => charts.forEach(c => c.dispose()))
</script>

<style scoped>
.dashboard { padding: 16px; }
.dash-header h2 { color: #F5D488; margin-bottom: 16px; }
.dash-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
@media (max-width: 1024px) {
  .dash-cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .dash-cards { grid-template-columns: 1fr; }
}
</style>
