<template>
  <div class="enterprise-list">
    <div class="list-toolbar">
      <el-input v-model="searchKeyword" placeholder="搜索企业名称" clearable :prefix-icon="Search" style="width: 200px" />
      <el-select v-model="filterIndustry" placeholder="全部行业" clearable style="width: 130px">
        <el-option v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
      </el-select>
      <el-select v-model="filterStage" placeholder="全部阶段" clearable style="width: 130px">
        <el-option v-for="st in stages" :key="st" :label="st" :value="st" />
      </el-select>
      <el-button type="primary" :disabled="selectedRows.length < 2" @click="showCompare">
        对比 ({{ selectedRows.length }})
      </el-button>
      <span class="hint" v-if="selectedRows.length < 2">勾选2-4家企业进行对比</span>
    </div>
    <el-skeleton v-if="loading" :rows="5" animated style="margin-top: 12px" />
    <template v-else>
    <el-table :data="pagedData" stripe @row-click="handleClick" v-loading="loading" @selection-change="handleSelectionChange" ref="tableRef">
      <el-table-column type="selection" width="45" />
      <el-table-column prop="name" label="企业名称" min-width="120" />
      <el-table-column prop="industry" label="行业" width="100" />
      <el-table-column prop="stage" label="研发阶段" width="100" />
      <el-table-column label="当前估值" width="120">
        <template #default="{ row }">{{ formatMoney(row.current_valuation) }}</template>
      </el-table-column>
      <el-table-column label="风险评分" width="100">
        <template #default="{ row }">
          <el-tag :type="riskType(row.risk_score)">{{ (row.risk_score * 100).toFixed(1) }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="130" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" link @click.stop="handleEdit(row)">编辑</el-button>
          <el-button type="danger" size="small" link @click.stop="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="list-pagination" v-if="filteredData.length > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="filteredData.length"
        :page-sizes="[5, 10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        background
      />
    </div>
    <el-empty v-if="!loading && filteredData.length === 0" description="未找到匹配的企业" />
    </template>

    <el-dialog v-model="editDialog" title="编辑企业" width="500px" append-to-body>
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="企业名称">
          <el-input v-model="editForm.name" placeholder="请输入企业名称" />
        </el-form-item>
        <el-form-item label="所属行业">
          <el-select v-model="editForm.industry" placeholder="选择行业" teleported>
            <el-option v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
          </el-select>
        </el-form-item>
        <el-form-item label="研发阶段">
          <el-select v-model="editForm.stage" placeholder="选择研发阶段" teleported>
            <el-option label="立项预研" value="立项预研" />
            <el-option label="原型验证" value="原型验证" />
            <el-option label="流片成功" value="流片成功" />
            <el-option label="商业化量产" value="商业化量产" />
            <el-option label="上市预备" value="上市预备" />
          </el-select>
        </el-form-item>
        <el-form-item label="成立年份">
          <el-input-number v-model="editForm.founded_year" :min="2000" :max="2026" />
        </el-form-item>
        <el-form-item label="员工人数">
          <el-input-number v-model="editForm.employee_count" :min="1" :max="10000" />
        </el-form-item>
        <el-form-item label="研发占比">
          <el-slider v-model="editRdPercent" :min="0" :max="100" :step="5" show-input />
        </el-form-item>
        <el-form-item label="企业描述">
          <el-input v-model="editForm.description" type="textarea" :rows="2" placeholder="请输入企业描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialog = false">取消</el-button>
        <el-button type="primary" @click="handleEditSubmit" :loading="editSubmitting">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="compareDialog" title="企业对比" width="70%" top="5vh" append-to-body @opened="renderRadar" @closed="disposeRadar">
      <el-table :data="compareRows" border style="width: 100%">
        <el-table-column prop="label" label="指标" width="120" fixed />
        <el-table-column v-for="e in selectedRows" :key="e.id" :label="e.name" min-width="120">
          <template #default="{ row }">{{ row.values[e.id] }}</template>
        </el-table-column>
      </el-table>
      <div ref="radarChart" style="height: 350px; margin-top: 16px"></div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getEnterprises, deleteEnterprise, updateEnterprise, type Enterprise } from '@/api/enterprise'

const router = useRouter()
const enterprises = ref<Enterprise[]>([])
const loading = ref(false)
const industries = ['半导体', '航天', '生物医药', '高端装备', '新材料', '人工智能']
const stages = ['立项预研', '原型验证', '流片成功', '商业化量产', '上市预备']

const searchKeyword = ref('')
const filterIndustry = ref('')
const filterStage = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  let list = enterprises.value
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    list = list.filter(e => e.name.toLowerCase().includes(kw))
  }
  if (filterIndustry.value) {
    list = list.filter(e => e.industry === filterIndustry.value)
  }
  if (filterStage.value) {
    list = list.filter(e => e.stage === filterStage.value)
  }
  return list
})

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

watch([searchKeyword, filterIndustry, filterStage], () => {
  currentPage.value = 1
})

const editDialog = ref(false)
const editSubmitting = ref(false)
const editRdPercent = ref(35)
const editForm = ref({
  id: '',
  name: '',
  industry: '半导体',
  stage: '立项预研',
  founded_year: 2020,
  employee_count: 50,
  description: '',
})

const selectedRows = ref<Enterprise[]>([])
const compareDialog = ref(false)
const radarChart = ref<HTMLElement>()
let radarInstance: echarts.ECharts | null = null

