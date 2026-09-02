"use strict";

const I18N = {
  en: {
    siteTitle: "QQQ Historical Analog",
    metaDescription: "Find historically similar QQQ price patterns and examine what happened next.",
    languageAria: "Language",
    skipLink: "Skip to analysis",
    eyebrow: "Quantitative research tool",
    subtitle: "Find historically similar QQQ price patterns and examine what happened next.",
    marketSummaryAria: "Current QQQ market summary",
    asOf: "As of",
    regime: "Regime",
    lastUpdated: "Last updated",
    analysisControlsAria: "Analysis controls",
    observationWindow: "Observation window",
    lookbackAria: "Lookback window",
    sameRegimeOnly: "Same Market Regime Only",
    sameRegimeHint: "Match Bull/Bear state using the 200-day moving average",
    loading: "Loading historical analogs…",
    errorTitle: "Could not load the analysis data.",
    errorBody: "Start a local server from the project folder, then refresh this page.",
    retry: "Try again",
    normalizedPricePath: "Normalized price path",
    currentPattern: "Current QQQ Pattern",
    currentChartAria: "Current QQQ normalized price chart",
    statCardsAria: "Key forward statistics",
    pastOutcome: "Past pattern + realized outcome",
    historicalAnalogPaths: "Historical Analog Paths",
    analogNote: "Current QQQ ends at Day 0. Historical outcomes continue for 30 trading days.",
    analogChartAria: "Historical analog price paths and forward return distribution",
    currentPatternLegend: "Current pattern",
    historicalAnalogsLegend: "Historical analogs",
    forwardMedianLegend: "Forward median",
    rangeLegend: "25–75% range",
    outcomeDistribution: "Outcome distribution",
    forwardReturns: "Forward Returns",
    topIndependent: "Top independent matches",
    horizon: "Horizon",
    upProbability: "Up probability",
    average: "Average",
    median: "Median",
    best: "Best",
    worst: "Worst",
    acrossWindows: "Across observation windows",
    historicalConsensus: "Historical Consensus",
    consensusFootnote: "Based on each window's historical 20D outcomes—not a price prediction.",
    rankedSimilarity: "Ranked by blended path similarity",
    topHistoricalMatches: "Top Historical Matches",
    selectRow: "Select a row to highlight its path",
    rank: "Rank",
    period: "Period",
    similarity: "Similarity",
    maxDrawdown: "Max drawdown",
    methodologyAria: "Methodology summary",
    pricePath: "Price path",
    normalizedRmseWeight: "Normalized-path RMSE weight",
    dailyReturns: "Daily returns",
    returnRmseWeight: "Return-path RMSE weight",
    tradingDays: "Trading days",
    minSeparation: "Minimum analog separation",
    forwardWindow: "Forward window",
    realizedOnly: "Realized outcomes only",
    disclaimer: "Historical similarity does not imply future performance. This tool is for research and educational purposes only and does not constitute investment advice.",
    dataSourcePrefix: "Data source",
    bullRegime: "Bull Regime",
    bearRegime: "Bear Regime",
    bull: "Bull",
    bear: "Bear",
    dayReturn: "{days}D return",
    upProbability20: "20D Up Probability",
    medianReturn20: "20D Median Return",
    medianReturn30: "30D Median Return",
    medianMaxDrawdown: "Median Max Drawdown",
    independentAnalogs: "{count} independent analogs",
    medianRealized: "Median realized outcome",
    withinForward: "Within the forward 30D window",
    highlightedAnalog: "Highlighted analog · {date}",
    similarityLabel: "Similarity",
    return20Label: "20D return",
    maxDd30Label: "30D max DD",
    normalizedLabel: "Normalized",
    rangeName: "25–75% range",
    forwardMedianName: "Forward median",
    currentQqq: "Current QQQ",
    matchEnd: "MATCH END",
    tradingDaysAxis: "TRADING DAYS",
    pastDay: "Past Day {day}",
    forwardDay: "Forward Day +{day}",
    windowLabel: "{days}D window",
    upMedian20: "20D up · median {value}",
    overall: "Overall: {signal}",
    selectAnalog: "Select analog ending {date}",
    signal_bullish: "Bullish",
    signal_bearish: "Bearish",
    signal_neutral: "Neutral",
    signal_mixed: "Mixed",
    similarityBreakdown: "Similarity breakdown",
    blendedWeightNote: "Final score = 70% price path + 30% daily returns",
    priceSimilarity: "Price-path similarity",
    returnSimilarity: "Daily-return similarity",
    priceRmse: "Price-path RMSE",
    returnRmse: "Return-path RMSE",
    weightLabel: "{value}% weight",
    lowerIsCloser: "Lower is closer",
    scoreNotProbability: "Similarity scores are ranking measures—not probabilities.",
    auditTrail: "Audit trail",
    dataProvenance: "Data Provenance",
    algorithmVersion: "Algorithm {version}",
    source: "Source",
    priceField: "Price field",
    adjustment: "Adjustment",
    coverage: "Coverage",
    rows: "Trading days",
    generated: "Generated",
    datasetFingerprint: "Dataset fingerprint",
  },
  zh: {
    siteTitle: "QQQ 历史相似行情",
    metaDescription: "寻找与 QQQ 当前走势最相似的历史行情，并查看随后真实发生了什么。",
    languageAria: "语言",
    skipLink: "跳到分析内容",
    eyebrow: "量化研究工具",
    subtitle: "寻找与 QQQ 当前走势最相似的历史行情，并查看随后真实发生了什么。",
    marketSummaryAria: "QQQ 当前市场概况",
    asOf: "截至日期",
    regime: "市场环境",
    lastUpdated: "数据更新",
    analysisControlsAria: "分析设置",
    observationWindow: "观察窗口",
    lookbackAria: "选择观察窗口",
    sameRegimeOnly: "仅匹配相同市场环境",
    sameRegimeHint: "使用200日均线匹配牛市或熊市状态",
    loading: "正在加载历史相似行情…",
    errorTitle: "无法加载分析数据。",
    errorBody: "请从项目目录启动本地服务器，然后刷新页面。",
    retry: "重试",
    normalizedPricePath: "归一化价格路径",
    currentPattern: "当前 QQQ 走势",
    currentChartAria: "当前 QQQ 归一化价格走势图",
    statCardsAria: "核心后续统计",
    pastOutcome: "历史形态 + 实际后续",
    historicalAnalogPaths: "历史相似行情路径",
    analogNote: "当前 QQQ 走势结束于第0日；历史案例继续展示未来30个交易日。",
    analogChartAria: "历史相似行情路径与未来收益分布图",
    currentPatternLegend: "当前走势",
    historicalAnalogsLegend: "历史相似案例",
    forwardMedianLegend: "后续中位数",
    rangeLegend: "25–75%区间",
    outcomeDistribution: "后续结果分布",
    forwardReturns: "后续收益统计",
    topIndependent: "独立历史案例",
    horizon: "周期",
    upProbability: "上涨比例",
    average: "平均收益",
    median: "中位数收益",
    best: "最好",
    worst: "最差",
    acrossWindows: "多观察窗口对比",
    historicalConsensus: "历史共识",
    consensusFootnote: "基于各窗口历史案例的20日结果，并非价格预测。",
    rankedSimilarity: "按综合路径相似度排序",
    topHistoricalMatches: "最相似历史行情",
    selectRow: "点击一行可在图中高亮对应路径",
    rank: "排名",
    period: "区间",
    similarity: "相似度",
    maxDrawdown: "最大回撤",
    methodologyAria: "方法说明",
    pricePath: "价格路径",
    normalizedRmseWeight: "归一化路径 RMSE 权重",
    dailyReturns: "每日收益",
    returnRmseWeight: "收益路径 RMSE 权重",
    tradingDays: "交易日",
    minSeparation: "历史案例最小间隔",
    forwardWindow: "后续窗口",
    realizedOnly: "仅使用真实历史结果",
    disclaimer: "历史相似并不代表未来表现。本工具仅供研究和教育用途，不构成任何投资建议。",
    dataSourcePrefix: "数据来源",
    bullRegime: "牛市环境",
    bearRegime: "熊市环境",
    bull: "牛市",
    bear: "熊市",
    dayReturn: "{days}日收益",
    upProbability20: "20日上涨比例",
    medianReturn20: "20日中位数收益",
    medianReturn30: "30日中位数收益",
    medianMaxDrawdown: "最大回撤中位数",
    independentAnalogs: "{count}个独立案例",
    medianRealized: "历史结果中位数",
    withinForward: "未来30个交易日内",
    highlightedAnalog: "高亮历史案例 · {date}",
    similarityLabel: "相似度",
    return20Label: "20日收益",
    maxDd30Label: "30日最大回撤",
    normalizedLabel: "归一化价格",
    rangeName: "25–75%区间",
    forwardMedianName: "后续中位数",
    currentQqq: "当前 QQQ",
    matchEnd: "案例结束日",
    tradingDaysAxis: "交易日",
    pastDay: "历史第 {day} 日",
    forwardDay: "未来第 {day} 日",
    windowLabel: "{days}日窗口",
    upMedian20: "20日上涨 · 中位数 {value}",
    overall: "整体：{signal}",
    selectAnalog: "选择结束于 {date} 的历史案例",
    signal_bullish: "看多",
    signal_bearish: "看空",
    signal_neutral: "中性",
    signal_mixed: "分歧",
    similarityBreakdown: "相似度分解",
    blendedWeightNote: "综合分数 = 70%价格路径 + 30%每日收益",
    priceSimilarity: "价格路径相似度",
    returnSimilarity: "每日收益相似度",
    priceRmse: "价格路径 RMSE",
    returnRmse: "收益路径 RMSE",
    weightLabel: "权重 {value}%",
    lowerIsCloser: "数值越低越接近",
    scoreNotProbability: "相似度仅用于排序，并非概率。",
    auditTrail: "审计信息",
    dataProvenance: "数据可追溯性",
    algorithmVersion: "算法版本 {version}",
    source: "数据源",
    priceField: "价格字段",
    adjustment: "复权方式",
    coverage: "数据区间",
    rows: "交易日数量",
    generated: "生成时间",
    datasetFingerprint: "数据指纹",
  },
};

