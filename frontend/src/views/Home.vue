<template>
  <div class="home-view">
    <!-- Hero Banner -->
    <section class="hero" ref="heroRef">
      <div class="hero-bg"></div>
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <img src="@/assets/images/hero-banner.svg" alt="工银科创桥" class="hero-svg" />
        <div class="hero-cta">
          <el-button type="primary" size="large" round @click="scrollTo('enterprise-section')">
            开始评估
          </el-button>
          <el-button size="large" round class="cta-secondary" @click="scrollTo('capability-section')">
            了解平台
          </el-button>
        </div>
      </div>
    </section>

    <!-- 核心能力 -->
    <section class="capability-section" ref="capability-section">
      <div class="section-header">
        <h2 class="section-title">平台核心能力</h2>
        <p class="section-subtitle">AI 驱动的硬科技企业全生命周期金融服务</p>
      </div>
      <div class="capability-grid">
        <div
          v-for="cap in capabilities"
          :key="cap.title"
          class="capability-card"
        >
          <div class="cap-icon" :style="{ background: cap.iconBg }">
            <span v-html="cap.icon"></span>
          </div>
          <h3 class="cap-title">{{ cap.title }}</h3>
          <p class="cap-desc">{{ cap.desc }}</p>
          <div class="cap-tags">
            <span v-for="t in cap.tags" :key="t" class="cap-tag">{{ t }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 里程碑投贷联动 -->
    <section class="milestone-section">
      <div class="section-header">
        <h2 class="section-title">里程碑式投贷联动</h2>
        <p class="section-subtitle">以研发里程碑为触发器，动态匹配金融工具包</p>
      </div>
      <div class="milestone-flow">
        <div
          v-for="(ms, i) in milestones"
          :key="ms.stage"
          class="ms-step"
          :class="{ 'ms-active': i === 2 }"
        >
          <div class="ms-node">
            <span class="ms-index">{{ i + 1 }}</span>
          </div>
          <div class="ms-info">
            <div class="ms-stage">{{ ms.stage }}</div>
            <div class="ms-tools">{{ ms.tools }}</div>
          </div>
          <div v-if="i < milestones.length - 1" class="ms-connector"></div>
        </div>
      </div>
    </section>

    <!-- 企业列表 -->
    <section class="enterprise-section" ref="enterprise-section">
      <div class="section-header light">
        <h2 class="section-title light">硬科技企业库</h2>
        <el-button type="primary" @click="showDialog = true">
          <el-icon><Plus /></el-icon>&nbsp;创建企业
        </el-button>
      </div>
      <div class="enterprise-card">
        <EnterpriseList />
      </div>
    </section>

    <!-- 创建企业对话框 -->
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
import { Plus } from '@element-plus/icons-vue'
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

const capabilities = [
  {
    title: 'AI 评估引擎',
    desc: '基于专利引用网络建模与研发团队画像，对轻资产科创企业进行多维度动态估值，突破传统财务指标局限。',
    tags: ['专利引用网络', '团队画像', '动态估值'],
    iconBg: 'linear-gradient(135deg, #C7000B, #FF5A4E)',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
  },
  {
    title: '里程碑触发动态授信',
    desc: '以研发里程碑进度为触发器，实时调整授信额度。进度系数 × 风险系数动态计算，让资金精准匹配研发节奏。',
    tags: ['里程碑触发', '动态额度', '进度驱动'],
    iconBg: 'linear-gradient(135deg, #E8B34B, #F5D488)',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#0A1730" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
  },
  {
    title: '投贷联动工作台',
    desc: '股·债·保三维金融工具包智能匹配，从知识产权质押贷到可转债，覆盖硬科技企业全生命周期融资需求。',
    tags: ['股债保联动', '工具包匹配', '全周期覆盖'],
    iconBg: 'linear-gradient(135deg, #143061, #2A5298)',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M17 7V5a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v2"/></svg>',
  },
  {
    title: '风控看板',
    desc: '实时风险评分趋势监控，里程碑进度偏低与延迟自动预警，为投贷决策提供动态风险依据。',
    tags: ['实时监控', '智能预警', '风险趋势'],
    iconBg: 'linear-gradient(135deg, #0E2145, #1E4280)',
    icon: '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#F5D488" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
  },
]

const milestones = [
  { stage: '立项 / 预研', tools: '知识产权质押贷 + 研发补贴' },
  { stage: '原型验证', tools: 'AI 动态估值授信 + 股权跟投' },
  { stage: '流片 / 临床 II 期', tools: '投贷联动（银行授信 + VC 跟投）' },
  { stage: '商业化量产', tools: '供应链票据 + 订单融资' },
  { stage: '上市预备', tools: '可转债 + 科创专项债' },
]

function scrollTo(className: string) {
  const el = document.querySelector(`.${className}`)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

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
.home-view {
  padding: 0;
}

/* ===== Hero ===== */
.hero {
  position: relative;
  min-height: 520px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(135deg, #0A1730 0%, #0E2145 55%, #143061 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
  background: url('../assets/images/hero-bg.png') center / cover no-repeat;
  opacity: 0.22;
  filter: saturate(1.2);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 12% 10%, rgba(199, 0, 11, 0.18) 0%, transparent 60%),
              radial-gradient(ellipse at 90% 15%, rgba(232, 179, 75, 0.15) 0%, transparent 55%),
              linear-gradient(180deg, transparent 70%, #0A1730 100%);
}

.hero-content {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1200px;
  text-align: center;
  padding: 24px;
}

.hero-svg {
  width: 100%;
  max-width: 1100px;
  height: auto;
  filter: drop-shadow(0 8px 32px rgba(0, 0, 0, 0.4));
}

.hero-cta {
  margin-top: 20px;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.cta-secondary {
  background: transparent !important;
  border-color: #E8B34B !important;
  color: #F5D488 !important;
}
.cta-secondary:hover {
  background: rgba(232, 179, 75, 0.12) !important;
}

/* ===== Section Header ===== */
.section-header {
  text-align: center;
  padding: 48px 24px 32px;
  background: #0A1730;
}

.section-title {
  font-size: 30px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 2px;
}
.section-title::after {
  content: '';
  display: block;
  width: 48px;
  height: 3px;
  margin: 12px auto 0;
  background: linear-gradient(90deg, #C7000B, #E8B34B);
  border-radius: 2px;
}

.section-subtitle {
  margin-top: 12px;
  font-size: 15px;
  color: #9FB4DA;
  letter-spacing: 1px;
}

.section-header.light {
  background: #0E2145;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px 24px 16px;
  text-align: left;
}
.section-title.light {
  font-size: 24px;
  color: #fff;
}
.section-title.light::after {
  margin: 8px 0 0;
}

/* ===== Capability Cards ===== */
.capability-section {
  background: #0A1730;
  padding-bottom: 56px;
}

.capability-grid {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.capability-card {
  background: linear-gradient(160deg, rgba(20, 48, 97, 0.6), rgba(14, 33, 69, 0.4));
  border: 1px solid rgba(91, 125, 187, 0.25);
  border-radius: 12px;
  padding: 28px 20px;
  transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
  backdrop-filter: blur(8px);
}
.capability-card:hover {
  transform: translateY(-6px);
  border-color: rgba(232, 179, 75, 0.5);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.cap-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.cap-title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 8px;
}

.cap-desc {
  font-size: 13px;
  line-height: 1.7;
  color: #9FB4DA;
  margin-bottom: 14px;
}

.cap-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.cap-tag {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 10px;
  background: rgba(232, 179, 75, 0.12);
  color: #F5D488;
  border: 1px solid rgba(232, 179, 75, 0.2);
}

/* ===== Milestone Flow ===== */
.milestone-section {
  background: linear-gradient(180deg, #0A1730 0%, #0E2145 100%);
  padding-bottom: 56px;
}

.milestone-flow {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.ms-step {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.ms-node {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(199, 0, 11, 0.15);
  border: 2px solid #C7000B;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  position: relative;
  z-index: 2;
}
.ms-step.ms-active .ms-node {
  background: rgba(255, 90, 78, 0.2);
  border-color: #FF5A4E;
  box-shadow: 0 0 20px rgba(255, 90, 78, 0.4);
}

.ms-index {
  font-size: 18px;
  font-weight: 700;
  color: #F5D488;
}

.ms-info {
  max-width: 180px;
}

.ms-stage {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 6px;
}

.ms-tools {
  font-size: 12px;
  color: #9FB4DA;
  line-height: 1.6;
}

.ms-connector {
  position: absolute;
  top: 23px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #E8B34B, rgba(232, 179, 75, 0.3));
  z-index: 1;
}

/* ===== Enterprise Section ===== */
.enterprise-section {
  background: #0E2145;
  min-height: 400px;
  padding-bottom: 48px;
}

.enterprise-card {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  background: rgba(10, 23, 48, 0.5);
  border: 1px solid rgba(91, 125, 187, 0.2);
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  backdrop-filter: blur(8px);
}

/* ===== Responsive ===== */
@media (max-width: 1024px) {
  .capability-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .milestone-flow {
    flex-direction: column;
    gap: 24px;
  }
  .ms-connector {
    display: none;
  }
}

@media (max-width: 640px) {
  .capability-grid {
    grid-template-columns: 1fr;
  }
  .hero-svg {
    max-width: 100%;
  }
}
</style>
