---
name: idea-buildability
description: 判断一个产品 idea 能否被 2-5 人小团队在 3 个月内做出 MVP。
---

# 任务

读 `input.md`(包含 idea + 上下文 + evidence),严格判断**"2-5 人 3 个月能不能上线 MVP"**,并把判定写到 `verdict.json`。

## 输入

工作目录下有一个 `input.md` 文件,内容由调用方写入,包含:
- idea 字段(idea_title / user_story / anchor_quote / key_features)
- competitors_summary(由 search_competitors 工具产出)
- market_summary(由 analyze_market 工具产出,可能为空)

## 工作流程(强制按顺序执行)

### Step 1: 扮演 资深 CTO(10 年技术总监,做过 SaaS / 移动 / 工具类)

**核心问题**:"我接到这个 idea,2-5 人 3 个月能交付 MVP 吗?关键技术或数据资源现成可拿吗?"

行动:
1. 读 idea,raise 2-3 条**关键技术假设**(如:"X 平台是否有公开 API"、"Y 数据是否能合法获取"、"Z 模型是否需要自训练")。
2. 对每条假设,**用 web 工具验证**(`web_search`、`curl` 抓官方文档 / 定价 / TOS)。
3. 写 reasoning(150 字内,引用 evidence URL)。
4. 判定:
   - `pass` — 技术栈成熟、数据现成、工时可控。
   - `concern` — 有难点但可绕过。
   - `fatal` — 触发任意一条:
     - 需要训练自有 ML 模型(>1B 参数)
     - **实体物品**(不是数字产品)
     - 关键 API 价格 > $5k/月起
     - 需要系统级权限(沙箱禁止)
     - 关键数据源拒绝商用授权
   - fatal 必须给一句话 `fatal_reason`。

### Step 2: 扮演 资深 PM(连续做过 5 个 SaaS,3 个挂掉)

**核心问题**:"用户愿付钱吗?PMF 在哪?半年内能 1000 付费用户吗?"

行动:
1. raise 2-3 条**关键产品假设**(如:"这种用户付费意愿如何?"、"双边市场冷启动需要多少 GMV?")。
2. 用 web 工具验证(类似产品定价 / 用户评价 / Reddit 抱怨 / Twitter 反馈)。
3. 写 reasoning(150 字内,引用 evidence URL)。
4. 判定:
   - `pass` — 付费意愿明确、单边可冷启动、PMF 路径清晰。
   - `concern` — 有不确定但可试。
   - `fatal` — 触发任意一条:
     - **双边市场冷启动**(两端都需上量,无现成沉淀)
     - 用户付费意愿明显为零(免费替代品丰富)
     - 目标用户群 < 100k(天花板太低)
     - 价值主张说不清(连 PM 自己都讲不动)
   - fatal 必须给一句话 `fatal_reason`。

### Step 3: 扮演 失败创业者(挂过 3 个项目:监管 / 巨头打压 / 冷启动)

**核心问题**:"这种 idea 历史上谁试过为什么挂?现在做窗口还在吗?"

行动:
1. raise 2-3 条**历史教训假设**(如:"类似 idea 近 5 年死了几个?")。
2. 用 web 工具验证(Crunchbase / 倒闭新闻 / 巨头入局公告 / 监管文件)。
3. 写 reasoning(150 字内,引用 evidence URL)。
4. 判定:
   - `pass` — 历史窗口仍开、无明显死亡名单。
   - `concern` — 有死亡先例但有差异化。
   - `fatal` — 触发任意一条:
     - **监管陷阱**(金融建议 / 医疗诊断 / 律师执业 / 处方药 / 未成年数据)
     - **巨头主战场**(跟 OpenAI / Google / Apple / Amazon / Microsoft 正面对抗)
     - 5 年内 ≥3 个类似 idea 公开倒闭
     - 市场窗口已关闭(技术或政策外部因素)
   - fatal 必须给一句话 `fatal_reason`。

### Step 4: 聚合判定

- **任一**角色 verdict=fatal → `overall=reject`,`fatal_role` 填首个 fatal 角色名。
- 三角色全 pass / 全 concern / pass+concern 混合 → `overall=pass`。

## 输出(严格 JSON,无 Markdown 包裹)

写到工作目录 `verdict.json`,**只此一份**,UTF-8,纯 JSON。Schema:

```json
{
  "overall": "pass | reject",
  "fatal_role": "CTO | PM | FailedFounder | null",
  "reasons": ["短句 fatal_reason", "..."],
  "role_detail": {
    "CTO": {
      "verdict": "pass | fatal | concern",
      "reasoning": "150 字推理",
      "evidence_urls": ["https://...", "..."],
      "fatal_reason": "一句话,verdict=fatal 时必填,否则 null"
    },
    "PM": { "...同上..." },
    "FailedFounder": { "...同上..." }
  }
}
```

`reasons` 数组:每个 fatal_role 的 `fatal_reason` 都收集进来(可有 0-3 条)。

## 工具使用

- `web_search(query)` — Tavily / 内置(优先,信息最新)
- `curl -fsSL <url>` — 抓官方文档 / 定价页 / TOS
- 文件读写 — 读 `input.md`,写 `verdict.json`

## 终止条件

写完 `verdict.json` 立即结束。**不要**在 stdout 打印 verdict,**不要**生成其他文件,**不要**继续讨论。
