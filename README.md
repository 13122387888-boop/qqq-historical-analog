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
│   └── walk_forward_validation.json # 多历史时点无前视校验报告
├── scripts/
│   ├── fetch_data.py         # 下载、清洗并保存日线
│   ├── calculate_analogs.py  # 相似度、去重、未来表现和统计
│   └── validate_walk_forward.py # 滚动时点无前视审计
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

## 安装与生成数据

建议使用 Python 3.10+。

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
python scripts/calculate_analogs.py
python scripts/validate_walk_forward.py
```

第一条命令会输出 `data/qqq.csv` 和 `data/source.json`，第二条命令会输出 `data/analogs.json` 并在终端打印 15D Top Matches 与 5/10/20/30D Up Probability，方便人工复核。第三条命令会在多个历史截止日重新计算结果，并通过“污染截止日后的数据”验证任何未来价格都不会改变当时可见的匹配结果，报告写入 `data/walk_forward_validation.json`。

运行自动化校验：

```bash
python -m unittest discover -s tests -v
```

测试会检查归一化公式、未来价格不影响相似度、±20 交易日去重、每个结果都有完整 30D 未来路径、数据来源指纹、滚动无前视报告，以及四个窗口和两种 Regime 模式的数据契约。

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

项目全部使用相对路径，并包含 `.nojekyll`，因此不需要额外构建步骤。每次更新行情后，重新运行上述三个 Python 脚本，并提交 `data/qqq.csv`、`data/analogs.json`、`data/source.json` 和 `data/walk_forward_validation.json` 即可。

## 第一版边界

- 仅分析 QQQ Adj Close（不可用时使用 Close）。
- Regime 仅按 Price > MA200 判定 Bull，否则 Bear。
- 不使用 RSI、MACD、VIX、宏观数据、新闻、期权或机器学习。
- Historical Consensus 只是四个观察窗口的历史结果汇总，不是预测或目标价。
