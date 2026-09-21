window.slideDataMap.set(19, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-circuit.png');">

    <div class="absolute inset-0" style="background:linear-gradient(175deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.92) 48%, rgba(14,33,69,0.74) 100%);"></div>
    <div class="absolute" style="top:-200px; right:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(91,125,187,0.20) 0%, rgba(91,125,187,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; left:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.16) 0%, rgba(232,179,75,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 02 · 工程实现</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">让 AI 在银行生产环境里稳定落地</h2>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <!-- 前两个亮点 -->
      <div class="mt-[26px] flex gap-[18px]">
        <div class="flex-1 p-[20px]" style="background:rgba(20,48,97,0.78); border:1px solid rgba(232,179,75,0.42); border-top:4px solid #E8B34B; backdrop-filter:blur(8px); box-shadow:0 0 24px rgba(232,179,75,0.10);">
          <div class="flex items-center gap-3">
            <span class="w-[30px] h-[30px] flex items-center justify-center text-[15px] font-bold" style="background:rgba(232,179,75,0.18); border:1px solid rgba(232,179,75,0.5); color:#F5D488;">1</span>
            <span class="text-[21px] font-bold" style="color:#F5D488;">优雅降级</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            模型文件缺失或推理失败时，自动回退到规则公式，并在结果中标注估值来源——<span style="color:#F5D488;">保证服务可用性不因模型异常中断</span>。这是银行级系统的必备能力。
          </p>
        </div>

        <div class="flex-1 p-[20px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #C7000B; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[30px] h-[30px] flex items-center justify-center text-[15px] font-bold" style="background:rgba(199,0,11,0.20); border:1px solid rgba(199,0,11,0.5); color:#FF5A4E;">2</span>
            <span class="text-[21px] font-bold" style="color:#F5D488;">实时联动</span>
          </div>
          <p class="mt-4 text-[15px] leading-[27px]" style="color:#E0E6F0;">
            里程碑进度滑块拖动时，状态流转与授信额度同步重算；任一要素调整后全部指标一并刷新，做到<span style="color:#F5D488;">所见即所得</span>。
          </p>
        </div>
      </div>

      <!-- 后三个亮点 -->
      <div class="mt-[18px] flex gap-[18px]">
        <div class="flex-1 p-[18px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #5B7DBB; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[28px] h-[28px] flex items-center justify-center text-[14px] font-bold" style="background:rgba(91,125,187,0.22); border:1px solid rgba(91,125,187,0.5); color:#9FB4DA;">3</span>
            <span class="text-[19px] font-bold" style="color:#F5D488;">可追溯性</span>
          </div>
          <p class="mt-3 text-[14px] leading-[25px]" style="color:#E0E6F0;">
            估值与风险结果均标注产出来源（ML 模型 / 规则回退），便于风控人员复核与<span style="color:#F5D488;">监管审计</span>。
          </p>
        </div>

        <div class="flex-1 p-[18px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #F5D488; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[28px] h-[28px] flex items-center justify-center text-[14px] font-bold" style="background:rgba(245,212,136,0.18); border:1px solid rgba(245,212,136,0.5); color:#F5D488;">4</span>
            <span class="text-[19px] font-bold" style="color:#F5D488;">可视化与响应式</span>
          </div>
          <p class="mt-3 text-[14px] leading-[25px]" style="color:#E0E6F0;">
            ECharts 深色主题深度适配；7 个业务组件、6 类图表形态，支持 <span style="color:#F5D488;">1024px 与 640px</span> 断点自适应。
          </p>
        </div>

        <div class="flex-1 p-[18px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #FF5A4E; backdrop-filter:blur(8px);">
          <div class="flex items-center gap-3">
            <span class="w-[28px] h-[28px] flex items-center justify-center text-[14px] font-bold" style="background:rgba(199,0,11,0.20); border:1px solid rgba(199,0,11,0.5); color:#FF5A4E;">5</span>
            <span class="text-[19px] font-bold" style="color:#F5D488;">链路完整性</span>
          </div>
          <p class="mt-3 text-[14px] leading-[25px]" style="color:#E0E6F0;">
            <span style="color:#F5D488;">13 个 REST 端点</span>覆盖企业、估值、团队、专利、里程碑、授信、风控全链路。
          </p>
        </div>
      </div>

      <!-- 底部技术栈汇总 -->
      <div class="absolute bottom-[46px] left-0 w-full flex items-center gap-[14px]">
        <div class="px-5 py-[12px] text-[15px]" style="background:rgba(232,179,75,0.12); border:1px solid rgba(232,179,75,0.35); color:#F5D488;">Vue 3 + TypeScript</div>
        <div class="px-5 py-[12px] text-[15px]" style="background:rgba(232,179,75,0.12); border:1px solid rgba(232,179,75,0.35); color:#F5D488;">FastAPI + SQLAlchemy 2</div>
        <div class="px-5 py-[12px] text-[15px]" style="background:rgba(199,0,11,0.12); border:1px solid rgba(199,0,11,0.35); color:#FF5A4E;">XGBoost + scikit-learn</div>
        <div class="px-5 py-[12px] text-[15px]" style="background:rgba(199,0,11,0.12); border:1px solid rgba(199,0,11,0.35); color:#FF5A4E;">NetworkX PageRank</div>
        <div class="px-5 py-[12px] text-[15px]" style="background:rgba(20,48,97,0.62); border:1px solid rgba(91,125,187,0.30); color:#9FB4DA;">SQLite / MySQL + Redis（可选）</div>
      </div>

    </div>
  </div>
`);
