import request from './request'

export interface RecognitionResult {
  id: string
  datasetId: string
  modulation: string
  confidence: number
  snr: number
  symbolRate?: number
  freqOffset?: number
  createdAt: string
}

export function startRecognition(datasetId: string) {
  return request.post<RecognitionResult>(`/recognition/start`, { datasetId })
}

export function getRecognitionResult(id: string) {
  return request.get<RecognitionResult>(`/recognition/${id}`)
}

export function getRecognitionHistory() {
  return request.get<RecognitionResult[]>('/recognition/history')
}

export function getVisualization(datasetId: string) {
  return request.get<{
    waterfall: number[][]
    constellation: { i: number; q: number }[]
  }>(`/recognition/visualization/${datasetId}`)
}
