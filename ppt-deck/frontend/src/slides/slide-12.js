window.slideDataMap.set(12, `
  <div class="w-[1440px] h-[810px] shadow-2xl relative overflow-hidden slide-bg font-body"
       style="background-image:url('/assets/images/bg-network.png');">

    <div class="absolute inset-0" style="background:linear-gradient(150deg, rgba(10,23,48,0.97) 0%, rgba(10,23,48,0.92) 46%, rgba(14,33,69,0.76) 100%);"></div>
    <div class="absolute" style="top:-200px; left:-160px; width:720px; height:720px; border-radius:9999px; background:radial-gradient(circle, rgba(232,179,75,0.18) 0%, rgba(232,179,75,0) 68%);"></div>
    <div class="absolute" style="bottom:-220px; right:-160px; width:680px; height:680px; border-radius:9999px; background:radial-gradient(circle, rgba(199,0,11,0.14) 0%, rgba(199,0,11,0) 70%);"></div>

    <div class="relative w-[1350px] h-[720px] mx-auto" style="margin-top:45px;">

      <!-- 页眉 -->
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-3">
            <span class="inline-block w-[3px] h-[20px]" style="background:linear-gradient(180deg,#E8B34B,#C7000B);"></span>
            <span class="text-[14px] tracking-[4px] text-[#E8B34B]">PART 01 · 产品演示 02</span>
          </div>
          <h2 class="mt-4 text-[34px] font-bold tracking-[2px]" style="color:#F5D488;">专利引用网络：让单件专利的影响力被看见</h2>
        </div>
        <div class="w-[220px] mt-3">
          <div class="text-[13px] text-[#9FB4DA] text-right">节点大小 ＝ PageRank 值</div>
          <div class="mt-2 text-[13px] text-[#9FB4DA] text-right">颜色 ＝ 质量等级</div>
        </div>
      </div>
      <div class="mt-4 w-[160px] h-[3px]" style="background:linear-gradient(90deg,#C7000B,#E8B34B);"></div>

      <!-- 两个图表面板 -->
      <div class="mt-[22px] flex gap-[20px]">
        <!-- 网络图 -->
        <div class="flex-1" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); backdrop-filter:blur(8px);">
          <div class="px-[18px] py-[14px] flex items-center justify-between" style="border-bottom:1px solid rgba(91,125,187,0.22);">
            <span class="text-[16px] font-semibold" style="color:#F5D488;">力导向引用网络</span>
            <span class="text-[13px] text-[#9FB4DA]">可拖拽漫游</span>
          </div>
          <div class="p-[12px] flex items-center justify-center">
            <svg width="520" height="392" viewBox="0 0 520 392">
              <g stroke="#5B7DBB" stroke-width="1.4" opacity="0.55">
                <line x1="90" y1="200" x2="200" y2="110"/>
                <line x1="90" y1="200" x2="215" y2="260"/>
                <line x1="90" y1="200" x2="150" y2="330"/>
                <line x1="90" y1="200" x2="120" y2="145"/>
                <line x1="90" y1="200" x2="60" y2="90"/>
                <line x1="200" y1="110" x2="330" y2="175"/>
                <line x1="200" y1="110" x2="345" y2="60"/>
                <line x1="215" y1="260" x2="330" y2="175"/>
                <line x1="215" y1="260" x2="150" y2="330"/>
                <line x1="330" y1="175" x2="420" y2="290"/>
                <line x1="330" y1="175" x2="470" y2="130"/>
                <line x1="420" y1="290" x2="500" y2="215"/>
                <line x1="345" y1="60" x2="470" y2="130"/>
                <line x1="150" y1="330" x2="255" y2="355"/>
                <line x1="215" y1="260" x2="255" y2="355"/>
                <line x1="420" y1="290" x2="390" y2="380"/>
                <line x1="120" y1="145" x2="60" y2="90"/>
              </g>
              <g>
                <circle cx="60" cy="90" r="9" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="90" cy="200" r="26" fill="#E8B34B"/>
                <circle cx="120" cy="145" r="8" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="150" cy="330" r="11" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="200" cy="110" r="18" fill="#F5D488"/>
                <circle cx="215" cy="260" r="16" fill="#E8B34B"/>
                <circle cx="255" cy="355" r="10" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="330" cy="175" r="22" fill="#E8B34B"/>
                <circle cx="345" cy="60" r="12" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="390" cy="380" r="9" fill="#C7000B"/>
                <circle cx="420" cy="290" r="14" fill="#F5D488"/>
                <circle cx="470" cy="130" r="10" fill="#5B7DBB" opacity="0.9"/>
                <circle cx="500" cy="215" r="8" fill="#C7000B"/>
              </g>
              <g fill="#9FB4DA" font-size="11">
                <text x="46" y="215" fill="#F5D488" font-size="12">核心专利</text>
              </g>
            </svg>
          </div>
        </div>

        <!-- 趋势图 -->
        <div class="w-[560px] flex flex-col" style="background:rgba(14,33,69,0.72); border:1px solid rgba(91,125,187,0.30); backdrop-filter:blur(8px);">
          <div class="px-[18px] py-[14px] flex items-center justify-between" style="border-bottom:1px solid rgba(91,125,187,0.22);">
            <span class="text-[16px] font-semibold" style="color:#F5D488;">引用趋势 · 质量评分</span>
            <span class="text-[13px] text-[#9FB4DA]">双 Y 轴</span>
          </div>
          <div class="flex-1 p-[16px] flex items-center justify-center">
            <svg width="520" height="300" viewBox="0 0 520 300">
              <g stroke="#5B7DBB" stroke-width="1" opacity="0.25">
                <line x1="50" y1="40" x2="500" y2="40"/>
                <line x1="50" y1="100" x2="500" y2="100"/>
                <line x1="50" y1="160" x2="500" y2="160"/>
                <line x1="50" y1="220" x2="500" y2="220"/>
                <line x1="50" y1="265" x2="500" y2="265"/>
              </g>
              <polyline points="50,235 125,215 200,180 275,140 350,100 425,70 500,55"
                        fill="none" stroke="#E8B34B" stroke-width="3"/>
              <polyline points="50,245 125,238 200,222 275,198 350,172 425,150 500,128"
                        fill="none" stroke="#C7000B" stroke-width="3" stroke-dasharray="6,4"/>
              <g fill="#E8B34B">
                <circle cx="50" cy="235" r="4"/><circle cx="125" cy="215" r="4"/>
                <circle cx="200" cy="180" r="4"/><circle cx="275" cy="140" r="4"/>
                <circle cx="350" cy="100" r="4"/><circle cx="425" cy="70" r="4"/>
                <circle cx="500" cy="55" r="4"/>
              </g>
              <g fill="#C7000B">
                <circle cx="50" cy="245" r="4"/><circle cx="125" cy="238" r="4"/>
                <circle cx="200" cy="222" r="4"/><circle cx="275" cy="198" r="4"/>
                <circle cx="350" cy="172" r="4"/><circle cx="425" cy="150" r="4"/>
                <circle cx="500" cy="128" r="4"/>
              </g>
              <g fill="#9FB4DA" font-size="11">
                <text x="42" y="288">2020</text><text x="117" y="288">2021</text>
                <text x="192" y="288">2022</text><text x="267" y="288">2023</text>
                <text x="342" y="288">2024</text><text x="417" y="288">2025</text>
                <text x="486" y="288">2026</text>
              </g>
              <g font-size="12">
                <rect x="60" y="30" width="16" height="3" fill="#E8B34B"/>
                <text x="84" y="36" fill="#9FB4DA">引用次数</text>
                <rect x="160" y="30" width="16" height="3" fill="#C7000B"/>
                <text x="184" y="36" fill="#9FB4DA">质量评分</text>
              </g>
            </svg>
          </div>
        </div>
      </div>

      <!-- 底部质量模型 -->
      <div class="absolute bottom-[46px] left-0 w-full flex gap-[14px]">
        <div class="px-5 py-[14px]" style="background:rgba(232,179,75,0.10); border-left:4px solid #E8B34B; backdrop-filter:blur(8px);">
          <span class="text-[13px] tracking-[2px] text-[#9FB4DA]">专利质量模型</span>
          <span class="ml-3 text-[16px]" style="color:#E0E6F0;">引用 <span style="color:#F5D488;">30%</span> ＋ PageRank <span style="color:#F5D488;">25%</span> ＋ 同族 <span style="color:#F5D488;">20%</span> ＋ 国际布局 <span style="color:#F5D488;">15%</span> ＋ 诉讼 <span style="color:#F5D488;">10%</span></span>
        </div>
        <div class="px-5 py-[14px]" style="border:1px solid rgba(91,125,187,0.30); background:rgba(14,33,69,0.55);">
          <span class="text-[13px] tracking-[2px] text-[#9FB4DA]">团队画像联动</span>
          <span class="ml-3 text-[16px]" style="color:#E0E6F0;">论文总数 · 专利总数 · 总引用数 · 平均 H 指数</span>
        </div>
      </div>

    </div>
  </div>
`);
