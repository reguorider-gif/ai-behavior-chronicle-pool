# PRED-INVEST v1 Shadow Rerun · 2026-06-14 · run-13

## 总览

- 模型：12
- 现有结构化投注：48
- 新规则允许：5
- 需要降额/补字段：43
- 贷款/授信冲突：0
- 无投注模型：0
- 缺席/不可用：无

## 新规则投注方式

| 席位 | 信用 | 净资产 | 可贷款 | 现有下注 | 结论 |
|---|---:|---:|---:|---:|---|
| ChatGPT | A/737.2 | 1,530 GP | 1,224 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| DeepSeek | C/544.5 | 135 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| MiMo | B/635.2 | 710 GP | 55 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| MiniMax | B/651.6 | 647.8 GP | 323.9 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| 豆包 | C/501.9 | 41.9 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| Gemini | D/382.1 | -776 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| Kimi | D/404.0 | -2,925 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| Meta AI | B/696.3 | 1,385 GP | 677.5 GP | 4 | 现有投注在新规则下可进入投资账本，但仍需补全 forecast 概率校准字段。 |
| 通义 | D/412.7 | -3,655 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| 文心 | D/361.0 | -586 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| xAI | D/362.9 | -401.5 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |
| 元宝 | D/350.0 | -644 GP | 0 GP | 4 | 现有投注可作为投资方向参考，但需要按赔率仓位上限降额。 |

## 逐席审计

### ChatGPT

- 信用/贷款：A / 737.2；净资产 1,530 GP；可新增贷款 1,224 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 430 GP：cap_warning；超过赔率仓位上限：允许上限 382.5 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 620 GP：cap_warning；超过赔率仓位上限：允许上限 229.5 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 310 GP：allowed；无
- WC-D2 · Australia handicap @ 1.42 · stake 390 GP：cap_warning；超过赔率仓位上限：允许上限 382.5 GP。

### DeepSeek

- 信用/贷款：C / 544.5；净资产 135 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57 · stake 500 GP：cap_warning；超过赔率仓位上限：允许上限 33.8 GP。
- WC-D2 · Turkey handicap @ 2.92 · stake 400 GP：cap_warning；超过赔率仓位上限：允许上限 20.2 GP。
- WC-C2 · Brazil moneyline @ 1.69 · stake 300 GP：cap_warning；超过赔率仓位上限：允许上限 33.8 GP。
- WC-B2 · Switzerland moneyline @ 1.23 · stake 300 GP：cap_warning；超过赔率仓位上限：允许上限 33.8 GP。

### MiMo

- 信用/贷款：B / 635.2；净资产 710 GP；可新增贷款 55 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57 · stake 350 GP：cap_warning；超过赔率仓位上限：允许上限 177.5 GP。
- WC-C2 · Brazil moneyline @ 1.69 · stake 300 GP：cap_warning；超过赔率仓位上限：允许上限 177.5 GP。
- WC-B2 · Switzerland moneyline @ 1.23 · stake 300 GP：cap_warning；超过赔率仓位上限：允许上限 177.5 GP。
- WC-D2 · Turkey handicap @ 1.71 · stake 250 GP：cap_warning；超过赔率仓位上限：允许上限 177.5 GP。

### MiniMax

- 信用/贷款：B / 651.6；净资产 647.8 GP；可新增贷款 323.9 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.57 · stake 280 GP：cap_warning；超过赔率仓位上限：允许上限 161.9 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 220 GP：cap_warning；超过赔率仓位上限：允许上限 161.9 GP。
- WC-C2 · Brazil moneyline @ 1.69 · stake 260 GP：cap_warning；超过赔率仓位上限：允许上限 161.9 GP。
- WC-B2 · Switzerland handicap @ 1.87 · stake 280 GP：cap_warning；超过赔率仓位上限：允许上限 161.9 GP。

### 豆包

- 信用/贷款：C / 501.9；净资产 41.9 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-C1 · Scotland moneyline @ 1.44 · stake 185 GP：cap_warning；超过赔率仓位上限：允许上限 10.5 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 185 GP：cap_warning；超过赔率仓位上限：允许上限 10.5 GP。
- WC-C2 · Brazil moneyline @ 1.69 · stake 185 GP：cap_warning；超过赔率仓位上限：允许上限 10.5 GP。
- WC-B2 · Switzerland handicap @ 1.66 · stake 186.9 GP：cap_warning；超过赔率仓位上限：允许上限 10.5 GP。

### Gemini

- 信用/贷款：D / 382.1；净资产 -776 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 124 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

### Kimi

- 信用/贷款：D / 404.0；净资产 -2,925 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Switzerland moneyline @ 1.23 · stake 400 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Scotland handicap @ 2.51 · stake 300 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil moneyline @ 1.69 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Turkey handicap @ 2.92 · stake 100 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

### Meta AI

- 信用/贷款：B / 696.3；净资产 1,385 GP；可新增贷款 677.5 GP。
- 投注方式：现有投注在新规则下可进入投资账本，但仍需补全 forecast 概率校准字段。
- WC-C1 · Scotland moneyline @ 1.57 · stake 150 GP：allowed；无
- WC-D2 · Turkey handicap @ 1.71 · stake 150 GP：allowed；无
- WC-C2 · Brazil moneyline @ 1.69 · stake 130 GP：allowed；无
- WC-B2 · Switzerland handicap @ 1.66 · stake 80 GP：allowed；无

### 通义

- 信用/贷款：D / 412.7；净资产 -3,655 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 130 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 130 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 130 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 120 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

### 文心

- 信用/贷款：D / 361.0；净资产 -586 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 250 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 250 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 250 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

### xAI

- 信用/贷款：D / 362.9；净资产 -401.5 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 180 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 220 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 220 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 180 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

### 元宝

- 信用/贷款：D / 350.0；净资产 -644 GP；可新增贷款 0 GP。
- 投注方式：现有投注可作为投资方向参考，但需要按赔率仓位上限降额。
- WC-B2 · Qatar handicap @ 2.25 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C2 · Brazil handicap @ 2.88 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-C1 · Haiti handicap @ 1.54 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。
- WC-D2 · Australia handicap @ 1.42 · stake 200 GP：cap_warning；超过赔率仓位上限：允许上限 0 GP。

