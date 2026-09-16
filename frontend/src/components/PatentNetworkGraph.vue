<template>
  <div class="patent-network-wrap">
    <div class="patent-network" ref="chartRef"></div>
    <div class="chart-toolbar">
      <el-radio-group v-model="chartType" size="small" @change="renderChart">
        <el-radio-button value="line">折线图</el-radio-button>
        <el-radio-button value="graph">力导向网络</el-radio-button>
      </el-radio-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getPatents, type PatentNetwork } from '@/api/enterprise'

const props = defineProps<{ enterpriseId: string }>()
const chartRef = ref<HTMLElement>()
const chartType = ref<'line' | 'graph'>('line')
let chart: echarts.ECharts | null = null
let networkData: PatentNetwork | null = null

function renderLineChart() {
  if (!chart || !networkData) return
  const sorted = [...networkData.nodes]
    .filter((n: any) => n.filed_at)
    .sort((a: any, b: any) => a.filed_at.localeCompare(b.filed_at))
  const dates = sorted.map((n: any) => n.filed_at.slice(0, 10))
  const citedCounts = sorted.map((n: any) => n.cited_count)
  const qualities = sorted.map((n: any) => Number((n.quality * 100).toFixed(2)))

  chart.setOption({
    title: { text: '专利引用趋势', left: 'center', textStyle: { fontSize: 14, color: '#F5D488' } },
    tooltip: { trigger: 'axis' },
    legend: { data: ['引用次数', '质量评分(%)'], bottom: 0, textStyle: { color: '#9FB4DA' } },
    grid: { left: '8%', right: '8%', bottom: '15%', top: '15%' },
    xAxis: { type: 'category', name: '时间', data: dates, axisLabel: { rotate: 30, fontSize: 10, color: '#9FB4DA' }, nameTextStyle: { color: '#9FB4DA' } },
    yAxis: [
      { type: 'value', name: '引用次数', position: 'left', axisLabel: { color: '#9FB4DA' }, nameTextStyle: { color: '#9FB4DA' }, splitLine: { lineStyle: { color: 'rgba(91,125,187,0.15)' } } },
      { type: 'value', name: '质量(%)', position: 'right', max: 100, axisLabel: { color: '#9FB4DA' }, nameTextStyle: { color: '#9FB4DA' }, splitLine: { show: false } },
    ],
    series: [
      { name: '引用次数', type: 'line', data: citedCounts, smooth: true, itemStyle: { color: '#409eff' }, areaStyle: { opacity: 0.1 } },
      { name: '质量评分(%)', type: 'line', yAxisIndex: 1, data: qualities, smooth: true, itemStyle: { color: '#E8B34B' } },
    ],
  }, true)
}

function renderGraphChart() {
  if (!chart || !networkData) return
  const nodes = networkData.nodes.map((n: any) => ({
    id: n.id,
    name: n.title?.length > 10 ? n.title.slice(0, 10) + '...' : n.title,
    symbolSize: 10 + n.pagerank * 200,
    itemStyle: { color: getColorByQuality(n.quality) },
    value: `PR: ${n.pagerank}\n引用: ${n.in_degree}\n质量: ${(n.quality * 100).toFixed(1)}%`,
  }))
  const links = networkData.edges.map((e: any) => ({ source: e.source, target: e.target }))
  chart.setOption({
    title: { text: '专利引用网络', left: 'center', textStyle: { fontSize: 14, color: '#F5D488' } },
    tooltip: { formatter: (p: any) => p.dataType === 'node' ? `${p.data.name}\n${p.data.value}` : '' },
    series: [{
      type: 'graph', layout: 'force', roam: true, draggable: true,
      force: { repulsion: 100, edgeLength: 50, gravity: 0.1 },
      label: { show: true, fontSize: 8, color: '#E0E6F0' },
      lineStyle: { color: 'rgba(91,125,187,0.4)', curveness: 0.1 },
      data: nodes, links,
    }],
  }, true)
}

function renderChart() {
  if (chartType.value === 'line') renderLineChart()
  else renderGraphChart()
}

function getColorByQuality(q: number): string {
  if (q > 0.7) return '#67c23a'
  if (q > 0.4) return '#e6a23c'
  return '#f56c6c'
}

async function loadData() {
  try {
    networkData = await getPatents(props.enterpriseId) as any
    if (chart) renderChart()
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
.patent-network-wrap { width: 100%; height: 100%; display: flex; flex-direction: column; }
.chart-toolbar { padding: 4px 8px; text-align: center; }
.patent-network { width: 100%; flex: 1; min-height: 400px; }
</style>
