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
import { checkAlerts, getRiskTrend, type RiskAlert, type RiskTrendPoint } from '@/api/credit'

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
    title: { text: '风险评分趋势', left: 'center', textStyle: { fontSize: 14, color: '#F5D488' } },
    tooltip: { trigger: 'axis', formatter: (p: any) => {
      const idx = p[0].dataIndex
      return `${trend[idx].milestone}<br/>日期: ${p[0].name}<br/>风险: ${p[0].value}%<br/>进度: ${p[1]?.value || 0}%`
    }},
    legend: { data: ['风险评分(%)', '里程碑进度(%)'], bottom: 5, textStyle: { color: '#9FB4DA' } },
    grid: { left: '10%', right: '10%', bottom: '25%', top: '15%' },
    xAxis: { type: 'category', name: '时间', data: dates, axisLabel: { rotate: 30, fontSize: 10, interval: 0, color: '#9FB4DA' }, nameTextStyle: { color: '#9FB4DA' } },
    yAxis: { type: 'value', name: '(%)', max: 100, axisLabel: { color: '#9FB4DA' }, nameTextStyle: { color: '#9FB4DA' }, splitLine: { lineStyle: { color: 'rgba(91,125,187,0.15)' } } },
    series: [
      { name: '风险评分(%)', type: 'line', data: risks, smooth: true, itemStyle: { color: '#FF5A4E' }, areaStyle: { opacity: 0.1 } },
      { name: '里程碑进度(%)', type: 'line', data: progresses, smooth: true, itemStyle: { color: '#E8B34B' } },
    ],
  }, true)
}

async function loadData() {
  try {
    const trend = await getRiskTrend(props.enterpriseId) as any
    if (chart) renderChart(trend)
  } catch {}
}

async function checkNow() {
  checking.value = true
  try {
    const res = await checkAlerts(props.enterpriseId) as any
    alerts.value = (res.alerts || []).map((a: any, i: number) => ({
      id: `${a.type}-${i}`,
      alert_type: a.type,
      severity: a.severity,
      message: a.message,
      is_resolved: '0',
      created_at: new Date().toISOString(),
    }))
  } finally { checking.value = false }
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
.risk-chart { width: 100%; height: 300px; }
</style>
