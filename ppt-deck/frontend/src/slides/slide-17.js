window.slideDataMap.set(17, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-lab-human.png'); background-position:center right;">

    <div class="absolute inset-0" style="background:linear-gradient(112deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.93) 40%, rgba(14,33,69,0.70) 70%, rgba(20,48,97,0.50) 100%);"></div>
    <div class="absolute" style="top:-200px; left:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.20) 0%, rgba(232,179,75,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; right:-160px; width:680px; height:680px; border-radius:9999px; background:radial-gradient(circle, rgba(199,0,11,0.16) 0%, rgba(199,0,11,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 02 · AI 引擎</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">两个 XGBoost 模型，撑起估值与风险两侧</h2>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <!-- 双模型 -->
      <div class="mt-[24px] flex gap-[20px]">
        <!-- 估值模型 -->
        <div class="flex-1 p-[20px]" style="background:rgba(14,33,69,0.74); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #E8B34B; backdrop-filter:blur(8px);">
          <div class="flex items-center justify-between">
            <span class="text-[22px] font-bold" style="color:#F5D488;">估值预测模型</span>
            <span class="text-[13px] px-3 py-1" style="background:rgba(232,179,75,0.14); border:1px solid rgba(232,179,75,0.45); color:#F5D488;">Regressor</span>
          </div>

          <!-- 核心指标 -->
          <div class="mt-4 flex gap-[12px]">
            <div class="flex-1 p-[12px] text-center" style="background:rgba(10,23,48,0.60); border:1px solid rgba(232,179,75,0.32);">
              <div class="text-[30px] font-bold font-title" style="color:#F5D488;">0.927</div>
              <div class="mt-1 text-[12px] text-[#9FB4DA]">基础估值 R²</div>
            </div>
            <div class="flex-1 p-[12px] text-center" style="background:rgba(10,23,48,0.60); border:1px solid rgba(232,179,75,0.32);">
              <div class="text-[30px] font-bold font-title" style="color:#F5D488;">0.954</div>
              <div class="mt-1 text-[12px] text-[#9FB4DA]">当前估值 R²</div>
            </div>
          </div>

          <div class="mt-4 space-y-[8px]">
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">训练样本</span><span style="color:#E0E6F0;">2000 条硬科技企业数据</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">输入特征</span><span style="color:#E0E6F0;">8 个（含行业与阶段类别）</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">模型配置</span><span style="color:#E0E6F0;">300 棵树 · max_depth = 6</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">预处理</span><span style="color:#E0E6F0;">OneHotEncoder ＋ 数值直通</span>
            </div>
          </div>

          <div class="mt-4 pt-3" style="border-top:1px dashed rgba(91,125,187,0.30);">
            <div class="text-[13px] tracking-[2px] text-[#9FB4DA]">特 征 工 程</div>
            <p class="mt-2 text-[13px] leading-[22px]" style="color:#E0E6F0;">
              引入非线性与交互项：patent_count^0.7、team_score^1.5、log(employee_count)、√（质量 × 团队评分）
            </p>
          </div>
        </div>

        <!-- 风险模型 -->
        <div class="flex-1 p-[20px]" style="background:rgba(14,33,69,0.74); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #C7000B; backdrop-filter:blur(8px);">
          <div class="flex items-center justify-between">
            <span class="text-[22px] font-bold" style="color:#F5D488;">破产风险预测模型</span>
            <span class="text-[13px] px-3 py-1" style="background:rgba(199,0,11,0.16); border:1px solid rgba(199,0,11,0.45); color:#FF5A4E;">Classifier</span>
          </div>

          <div class="mt-4 flex gap-[12px]">
            <div class="flex-1 p-[12px] text-center" style="background:rgba(10,23,48,0.60); border:1px solid rgba(199,0,11,0.32);">
              <div class="text-[30px] font-bold font-title" style="color:#FF5A4E;">0.958</div>
              <div class="mt-1 text-[12px] text-[#9FB4DA]">AUC</div>
            </div>
            <div class="flex-1 p-[12px] text-center" style="background:rgba(10,23,48,0.60); border:1px solid rgba(199,0,11,0.32);">
              <div class="text-[30px] font-bold font-title" style="color:#FF5A4E;">96.9<span class="text-[16px]">%</span></div>
              <div class="mt-1 text-[12px] text-[#9FB4DA]">Accuracy</div>
            </div>
          </div>

          <div class="mt-4 space-y-[8px]">
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">训练数据</span><span style="color:#E0E6F0;">真实企业财务公开数据集 6819 条</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">特征维度</span><span style="color:#E0E6F0;">95 个财务特征</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">类别分布</span><span style="color:#E0E6F0;">未破产 6599 vs 破产 220</span>
            </div>
            <div class="flex justify-between text-[14px]">
              <span class="text-[#9FB4DA]">不平衡处理</span><span style="color:#E0E6F0;">scale_pos_weight = 30</span>
            </div>
          </div>

          <div class="mt-4 pt-3" style="border-top:1px dashed rgba(91,125,187,0.30);">
            <div class="text-[13px] tracking-[2px] text-[#9FB4DA]">T O P 5 特 征</div>
            <p class="mt-2 text-[13px] leading-[22px]" style="color:#E0E6F0;">
              税后持续利率 12.9% · 近四季持续 EPS 7.7% · 净利润/总资产 7.4% · 净值/资产 4.1% · 借款依赖度 4.1%
            </p>
          </div>
        </div>
      </div>

      <!-- 推理链路 -->
      <div class="absolute bottom-[46px] left-0 w-full px-6 py-[16px] flex items-center gap-4"
           style="background:rgba(14,33,69,0.62); border-left:4px solid #E8B34B; backdrop-filter:blur(8px);">
        <span class="text-[14px] tracking-[2px] whitespace-nowrap" style="color:#E8B34B;">推理链路</span>
        <span class="text-[16px]" style="color:#E0E6F0;">
          请求进入 → 组装特征（专利数 · PageRank 质量 · 团队评分） → <span style="color:#F5D488;">双模型并行推理</span> → 输出基础/当前估值与风险评分 → 异常时回退规则公式
        </span>
      </div>

    </div>
  </div>
`);
