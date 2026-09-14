<template>
  <div class="patent-network" ref="chartRef"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getPatents, type PatentNetwork } from '@/api/enterprise'

const props = defineProps<{ enterpriseId: string }>()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

function renderChart(data: PatentNetwork) {
  if (!chart) return

  const sorted = [...data.nodes]
    .filter((n: any) => n.filed_at)
    .sort((a: any, b: any) => a.filed_at.localeCompare(b.filed_at))

  const dates = sorted.map((n: any) => n.filed_at.slice(0, 10))
  const citedCounts = sorted.map((n: any) => n.cited_count)
  const qualities = sorted.map((n: any) => Number((n.quality * 100).toFixed(2)))

  chart.setOption({
    title: { text: '专利引用趋势', left: 'center', textStyle: { fontSize: 14 } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['引用次数', '质量评分(%)'], bottom: 0 },
    grid: { left: '8%', right: '8%', bottom: '15%', top: '15%' },
    xAxis: { type: 'category', name: '时间', data: dates, axisLabel: { rotate: 30, fontSize: 10 } },
    yAxis: [
      { type: 'value', name: '引用次数', position: 'left' },
      { type: 'value', name: '质量(%)', position: 'right', max: 100 },
    ],
    series: [
      {
        name: '引用次数',
        type: 'line',
        data: citedCounts,
        smooth: true,
        itemStyle: { color: '#409eff' },
        areaStyle: { opacity: 0.1 },
      },
      {
        name: '质量评分(%)',
        type: 'line',
        yAxisIndex: 1,
        data: qualities,
        smooth: true,
        itemStyle: { color: '#67c23a' },
      },
    ],
  })
}

async function loadData() {
  try {
    const data = await getPatents(props.enterpriseId) as any
    if (chart) renderChart(data)
  } catch {}
}

watch(() => props.enterpriseId, loadData)

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    loadData()
  }
})

onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.patent-network { width: 100%; height: 100%; min-height: 300px; }
</style>
