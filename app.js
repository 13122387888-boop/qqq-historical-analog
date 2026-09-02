"use strict";

const I18N = {
  en: {
    siteTitle: "QQQ Historical Analog",
    metaDescription: "Find historically similar QQQ price patterns and examine what happened next.",
    languageAria: "Language",
    dataNotes: "Data notes",
    closeDialog: "Close data notes",
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
    upProbability: "Analog up rate",
    average: "Average",
    median: "Median",
    best: "Best",
    worst: "Worst",
    acrossWindows: "Across observation windows",
    historicalConsensus: "Evidence-gated Outlook",
    consensusFootnote: "A direction is shown only when holdout Brier advantage is statistically validated; otherwise the result is inconclusive.",
    rankedSimilarity: "Ranked by development-selected V2 similarity",
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
    calibratedUpProbability20: "20D Calibrated Up Probability",
    analogEvidenceDetail: "{weight}% analog evidence · ESS {ess}",
    calibratedProbabilityDetail: "Regime base {base} · analog edge {edge} · evidence {weight}% · ESS {ess}",
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
    signal_inconclusive: "Inconclusive",
    similarityBreakdown: "Similarity breakdown",
    blendedWeightNote: "V2 weights: {price}% path · {returns}% returns · {regime}% state",
    priceSimilarity: "Price-path similarity",
    returnSimilarity: "Daily-return similarity",
    regimeSimilarity: "Market-state similarity",
    selectedCaseWeight: "Selected-case weight",
    effectiveSampleSize: "Effective sample size {value}",
    priceRmse: "Price-path RMSE",
    returnRmse: "Return-path RMSE",
    weightLabel: "{value}% weight",
    lowerIsCloser: "Lower is closer",
    scoreNotProbability: "Similarity scores are ranking measures—not probabilities.",
    auditTrail: "Audit trail",
    dataProvenance: "Data Provenance",
    algorithmVersion: "V1 {version} · V2 {v2}",
    source: "Source",
    priceField: "Price field",
    adjustment: "Adjustment",
    coverage: "Coverage",
    rows: "Trading days",
    generated: "Generated",
    datasetFingerprint: "Dataset fingerprint",
    modelValidation: "Point-in-time model validation",
    walkForwardBacktest: "V1 vs V2 Walk-forward Backtest",
    backtestNote: "V2 parameters were selected on 2010–2022 only, then evaluated on the 2023+ holdout. Lower Brier is better.",
    v1Brier: "V1 Brier",
    v2Brier: "V2 Brier",
    regimeBaseline: "Regime baseline",
    brierSkill: "Brier skill",
    hitRate: "Hit rate",
    evidence: "Evidence",
    horizonsBeatBaseline: "{count}/4 horizons have validated analog edge",
    verdict_validated_edge: "Validated edge",
    verdict_promising_not_conclusive: "Promising, not conclusive",
    verdict_no_observed_edge: "No observed edge",
    prospectiveValidation: "Prospective validation",
    shadowChallenger: "Shadow Challenger",
    shadowNote: "Frozen research model; it does not affect the official outlook.",
    shadowWaiting: "Waiting for outcomes",
    shadowReview: "Eligible for review",
    shadowIssued: "Forecast issued",
    latestObservationOnly: "Latest observation only",
    shadowRiskTarget: "30D ≥3% drawdown",
    challengerProbability: "Challenger probability",
    shadowBaseline: "Regime baseline",
    sameRegimeHistory: "Same-MA200-regime history",
    shadowEvidence: "Forward evidence",
    shadowEvidenceCount: "{matured} matured · {pending} pending",
    shadowPromotionGate: "Minimum {count} matured forecasts + positive 95% CI",
    methodologyAndAudit: "Methodology and audit",
    notesDataTitle: "Data convention",
    notesDataBody: "QQQ daily data from {source}; {field} is used with {adjustment}. Coverage: {start} to {end}, {rows} trading days.",
    notesAnalogTitle: "Published V1 analog model",
    notesAnalogBody: "The similarity rank combines 70% normalized-price-path RMSE and 30% daily-return RMSE. It selects 20 cases separated by more than 20 trading days. Similarity is a ranking score, not a probability.",
    notesV2Title: "Selected V2 configuration",
    notesV2Body: "For the current {lookback}D view, development-only selection chose {price}% price path, {returns}% daily returns and {regime}% soft market state; Top {topK}, {kernel}. The 20D probability gives analog evidence a {alpha}% weight and shrinks the rest toward the same-regime base rate.",
    notesPointInTimeTitle: "Point-in-time rule",
    notesPointInTimeBody: "At each historical forecast date, candidate outcomes had to be fully known: candidate end + 30 trading days could not exceed the forecast date. Future rows never enter similarity calculations.",
    notesBacktestTitle: "Backtest convention",
    notesBacktestBody: "Forecasts are generated every trading day from {backtestStart} to {backtestEnd}. The development period ends in 2022; {holdout} is shown as the retrospective holdout. Overlapping forecasts are retained, so 95% uncertainty uses a {block}-day moving-block bootstrap.",
    notesMetricsTitle: "How to read the metrics",
    notesMetricsBody: "Brier score evaluates probability accuracy and is better when lower. Brier skill above 0% means the analog model beats the point-in-time probability for the same MA200 regime. Hit rate is secondary and does not measure calibration.",
    notesShadowTitle: "Prospective shadow test",
    notesShadowBody: "The frozen challenger estimates the chance of a 3% peak-to-trough drawdown within 30 trading days. It began on {shadowStart}; {shadowMatured} forecasts have matured and {shadowPending} remain pending. It never changes the official outlook automatically and is reviewed only after at least {shadowMinimum} matured forecasts with a positive 95% block-bootstrap lower bound.",
    notesAuditTitle: "Interpretation boundary",
    notesAuditBody: "The no-look-ahead audit verifies data isolation; the backtest measures historical predictive value. V2 was selected without using the 2023+ holdout, but its small holdout improvement is not statistically conclusive and does not guarantee future performance.",
    optimizedV2Weight: "Optimized V2 weight",
    softMarketState: "Soft market state",
    selectedAnalogCount: "Selected analogs",
    distanceWeighted: "Distance weighted",
    equalWeighted: "Equal weighted",
  },
  zh: {
    siteTitle: "QQQ 历史相似行情",
    metaDescription: "寻找与 QQQ 当前走势最相似的历史行情，并查看随后真实发生了什么。",
    languageAria: "语言",
    dataNotes: "数据口径",
    closeDialog: "关闭数据口径",
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
    upProbability: "相似案例上涨率",
    average: "平均收益",
    median: "中位数收益",
    best: "最好",
    worst: "最差",
    acrossWindows: "多观察窗口对比",
    historicalConsensus: "证据门槛结论",
    consensusFootnote: "只有留出期 Brier 优势通过统计检验才显示方向，否则统一标为证据不足。",
    rankedSimilarity: "按开发期选出的V2相似度排序",
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
    calibratedUpProbability20: "20日校准后上涨概率",
    analogEvidenceDetail: "相似行情证据权重 {weight}% · 有效样本 {ess}",
    calibratedProbabilityDetail: "市场环境基础 {base} · 相似增量 {edge} · 证据权重 {weight}% · 有效样本 {ess}",
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
    signal_inconclusive: "证据不足",
    similarityBreakdown: "相似度分解",
    blendedWeightNote: "V2权重：价格{price}% · 收益{returns}% · 环境{regime}%",
    priceSimilarity: "价格路径相似度",
    returnSimilarity: "每日收益相似度",
    regimeSimilarity: "市场状态相似度",
    selectedCaseWeight: "该案例分析权重",
    effectiveSampleSize: "有效样本量 {value}",
    priceRmse: "价格路径 RMSE",
    returnRmse: "收益路径 RMSE",
    weightLabel: "权重 {value}%",
    lowerIsCloser: "数值越低越接近",
    scoreNotProbability: "相似度仅用于排序，并非概率。",
    auditTrail: "审计信息",
    dataProvenance: "数据可追溯性",
    algorithmVersion: "V1 {version} · V2 {v2}",
    source: "数据源",
    priceField: "价格字段",
    adjustment: "复权方式",
    coverage: "数据区间",
    rows: "交易日数量",
    generated: "生成时间",
    datasetFingerprint: "数据指纹",
    modelValidation: "逐时点模型验证",
    walkForwardBacktest: "V1 与 V2 滚动回测",
    backtestNote: "V2参数只用2010—2022年选择，再在2023年后的留出期检验；Brier越低越好。",
    v1Brier: "V1 Brier",
    v2Brier: "V2 Brier",
    regimeBaseline: "市场环境基准",
    brierSkill: "Brier 提升",
    hitRate: "方向命中率",
    evidence: "证据判断",
    horizonsBeatBaseline: "{count}/4 个周期的相似增量通过检验",
    verdict_validated_edge: "优势通过检验",
    verdict_promising_not_conclusive: "有改善但证据不足",
    verdict_no_observed_edge: "暂未观察到优势",
    prospectiveValidation: "前向验证",
    shadowChallenger: "影子挑战模型",
    shadowNote: "参数已经冻结，仅用于积累研究证据，不影响正式结论。",
    shadowWaiting: "等待结果成熟",
    shadowReview: "可以进入复核",
    shadowIssued: "预测登记日",
    latestObservationOnly: "只登记最新观测，不回填",
    shadowRiskTarget: "30日内≥3%回撤",
    challengerProbability: "挑战模型概率",
    shadowBaseline: "市场环境基准",
    sameRegimeHistory: "同MA200环境历史统计",
    shadowEvidence: "前向证据",
    shadowEvidenceCount: "已成熟 {matured} · 待验证 {pending}",
    shadowPromotionGate: "至少{count}条成熟预测，且95%置信区间下界大于零",
    methodologyAndAudit: "方法与审计说明",
    notesDataTitle: "数据口径",
    notesDataBody: "QQQ 日线来自 {source}；使用 {field}，复权方式为{adjustment}。覆盖 {start} 至 {end}，共 {rows} 个交易日。",
    notesAnalogTitle: "当前发布的 V1 相似模型",
    notesAnalogBody: "相似度排名由70%归一化价格路径 RMSE和30%每日收益 RMSE组成；选取20个案例，案例结束日彼此间隔超过20个交易日。相似度只是排序分数，不是概率。",
    notesV2Title: "V2已选参数",
    notesV2Body: "当前{lookback}日视图仅用开发期选出：价格路径{price}%、每日收益{returns}%、软市场状态{regime}%；Top {topK}，{kernel}。20日概率仅给予相似行情{alpha}%证据权重，其余向同市场环境基础概率收缩。",
    notesPointInTimeTitle: "逐时点规则",
    notesPointInTimeBody: "在每个历史预测日，候选案例的结果必须已经完整发生，即候选结束日加30个交易日不得晚于预测日；相似度计算绝不读取未来行。",
    notesBacktestTitle: "回测口径",
    notesBacktestBody: "从 {backtestStart} 至 {backtestEnd} 的每个交易日生成预测；开发期截至2022年，{holdout}作为回溯式留出期展示。相邻预测存在重叠，因此95%不确定性采用{block}日移动区块自助法估计。",
    notesMetricsTitle: "指标怎么读",
    notesMetricsBody: "Brier 分数衡量概率准确度，越低越好；Brier 提升高于0%表示相似模型优于当时同MA200市场环境的基础上涨概率。方向命中率只是辅助指标，不能衡量概率校准。",
    notesShadowTitle: "影子前向检验",
    notesShadowBody: "冻结的挑战模型估计未来30个交易日内出现3%峰谷回撤的概率。检验始于{shadowStart}；当前已有{shadowMatured}条预测成熟，{shadowPending}条等待结果。它不会自动改变正式结论，只有至少{shadowMinimum}条预测成熟且区块自助法95%置信区间下界大于零时，才进入人工复核。",
    notesAuditTitle: "结论边界",
    notesAuditBody: "无前视审计验证数据隔离，滚动回测检验历史预测价值。V2选参没有使用2023年后的留出期，但留出期改善很小且统计证据不足，也不保证未来表现。",
    optimizedV2Weight: "V2优化权重",
    softMarketState: "软市场状态",
    selectedAnalogCount: "入选案例数",
    distanceWeighted: "按距离加权",
    equalWeighted: "等权",
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
  backtest: null,
  v2: null,
  shadow: null,
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
  dataNotesButton: document.querySelector("#data-notes-button"),
  dataNotesDialog: document.querySelector("#data-notes-dialog"),
  dataNotesClose: document.querySelector("#data-notes-close"),
  dataNotesBody: document.querySelector("#data-notes-body"),
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
  backtestPanel: document.querySelector("#backtest-panel"),
  backtestPeriod: document.querySelector("#backtest-period"),
  backtestSummary: document.querySelector("#backtest-summary"),
  backtestTable: document.querySelector("#backtest-table-body"),
  shadowPanel: document.querySelector("#shadow-panel"),
  shadowStatus: document.querySelector("#shadow-status"),
  shadowIssuedDate: document.querySelector("#shadow-issued-date"),
  shadowRiskProbability: document.querySelector("#shadow-risk-probability"),
  shadowBaselineProbability: document.querySelector("#shadow-baseline-probability"),
  shadowEvidenceCount: document.querySelector("#shadow-evidence-count"),
  shadowPromotionGate: document.querySelector("#shadow-promotion-gate"),
  methodPriceWeight: document.querySelector("#method-price-weight"),
  methodReturnWeight: document.querySelector("#method-return-weight"),
  methodRegimeWeight: document.querySelector("#method-regime-weight"),
  methodTopK: document.querySelector("#method-top-k"),
  methodKernel: document.querySelector("#method-kernel"),
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

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
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

function getV2Selection(lookback = state.lookback, mode = state.mode) {
  return state.v2?.selections?.[String(lookback)]?.[mode] || null;
}

function getViewData() {
  return getV2Selection()?.current_forecast?.display_view || getLookbackData()[state.mode];
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
  const v2Forecast = getV2Selection()?.current_forecast;
  const calibrated20 = v2Forecast?.horizons?.["20d"];
  const cards = [
    {
      label: t(calibrated20 ? "calibratedUpProbability20" : "upProbability20"),
      value: formatPercent(calibrated20?.calibrated_probability ?? stats["20d"].up_probability, 0, false),
      detail: calibrated20
        ? t("calibratedProbabilityDetail", {
            base: formatPercent(calibrated20.regime_probability, 0, false),
            edge: `${calibrated20.calibrated_probability >= calibrated20.regime_probability ? "+" : ""}${((calibrated20.calibrated_probability - calibrated20.regime_probability) * 100).toFixed(1)}pp`,
            weight: Math.round(calibrated20.analog_evidence_weight * 100),
            ess: v2Forecast.effective_sample_size.toFixed(1),
          })
        : t("independentAnalogs", { count: view.matches.length }),
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
  const selection = getV2Selection();
  const profile = selection?.champion?.profile || {
    price_weight: 0.7,
    return_weight: 0.3,
    regime_weight: 0,
  };
  const metrics = [
    { label: t("priceSimilarity"), value: `${match.price_similarity.toFixed(1)}%`, detail: t("weightLabel", { value: Math.round(profile.price_weight * 100) }) },
    { label: t("returnSimilarity"), value: `${match.return_similarity.toFixed(1)}%`, detail: t("weightLabel", { value: Math.round(profile.return_weight * 100) }) },
    { label: t("regimeSimilarity"), value: `${(match.regime_similarity ?? 100).toFixed(1)}%`, detail: t("weightLabel", { value: Math.round(profile.regime_weight * 100) }) },
    { label: t("selectedCaseWeight"), value: formatPercent(match.analysis_weight ?? 1 / getViewData().matches.length, 1, false), detail: t("effectiveSampleSize", { value: (selection?.current_forecast?.effective_sample_size ?? getViewData().matches.length).toFixed(1) }) },
  ];
  elements.similarityBreakdown.innerHTML = `
    <div class="breakdown-intro">
      <strong>${t("similarityBreakdown")}</strong>
      <span>${t("blendedWeightNote", {
        price: Math.round(profile.price_weight * 100),
        returns: Math.round(profile.return_weight * 100),
        regime: Math.round(profile.regime_weight * 100),
      })}</span>
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
    v2: state.v2?.model_version || "—",
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

function renderBacktest() {
  const v1Result = state.backtest?.results?.[String(state.lookback)]?.[state.mode];
  const v2Result = getV2Selection()?.backtest;
  if (!v1Result || !v2Result) {
    elements.backtestPanel.hidden = true;
    return;
  }

  const horizons = [5, 10, 20, 30];
  const holdoutRows = horizons.map((horizon) => ({
    v1: v1Result[`${horizon}d`].holdout,
    v2: v2Result[`${horizon}d`].holdout,
  }));
  const positiveCount = holdoutRows.filter((row) => row.v2.verdict === "validated_edge").length;
  const setup = state.v2.selection_policy || state.backtest.setup || {};
  elements.backtestPanel.hidden = false;
  elements.backtestPeriod.textContent = (setup.holdout_period || "—").replace(" to ", " → ");
  elements.backtestSummary.textContent = t("horizonsBeatBaseline", { count: positiveCount });
  elements.backtestSummary.className = `backtest-summary ${positiveCount >= 3 ? "positive" : positiveCount === 0 ? "negative" : "mixed"}`;

  elements.backtestTable.innerHTML = horizons
    .map((horizon, index) => {
      const row = holdoutRows[index];
      const ci = row.v2.brier_advantage_vs_regime_ci95 || [];
      const verdict = t(`verdict_${row.v2.verdict}`);
      return `<tr>
        <td><strong>${horizon}D</strong><small>n=${Number(row.v2.sample_count).toLocaleString()}</small></td>
        <td>${row.v1.analog_brier.toFixed(3)}</td>
        <td>${row.v2.v2_brier.toFixed(3)}</td>
        <td>${row.v2.regime_brier.toFixed(3)}</td>
        <td class="${valueClass(row.v2.brier_skill_vs_regime)}">${formatPercent(row.v2.brier_skill_vs_regime)}</td>
        <td><span class="evidence-chip ${row.v2.verdict}" title="95% CI: ${ci.map((value) => Number(value).toFixed(4)).join(" → ")}">${verdict}</span></td>
      </tr>`;
    })
    .join("");
}

function renderShadowValidation() {
  const shadow = state.shadow;
  const latest = shadow?.records?.at(-1);
  const evaluation = shadow?.evaluation;
  if (!shadow || !latest || !evaluation) {
    elements.shadowPanel.hidden = true;
    return;
  }
  const reviewEligible = evaluation.promotion_status === "eligible_for_model_review";
  elements.shadowPanel.hidden = false;
  elements.shadowStatus.textContent = t(reviewEligible ? "shadowReview" : "shadowWaiting");
  elements.shadowStatus.className = `shadow-status ${reviewEligible ? "review" : "pending"}`;
  elements.shadowIssuedDate.textContent = compactDate(latest.forecast_date);
  elements.shadowRiskProbability.textContent = formatPercent(latest.challenger_probability, 0, false);
  elements.shadowBaselineProbability.textContent = formatPercent(latest.baseline_probability, 0, false);
  elements.shadowEvidenceCount.textContent = t("shadowEvidenceCount", {
    matured: evaluation.matured_forecasts,
    pending: evaluation.pending_forecasts,
  });
  elements.shadowPromotionGate.textContent = t("shadowPromotionGate", {
    count: evaluation.minimum_matured_forecasts,
  });
}

function renderMethodology() {
  const champion = getV2Selection()?.champion;
  if (!champion) return;
  elements.methodPriceWeight.textContent = `${Math.round(champion.profile.price_weight * 100)}%`;
  elements.methodReturnWeight.textContent = `${Math.round(champion.profile.return_weight * 100)}%`;
  elements.methodRegimeWeight.textContent = `${Math.round(champion.profile.regime_weight * 100)}%`;
  elements.methodTopK.textContent = `K=${champion.top_k}`;
  elements.methodKernel.textContent = t(champion.kernel === "distance" ? "distanceWeighted" : "equalWeighted");
}

function renderDataNotes() {
  if (!state.data || !state.backtest) return;
  const provenance = state.data.data_provenance || {};
  const setup = state.backtest.setup || {};
  const selection = getV2Selection();
  const champion = selection?.champion;
  const profile = champion?.profile || { price_weight: 0.7, return_weight: 0.3, regime_weight: 0 };
  const alpha20 = selection?.horizon_calibration?.["20d"]?.alpha ?? 0;
  const shadowEvaluation = state.shadow?.evaluation || {};
  const shadowStart = state.shadow?.records?.[0]?.forecast_date || "—";
  const variables = {
    source: localizedDataSource(provenance.source || state.data.data_source || "—"),
    field: provenance.price_field || "—",
    adjustment: localizedAdjustment(provenance.adjustment),
    start: provenance.start_date || "—",
    end: provenance.end_date || "—",
    rows: Number(provenance.row_count || 0).toLocaleString(state.language === "zh" ? "zh-CN" : "en-US"),
    backtestStart: setup.evaluation_start || "—",
    backtestEnd: setup.evaluation_end || "—",
    holdout: (setup.holdout_period || "—").replace(" to ", " → "),
    block: setup.bootstrap_block_days || 30,
    lookback: state.lookback,
    price: Math.round(profile.price_weight * 100),
    returns: Math.round(profile.return_weight * 100),
    regime: Math.round(profile.regime_weight * 100),
    topK: champion?.top_k || 20,
    kernel: t(champion?.kernel === "distance" ? "distanceWeighted" : "equalWeighted"),
    alpha: Math.round(alpha20 * 100),
    shadowStart,
    shadowMatured: shadowEvaluation.matured_forecasts ?? 0,
    shadowPending: shadowEvaluation.pending_forecasts ?? 0,
    shadowMinimum: shadowEvaluation.minimum_matured_forecasts ?? 252,
  };
  const sections = [
    ["notesDataTitle", "notesDataBody"],
    ["notesAnalogTitle", "notesAnalogBody"],
    ["notesV2Title", "notesV2Body"],
    ["notesPointInTimeTitle", "notesPointInTimeBody"],
    ["notesBacktestTitle", "notesBacktestBody"],
    ["notesMetricsTitle", "notesMetricsBody"],
    ["notesShadowTitle", "notesShadowBody"],
    ["notesAuditTitle", "notesAuditBody"],
  ];
  elements.dataNotesBody.innerHTML = sections
    .map(([titleKey, bodyKey]) => `<section><h3>${escapeHtml(t(titleKey))}</h3><p>${escapeHtml(t(bodyKey, variables))}</p></section>`)
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
  let consensus = state.data.consensus[state.mode];
  if (state.v2) {
    const windows = {};
    const labels = [];
    for (const lookback of [10, 15, 20, 30]) {
      const selection = getV2Selection(lookback, state.mode);
      const forecast = selection.current_forecast.horizons["20d"];
      const probability = forecast.calibrated_probability;
      const validated = selection.backtest?.["20d"]?.holdout?.verdict === "validated_edge";
      const signal = validated
        ? probability >= 0.6
          ? "bullish"
          : probability < 0.4
            ? "bearish"
            : "neutral"
        : "inconclusive";
      labels.push(signal);
      windows[String(lookback)] = {
        signal,
        up_probability_20d: probability,
        median_return_20d: forecast.weighted_median_return,
      };
    }
    consensus = {
      overall: labels.every((label) => label === "inconclusive")
        ? "inconclusive"
        : labels.filter((label) => label === "bullish").length >= 3
        ? "bullish"
        : labels.filter((label) => label === "bearish").length >= 3
          ? "bearish"
          : "mixed",
      windows,
    };
  }
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
  renderBacktest();
  renderShadowValidation();
  renderMethodology();
  renderProvenance();
  renderDataNotes();
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
  const v2Forecast = getV2Selection()?.current_forecast?.horizons?.["20d"];
  return {
    lookback: state.lookback,
    sameRegimeOnly,
    matchCount: getViewData().matches.length,
    upProbability20d: v2Forecast?.calibrated_probability ?? getViewData().statistics["20d"].up_probability,
    medianReturn20d: v2Forecast?.weighted_median_return ?? getViewData().statistics["20d"].median,
  };
}

function bindControls() {
  elements.dataNotesButton.addEventListener("click", () => {
    if (typeof elements.dataNotesDialog.showModal === "function") {
      elements.dataNotesDialog.showModal();
    } else {
      elements.dataNotesDialog.setAttribute("open", "");
    }
  });
  elements.dataNotesClose.addEventListener("click", () => elements.dataNotesDialog.close());
  elements.dataNotesDialog.addEventListener("click", (event) => {
    if (event.target === elements.dataNotesDialog) elements.dataNotesDialog.close();
  });

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
    const [analysisResponse, backtestResponse, v2Response, shadowResponse] = await Promise.all([
      fetch("./data/analogs.json", { cache: "no-store" }),
      fetch("./data/backtest.json", { cache: "no-store" }),
      fetch("./data/v2_model.json", { cache: "no-store" }),
      fetch("./data/shadow_validation.json", { cache: "no-store" }).catch(() => null),
    ]);
    if (!analysisResponse.ok) throw new Error(`Analysis data HTTP ${analysisResponse.status}`);
    if (!backtestResponse.ok) throw new Error(`Backtest data HTTP ${backtestResponse.status}`);
    if (!v2Response.ok) throw new Error(`V2 model HTTP ${v2Response.status}`);
    [state.data, state.backtest, state.v2, state.shadow] = await Promise.all([
      analysisResponse.json(),
      backtestResponse.json(),
      v2Response.json(),
      shadowResponse?.ok ? shadowResponse.json() : Promise.resolve(null),
    ]);
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
