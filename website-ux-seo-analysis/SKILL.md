---
name: website-ux-seo-analysis
description: Use when asked to analyze a live website, SaaS product, web app, landing page, competitor site, or AI tool, especially with logged-in UX, Google/OAuth login, pre-authenticated Chrome sessions, payment avoidance, SEO/keyword research, competitor comparison, feasibility scoring, or a Markdown report saved locally.
---

# Website UX SEO Analysis

## Overview

Produce evidence-based website analysis reports from real browsing, not guesses. The target is always the website URL or domain supplied by the user; do not treat any prior analyzed site as fixed. Cover the logged-in product experience when required, avoid dangerous/payment actions, verify SEO facts from live pages, include only keyword metrics with external data sources, and end with a similar-product feasibility score when requested.

## Workflow

1. Confirm the target URL supplied in the current user request, required login state, output path/name, and any forbidden actions.
2. Use Chrome before any browsing. Follow **Browser Routing Rules** below; Chrome is required for every website visit in this skill, including public/no-login pages.
3. Browse like a real user: public pages first, then login, then dashboard/workspace/core flows.
4. Avoid irreversible or high-risk actions unless explicitly requested:
   - Do not purchase, subscribe, upgrade, enter payment details, configure Stripe/checkout, delete projects, publish live content, change domains, invite users, or modify billing.
   - You may observe these entry points and record that they exist.
5. Capture factual evidence: visible UI text, URLs, page states, error messages, module names, metadata, robots, sitemap, headers, and source links.
6. Write the report in the user’s requested language and format, usually Markdown.
7. Save the report to the requested directory. If no filename is specified, use a concise snake_case filename derived from the domain.

## Browser Routing Rules

Always use Chrome for website browsing in this skill. This applies to every target website and every login state, including public landing pages, no-login SEO checks, pricing pages, blogs, dashboards, OAuth flows, and authenticated product testing.

Start in Chrome from the first page load. Do not first collect public UX evidence in the in-app browser and “switch later”; that can miss login buttons, FedCM/One Tap prompts, profile-specific pages, consent states, and logged-in redirects.

Chrome means the Chrome plugin connected to the user's existing Chrome profile. Use the Chrome plugin/browser-client workflow and its claimed/new Chrome tabs. Do not satisfy any website visit for this skill by using Playwright in any form, including standalone Playwright tools, `mcp__playwright__`, `browser_navigate`, a Playwright-launched browser, a new browser context, the in-app browser, or the Chrome plugin's `tab.playwright` API. Use Chrome tab methods and non-Playwright Chrome capabilities such as `goto`, `title`, `url`, `screenshot`, `dom_cua`, `cua`, and `dev.logs` instead.

When Chrome is unavailable or a cross-origin OAuth/FedCM control requires human interaction, state the blocker precisely, keep the Chrome tab as a handoff if useful, and continue with the deepest safe analysis possible. Never inspect cookies, local storage, saved passwords, tokens, or browser profile internals.

## Login-Based UX Testing

When login is required:

- Attempt the requested login method, such as Google OAuth, using the active browser session.
- Do not ask the user for permission again if they explicitly told you to log in yourself and the browser already contains an eligible account/session.
- Do not inspect cookies, passwords, local storage, session stores, or profile internals.
- Do not expose personal email addresses, tokens, Bearer values, or account identifiers in the report. Use phrases like “logged-in account” or “Pro account state” unless the user explicitly asks for the exact account detail.
- If login fails because credentials, MFA, CAPTCHA, or user approval is required, state the blocker precisely and continue with the deepest safe non-logged-in analysis possible.

During product testing, include:

- Homepage and onboarding path.
- Login/register path.
- Dashboard/project list/account state.
- Primary creation or task flow.
- Existing completed project or sample state if new creation fails.
- Navigation modules and empty states.
- Settings, export, publish, analytics, integrations, and admin/back-end modules when safe.
- Error states and recovery quality.

## SEO Data Collection

Gather live SEO evidence with browser and HTTP checks:

- Page title, meta description, H1/H2, canonical, lang, OG/Twitter tags.
- `robots.txt`, sitemap URL count, first representative sitemap URLs.
- HTTP status, cache/server/framework signals, redirects, hreflang, security headers.
- Indexability risks: blocked paths, canonical mismatches, duplicate URL patterns, empty rendered content, noindex, client rendering issues.
- Structured data presence or absence.
- Content architecture: homepage copy, feature pages, docs, how-to pages, pricing, affiliate, blog, comparison pages.
- External footprint: official docs, Product Hunt, directories, reviews, social/community links, and relevant competitor sources.

Always cite the sources used in the report with links.

## Keyword Metrics Rules

Keyword data must be source-backed.

