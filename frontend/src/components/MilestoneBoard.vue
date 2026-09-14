<template>
  <div class="milestone-board">
    <el-timeline>
      <el-timeline-item
        v-for="ms in milestones"
        :key="ms.id"
        :type="statusType(ms.status)"
        :timestamp="ms.expected_date?.slice(0, 10)"
      >
        <el-card shadow="hover" style="margin-bottom: 8px">
          <div style="display: flex; justify-content: space-between; align-items: center">
            <strong>{{ ms.name }}</strong>
            <el-tag :type="statusType(ms.status)" size="small">{{ statusLabel(ms.status) }}</el-tag>
          </div>
          <p style="color: #999; font-size: 12px; margin: 4px 0">{{ ms.description }}</p>
          <el-progress :percentage="Number((ms.progress * 100).toFixed(2))" :status="ms.status === 'completed' ? 'success' : ''" />
          <div style="margin-top: 8px; display: flex; gap: 8px; align-items: center">
            <el-button size="small" @click="loadTools(ms.id)">查看金融工具</el-button>
            <el-slider v-if="ms.status !== 'completed'" v-model="ms.progressPercent" :min="0" :max="100" :step="1" style="flex: 1" @change="updateMs(ms)" />
          </div>
          <div v-if="tools[ms.id]" style="margin-top: 8px">
            <el-tag v-for="t in tools[ms.id]" :key="t.id" style="margin: 2px" type="info">
              {{ t.tool_name }}: {{ formatMoney(t.amount) }}
            </el-tag>
          </div>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getMilestones, getTools, updateProgress, type Milestone, type FinancialTool } from '@/api/milestone'

const props = defineProps<{ enterpriseId: string }>()
const milestones = ref<Milestone[]>([])
const tools = ref<Record<string, FinancialTool[]>>({})

async function loadData() {
  try {
    const res = await getMilestones(props.enterpriseId) as any
    milestones.value = res.map((ms: any) => ({ ...ms, progressPercent: Number((ms.progress * 100).toFixed(2)) }))
  } catch {}
}

async function loadTools(msId: string) {
  try { tools.value[msId] = await getTools(msId) as any } catch {}
}

async function updateMs(ms: any) {
  try {
    await updateProgress(ms.id, ms.progressPercent / 100)
    ElMessage.success(`进度已更新: ${ms.progressPercent}%`)
    await loadData()
  } catch {
    ElMessage.error('更新失败')
  }
}

function statusType(status: string): string {
  return { completed: 'success', in_progress: 'primary', pending: 'info' }[status] || 'info'
}

function statusLabel(status: string): string {
  return { completed: '已完成', in_progress: '进行中', pending: '待启动' }[status] || status
}

function formatMoney(val: number): string {
  if (val >= 10000) return (val / 10000).toFixed(2) + '万'
  return val.toFixed(2)
}

watch(() => props.enterpriseId, loadData, { immediate: true })
</script>

<style scoped>
.milestone-board { padding: 12px; }
</style>
