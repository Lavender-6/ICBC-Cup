<template>
  <div class="risk-warning">
    <div class="risk-chart" ref="chartRef"></div>
    <div style="margin-top: 8px">
      <el-button size="small" @click="checkNow" :loading="checking">检查风险预警</el-button>
    </div>
    <el-empty v-if="!alerts.length" description="暂无风险预警" :image-size="40" style="margin-top: 8px" />
    <el-alert
      v-for="a in alerts"
      :key="a.id"
      :type="alertType(a.severity)"
      :title="a.message"
      :closable="false"
      show-icon
      style="margin-top: 8px"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getAlerts, checkAlerts, getRiskTrend, type RiskAlert, type RiskTrendPoint } from '@/api/credit'

const props = defineProps<{ enterpriseId: string }>()
const chartRef = ref<HTMLElement>()
const alerts = ref<RiskAlert[]>([])
const checking = ref(false)
let chart: echarts.ECharts | null = null

function renderChart(trend: RiskTrendPoint[]) {
  if (!chart || !trend.length) return
  const dates = trend.map(p => p.date)
  const risks = trend.map(p => Number((p.risk_score * 100).toFixed(2)))
  const progresses = trend.map(p => Number((p.progress * 100).toFixed(2)))

  chart.setOption({
    title: { text: '风险评分趋势', left: 'center', textStyle: { fontSize: 14 } },
    tooltip: { trigger: 'axis', formatter: (p: any) => {
      const idx = p[0].dataIndex
      return `${trend[idx].milestone}<br/>日期: ${p[0].name}<br/>风险: ${p[0].value}%<br/>进度: ${p[1]?.value || 0}%`
    }},
    legend: { data: ['风险评分(%)', '里程碑进度(%)'], bottom: 0 },
    grid: { left: '10%', right: '10%', bottom: '15%', top: '15%' },
    xAxis: { type: 'category', name: '时间', data: dates, axisLabel: { rotate: 30, fontSize: 10 } },
    yAxis: { type: 'value', name: '(%)', max: 100 },
    series: [
      { name: '风险评分(%)', type: 'line', data: risks, smooth: true, itemStyle: { color: '#f56c6c' }, areaStyle: { opacity: 0.1 } },
      { name: '里程碑进度(%)', type: 'line', data: progresses, smooth: true, itemStyle: { color: '#409eff' } },
    ],
  }, true)
}

async function loadData() {
  try {
    alerts.value = await getAlerts(props.enterpriseId) as any
    const trend = await getRiskTrend(props.enterpriseId) as any
    if (chart) renderChart(trend)
  } catch {}
}

async function checkNow() {
  checking.value = true
  try { await checkAlerts(props.enterpriseId); await loadData() } finally { checking.value = false }
}

function alertType(severity: string): string {
  return { critical: 'error', warning: 'warning', info: 'info' }[severity] || 'info'
}

watch(() => props.enterpriseId, loadData, { immediate: true })

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    loadData()
  }
})

onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.risk-warning { padding: 8px; }
.risk-chart { width: 100%; height: 200px; }
</style>
