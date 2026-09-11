import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface RecognitionResult {
  modulation: string
  confidence: number
  snr: number
  symbolRate?: number
  freqOffset?: number
}

export const useRecognitionStore = defineStore('recognition', () => {
  const currentDatasetId = ref<string | null>(null)
  const recognitionResult = ref<RecognitionResult | null>(null)
  const isProcessing = ref(false)
  const waterfallData = ref<number[][]>([])
  const constellationData = ref<{ i: number; q: number }[]>([])

  function setDataset(id: string) {
    currentDatasetId.value = id
    recognitionResult.value = null
    waterfallData.value = []
    constellationData.value = []
  }

  function setResult(result: RecognitionResult) {
    recognitionResult.value = result
    isProcessing.value = false
  }

  function setVisualization(waterfall: number[][], constellation: { i: number; q: number }[]) {
    waterfallData.value = waterfall
    constellationData.value = constellation
  }

  return {
    currentDatasetId,
    recognitionResult,
    isProcessing,
    waterfallData,
    constellationData,
    setDataset,
    setResult,
    setVisualization,
  }
})