function initialLanguage() {
  try {
    const saved = localStorage.getItem("qqq-analog-language");
    if (saved === "en" || saved === "zh") return saved;
  } catch (error) {
    console.warn("Could not read language preference:", error);
  }
  return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
}

const state = {
  data: null,
  language: initialLanguage(),
  lookback: 30,
  mode: "all_regimes",
  selectedRank: 1,
  analogChart: null,
  resizeObserver: null,
};

function t(key, variables = {}) {
  const template = I18N[state.language]?.[key] ?? I18N.en[key] ?? key;
  return template.replace(/\{(\w+)\}/g, (_, name) => variables[name] ?? `{${name}}`);
}

const COLORS = {
  text: "#dbe6ed",
  muted: "#71838f",
  grid: "#1a2731",
  cyan: "#3bd4e7",
  green: "#62dfa0",
  red: "#ff7185",
  amber: "#f5bc66",
  analog: "rgba(124, 156, 171, 0.30)",
};

const elements = {
  loading: document.querySelector("#loading-state"),
  error: document.querySelector("#error-state"),
  dashboard: document.querySelector("#dashboard"),
  retry: document.querySelector("#retry-button"),
  languageButtons: [...document.querySelectorAll("[data-language]")],
  lookbackButtons: [...document.querySelectorAll("[data-lookback]")],
  regimeOnly: document.querySelector("#regime-only"),
  currentPrice: document.querySelector("#current-price"),
  currentDate: document.querySelector("#current-date"),
  currentRegime: document.querySelector("#current-regime"),
  lastUpdated: document.querySelector("#last-updated"),
  statCards: document.querySelector("#stat-cards"),
  selectedMatchCard: document.querySelector("#selected-match-card"),
  similarityBreakdown: document.querySelector("#similarity-breakdown"),
  returnsTable: document.querySelector("#returns-table-body"),
  consensusGrid: document.querySelector("#consensus-grid"),
  overallConsensus: document.querySelector("#overall-consensus"),
  matchesTable: document.querySelector("#matches-table-body"),
  dataSource: document.querySelector("#data-source"),
  provenanceGrid: document.querySelector("#provenance-grid"),
  algorithmVersion: document.querySelector("#algorithm-version"),
};

