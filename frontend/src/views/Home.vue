<template>
  <div class="home-view">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span>硬科技企业列表</span>
          <div style="display: flex; gap: 8px; align-items: center">
            <el-tag type="info">工银科创桥</el-tag>
            <el-button type="primary" size="small" @click="showDialog = true">+ 创建企业</el-button>
          </div>
        </div>
      </template>
      <EnterpriseList />
    </el-card>

    <el-dialog v-model="showDialog" title="创建硬科技企业" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="企业名称">
          <el-input v-model="form.name" placeholder="请输入企业名称" />
        </el-form-item>
        <el-form-item label="所属行业">
          <el-select v-model="form.industry" placeholder="选择行业">
            <el-option v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
          </el-select>
        </el-form-item>
        <el-form-item label="研发阶段">
          <el-select v-model="form.stage" placeholder="选择研发阶段">
            <el-option label="立项预研" value="立项预研" />
            <el-option label="原型验证" value="原型验证" />
            <el-option label="流片成功" value="流片成功" />
            <el-option label="商业化量产" value="商业化量产" />
            <el-option label="上市预备" value="上市预备" />
          </el-select>
        </el-form-item>
        <el-form-item label="成立年份">
          <el-input-number v-model="form.founded_year" :min="2000" :max="2026" />
        </el-form-item>
        <el-form-item label="员工人数">
          <el-input-number v-model="form.employee_count" :min="1" :max="10000" />
        </el-form-item>
        <el-form-item label="研发占比">
          <el-slider v-model="rdRatioPercent" :min="0" :max="100" :step="5" show-input />
        </el-form-item>
        <el-form-item label="专利数量">
          <el-input-number v-model="form.patent_count" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="企业描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="请输入企业描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import EnterpriseList from '@/components/EnterpriseList.vue'
import { createEnterprise } from '@/api/enterprise'

const showDialog = ref(false)
const submitting = ref(false)
const industries = ['半导体', '航天', '生物医药', '高端装备', '新材料', '人工智能']
const rdRatioPercent = ref(35)

const form = ref({
  name: '',
  industry: '半导体',
  stage: '立项预研',
  founded_year: 2020,
  employee_count: 50,
  patent_count: 10,
  description: '',
})

async function handleSubmit() {
  if (!form.value.name) {
    ElMessage.warning('请输入企业名称')
    return
  }
  submitting.value = true
  try {
    await createEnterprise({
      ...form.value,
      rd_ratio: rdRatioPercent.value / 100,
    })
    ElMessage.success('企业创建成功')
    showDialog.value = false
    window.location.reload()
  } catch {
    ElMessage.error('创建失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.home-view { padding: 16px; }
</style>
