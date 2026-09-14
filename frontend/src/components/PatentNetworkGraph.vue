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
let networkData: PatentNetwork | null = null

function renderChart() {
  if (!chart || !networkData) return

  const nodes = networkData.nodes.map((n: any) => ({
    id: n.id,
    name: n.title.length > 10 ? n.title.slice(0, 10) + '...' : n.title,
    symbolSize: 10 + n.pagerank * 200,
    itemStyle: { color: getColorByQuality(n.quality) },
    value: `PR: ${n.pagerank}\n引用: ${n.in_degree}\n质量: ${(n.quality * 100).toFixed(1)}%`,
  }))

  const links = networkData.edges.map((e: any) => ({ source: e.source, target: e.target }))

  chart.setOption({
    title: { text: '专利引用网络', left: 'center', textStyle: { fontSize: 14 } },
    tooltip: { formatter: (p: any) => p.dataType === 'node' ? `${p.data.name}\n${p.data.value}` : '' },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      force: { repulsion: 100, edgeLength: 50, gravity: 0.1 },
      label: { show: true, fontSize: 8 },
      lineStyle: { color: '#aaa', curveness: 0.1 },
      data: nodes,
      links,
    }],
  })
}

function getColorByQuality(q: number): string {
  if (q > 0.7) return '#67c23a'
  if (q > 0.4) return '#e6a23c'
  return '#f56c6c'
}

async function loadData() {
  try {
    networkData = await getPatents(props.enterpriseId) as any
    renderChart()
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
