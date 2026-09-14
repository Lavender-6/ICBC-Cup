<template>
  <div class="risk-warning">
    <el-button size="small" @click="checkNow" :loading="checking" style="margin-bottom: 8px">
      检查风险预警
    </el-button>
    <el-empty v-if="!alerts.length" description="暂无风险预警" :image-size="60" />
    <el-alert
      v-for="a in alerts"
      :key="a.id"
      :type="alertType(a.severity)"
      :title="a.message"
      :closable="false"
      show-icon
      style="margin-bottom: 8px"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { getAlerts, checkAlerts, type RiskAlert } from '@/api/credit'

const props = defineProps<{ enterpriseId: string }>()
const alerts = ref<RiskAlert[]>([])
const checking = ref(false)

async function loadData() {
  try { alerts.value = await getAlerts(props.enterpriseId) as any } catch {}
}

async function checkNow() {
  checking.value = true
  try { await checkAlerts(props.enterpriseId); await loadData() } finally { checking.value = false }
}

function alertType(severity: string): string {
  return { critical: 'error', warning: 'warning', info: 'info' }[severity] || 'info'
}

watch(() => props.enterpriseId, loadData, { immediate: true })
</script>

<style scoped>
.risk-warning { padding: 12px; }
</style>
