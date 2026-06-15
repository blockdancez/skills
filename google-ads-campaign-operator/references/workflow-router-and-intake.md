# Workflow Router And Intake

Use this reference before making recommendations when the user's stage is unclear or when the user is before launch. The goal is to prevent blind campaign creation and route the user into the right workflow.

## Stage Classification

Classify the request from artifacts first:

- **No Campaign Yet / Product Prep**: no campaign exists, no landing page is provided, or the user asks what to prepare.
- **Research And Planning**: user asks for keywords, Keyword Planner steps, competitor research, market choice, budget, bidding, or campaign structure before launch.
- **Campaign Build**: user asks how to create a campaign/ad group/ad and has product, landing page, conversion goal, budget, and target market.
- **Ad/Asset Filling**: user shows a Google Ads editor screen and needs exact field values, titles, descriptions, snippets, paths, or URL options.
- **Launch QA**: campaign is nearly ready; user asks whether to launch, whether settings are correct, or whether there is risk.
- **Performance Optimization**: user provides reports, analytics screenshots, database counts, conversion screenshots, or asks what to keep/pause/add.
- **Strategic Review / Expansion**: user asks whether to scale, cut, expand, change market, change product, or interpret growth trajectory.
- **Troubleshooting**: user has an error, rejection, no spend, unexpected bid strategy, conversion mismatch, or Google Ads UI confusion.

If multiple stages apply, choose the earliest unresolved blocker. Example: if the user asks to build a campaign but has no landing page or conversion goal, route to Product Prep before Campaign Build.

## Domain-Only Launch Request

Use this hard rule when the user says things like:

```text
想要开启 lumi.new 的投放，该怎么做
How do I start ads for example.com?
I want to launch Google Ads for {product/domain}
```

If the only concrete input is a product name, domain, or short product description, classify as **Research And Planning**. Do not classify as Campaign Build, even if the user says "start", "launch", "投放", or "建广告".

Expected behavior:

1. State that this is a first-launch planning task.
2. Inspect the landing page if browser/network access is available; otherwise ask for the landing page content or screenshots.
3. Separate confirmed product facts from assumptions.
4. Identify the missing launch gates: target market/language, primary conversion, budget/CPC guardrail, keyword evidence, tracking status.
5. Give a phased workflow: landing page audit -> Keyword Planner -> competitor/category research -> campaign architecture -> ad copy/assets -> launch QA -> 24h/72h/7d optimization.
6. Ask at most three blocking questions.

Forbidden before the launch gates are known:

- Paste-ready campaign name.
- Paste-ready ad group names.
- Paste-ready exact/phrase/broad keyword blocks.
- Paste-ready negative keyword blocks.
- Paste-ready RSA headlines/descriptions.
- Specific daily budget, CPC cap, tCPA, or location settings invented by the agent.
- Specific conversion action names invented from guesswork.

Allowed before the launch gates are known:

- Readiness diagnosis.
- Research plan.
- Keyword Planner field instructions.
- Competitor/category research checklist.
- Hypothesis-only seed keyword themes, clearly marked as not ready to paste.
- Landing page improvement checklist.
- The smallest next action and the data to export.

Failure pattern to avoid:

```text
Bad: "先这样建一个 Search Campaign: campaign name..., budget $30/day, keywords..., negatives..., headlines..."
Why bad: it turns a planning request into live operations without target market, conversion goal, budget guardrail, keyword evidence, and tracking confirmation.
```

Preferred response skeleton:

```text
我先把当前任务归类为：Research And Planning / 首次投放准备。
依据：你只给了产品/域名，还没有确认目标市场、转化目标、预算、关键词数据和追踪状态。
现在不能直接做：不能直接给可复制的广告系列、关键词、否定词或预算，因为这些会变成未经验证的投放操作。

我会按这个顺序推进：
1. 先分析落地页和产品承诺。
2. 用 Keyword Planner 拉关键词和预测数据。
3. 做竞品/类别搜索结果检查。
4. 再决定广告系列结构、关键词、否定词、出价和广告文案。
5. 上线前做 QA，上线后按 24h/72h/7d 节奏优化。

我现在需要确认 3 件事：
1. 首投市场/语言是什么？
2. 主转化目标是什么？
3. 每日测试预算或最大可接受 CPA/CPC 是多少？
```

## Minimum Readiness Checks

Before campaign creation, verify or explicitly mark as assumption:

- Product promise: what problem the product solves and for whom.
- Landing page: URL, language, first-screen message, CTA, pricing/limits, screenshots/proof, mobile readiness.
- Conversion goal: primary business event, secondary activation event, diagnostic events.
- Market: countries, languages, location option, device assumptions, support/payment readiness.
- Budget guardrail: daily budget, max CPC or target CPA, stop rule, acceptable learning spend.
- Keyword evidence: seed terms, Keyword Planner/export data, existing search terms, SEO/GSC data, or competitor/category evidence.
- Tracking: UTMs, Google Ads conversion action status, analytics events, backend/CRM funnel availability.
- Assets: headlines, descriptions, sitelinks, structured snippets, images/screenshots if useful.

Readiness result:

```text
Stage:
Readiness: Ready / Ready for small test / Blocked
Blocking items:
Safe next step:
Data or screenshot needed:
```

## Asking Questions

Ask only when the answer changes the recommendation. Ask at most three questions and keep them concrete:

- What is the exact landing page URL?
- Which country/language should this campaign target first?
- Which event should count as the primary conversion?
- What daily budget and max CPC/CPA guardrail are acceptable?
- Can you export keyword ideas or forecasts from Keyword Planner for the proposed market?

If a reasonable default exists and risk is low, proceed with a labeled assumption instead of stopping. Domain-only launch requests are not low risk for paste-ready build instructions; use assumptions only for non-actionable planning examples.

## Artifact To Workflow Map

Use these routes:

- Product URL only -> inspect landing page promise, then use `prelaunch-and-keyword-research.md`; do not output paste-ready campaign build until launch gates are known.
- Product description only -> define offer, audience, landing page requirements, and seed keyword categories.
- Google Ads Keyword Planner screenshot -> explain which card/tab to use, fields to fill, filters, export, and interpretation.
- Google Ads ad editor screenshot -> use `google-ads-practical-playbook.md` for field values; do not rewrite unrequested account-level settings unless a risk is visible.
- Keyword/search-term CSVs -> run `scripts/analyze_google_ads_csvs.py`, then follow the optimization SOP.
- Analytics/database/conversion screenshots -> map funnel quality before keyword/budget actions.
- Competitor names or category -> use `prelaunch-and-keyword-research.md` and `growth-strategy-playbook.md`.
- Budget/bid question -> verify conversion reliability, CPA, CPC, volume, and campaign stage before changing.

## First Response Pattern

When the user invokes this skill with mixed materials, start with:

```text
我先把当前任务归类为：{stage}
依据：{artifacts/evidence}
现在不能直接做的事：{unsafe action, if any}
我会先做：{next workflow}
```

Then continue into the relevant reference workflow and produce exact operations.

## Safety Rules

- Never create or recommend a live campaign solely from a product idea without landing page, conversion goal, target market, and budget guardrail.
- Never treat Google Ads recommendations, auto-apply suggestions, broad-match suggestions, or Keyword Planner ideas as approved actions.
- Never add negatives without checking targeted keyword conflicts and scope.
- Never mix languages or markets in one campaign when landing page, ad copy, and keywords do not match.
- Never optimize to weak diagnostic events unless the user accepts a learning-only phase.