const compareRows = computed(() => {
  if (selectedRows.value.length === 0) return []
  return [
    { label: '行业', values: Object.fromEntries(selectedRows.value.map(e => [e.id, e.industry])) },
    { label: '研发阶段', values: Object.fromEntries(selectedRows.value.map(e => [e.id, e.stage])) },
    { label: '成立年份', values: Object.fromEntries(selectedRows.value.map(e => [e.id, e.founded_year || '-'])) },
    { label: '员工人数', values: Object.fromEntries(selectedRows.value.map(e => [e.id, e.employee_count || '-'])) },
    { label: '研发占比', values: Object.fromEntries(selectedRows.value.map(e => [e.id, ((e.rd_ratio || 0) * 100).toFixed(0) + '%'])) },
    { label: '当前估值(万)', values: Object.fromEntries(selectedRows.value.map(e => [e.id, (e.current_valuation / 10000).toFixed(2)])) },
    { label: '基础估值(万)', values: Object.fromEntries(selectedRows.value.map(e => [e.id, (e.base_valuation / 10000).toFixed(2)])) },
    { label: '风险评分', values: Object.fromEntries(selectedRows.value.map(e => [e.id, (e.risk_score * 100).toFixed(1) + '%'])) },
  ]
})

function handleSelectionChange(rows: Enterprise[]) {
  selectedRows.value = rows.slice(0, 4)
}

function showCompare() {
  if (selectedRows.value.length < 2) {
    ElMessage.warning('请至少选择2家企业')
    return
  }
  compareDialog.value = true
}

function renderRadar() {
  if (!radarChart.value) return
  radarInstance = echarts.init(radarChart.value)
  const indicators = [
    { name: '估值规模', max: 1 },
    { name: '研发投入', max: 1 },
    { name: '团队规模', max: 1 },
    { name: '安全度', max: 1 },
    { name: '成长性', max: 1 },
  ]
  const maxVal = Math.max(...selectedRows.value.map(e => e.current_valuation))
  const maxEmp = Math.max(...selectedRows.value.map(e => e.employee_count || 1))
  const clamp = (v: number) => Math.max(0, Math.min(1, v))
  radarInstance.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, textStyle: { color: '#9FB4DA' } },
    radar: { indicator: indicators, axisName: { color: '#9FB4DA' }, splitLine: { lineStyle: { color: 'rgba(91,125,187,0.2)' } }, splitArea: { areaStyle: { color: ['rgba(10,23,48,0.3)', 'rgba(10,23,48,0.1)'] } } },
    series: [{
      type: 'radar',
      data: selectedRows.value.map(e => ({
        name: e.name,
        value: [
          clamp(e.current_valuation / maxVal),
          clamp(e.rd_ratio || 0.35),
          clamp((e.employee_count || 1) / maxEmp),
          clamp(1 - e.risk_score),
          clamp((e.current_valuation - e.base_valuation) / (e.base_valuation || 1)),
        ],
      })),
    }],
    color: ['#C7000B', '#E8B34B', '#5B7DBB', '#FF5A4E'],
  })
}

function disposeRadar() {
  radarInstance?.dispose()
  radarInstance = null
}

async function loadData() {
  loading.value = true
  try {
    const res = await getEnterprises()
    enterprises.value = res as any
  } finally {
    loading.value = false
  }
}

function handleClick(row: Enterprise) {
  router.push(`/enterprise/${row.id}`)
}

function handleEdit(row: Enterprise) {
  editForm.value = {
    id: row.id,
    name: row.name,
    industry: row.industry,
    stage: row.stage,
    founded_year: row.founded_year || 2020,
    employee_count: row.employee_count || 50,
    description: row.description || '',
  }
  editRdPercent.value = Math.round((row.rd_ratio || 0.35) * 100)
  editDialog.value = true
}

async function handleEditSubmit() {
  if (!editForm.value.name) {
    ElMessage.warning('请输入企业名称')
    return
  }
  editSubmitting.value = true
  try {
    await updateEnterprise(editForm.value.id, {
      name: editForm.value.name,
      industry: editForm.value.industry,
      stage: editForm.value.stage,
      founded_year: editForm.value.founded_year,
      employee_count: editForm.value.employee_count,
      rd_ratio: editRdPercent.value / 100,
      description: editForm.value.description,
    })
    ElMessage.success('保存成功')
    editDialog.value = false
    loadData()
  } catch {
    ElMessage.error('保存失败')
  } finally {
    editSubmitting.value = false
  }
}

async function handleDelete(row: Enterprise) {
  try {
    await ElMessageBox.confirm(`确认删除企业「${row.name}」？`, '提示', { type: 'warning' })
    await deleteEnterprise(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {}
}

function formatMoney(val: number): string {
  if (val >= 10000) return (val / 10000).toFixed(2) + ' 万'
  return val.toFixed(2)
}

function riskType(score: number): string {
  if (score < 0.3) return 'success'
  if (score < 0.6) return 'warning'
  return 'danger'
}

onMounted(loadData)
onUnmounted(disposeRadar)
</script>

<style scoped>
.enterprise-list { padding: 8px; }
.list-toolbar { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
.hint { color: #9FB4DA; font-size: 13px; }
.list-pagination { display: flex; justify-content: center; margin-top: 16px; }
</style>
