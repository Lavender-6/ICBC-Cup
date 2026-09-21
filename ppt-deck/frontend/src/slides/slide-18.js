window.slideDataMap.set(18, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-network.png');">

    <div class="absolute inset-0" style="background:linear-gradient(140deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.92) 46%, rgba(14,33,69,0.74) 100%);"></div>
    <div class="absolute" style="top:-200px; left:-160px; width:700px; height:700px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.18) 0%, rgba(232,179,75,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; right:-160px; width:680px; height:680px; border-radius:9999px; background:radial-gradient(circle, rgba(199,0,11,0.14) 0%, rgba(199,0,11,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center gap-3">
        <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
        <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 02 · 图算法</span>
      </div>
      <h2 class="mt-4 text-[36px] font-bold tracking-[2px]" style="color:#F5D488;">用图算法量化一件专利的真实影响力</h2>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <div class="mt-[26px] flex gap-[22px]">
        <!-- 左侧：为什么与算法 -->
        <div class="flex-1 flex flex-col gap-[16px]">
          <div class="p-[20px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:4px solid #E8B34B; backdrop-filter:blur(8px);">
            <div class="text-[19px] font-bold" style="color:#F5D488;">为什么用「图」而不是「计数」</div>
            <p class="mt-3 text-[15px] leading-[27px]" style="color:#E0E6F0;">
              专利的价值不只在于被引用多少次，更在于它在整个技术脉络中的<span style="color:#F5D488;">位置</span>——被一件核心专利引用，与被一件边缘专利引用，含金量完全不同。
            </p>
          </div>

          <div class="p-[20px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:4px solid #C7000B; backdrop-filter:blur(8px);">
            <div class="text-[19px] font-bold" style="color:#F5D488;">算法实现</div>
            <p class="mt-3 text-[15px] leading-[27px]" style="color:#E0E6F0;">
              以 NetworkX 构建<span style="color:#F5D488;">有向引用图</span>（专利为节点、引用关系为边），运行 PageRank（<span style="color:#F5D488;">alpha = 0.85</span>）计算每件专利的中心性权重。
            </p>
          </div>

          <div class="p-[20px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); border-left:4px solid #5B7DBB; backdrop-filter:blur(8px);">
            <div class="text-[19px] font-bold" style="color:#F5D488;">如何进入风控链路</div>
            <p class="mt-3 text-[15px] leading-[27px]" style="color:#E0E6F0;">
              PageRank 结果作为专利质量的维度之一合成质量分，再回流为企业估值与授信输入——让图计算的产出<span style="color:#F5D488;">直接作用于额度</span>。
            </p>
          </div>
        </div>

        <!-- 右侧：可视化与权重 -->
        <div class="w-[520px] flex flex-col gap-[16px]">
          <div class="p-[18px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); backdrop-filter:blur(8px);">
            <div class="flex items-center justify-between">
              <span class="text-[16px] font-semibold" style="color:#F5D488;">引用网络中的节点位置</span>
              <span class="text-[13px] text-[#9FB4DA]">节点越大，中心性越高</span>
            </div>
            <div class="mt-3 flex items-center justify-center">
              <svg width="470" height="196" viewBox="0 0 470 196">
                <g stroke="#5B7DBB" stroke-width="1.4" opacity="0.55">
                  <line x1="60" y1="98" x2="160" y2="40"/>
                  <line x1="60" y1="98" x2="160" y2="156"/>
                  <line x1="160" y1="40" x2="275" y2="98"/>
                  <line x1="160" y1="156" x2="275" y2="98"/>
                  <line x1="275" y1="98" x2="380" y2="46"/>
                  <line x1="275" y1="98" x2="380" y2="150"/>
                  <line x1="380" y1="46" x2="440" y2="98"/>
                  <line x1="380" y1="150" x2="440" y2="98"/>
                </g>
                <circle cx="60" cy="98" r="12" fill="#5B7DBB" opacity="0.85"/>
                <circle cx="160" cy="40" r="15" fill="#E8B34B"/>
                <circle cx="160" cy="156" r="11" fill="#5B7DBB" opacity="0.85"/>
                <circle cx="275" cy="98" r="26" fill="#E8B34B"/>
                <circle cx="380" cy="46" r="13" fill="#F5D488"/>
                <circle cx="380" cy="150" r="10" fill="#5B7DBB" opacity="0.85"/>
                <circle cx="440" cy="98" r="9" fill="#C7000B"/>
                <text x="248" y="136" fill="#F5D488" font-size="12">枢纽专利</text>
              </svg>
            </div>
          </div>

          <div class="flex-1 p-[18px]" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); backdrop-filter:blur(8px);">
            <div class="text-[16px] font-semibold" style="color:#F5D488;">专利质量评分构成</div>
            <div class="mt-4 space-y-[11px]">
              <div class="flex items-center gap-3">
                <span class="w-[86px] text-[14px] text-[#9FB4DA]">引用次数</span>
                <div class="flex-1 h-[12px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:100%; height:100%; background:linear-gradient(90deg,#5B7DBB,#9FB4DA);"></div>
                </div>
                <span class="w-[46px] text-right text-[14px]" style="color:#F5D488;">30%</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="w-[86px] text-[14px] text-[#9FB4DA]">PageRank</span>
                <div class="flex-1 h-[12px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:83%; height:100%; background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>
                </div>
                <span class="w-[46px] text-right text-[14px]" style="color:#F5D488;">25%</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="w-[86px] text-[14px] text-[#9FB4DA]">同族规模</span>
                <div class="flex-1 h-[12px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:67%; height:100%; background:linear-gradient(90deg,#5B7DBB,#9FB4DA);"></div>
                </div>
                <span class="w-[46px] text-right text-[14px]" style="color:#F5D488;">20%</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="w-[86px] text-[14px] text-[#9FB4DA]">国际布局</span>
                <div class="flex-1 h-[12px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:50%; height:100%; background:linear-gradient(90deg,#5B7DBB,#9FB4DA);"></div>
                </div>
                <span class="w-[46px] text-right text-[14px]" style="color:#F5D488;">15%</span>
              </div>
              <div class="flex items-center gap-3">
                <span class="w-[86px] text-[14px] text-[#9FB4DA]">诉讼情况</span>
                <div class="flex-1 h-[12px]" style="background:rgba(91,125,187,0.20);">
                  <div style="width:33%; height:100%; background:linear-gradient(90deg,#E8B34B,#F5D488);"></div>
                </div>
                <span class="w-[46px] text-right text-[14px]" style="color:#F5D488;">10%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部差异化 -->
      <div class="absolute bottom-[46px] left-0 w-full px-6 py-[16px] flex items-center gap-4"
           style="background:rgba(232,179,75,0.10); border-left:4px solid #E8B34B; backdrop-filter:blur(8px);">
        <span class="text-[14px] tracking-[2px] whitespace-nowrap" style="color:#E8B34B;">差异化价值</span>
        <span class="text-[16px]" style="color:#E0E6F0;">
          把单件专利从「一个计数」升级为「一个位置」，让银行的知识产权评估<span style="color:#F5D488;">从数量逻辑走向结构逻辑</span>
        </span>
      </div>

    </div>
  </div>
`);