function applyStaticTranslations() {
  document.documentElement.lang = state.language === "zh" ? "zh-CN" : "en";
  document.title = t("siteTitle");
  document.querySelector('meta[name="description"]')?.setAttribute("content", t("metaDescription"));
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", t(element.dataset.i18nAria));
  });
  elements.languageButtons.forEach((button) => {
    const active = button.dataset.language === state.language;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

function formatPercent(value, digits = 1, signed = true) {
  const percentage = value * 100;
  const sign = signed && percentage > 0 ? "+" : "";
  return `${sign}${percentage.toFixed(digits)}%`;
}

function valueClass(value) {
  if (value > 0) return "positive";
  if (value < 0) return "negative";
  return "";
}

function compactDate(dateString) {
  return new Intl.DateTimeFormat(state.language === "zh" ? "zh-CN" : "en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
  }).format(new Date(`${dateString}T00:00:00`));
}

function formatDateTime(dateString) {
  if (!dateString) return "—";
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return dateString;
  return new Intl.DateTimeFormat(state.language === "zh" ? "zh-CN" : "en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function localizedDataSource(source) {
  if (state.language !== "zh") return source;
  if (source === "Yahoo Finance via yfinance") return "Yahoo Finance（通过 yfinance）";
  if (source.startsWith("Longbridge Securities")) return "Longbridge Securities（前复权日线备用源）";
  return source;
}

function localizedAdjustment(adjustment) {
  if (state.language !== "zh") return adjustment || "—";
  if (adjustment === "Forward-adjusted OHLC") return "前复权 OHLC";
  if (adjustment === "Yahoo Finance Adj Close; OHLC unadjusted") return "Yahoo Finance 复权收盘价；OHLC 未复权";
  return adjustment || "—";
}

function getLookbackData() {
  return state.data.lookbacks[String(state.lookback)];
}

function getViewData() {
  return getLookbackData()[state.mode];
}

function baseAxis() {
  return {
    axisLine: { lineStyle: { color: COLORS.grid } },
    axisTick: { show: false },
    axisLabel: { color: COLORS.muted, fontFamily: "monospace", fontSize: 10 },
    splitLine: { lineStyle: { color: COLORS.grid, type: "dashed" } },
  };
}

function renderHeader() {
  const current = state.data.current;
  elements.currentPrice.textContent = `$${current.price.toFixed(2)}`;
  elements.currentDate.textContent = compactDate(current.date);
  elements.currentRegime.textContent = t(current.market_regime === "bull" ? "bullRegime" : "bearRegime");
  elements.currentRegime.classList.toggle("bear", current.market_regime === "bear");
  elements.lastUpdated.textContent = compactDate(state.data.last_updated);
  elements.dataSource.textContent = `${t("dataSourcePrefix")}: ${localizedDataSource(state.data.data_source)}`;
}

function renderStats() {
  const view = getViewData();
  const stats = view.statistics;
  const cards = [
    {
      label: t("upProbability20"),
      value: formatPercent(stats["20d"].up_probability, 0, false),
      detail: t("independentAnalogs", { count: view.matches.length }),
      className: "primary",
    },
    {
      label: t("medianReturn20"),
      value: formatPercent(stats["20d"].median),
      detail: t("medianRealized"),
      sign: stats["20d"].median,
    },
    {
      label: t("medianReturn30"),
      value: formatPercent(stats["30d"].median),
      detail: t("medianRealized"),
      sign: stats["30d"].median,
    },
    {
      label: t("medianMaxDrawdown"),
      value: formatPercent(stats.median_max_drawdown_30d),
      detail: t("withinForward"),
      sign: stats.median_max_drawdown_30d,
    },
  ];

  elements.statCards.innerHTML = cards
    .map(
      (card) => `
        <article class="stat-card ${card.className || ""}">
          <span class="stat-label">${card.label}</span>
          <strong class="${card.sign == null ? "" : valueClass(card.sign)}">${card.value}</strong>
          <small>${card.detail}</small>
        </article>`,
    )
    .join("");
}

function renderSelectedMatch() {
  const match = getViewData().matches.find((item) => item.rank === state.selectedRank) || getViewData().matches[0];
  state.selectedRank = match.rank;
  elements.selectedMatchCard.innerHTML = `
    <span class="match-title">${t("highlightedAnalog", { date: compactDate(match.end_date) })}</span>
    <div><strong>${match.similarity.toFixed(1)}%</strong><span>${t("similarityLabel")}</span></div>
    <div><strong class="${valueClass(match.returns["20d"])}">${formatPercent(match.returns["20d"])}</strong><span>${t("return20Label")}</span></div>
    <div><strong class="negative">${formatPercent(match.max_drawdown_30d)}</strong><span>${t("maxDd30Label")}</span></div>`;
}

function renderSimilarityBreakdown() {
  const match = getViewData().matches.find((item) => item.rank === state.selectedRank) || getViewData().matches[0];
  const metrics = [
    { label: t("priceSimilarity"), value: `${match.price_similarity.toFixed(1)}%`, detail: t("weightLabel", { value: 70 }) },
    { label: t("returnSimilarity"), value: `${match.return_similarity.toFixed(1)}%`, detail: t("weightLabel", { value: 30 }) },
    { label: t("priceRmse"), value: match.rmse.toFixed(3), detail: t("lowerIsCloser") },
    { label: t("returnRmse"), value: `${(match.return_rmse * 100).toFixed(3)}%`, detail: t("lowerIsCloser") },
  ];
  elements.similarityBreakdown.innerHTML = `
    <div class="breakdown-intro">
      <strong>${t("similarityBreakdown")}</strong>
      <span>${t("blendedWeightNote")}</span>
      <small>${t("scoreNotProbability")}</small>
    </div>
    ${metrics.map((metric) => `
      <div class="breakdown-metric">
        <span>${metric.label}</span>
        <strong>${metric.value}</strong>
        <small>${metric.detail}</small>
      </div>`).join("")}`;
}

function renderProvenance() {
  const provenance = state.data.data_provenance || {};
  const fingerprint = provenance.csv_sha256 || "—";
  elements.algorithmVersion.textContent = t("algorithmVersion", {
    version: state.data.algorithm_version || "—",
  });
  const items = [
    [t("source"), localizedDataSource(provenance.source || state.data.data_source || "—")],
    [t("priceField"), provenance.price_field || "—"],
    [t("adjustment"), localizedAdjustment(provenance.adjustment)],
    [t("coverage"), provenance.start_date && provenance.end_date ? `${provenance.start_date} → ${provenance.end_date}` : "—"],
    [t("rows"), provenance.row_count == null ? "—" : Number(provenance.row_count).toLocaleString(state.language === "zh" ? "zh-CN" : "en-US")],
    [t("generated"), formatDateTime(provenance.generated_at)],
    [t("datasetFingerprint"), fingerprint === "—" ? fingerprint : `${fingerprint.slice(0, 16)}…`],
  ];
  elements.provenanceGrid.innerHTML = items
    .map(([label, value], index) => `<div class="provenance-item">
      <dt>${label}</dt>
      <dd${index === items.length - 1 && fingerprint !== "—" ? ` title="SHA-256: ${fingerprint}"` : ""}>${value}</dd>
    </div>`)
    .join("");
}

function buildAnalogSeries() {
  const lookbackData = getLookbackData();
  const view = getViewData();
  const padPast = Array(state.lookback - 1).fill(null);
  const padFuture = Array(30).fill(null);
  const series = [];

  for (const match of view.matches) {
    const combined = [...match.historical_path, ...match.forward_path.slice(1)].map((value) => value * 100);
    const selected = match.rank === state.selectedRank;
    series.push({
      name: `#${match.rank} ${match.end_date}`,
      type: "line",
      data: combined,
      symbol: "none",
      smooth: 0.12,
      silent: !selected,
      z: selected ? 7 : 2,
      lineStyle: {
        width: selected ? 2.2 : 0.8,
        color: selected ? COLORS.amber : COLORS.analog,
        opacity: selected ? 1 : 0.7,
      },
      emphasis: { disabled: true },
    });
  }

  const distribution = view.forward_distribution;
  const lower = [...padPast, ...distribution.map((point) => point.p25 * 100)];
  const band = [...padPast, ...distribution.map((point) => (point.p75 - point.p25) * 100)];
  const median = [...padPast, ...distribution.map((point) => point.median * 100)];

  series.push(
    {
      name: "P25",
      type: "line",
      data: lower,
      stack: "distribution-band",
      symbol: "none",
      silent: true,
      lineStyle: { opacity: 0 },
      areaStyle: { opacity: 0 },
      z: 3,
    },
    {
      name: t("rangeName"),
      type: "line",
      data: band,
      stack: "distribution-band",
      symbol: "none",
      silent: true,
      lineStyle: { opacity: 0 },
      areaStyle: { color: "rgba(98, 223, 160, 0.16)" },
      z: 3,
    },
    {
      name: t("forwardMedianName"),
      type: "line",
      data: median,
      symbol: "none",
      smooth: 0.15,
      silent: true,
      lineStyle: { width: 3, color: COLORS.green },
      z: 8,
    },
    {
      name: t("currentQqq"),
      type: "line",
      data: [...lookbackData.current_path.map((value) => value * 100), ...padFuture],
      symbol: "none",
      smooth: 0.12,
      silent: true,
      lineStyle: { width: 3, color: COLORS.cyan },
      z: 9,
      markLine: {
        silent: true,
        symbol: "none",
        lineStyle: { color: "rgba(232,240,245,.45)", width: 1, type: "dashed" },
        label: {
          show: true,
          formatter: t("matchEnd"),
          position: "insideEndTop",
          color: "#9aabb6",
          fontFamily: "monospace",
          fontSize: 9,
        },
        data: [{ xAxis: "0" }],
      },
    },
  );
  return series;
}

function renderAnalogChart() {
  const xValues = Array.from({ length: state.lookback + 30 }, (_, index) => index - (state.lookback - 1));
  state.analogChart.setOption(
    {
      animationDuration: 320,
      grid: { left: 62, right: 24, top: 24, bottom: 58 },
      tooltip: {
        trigger: "axis",
        confine: true,
        backgroundColor: "#0a1017",
        borderColor: COLORS.grid,
        textStyle: { color: COLORS.text, fontFamily: "monospace", fontSize: 10 },
        formatter: (params) => {
          const visible = params
            .filter((item) => item.value != null && !["P25", t("rangeName")].includes(item.seriesName))
            .slice(0, 6);
          const title = Number(params[0]?.axisValue) <= 0
            ? t("pastDay", { day: params[0]?.axisValue })
            : t("forwardDay", { day: params[0]?.axisValue });
          return `${title}<br/>${visible
            .map((item) => `${item.marker}${item.seriesName}: <strong>${Number(item.value).toFixed(2)}%</strong>`)
            .join("<br/>")}`;
        },
      },
      xAxis: {
        ...baseAxis(),
        type: "category",
        boundaryGap: false,
        data: xValues.map(String),
        name: t("tradingDaysAxis"),
        nameLocation: "middle",
        nameGap: 36,
        nameTextStyle: { color: COLORS.muted, fontFamily: "monospace", fontSize: 9 },
        axisLabel: {
          ...baseAxis().axisLabel,
          formatter: (value) => {
            const number = Number(value);
            if (number === 0) return "0";
            if (number === -(state.lookback - 1) || number === 30 || number % 5 === 0) return number > 0 ? `+${number}` : String(number);
            return "";
          },
        },
        splitLine: { show: false },
      },
      yAxis: {
        ...baseAxis(),
        type: "value",
        scale: true,
        axisLabel: { ...baseAxis().axisLabel, formatter: (value) => `${value > 0 ? "+" : ""}${value.toFixed(0)}%` },
      },
      series: buildAnalogSeries(),
    },
    true,
  );
}

function renderReturnsTable() {
  const stats = getViewData().statistics;
  elements.returnsTable.innerHTML = [5, 10, 20, 30]
    .map((horizon) => {
      const row = stats[`${horizon}d`];
      return `<tr>
        <td><strong>${horizon}D</strong></td>
        <td>${formatPercent(row.up_probability, 0, false)}</td>
        <td class="${valueClass(row.average)}">${formatPercent(row.average)}</td>
        <td class="${valueClass(row.median)}">${formatPercent(row.median)}</td>
        <td class="positive">${formatPercent(row.best)}</td>
        <td class="negative">${formatPercent(row.worst)}</td>
      </tr>`;
    })
    .join("");
}

function renderConsensus() {
  const consensus = state.data.consensus[state.mode];
  elements.overallConsensus.textContent = t("overall", { signal: t(`signal_${consensus.overall}`) });
  elements.overallConsensus.className = `consensus-overall ${consensus.overall}`;
  elements.consensusGrid.innerHTML = [10, 15, 20, 30]
    .map((lookback) => {
      const item = consensus.windows[String(lookback)];
      return `<article class="consensus-item">
        <span class="window-label">${t("windowLabel", { days: lookback })}</span>
        <strong class="signal-${item.signal}">${t(`signal_${item.signal}`)}</strong>
        <p>${formatPercent(item.up_probability_20d, 0, false)}</p>
        <small>${t("upMedian20", { value: formatPercent(item.median_return_20d) })}</small>
      </article>`;
    })
    .join("");
}

function renderMatchesTable() {
  elements.matchesTable.innerHTML = getViewData().matches
    .map(
      (match) => `<tr data-rank="${match.rank}" class="${match.rank === state.selectedRank ? "selected" : ""}" tabindex="0" aria-label="${t("selectAnalog", { date: match.end_date })}">
        <td>#${String(match.rank).padStart(2, "0")}</td>
        <td>${match.start_date} → ${match.end_date}</td>
        <td>${match.similarity.toFixed(1)}%</td>
        <td><span class="regime-chip ${match.market_regime === "bear" ? "bear" : ""}">${t(match.market_regime)}</span></td>
        <td class="${valueClass(match.returns["5d"])}">${formatPercent(match.returns["5d"])}</td>
        <td class="${valueClass(match.returns["10d"])}">${formatPercent(match.returns["10d"])}</td>
        <td class="${valueClass(match.returns["20d"])}">${formatPercent(match.returns["20d"])}</td>
        <td class="${valueClass(match.returns["30d"])}">${formatPercent(match.returns["30d"])}</td>
        <td class="negative">${formatPercent(match.max_drawdown_30d)}</td>
      </tr>`,
    )
    .join("");

  elements.matchesTable.querySelectorAll("tr").forEach((row) => {
    const select = () => {
      state.selectedRank = Number(row.dataset.rank);
      renderSelectedMatch();
      renderSimilarityBreakdown();
      renderMatchesTable();
      renderAnalogChart();
    };
    row.addEventListener("click", select);
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        select();
      }
    });
  });
}

