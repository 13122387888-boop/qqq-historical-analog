# QQQ Historical Analog

一个纯静态、可本地运行并可直接部署到 GitHub Pages 的 QQQ 历史相似行情分析工具。项目先用 Python 下载和清洗日线、计算历史相似区间及其真实后续表现，再由 HTML / CSS / Vanilla JavaScript 读取预计算 JSON；浏览器不会实时扫描全部历史数据。页面支持中文 / English 即时切换，并会在当前浏览器保存语言偏好。

> Historical similarity does not imply future performance. This tool is for research and educational purposes only and does not constitute investment advice.

## 项目结构

```text
qqq-historical-analog/
├── index.html                 # 页面结构
├── style.css                 # 暗色金融终端主题与响应式样式
├── app.js                    # JSON 读取、筛选、图表和表格交互
├── favicon.svg
├── assets/
│   └── echarts.min.js        # 本地化 ECharts，无 CDN 依赖
├── data/
│   ├── qqq.csv               # 清洗后的 QQQ 日线
│   ├── analogs.json          # 四个窗口、两种 Regime 模式的完整结果
│   ├── source.json           # 数据来源、复权方式与 CSV 指纹
│   ├── walk_forward_validation.json # 多历史时点无前视校验报告
│   ├── backtest.json         # V1逐日滚动预测回测、基准与可靠性指标
│   ├── v2_model.json         # V2选参、留出检验、当前预测与展示案例
│   └── shadow_validation.json # 冻结挑战模型的前向预测账本
├── scripts/
│   ├── fetch_data.py         # 下载、清洗并保存日线
│   ├── calculate_analogs.py  # 相似度、去重、未来表现和统计
│   ├── validate_walk_forward.py # 滚动时点无前视审计
│   ├── backtest_walk_forward.py # V1 逐日滚动预测效果回测
│   ├── optimize_similarity_v2.py # V2开发期选参、概率收缩与留出检验
│   └── update_shadow_validation.py # 登记并结算影子前向预测
├── tests/
│   └── test_calculate_analogs.py
├── requirements.txt
├── .nojekyll
└── .gitignore
```

## 数据来源

`fetch_data.py` 默认先通过 `yfinance` 获取 Yahoo Finance 数据。本项目随附的 `qqq.csv` 在 2026-09-02 生成时遇到 Yahoo 限流，因此自动使用了 Longbridge Securities 的前复权日线作为只读备用源；实际覆盖 2000-01-03 至 2026-09-01，共 6,706 个交易日。备用源不提供单独的 Adj Close 字段，因此脚本按需求使用复权后的 Close 同步填入 Adj Close。

数据清洗包括：日期解析、数值转换、关键字段空值删除、重复日期去除、日期升序和非正价格排除。每次生成都会记录数据源、价格字段、复权方式、覆盖区间、行数、生成时间和 CSV 的 SHA-256 指纹；`analogs.json` 同时包含 schema 与算法版本，页面底部会直接展示这些审计信息。

## 相似度算法

每个 N 日窗口先把首日价格归一化为 100：

```text
normalized_price[i] = price[i] / price[0] × 100
```

随后分别计算归一化价格路径 RMSE 与日收益率路径 RMSE，并用稳定的单调指数映射转成 0–100 的显示分数：

```text
price_similarity  = 100 × exp(-price_rmse / 5.0)
return_similarity = 100 × exp(-return_rmse / 0.02)
final_similarity  = 0.70 × price_similarity + 0.30 × return_similarity
```

Similarity Score 仅是用于排序的相似度显示分数，不是上涨概率，也不是统计置信度。

为避免 Look-ahead Bias，相似度只读取 Historical Match 结束日及以前的数据；结束日之后的数据只用于 5/10/20/30D Forward Return、30D Max Drawdown / Max Gain 和 Forward Distribution。候选结束日必须拥有完整的未来 30 个交易日。候选按相似度降序贪心选择，任意两个最终案例的结束日索引距离必须大于 20 个交易日。

## 滚动回测

`backtest_walk_forward.py` 保持 V1 的 70/30 权重、Top 20 和去重规则不变，从 2010 年起在每个交易日重新生成当时可得的预测。候选案例必须满足“结束日 + 30 个交易日不晚于预测日”，因此预测时使用的每个候选结果在当时都已完整发生。2010—2022 年作为开发观察期，2023 年起作为回溯式留出期。

核心指标为 Brier Score（越低越好），并与当时同 MA200 市场环境下的历史上涨基础概率比较；同时记录方向命中率、收益中位数 MAE、50%/80%区间覆盖率和年度稳定性。由于相邻交易日预测的未来区间会重叠，95%区间使用30交易日移动区块自助法估计。页面中的“数据口径”弹窗集中说明数据源、复权、逐时点规则、回测划分和结论边界。

