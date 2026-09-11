import request from './request'

export interface Dataset {
  id: string
  name: string
  format: string
  size: number
  status: string
  createdAt: string
}

export function uploadDataset(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<Dataset>('/datasets/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function getDatasets() {
  return request.get<Dataset[]>('/datasets')
}

export function getDatasetById(id: string) {
  return request.get<Dataset>(`/datasets/${id}`)
}

export function deleteDataset(id: string) {
  return request.delete(`/datasets/${id}`)
}
