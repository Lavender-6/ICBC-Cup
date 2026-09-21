<template>
  <div class="milestone-board">
    <div style="margin-bottom: 12px; text-align: right">
      <el-button type="primary" size="small" @click="showAddDialog = true">+ 新增里程碑</el-button>
    </div>
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
            <div style="display: flex; gap: 8px; align-items: center">
              <el-tag :type="statusType(ms.status)" size="small">{{ statusLabel(ms.status) }}</el-tag>
              <el-button type="danger" size="small" link @click="handleDelete(ms)">删除</el-button>
            </div>
          </div>
          <p style="color: #9FB4DA; font-size: 12px; margin: 4px 0">{{ ms.description }}</p>
          <el-progress :percentage="Number((ms.progress * 100).toFixed(2))" :status="ms.status === 'completed' ? 'success' : ''" />
          <div style="margin-top: 8px; display: flex; gap: 8px; align-items: center">
            <el-button size="small" @click="loadTools(ms.id)">查看金融工具</el-button>
            <el-slider v-model="ms.progressPercent" :min="0" :max="100" :step="1" style="flex: 1" @change="updateMs(ms)" />
          </div>
          <div v-if="tools[ms.id]" style="margin-top: 8px">
            <el-tag v-for="t in tools[ms.id]" :key="t.id" style="margin: 2px" type="info">
              {{ t.tool_name }}: {{ formatMoney(t.amount) }}
            </el-tag>
          </div>
        </el-card>
      </el-timeline-item>
    </el-timeline>

    <el-dialog v-model="showAddDialog" title="新增里程碑" width="460px" append-to-body>
      <el-form :model="addForm" label-width="90px">
        <el-form-item label="名称">
          <el-input v-model="addForm.name" placeholder="如：流片成功阶段里程碑" />
        </el-form-item>
        <el-form-item label="研发阶段">
          <el-select v-model="addForm.stage" placeholder="选择阶段">
            <el-option label="立项预研" value="立项预研" />
            <el-option label="原型验证" value="原型验证" />
            <el-option label="流片成功" value="流片成功" />
            <el-option label="商业化量产" value="商业化量产" />
            <el-option label="上市预备" value="上市预备" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="addForm.description" type="textarea" :rows="2" placeholder="里程碑描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd" :loading="addSubmitting">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMilestones, getTools, updateProgress, createMilestone, deleteMilestone, type FinancialTool } from '@/api/milestone'

const props = defineProps<{ enterpriseId: string }>()
const milestones = ref<any[]>([])
const tools = ref<Record<string, FinancialTool[]>>({})

const showAddDialog = ref(false)
const addSubmitting = ref(false)
const addForm = ref({ name: '', stage: '立项预研', description: '' })

async function loadData() {
  try {
    const res = await getMilestones(props.enterpriseId) as any
    const stageOrder = ['立项预研', '原型验证', '流片成功', '商业化量产', '上市预备']
    const sorted = [...res].sort((a: any, b: any) => {
      const ia = stageOrder.indexOf(a.stage); const ib = stageOrder.indexOf(b.stage)
      return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib)
    })
    milestones.value = sorted.map((ms: any) => ({ ...ms, progressPercent: Number((ms.progress * 100).toFixed(2)) }))
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

async function handleAdd() {
  if (!addForm.value.name) {
    ElMessage.warning('请输入里程碑名称')
    return
  }
  addSubmitting.value = true
  try {
    await createMilestone(props.enterpriseId, { ...addForm.value })
    ElMessage.success('里程碑创建成功')
    showAddDialog.value = false
    addForm.value = { name: '', stage: '立项预研', description: '' }
    await loadData()
  } catch {
    ElMessage.error('创建失败')
  } finally {
    addSubmitting.value = false
  }
}

async function handleDelete(ms: any) {
  try {
    await ElMessageBox.confirm(`确认删除里程碑「${ms.name}」？`, '提示', { type: 'warning' })
    await deleteMilestone(ms.id)
    ElMessage.success('删除成功')
    await loadData()
  } catch {}
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
