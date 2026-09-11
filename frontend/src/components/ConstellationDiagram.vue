<template>
  <div class="constellation-plot" ref="chartRef"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { useRecognitionStore } from '@/stores/recognition'

const recognitionStore = useRecognitionStore()
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

function renderChart() {
  if (!chart) return
  const data = recognitionStore.constellationData
  const seriesData = data.map((p) => [p.i, p.q])

  chart.setOption({
    title: { text: '星座图 (I-Q)', left: 'center', textStyle: { fontSize: 14 } },
    xAxis: { name: 'I', type: 'value', scale: true, splitLine: { lineStyle: { type: 'dashed' } } },
    yAxis: { name: 'Q', type: 'value', scale: true, splitLine: { lineStyle: { type: 'dashed' } } },
    series: [
      {
        type: 'scatter',
        data: seriesData,
        symbolSize: 4,
        itemStyle: { color: '#409eff', opacity: 0.6 },
      },
    ],
  })
}

watch(() => recognitionStore.constellationData, renderChart, { deep: true })

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
.constellation-plot {
  width: 100%;
  height: 100%;
  min-height: 200px;
}
</style>
