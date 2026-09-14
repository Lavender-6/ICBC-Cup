<template>
  <div class="team-portrait">
    <el-row :gutter="12" v-if="team" style="margin-bottom: 12px">
      <el-col :span="6"><el-card shadow="hover"><el-statistic title="论文总数" :value="team.total_papers" /></el-card></el-col>
      <el-col :span="6"><el-card shadow="hover"><el-statistic title="专利总数" :value="team.total_patents" /></el-card></el-col>
      <el-col :span="6"><el-card shadow="hover"><el-statistic title="总引用数" :value="team.total_citations" /></el-card></el-col>
      <el-col :span="6"><el-card shadow="hover"><el-statistic title="平均H指数" :value="team.avg_h_index" :precision="1" /></el-card></el-col>
    </el-row>

    <el-table :data="team?.members || []" stripe size="small">
      <el-table-column prop="name" label="姓名" width="80" />
      <el-table-column prop="role" label="职位" width="100" />
      <el-table-column label="创始人" width="60">
        <template #default="{ row }">
          <el-tag v-if="row.is_founder" type="success" size="small">是</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="education" label="学历" width="60" />
      <el-table-column prop="paper_count" label="论文" width="60" />
      <el-table-column prop="citation_count" label="引用" width="60" />
      <el-table-column prop="h_index" label="H指数" width="60" />
      <el-table-column prop="patent_count" label="专利" width="60" />
      <el-table-column label="画像评分" width="120">
        <template #default="{ row }">
          <el-progress :percentage="Number((row.portrait_score * 100).toFixed(2))" :stroke-width="10" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { getTeam, type TeamPortrait } from '@/api/enterprise'

const props = defineProps<{ enterpriseId: string }>()
const team = ref<TeamPortrait | null>(null)

async function loadData() {
  try { team.value = await getTeam(props.enterpriseId) as any } catch {}
}

watch(() => props.enterpriseId, loadData, { immediate: true })
</script>

<style scoped>
.team-portrait { padding: 8px; }
</style>
