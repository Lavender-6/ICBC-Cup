window.slideDataMap.set(1, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-cover.png');">

    <!-- 深色遮罩：左上深、右下略亮，保留城市天际线与光桥 -->
    <div class="absolute inset-0" style="background:linear-gradient(115deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.93) 38%, rgba(14,33,69,0.78) 62%, rgba(20,48,97,0.55) 100%);"></div>
    <!-- 金色光晕 -->
    <div class="absolute" style="top:-160px; right:-120px; width:760px; height:760px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.22) 0%, rgba(232,179,75,0.06) 45%, rgba(232,179,75,0) 70%);"></div>
    <!-- 红色微光 -->
    <div class="absolute" style="bottom:-200px; left:-100px; width:620px; height:620px; border-radius:9999px; background:radial-gradient(circle, rgba(199,0,11,0.20) 0%, rgba(199,0,11,0) 68%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 顶部赛事标识 -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="inline-block w-[3px] h-[22px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
          <span class="text-[15px] tracking-[4px] text-[#9FB4DA]">第十七届「工行杯」全国大学生金融科技创新大赛</span>
        </div>
        <div class="text-[14px] tracking-[3px] text-[#E8B34B]">科 技 金 融 方 向</div>
      </div>

      <!-- 主标题区 -->
      <div class="mt-[130px]">
        <div class="text-[16px] tracking-[8px] text-[#9FB4DA] mb-5">HARD-TECH FINANCING PLATFORM</div>
        <h1 class="font-title text-[76px] font-bold tracking-[6px] leading-none" style="color:#F5D488; text-shadow:0 4px 30px rgba(232,179,75,0.25);">
          工银科创桥
        </h1>
        <div class="mt-7 w-[220px] h-[4px]" style="background:linear-gradient(90deg,#C7000B 0%,#E8B34B 100%);"></div>
        <h2 class="mt-7 text-[30px] tracking-[3px] text-[#E0E6F0] font-normal">
          硬科技企业里程碑式投贷联动平台
        </h2>
        <p class="mt-8 text-[22px] tracking-[2px]" style="color:#F5D488;">
          让研发的每一步，都成为可计量的信用
        </p>
      </div>

      <!-- 底部能力标签 -->
      <div class="absolute bottom-[60px] left-0 flex items-center gap-4">
        <div class="px-5 py-[10px] text-[15px] tracking-[1px]"
             style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.35); color:#9FB4DA; backdrop-filter:blur(8px);">
          AI 动态估值
        </div>
        <div class="px-5 py-[10px] text-[15px] tracking-[1px]"
             style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.35); color:#9FB4DA; backdrop-filter:blur(8px);">
          专利知识图谱
        </div>
        <div class="px-5 py-[10px] text-[15px] tracking-[1px]"
             style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.35); color:#9FB4DA; backdrop-filter:blur(8px);">
          里程碑触发
        </div>
        <div class="px-5 py-[10px] text-[15px] tracking-[1px]"
             style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.35); color:#9FB4DA; backdrop-filter:blur(8px);">
          投贷联动
        </div>
      </div>

      <!-- 右下角时长 -->
      <div class="absolute bottom-[60px] right-0 text-right">
        <div class="text-[40px] font-bold font-title" style="color:#E8B34B;">8<span class="text-[20px]"> min</span></div>
        <div class="text-[13px] tracking-[2px] text-[#9FB4DA] mt-1">项目汇报 · 20 页</div>
      </div>

    </div>
  </div>
`);