function renderAll(resetSelection = true) {
  if (resetSelection) state.selectedRank = 1;
  renderStats();
  renderSelectedMatch();
  renderSimilarityBreakdown();
  renderAnalogChart();
  renderReturnsTable();
  renderConsensus();
  renderMatchesTable();
  renderProvenance();
}

function applyAnalysisFilters(lookback, sameRegimeOnly) {
  const allowedLookbacks = [10, 15, 20, 30];
  if (!allowedLookbacks.includes(lookback)) {
    throw new TypeError("lookback must be one of 10, 15, 20, or 30.");
  }
  if (typeof sameRegimeOnly !== "boolean") {
    throw new TypeError("sameRegimeOnly must be a boolean.");
  }
  if (!state.data) {
    throw new Error("Analysis data is still loading.");
  }

  state.lookback = lookback;
  state.mode = sameRegimeOnly ? "same_regime" : "all_regimes";
  elements.regimeOnly.checked = sameRegimeOnly;
  elements.lookbackButtons.forEach((item) => {
    const active = Number(item.dataset.lookback) === state.lookback;
    item.classList.toggle("active", active);
    item.setAttribute("aria-pressed", String(active));
  });
  renderAll();
  return {
    lookback: state.lookback,
    sameRegimeOnly,
    matchCount: getViewData().matches.length,
    upProbability20d: getViewData().statistics["20d"].up_probability,
    medianReturn20d: getViewData().statistics["20d"].median,
  };
}

