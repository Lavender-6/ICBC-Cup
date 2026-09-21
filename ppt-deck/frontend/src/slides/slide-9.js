window.slideDataMap.set(9, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-circuit.png');">

    <div class="absolute inset-0" style="background:linear-gradient(165deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.92) 48%, rgba(14,33,69,0.74) 100%);"></div>
    <div class="absolute" style="top:-200px; right:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(91,125,187,0.20) 0%, rgba(91,125,187,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; left:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.16) 0%, rgba(232,179,75,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 01 · 业务流程</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">从数据接入到额度释放：端到端闭环</h2>
      <div class="mt-3 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>
      <div class="mt-3 text-[16px] text-[#9FB4DA]">把分散的技术信号，压缩成一次可执行的授信决策</div>

      <!-- 四步流程 -->
      <div class="mt-[30px] flex items-start gap-[14px]">
        <div class="flex-1 p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #5B7DBB; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[34px] h-[34px] flex items-center justify-center text-[17px] font-bold"
                  style="background:rgba(91,125,187,0.20); border:1px solid rgba(91,125,187,0.55); color:#9FB4DA;">1</span>
            <span class="text-[21px] font-semibold" style="color:#F5D488;">数据接入</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            企业基础信息、专利数据与引用关系、团队成员学术产出，以及 95 维财务特征一次性归集。
          </p>
          <div class="mt-4 pt-3 text-[13px] leading-[22px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            输入：工商 + 知识产权 + 人才 + 财务
          </div>
        </div>

        <div class="flex items-center justify-center pt-[52px] w-[26px] flex-shrink-0">
          <div class="text-[22px]" style="color:#5B7DBB;">&#10230;</div>
        </div>

        <div class="flex-1 p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #E8B34B; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[34px] h-[34px] flex items-center justify-center text-[17px] font-bold"
                  style="background:rgba(232,179,75,0.18); border:1px solid rgba(232,179,75,0.55); color:#F5D488;">2</span>
            <span class="text-[21px] font-semibold" style="color:#F5D488;">AI 评估</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            XGBoost 估值模型输出动态估值，破产风险模型输出破产概率，PageRank 计算专利影响力。
          </p>
          <div class="mt-4 pt-3 text-[13px] leading-[22px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            产出：估值区间 + 风险评分 + 专利质量分
          </div>
        </div>

        <div class="flex items-center justify-center pt-[52px] w-[26px] flex-shrink-0">
          <div class="text-[22px]" style="color:#E8B34B;">&#10230;</div>
        </div>

        <div class="flex-1 p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #C7000B; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[34px] h-[34px] flex items-center justify-center text-[17px] font-bold"
                  style="background:rgba(199,0,11,0.20); border:1px solid rgba(199,0,11,0.55); color:#FF5A4E;">3</span>
            <span class="text-[21px] font-semibold" style="color:#F5D488;">工具匹配</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            按当前研发里程碑匹配金融工具包；拖动进度即可实时重算授信额度，所见即所得。
          </p>
          <div class="mt-4 pt-3 text-[13px] leading-[22px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            产出：工具包清单 + 可执行额度
          </div>
        </div>

        <div class="flex items-center justify-center pt-[52px] w-[26px] flex-shrink-0">
          <div class="text-[22px]" style="color:#C7000B;">&#10230;</div>
        </div>

        <div class="flex-1 p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #F5D488; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[34px] h-[34px] flex items-center justify-center text-[17px] font-bold"
                  style="background:rgba(245,212,136,0.18); border:1px solid rgba(245,212,136,0.55); color:#F5D488;">4</span>
            <span class="text-[21px] font-semibold" style="color:#F5D488;">动态风控</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            风险评分与里程碑进度双线跟踪；延迟或进度偏低自动预警，并联动调整授信额度。
          </p>
          <div class="mt-4 pt-3 text-[13px] leading-[22px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            产出：预警事件 + 额度动态调整
          </div>
        </div>
      </div>

      <!-- 底部指标 -->
      <div class="absolute bottom-[46px] left-0 w-full flex gap-[18px]">
        <div class="px-6 py-[16px]" style="border:1px solid rgba(91,125,187,0.30); background:rgba(14,33,69,0.55);">
          <span class="text-[26px] font-bold font-title" style="color:#F5D488;">13</span>
          <span class="ml-2 text-[14px] text-[#9FB4DA]">个 REST 端点，全链路贯通</span>
        </div>
        <div class="px-6 py-[16px]" style="border:1px solid rgba(91,125,187,0.30); background:rgba(14,33,69,0.55);">
          <span class="text-[26px] font-bold font-title" style="color:#F5D488;">95</span>
          <span class="ml-2 text-[14px] text-[#9FB4DA]">维财务特征用于风险建模</span>
        </div>
        <div class="px-6 py-[16px]" style="border:1px solid rgba(91,125,187,0.30); background:rgba(14,33,69,0.55);">
          <span class="text-[26px] font-bold font-title" style="color:#F5D488;">5</span>
          <span class="ml-2 text-[14px] text-[#9FB4DA]">个里程碑阶段各绑定工具包</span>
        </div>
        <div class="flex-1 px-6 py-[16px] flex items-center" style="background:rgba(232,179,75,0.10); border-left:4px solid #E8B34B;">
          <span class="text-[16px]" style="color:#E0E6F0;">模型异常时自动回退规则公式，<span style="color:#F5D488;">服务不中断</span></span>
        </div>
      </div>

    </div>
  </div>
`);
