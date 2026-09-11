<template>
  <div class="waterfall-plot" ref="chartRef"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { useRecognitionStore } from '@/stores/recognition'

const recognitionStore = useRecognitionStore()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

function renderChart() {
  if (!chart || !recognitionStore.waterfallData.length) return
  const data = recognitionStore.waterfallData
  const times = data.map((_, i) => i)
  const freqs = data[0]?.map((_, j) => j) || []
  const heatmapData: [number, number, number][] = []
  data.forEach((row, t) => {
    row.forEach((val, f) => {
      heatmapData.push([t, f, val])
    })
  })

  chart.setOption({
    title: { text: '频谱瀑布图', left: 'center', textStyle: { fontSize: 14 } },
    tooltip: {},
    xAxis: { type: 'category', name: '时间', data: times },
    yAxis: { type: 'category', name: '频率', data: freqs },
    visualMap: {
      min: -20,
      max: 0,
      calculable: true,
      realtime: true,
      inRange: { color: ['#313695', '#4575b4', '#74add1', '#fee090', '#f46d43', '#a50026'] },
    },
    series: [{ type: 'heatmap', data: heatmapData, progressive: 1000 }],
  })
}

watch(() => recognitionStore.waterfallData, renderChart, { deep: true })

onMounted(() => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    renderChart()
  }
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.waterfall-plot {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