## V2 概率模型

V2只用2010—2022年开发期选择参数，2023年后的数据不参与选参。搜索空间包括价格路径、每日收益和软市场状态的组合权重、Top K（10/20/30）以及等权或距离加权。软市场状态由 Price/MA200、MA50/MA200、20日年化波动率和60日回撤组成。

V2不会直接把历史案例上涨比例当作预测概率，而使用保守收缩公式：

```text
calibrated_probability = regime_probability
                       + alpha × (analog_probability - regime_probability)
```

`alpha`只在开发期从0/25%/50%/75%/100%中选择；如果相似行情证据不稳定，模型会自动退回同MA200市场环境的基础概率。参数目标为“年度平均Brier优势减去0.25倍年度波动”，降低只在少数年份有效的过拟合风险。当前页面的折线图、案例表、加权分布和校准概率均来自已锁定的V2配置，V1结果保留在回测对照列中。

页面另外使用“证据门槛”约束方向性结论：只有留出期相对市场环境基准的 Brier 优势经移动区块自助法确认（95%区间下限高于0），才显示看多或看空；否则显示“证据不足”。概率卡同时拆分市场环境基础概率与相似行情增量，避免把市场长期上涨倾向误读成相似模型的独立预测能力。

## 影子前向验证

研究阶段发现“未来30个交易日内出现至少3%峰谷回撤”的内部状态模型值得继续观察，但历史置信区间仍跨过零，因此它不会进入正式结论。`update_shadow_validation.py` 已将模型结构冻结，并从最新观测日开始维护独立预测账本。

脚本每次只登记 `qqq.csv` 中最新日期的一条预测，不补录遗漏日期；已有预测在出现30个新交易日后自动结算。模型不会在影子期重新拟合，也不会自动升级。只有至少252条预测成熟，并且相对同MA200市场环境基准的Brier优势95%移动区块自助区间下界大于0时，才标记为可以人工复核。

## 安装与生成数据

建议使用 Python 3.10+。

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
python scripts/calculate_analogs.py
python scripts/validate_walk_forward.py
python scripts/backtest_walk_forward.py
python scripts/optimize_similarity_v2.py
python scripts/update_shadow_validation.py
```

第一条命令会输出 `data/qqq.csv` 和 `data/source.json`，第二条命令会输出 `data/analogs.json`。第三条命令通过“污染截止日后的数据”验证未来价格不会改变当时可见的匹配结果，报告写入 `data/walk_forward_validation.json`。第四条命令生成V1完整逐日预测回测并写入 `data/backtest.json`。第五条只用开发期选择V2参数、执行每日留出检验并输出 `data/v2_model.json`。

运行自动化校验：

```bash
python -m unittest discover -s tests -v
```

测试会检查归一化公式、未来价格不影响相似度、±20 交易日去重、每个结果都有完整 30D 未来路径、数据来源指纹、滚动无前视报告、四个窗口和两种 Regime 模式的数据契约，以及影子账本的冻结、幂等登记和30交易日结算规则。

## 本地启动

在项目根目录运行：

```bash
python -m http.server 8000
```

浏览器访问：

```text
http://localhost:8000
```

不要直接双击 `index.html`，因为浏览器通常会阻止 `file://` 页面读取本地 JSON。

## 部署到 GitHub Pages

1. 新建 GitHub 仓库并把此目录内容提交到仓库根目录。
2. 推送到 `main` 分支。
3. 打开仓库的 **Settings → Pages**。
4. 在 **Build and deployment** 中选择 **Deploy from a branch**。
5. 选择 `main` 与 `/(root)`，保存。
6. 等待 Pages 发布完成后访问 GitHub 提供的网址。

项目全部使用相对路径，并包含 `.nojekyll`，因此不需要额外构建步骤。每次更新行情后，重新运行上述六个 Python 脚本，并提交 `data/qqq.csv`、`data/analogs.json`、`data/source.json`、`data/walk_forward_validation.json`、`data/backtest.json`、`data/v2_model.json` 和 `data/shadow_validation.json` 即可。

## 第一版边界

- 仅分析 QQQ Adj Close（不可用时使用 Close）。
- Regime 仅按 Price > MA200 判定 Bull，否则 Bear。
- 正式V2不使用 RSI、MACD、VIX、宏观数据、新闻、期权或机器学习；影子挑战模型仅使用QQQ自身的均线位置、历史波动率和近期回撤。
- Historical Consensus 只是四个观察窗口的历史结果汇总，不是预测或目标价。