function bindControls() {
  elements.languageButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const nextLanguage = button.dataset.language;
      if (nextLanguage === state.language) return;
      state.language = nextLanguage;
      try {
        localStorage.setItem("qqq-analog-language", state.language);
      } catch (error) {
        console.warn("Could not save language preference:", error);
      }
      applyStaticTranslations();
      if (state.data) {
        renderHeader();
        renderAll(false);
      }
    });
  });

  elements.lookbackButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const nextLookback = Number(button.dataset.lookback);
      if (nextLookback === state.lookback) return;
      applyAnalysisFilters(nextLookback, elements.regimeOnly.checked);
    });
  });

  elements.regimeOnly.addEventListener("change", () => {
    applyAnalysisFilters(state.lookback, elements.regimeOnly.checked);
  });

  window.addEventListener("resize", () => {
    state.analogChart?.resize();
  });
}

function observeChartContainers() {
  if (!window.ResizeObserver || state.resizeObserver) return;
  let frame = null;
  state.resizeObserver = new ResizeObserver(() => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      state.analogChart?.resize();
    });
  });
  state.resizeObserver.observe(document.querySelector("#analog-chart"));
}

function registerWebMCP() {
  const context = document.modelContext;
  if (!context?.registerTool) return;
  const lifecycle = new AbortController();
  window.addEventListener("beforeunload", () => lifecycle.abort(), { once: true });

  const registration = context.registerTool(
    {
      name: "configure_analog_analysis",
      title: "Configure QQQ analog analysis",
      description: "Set the observation window and optional same-market-regime filter, then update the visible QQQ historical analog dashboard.",
      inputSchema: {
        type: "object",
        properties: {
          lookback: { type: "integer", enum: [10, 15, 20, 30] },
          sameRegimeOnly: { type: "boolean" },
        },
        required: ["lookback", "sameRegimeOnly"],
        additionalProperties: false,
      },
      annotations: { readOnlyHint: false, untrustedContentHint: false },
      execute(input) {
        if (!input || typeof input !== "object" || Array.isArray(input)) {
          throw new TypeError("Input must be an object.");
        }
        return applyAnalysisFilters(input.lookback, input.sameRegimeOnly);
      },
    },
    { signal: lifecycle.signal },
  );
  Promise.resolve(registration).catch((error) => console.warn("WebMCP registration failed:", error));
}

async function loadData() {
  elements.loading.hidden = false;
  elements.error.hidden = true;
  elements.dashboard.hidden = true;
  try {
    const response = await fetch("./data/analogs.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.data = await response.json();
    if (!window.echarts) throw new Error("ECharts failed to load.");
    renderHeader();
    elements.loading.hidden = true;
    elements.dashboard.hidden = false;
    await new Promise((resolve) => requestAnimationFrame(resolve));
    state.analogChart ||= echarts.init(document.querySelector("#analog-chart"), null, { renderer: "canvas" });
    state.analogChart.resize();
    observeChartContainers();
    renderAll();
  } catch (error) {
    console.error(error);
    elements.loading.hidden = true;
    elements.error.hidden = false;
  }
}

elements.retry.addEventListener("click", loadData);
bindControls();
applyStaticTranslations();
registerWebMCP();
loadData();
