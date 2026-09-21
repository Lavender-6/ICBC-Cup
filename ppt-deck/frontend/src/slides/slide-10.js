window.slideDataMap.set(10, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-lab-human.png'); background-position:center right;">

    <div class="absolute inset-0" style="background:linear-gradient(110deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.93) 42%, rgba(14,33,69,0.72) 72%, rgba(20,48,97,0.52) 100%);"></div>
    <div class="absolute" style="top:-200px; right:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.18) 0%, rgba(232,179,75,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; left:-160px; width:680px; height:680px; border-radius:9999px; background:radial-gradient(circle, rgba(199,0,11,0.16) 0%, rgba(199,0,11,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 01 · 落地验证</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">从实验室到量产：三类企业的融资推演</h2>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <!-- 三个行业 -->
      <div class="mt-[26px] flex gap-[20px]">
        <!-- 半导体 -->
        <div class="flex-1 flex flex-col p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #5B7DBB; backdrop-filter:blur(8px);">
          <div class="flex items-center justify-between">
            <span class="text-[22px] font-bold" style="color:#F5D488;">半导体芯片</span>
            <span class="text-[13px] px-3 py-1" style="background:rgba(91,125,187,0.18); border:1px solid rgba(91,125,187,0.45); color:#9FB4DA;">流片是关键节点</span>
          </div>
          <div class="mt-4 p-[14px]" style="background:rgba(199,0,11,0.10); border-left:3px solid #C7000B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">挑 战</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">流片成本高、研发周期长，没有可抵押的厂房设备</p>
          </div>
          <div class="mt-3 p-[14px]" style="background:rgba(232,179,75,0.10); border-left:3px solid #E8B34B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">推 演</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">
              原型验证阶段按 <span style="color:#F5D488;">25%</span> 释放额度；流片成功后触发投贷联动，比例升至 <span style="color:#F5D488;">40%</span>，银行授信与产业资本同步进入
            </p>
          </div>
          <div class="mt-3 pt-3 text-[13px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            参照：某 UWB 芯片企业以全量知识产权数据构建量化模型
          </div>
        </div>

        <!-- 生物医药 -->
        <div class="flex-1 flex flex-col p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #E8B34B; backdrop-filter:blur(8px);">
          <div class="flex items-center justify-between">
            <span class="text-[22px] font-bold" style="color:#F5D488;">生物医药</span>
            <span class="text-[13px] px-3 py-1" style="background:rgba(232,179,75,0.14); border:1px solid rgba(232,179,75,0.45); color:#F5D488;">临床 II 期</span>
          </div>
          <div class="mt-4 p-[14px]" style="background:rgba(199,0,11,0.10); border-left:3px solid #C7000B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">挑 战</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">临床周期长、成败二元化，传统财务报表「不好看」</p>
          </div>
          <div class="mt-3 p-[14px]" style="background:rgba(232,179,75,0.10); border-left:3px solid #E8B34B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">推 演</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">
              临床 II 期达标触发投贷联动；破产概率模型同步为「中试保融通」类保险提供<span style="color:#F5D488;">定价参考</span>
            </p>
          </div>
          <div class="mt-3 pt-3 text-[13px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            参照：某国家级中试平台获超 1 亿元中长期授信
          </div>
        </div>

        <!-- 高端装备 -->
        <div class="flex-1 flex flex-col p-[22px]" style="background:rgba(14,33,69,0.70); border:1px solid rgba(91,125,187,0.30); border-top:4px solid #C7000B; backdrop-filter:blur(8px);">
          <div class="flex items-center justify-between">
            <span class="text-[22px] font-bold" style="color:#F5D488;">高端装备 / 新材料</span>
            <span class="text-[13px] px-3 py-1" style="background:rgba(199,0,11,0.16); border:1px solid rgba(199,0,11,0.45); color:#FF5A4E;">量产爬坡</span>
          </div>
          <div class="mt-4 p-[14px]" style="background:rgba(199,0,11,0.10); border-left:3px solid #C7000B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">挑 战</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">中试放大阶段资金密集，但订单释放明显滞后</p>
          </div>
          <div class="mt-3 p-[14px]" style="background:rgba(232,179,75,0.10); border-left:3px solid #E8B34B;">
            <div class="text-[13px] tracking-[1px] text-[#9FB4DA]">推 演</div>
            <p class="mt-2 text-[15px] leading-[25px]" style="color:#E0E6F0;">
              量产阶段切换至供应链票据 + 订单融资（<span style="color:#F5D488;">30%</span>），<span style="color:#F5D488;">以真实订单替代抵押物</span>
            </p>
          </div>
          <div class="mt-3 pt-3 text-[13px] text-[#9FB4DA]" style="border-top:1px dashed rgba(91,125,187,0.30);">
            参照：某锂电材料企业经技术流评价获 6000 万元综合授信
          </div>
        </div>
      </div>

      <!-- 免责说明 -->
      <div class="absolute bottom-[46px] left-0 w-full px-6 py-[16px] flex items-center gap-4"
           style="background:rgba(199,0,11,0.12); border-left:4px solid #C7000B; backdrop-filter:blur(8px);">
        <span class="text-[14px] tracking-[2px] whitespace-nowrap" style="color:#FF5A4E;">合规说明</span>
        <span class="text-[16px]" style="color:#E0E6F0;">
          以上为基于公开报道情境的适用性推演，用于验证方案在不同硬科技赛道的适配能力，<span style="color:#F5D488;">并非本平台实际客户数据</span>
        </span>
      </div>

    </div>
  </div>
`);
