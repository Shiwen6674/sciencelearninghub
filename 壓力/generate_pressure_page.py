# -*- coding: utf-8 -*-
"""Generate the interactive pressure learning page."""

from pathlib import Path


HTML = r"""<!doctype html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>壓力 | 力與面積互動實驗室</title>
  <meta name="description" content="用互動模擬理解壓力、力與接觸面積的關係：P = F / A。">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%23117c7b'/%3E%3Cpath d='M32 10v28M20 28l12 12 12-12M16 52h32' stroke='white' stroke-width='6' stroke-linecap='round' stroke-linejoin='round' fill='none'/%3E%3C/svg%3E">
  <style>
    :root {
      color-scheme: light;
      --ink: #17212b;
      --muted: #5e6977;
      --line: #d9e2ea;
      --paper: #f7fafc;
      --panel: #ffffff;
      --teal: #117c7b;
      --teal-dark: #0b5d5c;
      --coral: #d84f35;
      --amber: #d89b23;
      --green: #368756;
      --blue: #2866a8;
      --soft-teal: #e4f4f1;
      --soft-coral: #fff0ec;
      --soft-amber: #fff5da;
      --shadow: 0 18px 38px rgba(23, 33, 43, 0.1);
      --radius: 8px;
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      font-family: "Noto Sans TC", "Microsoft JhengHei", "PingFang TC", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        linear-gradient(180deg, rgba(228, 244, 241, 0.95), rgba(247, 250, 252, 0.9) 36%, rgba(255, 245, 218, 0.38)),
        repeating-linear-gradient(90deg, rgba(23, 33, 43, 0.025) 0 1px, transparent 1px 56px),
        repeating-linear-gradient(0deg, rgba(23, 33, 43, 0.025) 0 1px, transparent 1px 56px);
      color: var(--ink);
      line-height: 1.65;
      min-height: 100vh;
    }

    button, input {
      font: inherit;
    }

    button {
      cursor: pointer;
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 10;
      border-bottom: 1px solid rgba(217, 226, 234, 0.9);
      background: rgba(247, 250, 252, 0.92);
      backdrop-filter: blur(14px);
    }

    .topbar-inner {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }

    .brand-mark {
      width: 42px;
      height: 42px;
      border-radius: var(--radius);
      display: grid;
      place-items: center;
      color: #fff;
      background: linear-gradient(135deg, var(--teal), var(--coral));
      box-shadow: 0 10px 24px rgba(17, 124, 123, 0.24);
      flex: 0 0 auto;
    }

    .brand-title {
      margin: 0;
      font-size: clamp(1.08rem, 2vw, 1.42rem);
      letter-spacing: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .formula-chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid rgba(17, 124, 123, 0.24);
      background: #fff;
      color: var(--teal-dark);
      border-radius: 999px;
      padding: 8px 14px;
      font-weight: 800;
      white-space: nowrap;
      box-shadow: 0 8px 20px rgba(23, 33, 43, 0.06);
    }

    main {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      padding: 24px 0 56px;
    }

    .app-grid {
      display: grid;
      grid-template-columns: minmax(300px, 390px) minmax(0, 1fr);
      gap: 18px;
      align-items: stretch;
    }

    .panel {
      border: 1px solid rgba(217, 226, 234, 0.95);
      background: rgba(255, 255, 255, 0.93);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }

    .controls {
      padding: 18px;
    }

    .section-kicker {
      color: var(--coral);
      font-size: 0.82rem;
      font-weight: 900;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    h2, h3 {
      line-height: 1.22;
      letter-spacing: 0;
    }

    h2 {
      margin: 6px 0 8px;
      font-size: clamp(1.45rem, 3vw, 2.25rem);
    }

    h3 {
      margin: 0 0 12px;
      font-size: clamp(1.06rem, 2vw, 1.28rem);
    }

    .lead {
      margin: 0 0 16px;
      color: var(--muted);
      font-size: 1rem;
    }

    .control-block {
      border-top: 1px solid var(--line);
      padding-top: 16px;
      margin-top: 16px;
    }

    .range-head {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 8px;
    }

    .range-head label {
      font-weight: 850;
    }

    .live-value {
      min-width: 112px;
      text-align: right;
      color: var(--teal-dark);
      font-weight: 900;
      font-variant-numeric: tabular-nums;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--teal);
    }

    .range-scale {
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 0.82rem;
      margin-top: 2px;
    }

    .preset-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }

    .preset {
      min-height: 48px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      color: var(--ink);
      font-weight: 800;
      padding: 10px 12px;
      transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease;
    }

    .preset:hover, .preset:focus-visible {
      transform: translateY(-1px);
      border-color: rgba(17, 124, 123, 0.45);
      background: var(--soft-teal);
      outline: none;
    }

    .preset.active {
      border-color: var(--teal);
      background: var(--soft-teal);
      color: var(--teal-dark);
    }

    .scene-panel {
      overflow: hidden;
      display: grid;
      grid-template-rows: auto 1fr auto;
      min-height: 620px;
    }

    .scene-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 18px;
      padding: 18px 18px 0;
    }

    .pressure-readout {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      padding: 14px 18px 0;
    }

    .metric {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 12px;
      background: #fff;
      min-height: 92px;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.84rem;
      font-weight: 800;
    }

    .metric strong {
      display: block;
      margin-top: 6px;
      font-size: clamp(1.15rem, 2.4vw, 1.7rem);
      line-height: 1.1;
      font-variant-numeric: tabular-nums;
    }

    .metric.pressure {
      border-color: rgba(216, 79, 53, 0.42);
      background: var(--soft-coral);
    }

    .canvas-wrap {
      position: relative;
      margin: 16px 18px 12px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      min-height: 360px;
      background: linear-gradient(180deg, #eef7f5, #fff);
      overflow: hidden;
    }

    #sceneCanvas {
      display: block;
      width: 100%;
      height: 100%;
      min-height: 360px;
    }

    .canvas-caption {
      position: absolute;
      left: 12px;
      top: 12px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .badge {
      border-radius: 999px;
      padding: 6px 10px;
      background: rgba(255, 255, 255, 0.9);
      border: 1px solid rgba(217, 226, 234, 0.9);
      color: var(--ink);
      font-weight: 850;
      font-size: 0.84rem;
      box-shadow: 0 6px 16px rgba(23, 33, 43, 0.08);
    }

    .badge.hot {
      color: #8f2616;
      background: #fff0ec;
      border-color: rgba(216, 79, 53, 0.32);
    }

    .explain-strip {
      border-top: 1px solid var(--line);
      padding: 14px 18px 18px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }

    .rule {
      border-left: 4px solid var(--teal);
      padding: 8px 10px;
      background: #fff;
      border-radius: var(--radius);
      min-height: 84px;
    }

    .rule:nth-child(2) {
      border-left-color: var(--coral);
    }

    .rule:nth-child(3) {
      border-left-color: var(--amber);
    }

    .rule strong {
      display: block;
      margin-bottom: 3px;
    }

    .rule span {
      color: var(--muted);
      font-size: 0.92rem;
    }

    .learning-grid {
      display: grid;
      grid-template-columns: 1.08fr 0.92fr;
      gap: 18px;
      margin-top: 18px;
    }

    .mini-panel {
      padding: 18px;
    }

    .comparison {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 12px;
    }

    .choice {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      padding: 12px;
      min-height: 150px;
      display: grid;
      align-content: space-between;
      gap: 10px;
      text-align: left;
    }

    .choice:hover, .choice:focus-visible {
      border-color: var(--teal);
      outline: none;
    }

    .choice-title {
      font-weight: 900;
      color: var(--ink);
    }

    .bar {
      height: 12px;
      border-radius: 999px;
      overflow: hidden;
      background: #edf2f6;
    }

    .bar i {
      display: block;
      height: 100%;
      background: linear-gradient(90deg, var(--teal), var(--coral));
      width: 50%;
    }

    .feedback {
      min-height: 52px;
      margin-top: 12px;
      border: 1px solid rgba(217, 226, 234, 0.95);
      background: #fff;
      border-radius: var(--radius);
      padding: 10px 12px;
      color: var(--muted);
    }

    .target-row {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px;
      align-items: center;
      margin-top: 12px;
    }

    .primary {
      min-height: 44px;
      border: 0;
      border-radius: var(--radius);
      color: #fff;
      background: var(--teal);
      font-weight: 900;
      padding: 10px 14px;
      box-shadow: 0 12px 20px rgba(17, 124, 123, 0.18);
    }

    .primary:hover, .primary:focus-visible {
      background: var(--teal-dark);
      outline: none;
    }

    .secondary {
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      color: var(--ink);
      font-weight: 850;
      padding: 9px 12px;
    }

    .quiz-list {
      display: grid;
      gap: 10px;
    }

    .quiz-item {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      padding: 12px;
    }

    .quiz-item p {
      margin: 0 0 10px;
      font-weight: 850;
    }

    .quiz-options {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .quiz-options button {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #f8fbfd;
      padding: 8px 10px;
      color: var(--ink);
      font-weight: 800;
    }

    .quiz-options button.correct {
      color: #135c34;
      background: #e9f7ee;
      border-color: rgba(54, 135, 86, 0.46);
    }

    .quiz-options button.wrong {
      color: #8f2616;
      background: #fff0ec;
      border-color: rgba(216, 79, 53, 0.4);
    }

    .quiz-feedback {
      margin-top: 8px;
      color: var(--muted);
      min-height: 26px;
    }

    .notebook {
      margin-top: 18px;
      padding: 18px;
    }

    textarea {
      width: 100%;
      min-height: 94px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 12px;
      font: inherit;
      color: var(--ink);
      background: #fff;
    }

    .footer-note {
      margin-top: 20px;
      color: var(--muted);
      font-size: 0.9rem;
    }

    @media (max-width: 960px) {
      .app-grid, .learning-grid {
        grid-template-columns: 1fr;
      }

      .scene-panel {
        min-height: auto;
      }
    }

    @media (max-width: 720px) {
      .topbar-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 12px 0;
      }

      .formula-chip {
        width: 100%;
        justify-content: center;
      }

      .pressure-readout,
      .explain-strip,
      .comparison,
      .preset-grid {
        grid-template-columns: 1fr;
      }

      .scene-header {
        flex-direction: column;
      }

      .canvas-wrap, #sceneCanvas {
        min-height: 320px;
      }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <div class="brand" aria-label="壓力互動實驗室">
        <div class="brand-mark" aria-hidden="true">
          <svg width="25" height="25" viewBox="0 0 24 24" fill="none">
            <path d="M12 3v11" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
            <path d="m7 10 5 5 5-5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M5 20h14" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
          </svg>
        </div>
        <h1 class="brand-title">壓力 | 力與面積互動實驗室</h1>
      </div>
      <div class="formula-chip" aria-label="壓力公式">P = F / A</div>
    </div>
  </header>

  <main>
    <section class="app-grid" aria-labelledby="mainTitle">
      <aside class="panel controls">
        <span class="section-kicker">Force - Area - Pressure</span>
        <h2 id="mainTitle">壓力不是「力很大」而已</h2>
        <p class="lead">壓力看的是每一小塊面積分到多少垂直作用力。同樣的力集中在較小面積上，壓力會明顯上升。</p>

        <div class="control-block">
          <div class="range-head">
            <label for="forceRange">垂直作用力 F</label>
            <output id="forceValue" class="live-value" for="forceRange">80 N</output>
          </div>
          <input id="forceRange" type="range" min="5" max="220" step="1" value="80">
          <div class="range-scale"><span>輕</span><span>重</span></div>
        </div>

        <div class="control-block">
          <div class="range-head">
            <label for="areaRange">接觸面積 A</label>
            <output id="areaValue" class="live-value" for="areaRange">40 cm²</output>
          </div>
          <input id="areaRange" type="range" min="1" max="220" step="1" value="40">
          <div class="range-scale"><span>尖、小</span><span>寬、大</span></div>
        </div>

        <div class="control-block">
          <h3>生活情境</h3>
          <div class="preset-grid" id="presetGrid"></div>
        </div>

        <div class="control-block">
          <h3>目標挑戰</h3>
          <p class="lead">把壓力調到接近 <strong>20 kPa</strong>。接近代表誤差小於 1 kPa。</p>
          <div class="target-row">
            <div class="feedback" id="targetFeedback">目前還沒有檢核。</div>
            <button class="primary" id="checkTarget">檢核</button>
          </div>
        </div>
      </aside>

      <section class="panel scene-panel" aria-labelledby="sceneTitle">
        <div class="scene-header">
          <div>
            <span class="section-kicker">Live Model</span>
            <h2 id="sceneTitle">同一個公式，看見三個量一起變</h2>
          </div>
          <button class="secondary" id="resetBtn">重設</button>
        </div>

        <div class="pressure-readout" aria-live="polite">
          <div class="metric">
            <span>力 F</span>
            <strong id="forceMetric">80 N</strong>
          </div>
          <div class="metric">
            <span>面積 A</span>
            <strong id="areaMetric">40 cm²</strong>
          </div>
          <div class="metric pressure">
            <span>壓力 P</span>
            <strong id="pressureMetric">20 kPa</strong>
          </div>
        </div>

        <div class="canvas-wrap">
          <div class="canvas-caption">
            <span class="badge" id="unitBadge">0.20 N/cm²</span>
            <span class="badge hot" id="feelBadge">清楚壓痕</span>
          </div>
          <canvas id="sceneCanvas" aria-label="力、接觸面積與壓力的視覺化模擬"></canvas>
        </div>

        <div class="explain-strip">
          <div class="rule">
            <strong>F 變大</strong>
            <span>面積不變時，每一單位面積分到更多力，P 上升。</span>
          </div>
          <div class="rule">
            <strong>A 變大</strong>
            <span>力被分散到更多面積，P 下降，感覺較不刺痛。</span>
          </div>
          <div class="rule">
            <strong>P 是比例</strong>
            <span>不是只看力，也不是只看面積，而是看 F 除以 A。</span>
          </div>
        </div>
      </section>
    </section>

    <section class="learning-grid" aria-label="比較與檢核">
      <section class="panel mini-panel">
        <span class="section-kicker">Compare</span>
        <h2>哪一個比較痛？</h2>
        <p class="lead">兩邊施力相同，差別只在接觸面積。選壓力較大的那一邊。</p>
        <div class="comparison">
          <button class="choice" id="choiceA">
            <span class="choice-title">A：鉛筆尖頂手指</span>
            <span>F = 20 N，A = 1 cm²</span>
            <span class="bar"><i style="width: 92%"></i></span>
          </button>
          <button class="choice" id="choiceB">
            <span class="choice-title">B：橡皮擦端頂手指</span>
            <span>F = 20 N，A = 24 cm²</span>
            <span class="bar"><i style="width: 18%"></i></span>
          </button>
        </div>
        <div class="feedback" id="compareFeedback">先判斷壓力，再看公式。A 的面積小很多。</div>
      </section>

      <section class="panel mini-panel">
        <span class="section-kicker">Misconception Check</span>
        <h2>最容易混淆的地方</h2>
        <div class="rule">
          <strong>壓力和力不同</strong>
          <span>100 N 分散在 200 cm² 上，可能比 20 N 集中在 1 cm² 上更不尖銳。</span>
        </div>
        <div class="rule" style="margin-top:10px;">
          <strong>只算垂直於接觸面的力</strong>
          <span>把板擦壓向垂直黑板時，造成黑板壓力的主要來源是手往黑板方向的施力。</span>
        </div>
      </section>
    </section>

    <section class="panel mini-panel" style="margin-top:18px;">
      <span class="section-kicker">Quiz</span>
      <h2>四題概念檢核</h2>
      <div class="quiz-list" id="quizList"></div>
      <div class="feedback" id="scoreBox">完成後會顯示得分。</div>
    </section>

    <section class="panel notebook">
      <span class="section-kicker">One Sentence</span>
      <h2>用一句話收束</h2>
      <textarea id="noteBox" placeholder="例如：同樣的力，如果接觸面積變小，壓力就會變大。"></textarea>
      <div class="target-row">
        <div class="feedback" id="noteFeedback">寫下來會留在這台電腦的瀏覽器中。</div>
        <button class="primary" id="saveNote">保存</button>
      </div>
      <p class="footer-note">概念依據：國中自然第 6 章「力與壓力」6-3 壓力，重點為壓力定義 `P = F / A`、垂直作用力與受力面積。</p>
    </section>
  </main>

  <script>
    const presets = [
      { id: "pencil", name: "鉛筆尖", force: 18, area: 1 },
      { id: "eraser", name: "橡皮擦端", force: 18, area: 28 },
      { id: "nail", name: "鐵釘撐豆腐", force: 10, area: 1 },
      { id: "kenzan", name: "劍山撐豆腐", force: 10, area: 90 },
      { id: "strapThin", name: "窄肩帶", force: 95, area: 18 },
      { id: "strapWide", name: "寬肩帶", force: 95, area: 120 },
      { id: "heel", name: "高跟鞋跟", force: 180, area: 4 },
      { id: "snowshoe", name: "雪鞋", force: 180, area: 210 }
    ];

    const quiz = [
      {
        q: "同樣 30 N 的力，接觸面積從 30 cm² 變成 3 cm²，壓力會怎樣？",
        options: ["變成 10 倍", "變成 1/10", "不變"],
        answer: 0,
        why: "P = F / A，面積變成 1/10，壓力變成 10 倍。"
      },
      {
        q: "20 N 作用在 10 cm² 上，壓力是多少 N/cm²？",
        options: ["0.5", "2", "200"],
        answer: 1,
        why: "20 / 10 = 2 N/cm²。"
      },
      {
        q: "為什麼指套可以保護手指？",
        options: ["增加接觸面積，降低壓力", "減少力的單位", "讓壓力方向消失"],
        answer: 0,
        why: "指套把針的作用力分散到較大的面積。"
      },
      {
        q: "國際單位 Pa 代表什麼？",
        options: ["N/m²", "N/cm", "kg/m²"],
        answer: 0,
        why: "帕斯卡 Pa 是每平方公尺承受多少牛頓，也就是 N/m²。"
      }
    ];

    const state = {
      force: 80,
      area: 40,
      activePreset: ""
    };

    const els = {
      forceRange: document.getElementById("forceRange"),
      areaRange: document.getElementById("areaRange"),
      forceValue: document.getElementById("forceValue"),
      areaValue: document.getElementById("areaValue"),
      forceMetric: document.getElementById("forceMetric"),
      areaMetric: document.getElementById("areaMetric"),
      pressureMetric: document.getElementById("pressureMetric"),
      unitBadge: document.getElementById("unitBadge"),
      feelBadge: document.getElementById("feelBadge"),
      presetGrid: document.getElementById("presetGrid"),
      canvas: document.getElementById("sceneCanvas"),
      resetBtn: document.getElementById("resetBtn"),
      checkTarget: document.getElementById("checkTarget"),
      targetFeedback: document.getElementById("targetFeedback"),
      compareFeedback: document.getElementById("compareFeedback"),
      quizList: document.getElementById("quizList"),
      scoreBox: document.getElementById("scoreBox"),
      noteBox: document.getElementById("noteBox"),
      saveNote: document.getElementById("saveNote"),
      noteFeedback: document.getElementById("noteFeedback")
    };

    const ctx = els.canvas.getContext("2d");
    const quizState = new Array(quiz.length).fill(null);

    function fmt(value, digits = 0) {
      return new Intl.NumberFormat("zh-TW", {
        maximumFractionDigits: digits,
        minimumFractionDigits: digits
      }).format(value);
    }

    function getPressure() {
      const areaM2 = state.area / 10000;
      const pa = state.force / areaM2;
      return {
        pa,
        kpa: pa / 1000,
        ncm2: state.force / state.area
      };
    }

    function pressureLevel(kpa) {
      if (kpa < 5) return "幾乎分散";
      if (kpa < 18) return "輕微壓痕";
      if (kpa < 45) return "清楚壓痕";
      if (kpa < 110) return "強烈集中";
      return "刺穿風險";
    }

    function setState(force, area, activePreset = "") {
      state.force = Math.max(5, Math.min(220, Math.round(force)));
      state.area = Math.max(1, Math.min(220, Math.round(area)));
      state.activePreset = activePreset;
      syncInputs();
      render();
    }

    function syncInputs() {
      els.forceRange.value = state.force;
      els.areaRange.value = state.area;
      document.querySelectorAll(".preset").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.id === state.activePreset);
      });
    }

    function renderValues() {
      const p = getPressure();
      els.forceValue.value = `${state.force} N`;
      els.areaValue.value = `${state.area} cm²`;
      els.forceMetric.textContent = `${state.force} N`;
      els.areaMetric.textContent = `${state.area} cm²`;
      els.pressureMetric.textContent = `${fmt(p.kpa, p.kpa >= 100 ? 0 : 1)} kPa`;
      els.unitBadge.textContent = `${fmt(p.ncm2, 2)} N/cm²`;
      els.feelBadge.textContent = pressureLevel(p.kpa);
    }

    function resizeCanvas() {
      const rect = els.canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      const width = Math.max(360, rect.width);
      const height = Math.max(320, rect.height);
      if (els.canvas.width !== Math.round(width * dpr) || els.canvas.height !== Math.round(height * dpr)) {
        els.canvas.width = Math.round(width * dpr);
        els.canvas.height = Math.round(height * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      return { width, height };
    }

    function roundedRect(x, y, w, h, r) {
      const radius = Math.min(r, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + radius, y);
      ctx.arcTo(x + w, y, x + w, y + h, radius);
      ctx.arcTo(x + w, y + h, x, y + h, radius);
      ctx.arcTo(x, y + h, x, y, radius);
      ctx.arcTo(x, y, x + w, y, radius);
      ctx.closePath();
    }

    function drawArrow(x, y1, y2, width, color) {
      ctx.save();
      ctx.strokeStyle = color;
      ctx.fillStyle = color;
      ctx.lineWidth = width;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(x, y1);
      ctx.lineTo(x, y2 - 18);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x, y2);
      ctx.lineTo(x - 13, y2 - 21);
      ctx.lineTo(x + 13, y2 - 21);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }

    function drawScene() {
      const { width, height } = resizeCanvas();
      const p = getPressure();
      ctx.clearRect(0, 0, width, height);

      const floorY = height * 0.76;
      const centerX = width * 0.5;
      const matW = Math.min(width * 0.78, 620);
      const matH = 58;
      const matX = centerX - matW / 2;

      const grad = ctx.createLinearGradient(0, 0, width, height);
      grad.addColorStop(0, "#e8f6f3");
      grad.addColorStop(0.55, "#ffffff");
      grad.addColorStop(1, "#fff4d8");
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, width, height);

      ctx.strokeStyle = "rgba(23, 33, 43, 0.08)";
      ctx.lineWidth = 1;
      for (let x = 0; x < width; x += 44) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 44) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      const contactW = Math.max(28, Math.min(matW * 0.82, Math.sqrt(state.area / 220) * matW * 0.82));
      const blockW = Math.max(contactW + 22, Math.min(matW * 0.9, contactW + 100));
      const blockH = 84 + (state.force / 220) * 44;
      const compression = Math.min(42, Math.max(4, p.kpa * 0.36));
      const contactX = centerX - contactW / 2;
      const blockX = centerX - blockW / 2;
      const blockY = floorY - matH - blockH + compression * 0.18;

      ctx.save();
      ctx.fillStyle = "#d8e5e1";
      roundedRect(matX, floorY - matH / 2, matW, matH, 8);
      ctx.fill();
      ctx.fillStyle = "#bfd4cf";
      roundedRect(contactX - 12, floorY - matH / 2 + 8, contactW + 24, 16 + compression * 0.58, 8);
      ctx.fill();
      ctx.restore();

      ctx.save();
      ctx.shadowColor = "rgba(23, 33, 43, 0.16)";
      ctx.shadowBlur = 18;
      ctx.shadowOffsetY = 10;
      ctx.fillStyle = "#fdfdfd";
      roundedRect(blockX, blockY, blockW, blockH, 8);
      ctx.fill();
      ctx.shadowColor = "transparent";
      ctx.strokeStyle = "#a8bac7";
      ctx.lineWidth = 2;
      roundedRect(blockX, blockY, blockW, blockH, 8);
      ctx.stroke();
      ctx.fillStyle = "#e7edf1";
      roundedRect(contactX, floorY - matH / 2 - 20, contactW, 22, 4);
      ctx.fill();
      ctx.restore();

      const arrowWidth = 5 + (state.force / 220) * 12;
      drawArrow(centerX, 42, blockY - 8, arrowWidth, "#d84f35");

      ctx.save();
      ctx.fillStyle = "#17212b";
      ctx.font = "800 15px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(`F = ${state.force} N`, centerX, 30);
      ctx.fillText(`A = ${state.area} cm²`, centerX, floorY + 52);
      ctx.restore();

      const density = Math.min(140, Math.max(10, Math.round(p.kpa * 1.25)));
      const rows = Math.ceil(Math.sqrt(density));
      const cols = rows;
      const dotGapX = contactW / Math.max(1, cols);
      const dotGapY = Math.max(7, (24 + compression) / Math.max(1, rows));
      ctx.save();
      ctx.fillStyle = p.kpa > 55 ? "rgba(216, 79, 53, 0.68)" : "rgba(17, 124, 123, 0.54)";
      let count = 0;
      for (let r = 0; r < rows && count < density; r += 1) {
        for (let c = 0; c < cols && count < density; c += 1) {
          const x = contactX + dotGapX * (c + 0.5);
          const y = floorY - matH / 2 + 12 + dotGapY * (r + 0.4);
          ctx.beginPath();
          ctx.arc(x, y, 2.2, 0, Math.PI * 2);
          ctx.fill();
          count += 1;
        }
      }
      ctx.restore();

      ctx.save();
      ctx.fillStyle = "#5e6977";
      ctx.font = "700 13px sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("紅色箭頭越粗：力越大", 18, height - 48);
      ctx.fillText("壓點越密：單位面積承受的力越集中", 18, height - 26);
      ctx.restore();
    }

    function renderPresets() {
      els.presetGrid.innerHTML = "";
      presets.forEach((item) => {
        const btn = document.createElement("button");
        btn.className = "preset";
        btn.type = "button";
        btn.dataset.id = item.id;
        btn.textContent = item.name;
        btn.addEventListener("click", () => setState(item.force, item.area, item.id));
        els.presetGrid.appendChild(btn);
      });
    }

    function renderQuiz() {
      els.quizList.innerHTML = "";
      quiz.forEach((item, index) => {
        const wrap = document.createElement("article");
        wrap.className = "quiz-item";
        const q = document.createElement("p");
        q.textContent = `${index + 1}. ${item.q}`;
        const options = document.createElement("div");
        options.className = "quiz-options";
        const feedback = document.createElement("div");
        feedback.className = "quiz-feedback";
        feedback.id = `quizFeedback${index}`;

        item.options.forEach((label, optionIndex) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.textContent = label;
          btn.addEventListener("click", () => answerQuiz(index, optionIndex));
          options.appendChild(btn);
        });

        wrap.append(q, options, feedback);
        els.quizList.appendChild(wrap);
      });
    }

    function answerQuiz(index, optionIndex) {
      quizState[index] = optionIndex;
      const item = quiz[index];
      const wrap = els.quizList.children[index];
      [...wrap.querySelectorAll("button")].forEach((btn, i) => {
        btn.classList.remove("correct", "wrong");
        if (i === item.answer) btn.classList.add("correct");
        if (i === optionIndex && i !== item.answer) btn.classList.add("wrong");
      });
      const feedback = document.getElementById(`quizFeedback${index}`);
      feedback.textContent = optionIndex === item.answer ? `答對。${item.why}` : `再想一次。${item.why}`;
      const answered = quizState.filter((v) => v !== null).length;
      const correct = quizState.filter((v, i) => v === quiz[i].answer).length;
      els.scoreBox.textContent = answered === quiz.length
        ? `完成：${correct} / ${quiz.length}。${correct === quiz.length ? "概念很穩。" : "錯題都和 F / A 的比例有關，回到模擬器再調一次會更清楚。"}`
        : `已完成 ${answered} / ${quiz.length} 題。`;
    }

    function render() {
      renderValues();
      drawScene();
    }

    function bindEvents() {
      els.forceRange.addEventListener("input", () => setState(Number(els.forceRange.value), state.area));
      els.areaRange.addEventListener("input", () => setState(state.force, Number(els.areaRange.value)));
      els.resetBtn.addEventListener("click", () => setState(80, 40));
      els.checkTarget.addEventListener("click", () => {
        const diff = Math.abs(getPressure().kpa - 20);
        els.targetFeedback.textContent = diff < 1
          ? "命中。這組 F / A 很接近 20 kPa。"
          : `目前差 ${fmt(diff, 1)} kPa。想降低 P，就減少 F 或增加 A；想提高 P，反過來。`;
      });
      document.getElementById("choiceA").addEventListener("click", () => {
        els.compareFeedback.textContent = "正確。兩邊都是 20 N，但 A 只有 1 cm²，所以 A 的壓力是 20 N/cm²。";
      });
      document.getElementById("choiceB").addEventListener("click", () => {
        els.compareFeedback.textContent = "B 的面積比較大，所以壓力較小。A 才是壓力較大的選項。";
      });
      els.saveNote.addEventListener("click", () => {
        localStorage.setItem("pressure-note", els.noteBox.value.trim());
        els.noteFeedback.textContent = els.noteBox.value.trim()
          ? "已保存。這句話就是你自己的壓力概念摘要。"
          : "目前是空白。";
      });
      window.addEventListener("resize", render);
    }

    function init() {
      renderPresets();
      renderQuiz();
      bindEvents();
      const savedNote = localStorage.getItem("pressure-note");
      if (savedNote) {
        els.noteBox.value = savedNote;
        els.noteFeedback.textContent = "已載入上次保存的一句話。";
      }
      syncInputs();
      render();
    }

    init();
  </script>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parent
    out_dir = root / "dist"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(HTML, encoding="utf-8")
    print("Generated dist/index.html")


if __name__ == "__main__":
    main()
