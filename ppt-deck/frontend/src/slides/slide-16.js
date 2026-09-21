window.slideDataMap.set(16, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-network.png');">

    <div class="absolute inset-0" style="background:linear-gradient(160deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.92) 48%, rgba(14,33,69,0.74) 100%);"></div>
    <div class="absolute" style="top:-200px; right:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(91,125,187,0.20) 0%, rgba(91,125,187,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; left:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.16) 0%, rgba(232,179,75,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 02 · 技术架构</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">四层解耦：从交互界面到底层模型</h2>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <!-- 四层 -->
      <div class="mt-[26px] flex flex-col gap-[14px]">
        <!-- 展现层 -->
        <div class="flex items-stretch" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:5px solid #F5D488; backdrop-filter:blur(8px);">
          <div class="w-[190px] flex-shrink-0 px-5 py-[16px] flex flex-col justify-center" style="border-right:1px solid rgba(91,125,187,0.22);">
            <div class="text-[12px] tracking-[2px] text-[#9FB4DA]">LAYER 01</div>
            <div class="mt-1 text-[20px] font-bold" style="color:#F5D488;">展现层</div>
          </div>
          <div class="flex-1 px-6 py-[16px]">
            <div class="flex flex-wrap gap-[10px]">
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Vue 3 Composition API</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">TypeScript</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Vite 5</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Element Plus</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">ECharts 5</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Pinia</span>
            </div>
            <div class="mt-3 text-[13px] text-[#9FB4DA]">玻璃拟态深色主题 · 1024px / 640px 双断点响应式</div>
          </div>
        </div>

        <!-- 服务层 -->
        <div class="flex items-stretch" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:5px solid #E8B34B; backdrop-filter:blur(8px);">
          <div class="w-[190px] flex-shrink-0 px-5 py-[16px] flex flex-col justify-center" style="border-right:1px solid rgba(91,125,187,0.22);">
            <div class="text-[12px] tracking-[2px] text-[#9FB4DA]">LAYER 02</div>
            <div class="mt-1 text-[20px] font-bold" style="color:#F5D488;">服务层</div>
          </div>
          <div class="flex-1 px-6 py-[16px]">
            <div class="flex flex-wrap gap-[10px]">
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">FastAPI</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">SQLAlchemy 2</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">企业服务</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">估值服务</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">授信服务</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">风控服务</span>
            </div>
            <div class="mt-3 text-[13px] text-[#9FB4DA]">四组业务服务 · 13 个 REST 端点对外暴露</div>
          </div>
        </div>

        <!-- AI 推理层 -->
        <div class="flex items-stretch" style="background:rgba(20,48,97,0.80); border:1px solid rgba(232,179,75,0.42); border-left:5px solid #C7000B; backdrop-filter:blur(8px); box-shadow:0 0 26px rgba(199,0,11,0.14);">
          <div class="w-[190px] flex-shrink-0 px-5 py-[16px] flex flex-col justify-center" style="border-right:1px solid rgba(91,125,187,0.22);">
            <div class="text-[12px] tracking-[2px] text-[#9FB4DA]">LAYER 03</div>
            <div class="mt-1 text-[20px] font-bold" style="color:#F5D488;">AI 推理层</div>
          </div>
          <div class="flex-1 px-6 py-[16px]">
            <div class="flex flex-wrap gap-[10px]">
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(199,0,11,0.14); border:1px solid rgba(199,0,11,0.40); color:#FF5A4E;">XGBoost 估值模型</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(199,0,11,0.14); border:1px solid rgba(199,0,11,0.40); color:#FF5A4E;">XGBoost 破产风险模型</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(232,179,75,0.12); border:1px solid rgba(232,179,75,0.40); color:#F5D488;">NetworkX PageRank</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">.joblib 热加载</span>
            </div>
            <div class="mt-3 text-[13px] text-[#9FB4DA]">双模型并行推理 ＋ 图计算，统一封装为单次 API 调用</div>
          </div>
        </div>

        <!-- 数据层 -->
        <div class="flex items-stretch" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:5px solid #5B7DBB; backdrop-filter:blur(8px);">
          <div class="w-[190px] flex-shrink-0 px-5 py-[16px] flex flex-col justify-center" style="border-right:1px solid rgba(91,125,187,0.22);">
            <div class="text-[12px] tracking-[2px] text-[#9FB4DA]">LAYER 04</div>
            <div class="mt-1 text-[20px] font-bold" style="color:#F5D488;">数据层</div>
          </div>
          <div class="flex-1 px-6 py-[16px]">
            <div class="flex flex-wrap gap-[10px]">
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Enterprise</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Patent / PatentCitation</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">TeamMember</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">Milestone / FinancialTool</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">CreditRecord / RiskAlert</span>
              <span class="px-3 py-[6px] text-[14px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.28); color:#E0E6F0;">SQLite / MySQL</span>
            </div>
            <div class="mt-3 text-[13px] text-[#9FB4DA]">含 95 维财务特征 JSON · Redis 可选，降级不影响主流程</div>
          </div>
        </div>
      </div>

    </div>
  </div>
`);
