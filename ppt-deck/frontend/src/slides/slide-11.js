window.slideDataMap.set(11, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-banker-human.png'); background-position:center right;">

    <div class="absolute inset-0" style="background:linear-gradient(108deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.93) 40%, rgba(14,33,69,0.70) 70%, rgba(20,48,97,0.50) 100%);"></div>
    <div class="absolute" style="top:-220px; left:-180px; width:720px; height:720px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.18) 0%, rgba(232,179,75,0) 68%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto flex gap-[28px]" style="margin-top:45px;">

      <!-- 左：解说 -->
      <div class="w-[380px] flex-shrink-0">
        <div class="flex items-center gap-3">
          <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
          <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 01 · 产品演示 01</span>
        </div>
        <h2 class="mt-4 text-[34px] font-bold tracking-[2px] leading-[46px]" style="color:#F5D488;">企业画像<br/>非财务资产如何被定价</h2>
        <div class="mt-5 w-[140px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

        <p class="mt-8 text-[16px] leading-[30px]" style="color:#E0E6F0;">
          系统把一家没有厂房、没有利润的硬科技企业，翻译成六个可直接比较的量化指标。
        </p>

        <div class="mt-8 p-[18px]" style="background:rgba(232,179,75,0.10); border-left:4px solid #E8B34B; backdrop-filter:blur(8px);">
          <div class="text-[13px] tracking-[2px] text-[#9FB4DA]">演 示 重 点</div>
          <p class="mt-3 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            切换不同企业时，估值与风险评分随专利质量、团队构成实时联动；右上角标注估值来源，结果<span style="color:#F5D488;">可追溯</span>。
          </p>
        </div>

        <div class="mt-8 flex items-center gap-3">
          <span class="w-[10px] h-[10px]" style="background:#E8B34B; border-radius:9999px;"></span>
          <span class="text-[14px] text-[#9FB4DA]">三个核心模块协同输出</span>
        </div>
      </div>

      <!-- 右：产品界面模拟 -->
      <div class="flex-1 flex flex-col">
        <!-- 窗口栏 -->
        <div class="h-[34px] flex items-center px-[16px] gap-[8px]" style="background:rgba(10,23,48,0.85); border:1px solid rgba(91,125,187,0.30); border-bottom:none;">
          <span class="w-[10px] h-[10px]" style="background:#FF5A4E; border-radius:9999px;"></span>
          <span class="w-[10px] h-[10px]" style="background:#E8B34B; border-radius:9999px;"></span>
          <span class="w-[10px] h-[10px]" style="background:#5B7DBB; border-radius:9999px;"></span>
          <span class="ml-3 text-[13px] text-[#9FB4DA]">工银科创桥 · 企业画像</span>
          <span class="ml-auto text-[12px] px-2 py-[2px]" style="background:rgba(232,179,75,0.16); border:1px solid rgba(232,179,75,0.45); color:#F5D488;">估值来源：ML 模型</span>
        </div>

        <!-- 主体 -->
        <div class="flex-1 p-[18px] flex flex-col gap-[14px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); backdrop-filter:blur(8px);">

          <!-- 模块1 -->
          <div class="flex gap-[14px]">
            <div class="w-[300px] p-[14px]" style="background:rgba(20,48,97,0.55); border:1px solid rgba(91,125,187,0.25);">
              <div class="text-[14px] tracking-[2px] text-[#9FB4DA]">基础信息</div>
              <div class="mt-3 space-y-[8px]">
                <div class="flex justify-between text-[14px]"><span class="text-[#9FB4DA]">所属行业</span><span style="color:#E0E6F0;">半导体</span></div>
                <div class="flex justify-between text-[14px]"><span class="text-[#9FB4DA]">研发阶段</span><span style="color:#E0E6F0;">原型验证</span></div>
                <div class="flex justify-between text-[14px]"><span class="text-[#9FB4DA]">员工人数</span><span style="color:#F5D488;">86 人</span></div>
                <div class="flex justify-between text-[14px]"><span class="text-[#9FB4DA]">研发占比</span><span style="color:#F5D488;">42%</span></div>
              </div>
            </div>

            <div class="flex-1 p-[14px]" style="background:rgba(20,48,97,0.55); border:1px solid rgba(91,125,187,0.25);">
              <div class="flex items-center justify-between">
                <span class="text-[14px] tracking-[2px] text-[#9FB4DA]">AI 估值结果</span>
                <span class="text-[13px] text-[#9FB4DA]">6 项指标同步输出</span>
              </div>
              <div class="mt-3 grid grid-cols-3 gap-[10px]">
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(91,125,187,0.22);">
                  <div class="text-[19px] font-bold" style="color:#F5D488;">8,600<span class="text-[12px]">万</span></div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">当前估值</div>
                </div>
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(91,125,187,0.22);">
                  <div class="text-[19px] font-bold" style="color:#F5D488;">7,200<span class="text-[12px]">万</span></div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">基础估值</div>
                </div>
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(199,0,11,0.35);">
                  <div class="text-[19px] font-bold" style="color:#FF5A4E;">18.4%</div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">风险评分</div>
                </div>
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(91,125,187,0.22);">
                  <div class="text-[19px] font-bold" style="color:#F5D488;">37</div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">专利数量</div>
                </div>
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(91,125,187,0.22);">
                  <div class="text-[19px] font-bold" style="color:#F5D488;">0.82</div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">平均专利质量</div>
                </div>
                <div class="p-[10px] text-center" style="background:rgba(10,23,48,0.55); border:1px solid rgba(91,125,187,0.22);">
                  <div class="text-[19px] font-bold" style="color:#F5D488;">88</div>
                  <div class="mt-1 text-[12px] text-[#9FB4DA]">团队评分</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 模块3 -->
          <div class="flex-1 p-[14px]" style="background:rgba(20,48,97,0.55); border:1px solid rgba(91,125,187,0.25);">
            <div class="flex items-center justify-between">
              <span class="text-[14px] tracking-[2px] text-[#9FB4DA]">研发团队画像</span>
              <span class="text-[13px] text-[#9FB4DA]">加权评分：论文 20% · 引用 20% · H 指数 15% · 专利 25% · 经验 20%</span>
            </div>
            <div class="mt-4 space-y-[10px]">
              <div class="flex items-center gap-4">
                <span class="w-[86px] text-[13px] text-[#9FB4DA]">学术论文</span>
                <div class="flex-1 h-[10px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:62%; height:100%; background:linear-gradient(90deg,#5B7DBB,#9FB4DA);"></div>
                </div>
                <span class="w-[52px] text-right text-[13px]" style="color:#F5D488;">20%</span>
              </div>
              <div class="flex items-center gap-4">
                <span class="w-[86px] text-[13px] text-[#9FB4DA]">引用总量</span>
                <div class="flex-1 h-[10px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:70%; height:100%; background:linear-gradient(90deg,#5B7DBB,#9FB4DA);"></div>
                </div>
                <span class="w-[52px] text-right text-[13px]" style="color:#F5D488;">20%</span>
              </div>
              <div class="flex items-center gap-4">
                <span class="w-[86px] text-[13px] text-[#9FB4DA]">H 指数</span>
                <div class="flex-1 h-[10px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:46%; height:100%; background:linear-gradient(90deg,#E8B34B,#F5D488);"></div>
                </div>
                <span class="w-[52px] text-right text-[13px]" style="color:#F5D488;">15%</span>
              </div>
              <div class="flex items-center gap-4">
                <span class="w-[86px] text-[13px] text-[#9FB4DA]">专利产出</span>
                <div class="flex-1 h-[10px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:88%; height:100%; background:linear-gradient(90deg,#C7000B,#FF5A4E);"></div>
                </div>
                <span class="w-[52px] text-right text-[13px]" style="color:#F5D488;">25%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
`);