- Use external keyword tools or APIs for numeric metrics: Google Keyword Planner, Ahrefs, Semrush, DataForSEO, seodata.dev, SearchVolume.io, Keyword Volume Checker, or another named provider.
- Actively try to obtain the core metrics the user requested: Google/global monthly search volume, major country/market traffic split, keyword difficulty, CPC, and paid competition. Use Google Keyword Planner, Ahrefs, Semrush, DataForSEO, or another named external provider when available.
- For every numeric keyword metric, record the source and query scope:
  - keyword
  - country/market
  - date checked
  - metric provider
  - global monthly volume when provided by the external tool
  - monthly volume
  - CPC
  - paid competition or PPC competition
  - Organic keyword difficulty only when an external tool returns it
- Never invent or model global volume, country splits, or keyword difficulty.
- If a metric is unavailable, write “未获取到可验证外部数据” or equivalent in the user’s language.
- Do not convert PPC competition into Organic KD. Keep them separate.
- If only one country is retrieved, report only that country’s numbers and list other countries as unavailable.
- Strategy labels such as priority, intent, and recommended landing page may be based on judgment, but label them as strategic recommendations rather than external metrics.

## Similar-Product Feasibility Scoring (v2)

> v2(2026-06-05):为治"评分集中 7 分坍塌"问题(历史数据 72% 都是 exact 7.0),
> 强制**每个维度由专属角色独立打分**、**每个分数必须列证据 + 扣分项**、
> 输出结构化 `verdict.json`。**不要再凭感觉给中庸分**。

### 角色与维度的强制绑定

每个维度由一个**专属角色**独立打分,**禁止用同一视角横扫 5 个维度**。每个维度只看对应角色的核心问题:

| 维度 | 专属角色 | 该角色必须回答的核心问题 |
|---|---|---|
| `tech_feasibility`(技术可行性) | 资深 CTO(10 年 SaaS 架构经验) | "我团队 2-5 人 3 月内能复刻这个产品核心吗?第三方 API / 数据集是否现成?" |
| `market_demand`(市场需求) | 资深 PM(连续做过 5 个 SaaS) | "用户已经在用什么替代?抱怨在哪?愿意付多少钱?6 月内可达 1000 付费用户吗?" |
| `competition_pressure`(竞争压力) | 投资人(看过 100+ deal) | "巨头(Google/Amazon/OpenAI/Apple)在这赛道吗?现有强玩家收割成本是多少?" |
| `differentiation`(差异化空间) | UX 设计师(B 端工具方向) | "新进者能在哪些交互 / 体验 / 工作流维度做出真不同?现有产品的差体验机会在哪?" |
| `mvp_difficulty`(MVP 落地难度) | 失败 SaaS 创业者(挂过 3 个项目) | "类似 idea 历史上谁试过为什么挂?监管 / 数据授权 / 冷启动死结存在吗?" |

### 评分规则(强制,不可跳过)

每个维度的输出**必须**包含三段。**任何一段缺失则该维度判废,verdict.json 会被代码侧拒绝**:

1. **`score`(0-10 整数或一位小数)**:该维度的分数。
2. **`evidence`(≥30 字)**:必须引用 Markdown 报告里**已经出现过的具体事实** — URL、报错信息、数字、模块名、竞品名、截图描述。**禁止**写"经评估觉得不错"这类无源判断。
3. **`deductions`(≥1 条具体扣分项)**:列出"扣了 (10-score) 分,因为 X"。X 必须是具体的失分原因,不能是"还有改进空间"这类废话。

**两条硬约束**:
- **没扣分项 → 不能给低分**(给 4 分必须列 ≥1 条扣分,给 2 分必须列 ≥2 条扣分,以此类推)
- **没强证据 → 不能给高分**(给 8+ 分必须有 ≥2 条具体 evidence 引用)

两端都堵死,治"safe default 7"。

### 总分 rubric(替换原"7 = 可尝试"安全话术)

把总分锚定到"同类产品中的相对位置",**不要再把 7 当作中庸安全位**:

| 分数 | 含义 |
|---|---|
| 0-3 | 同类末 10%,几乎没有可执行价值 |
| 4-5 | 同类中位偏下,有明显短板 |
| 6 | **同类中位**(50 百分位),无突出优势也无致命缺陷 |
| 7 | 同类前 30%(原"可尝试"含义,但锚定到比例) |
| 8 | 同类前 10% |
| 9-10 | 同类前 3%,需多维度强证据支撑 |

### 负向维度方向

`competition_pressure` 和 `mvp_difficulty` 是**负向维度**:`score` 越高代表压力 / 难度**越大**。
- 例如:OpenAI 直接做的赛道 → `competition_pressure.score = 9`(压力极大)
- 例如:需自训 LLM + 接入 50 家支付商 → `mvp_difficulty.score = 9`(落地极难)

`total_score` 由你(codex)在心智上**反向**这两个维度后再加权计算,**不要**让代码替你算。代码侧只校验你给的 total_score 在 0-10 范围、且与 5 个维度分布大致自洽。

### 必须输出 verdict.json

报告 Markdown 写完后,**必须**在工作目录额外写一个 `verdict.json` 文件(纯 JSON,无 markdown 包裹):

```json
{
  "dimensions": {
    "tech_feasibility": {
      "score": 0-10,
      "role": "CTO",
      "evidence": "≥30 字,引用 markdown 里出现过的事实",
      "deductions": ["扣了 X 分,因为 Y", "..."]
    },
    "market_demand": {
      "score": 0-10,
      "role": "PM",
      "evidence": "...",
      "deductions": ["..."]
    },
    "competition_pressure": {
      "score": 0-10,
      "role": "投资人",
      "evidence": "...",
      "deductions": ["..."]
    },
    "differentiation": {
      "score": 0-10,
      "role": "UX 设计师",
      "evidence": "...",
      "deductions": ["..."]
    },
    "mvp_difficulty": {
      "score": 0-10,
      "role": "失败 SaaS 创业者",
      "evidence": "...",
      "deductions": ["..."]
    }
  },
  "total_score": 0-10,
  "verdict_note": "为什么 5 个维度之间的差异化合理(≥40 字解释)"
}
```

verdict.json 失败 / 缺失时,代码侧会自动退回 markdown 末尾的"总分:X/10"正则提取(legacy 兼容),所以 Markdown 报告里**仍要**在"### 总评"小节末尾写一行 `总分:X/10`。这是失败兜底用的,**不能省**。

### 评分依据(来源)

基于以下证据做评估:
- 实际浏览到的网站 / 产品能力
- 发现的用户痛点(报错、UX 缺陷、缺失功能)
- SEO 与关键词证据(volume、KD、indexability)
- 竞品调研(类似产品的市占、定价、用户评价)
- 实施复杂度(技术栈、第三方依赖)
- 差异化机会(未被现有产品覆盖的体验维度)

`market_size / revenue / funding / competitor metrics` 等数字必须附外部来源。

## Report Structure

Use the structure the user requested. When unspecified, use exactly this top-level structure and do not add other top-level sections:

### Closed Report Schema

When using the default report structure, treat it as a closed schema.

- Do not add extra top-level sections beyond the sections listed in the default structure.
- Do not add evidence/artifact/screenshot/source-file sections unless the user explicitly asks for them.
- Evidence files, screenshots, raw HTML, logs, and browser notes may be saved or used internally, but should not appear as additional report sections.
- If extra material is useful, fold it into the nearest existing section instead of creating a new section.
- The final Markdown report must end at `## 五、参考来源` unless the user requested a custom structure.
- **Scoring detail goes to `verdict.json`** in the work directory(必须额外生成,不能只在 markdown 里写)。markdown 的"### 总评"小节仍写一行简短结论 + `总分:X/10`(给 legacy 正则用)。

```markdown
# {Domain} 网站用户体验与 SEO 分析报告

分析日期：
分析对象：
分析方式：
体验边界：

## 一、用户体验分析
### 1. 网站基本信息
### 2. 目标用户画像
### 3. 使用场景
### 4. 功能模块
### 5. 亮点与优点
### 6. 问题与缺点

## 二、SEO 分析
### 1. SEO 基本信息
### 2. SEO 现状概览
### 3. 技术 SEO 分析
### 4. 内容 SEO 分析
### 5. 关键词分析
### 6. 外链分析
### 7. 竞品对比分析

## 三、类似产品可行性评估
### 技术可行性
### 市场需求
### 竞争压力
### 差异化空间
### MVP 落地难度
### 总评

## 四、结论与优先级建议
## 五、参考来源
```

## Quality Bar

Before finalizing:

- Verify the report file exists and inspect key sections.
- Verify **`verdict.json` is written** to the work directory with all 5 dimensions, each having score + role + evidence + deductions, and a top-level `total_score` + `verdict_note`. **Missing verdict.json triggers a legacy regex fallback that is much less accurate.**
- Verify all website visits used the Chrome plugin/browser-client on the user's Chrome profile. Do not use Playwright in any form, including standalone Playwright, `mcp__playwright__`, the in-app browser, or Chrome `tab.playwright`. If Chrome was unavailable/blocked, state that precisely and do not replace Chrome browsing with another browser.
- Verify the final report follows the requested/default Markdown structure exactly. Do not include unrequested extra top-level sections such as “取证文件”, “附录”, “截图”, “原始证据”, or “补充材料”.
- Search the report for leaked sensitive data such as email addresses, tokens, cookies, or Bearer strings.
- Search for unsupported keyword phrases such as “估算”, “model”, “KD估算”, “主要国家流量估算”, or any numeric keyword metric without a source.
- **5 个维度的分数不能全在 6.5-7.5 之间** — 如果出现这种情况,说明你在求稳。重新审视每个维度,从专属角色视角找出真正差异化的扣分点。`verdict_note` 里要说明为什么分布合理。
- If a flow was blocked, state exactly what happened and how it affects confidence.
- Do not claim “all functions were fully tested” if payment, deletion, publishing, domain changes, or other unsafe actions were intentionally avoided.
