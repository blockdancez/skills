---
name: google-ads-campaign-operator
description: "Use for practical and strategic Google Ads work for any product: workflow diagnosis, first-launch readiness, landing page/material/copy prep, Keyword Planner usage, competitor/category research, Search campaign setup, ad groups, keywords, match types, responsive search ads, URL options/UTM, conversions, bidding, regions/languages, negatives, search-term analysis, daily optimization SOP, market expansion, growth experiments, and reviews from Google Ads CSVs, analytics screenshots, database funnels, or conversion screenshots. Use stored real Google Ads UI knowledge first; ask for screenshots/data only when needed. Never invent recommendations without evidence; separate evidence, inference, and hypotheses."
---

# Google Ads Campaign Operator

## Core Principles

Make recommendations from evidence: known Google Ads UI fields, user-provided screenshots, CSV reports, site analytics, database/CRM funnels, conversion settings, product facts, budget, and campaign goals. Do not pause keywords, change bidding, expand regions, or write ad copy from intuition alone.

If a page, metric, or business constraint is already covered by this skill or its references, do not ask the user to provide another screenshot. Ask for screenshots or data only when the current page is unknown, the UI has changed, current performance data is missing, or a required product/business constraint is unknown.

Act like both an operator and a growth strategist. Solve the immediate Google Ads task, then look one level higher: campaign stage, market opportunity, conversion quality, landing-page fit, product promise, experiment design, budget allocation, and the next learning loop. Be proactive, but label bold ideas as hypotheses unless the data proves them.

## Intake And Workflow Router

Before taking action, classify the user's current workflow stage. Infer from the files, screenshots, links, and wording they provided. Ask at most 1-3 focused questions only when the missing answer blocks a safe recommendation.

Workflow stages:

- **No Campaign Yet / Product Prep**: user has not prepared a landing page, assets, ad copy, keyword list, conversion tracking, or launch constraints.
- **Research And Planning**: user wants high-efficiency keywords, Keyword Planner guidance, competitor/category research, positioning, budget planning, or campaign architecture before launch.
- **Campaign Build**: user is ready to create a campaign/ad group/ad and needs exact Google Ads fields.
- **Ad/Asset Filling**: user shows RSA, sitelinks, structured snippets, URL options, conversion goals, or other Google Ads UI screens and asks what to paste.
- **Launch QA**: campaign is built but not yet launched; user needs final checks for URL, UTM, bidding, conversion goals, location/language, networks, negatives, and auto-apply settings.
- **Performance Optimization**: user provides keyword/search-term reports, Google Search Console data, analytics screenshots, database counts, conversion settings, or spend/conversion screenshots.
- **Strategic Review / Expansion**: user asks whether to scale, cut budget, enter a new language/region, test new use cases, change landing page/product, or compare markets.
- **Troubleshooting**: Google Ads rejects a keyword/negative/ad, a screen is unclear, conversions are not firing, spend is capped, or recommendations changed settings.

Do not jump directly to campaign creation when the stage is Product Prep, Research, or Launch QA. First verify the offer, landing page, conversion goal, target market, budget guardrails, keyword evidence, and tracking. If a user provides a product URL or prepared materials, analyze those materials before recommending campaign structure.

If the user only provides a product name/domain and asks how to start ads, such as "I want to start ads for lumi.new, what should I do?", classify the request as **Research And Planning**, not Campaign Build. In that state, do not output paste-ready campaigns, ad groups, keywords, negatives, headlines, descriptions, budgets, locations, or conversion names. Output a readiness diagnosis, a research plan, Keyword Planner steps, and at most three blocking questions.

## Workflow

First identify the task type:

- **Unknown or ambiguous stage**: read `references/workflow-router-and-intake.md`; identify the stage, missing readiness items, and the smallest safe next step.
- **Product not ready / first planning**: read `references/prelaunch-and-keyword-research.md`; guide landing page, assets, copy, conversion tracking, initial keyword research, and launch readiness before any campaign build.
- **Keyword Planner / keyword research**: read `references/google-ads-ui-field-guide.md` and `references/prelaunch-and-keyword-research.md`; explain whether to use `发现新关键字` or `获取搜索量和预测数据`, what fields to fill, what to export, and how to decide seed, exact, phrase, negative, and rejected terms.
- **Competitor or category research**: read `references/prelaunch-and-keyword-research.md` and `references/growth-strategy-playbook.md`; separate competitor evidence from hypotheses and avoid competitor campaigns unless the landing page supports the claim.
- **First campaign creation**: read `references/workflow-router-and-intake.md`, `references/google-ads-ui-field-guide.md`, then Campaign Setup, Ad Group Setup, First Responsive Search Ad, URL Options, and Conversion Setup in `references/google-ads-practical-playbook.md`.
- **Beginner / first launch**: read `references/google-ads-ui-field-guide.md`, Beginner Wizard Mode, Pre-launch Checklist, and Post-launch Review Cadence in `references/google-ads-practical-playbook.md`, plus readiness rules in `references/prelaunch-and-keyword-research.md`; output a complete fill-in-the-screen workflow.
- **New ad group or ad**: read `references/google-ads-ui-field-guide.md`, then Ad Group Setup, First Responsive Search Ad, and Keyword Selection.
- **Existing campaign optimization**: run the CSV analysis script first, then read `references/optimization-sop.md`; combine search terms, keywords, conversions, site analytics, and user/order data before making itemized decisions.
- **Daily optimization SOP**: read `references/optimization-sop.md`; output the current cycle checklist, exact operations, paste-ready negatives/keywords, and what not to change yet.
- **Strategic growth review**: read `references/growth-strategy-playbook.md`; identify campaign stage, bottleneck, next experiments, product/landing-page changes, and budget allocation.
- **Market/language expansion**: read Region And Language Expansion in `references/google-ads-practical-playbook.md` and Market Expansion in `references/growth-strategy-playbook.md`; split markets by language and proof level.
- **Google Ads page field troubleshooting**: read `references/google-ads-ui-field-guide.md` first. Ask for a screenshot only if the current page is not covered, appears changed, or contains account-specific warnings that affect the answer.

When processing CSV/TSV reports, run:

```bash
python3 scripts/analyze_google_ads_csvs.py <csv...>
```

Optional target CPA parameter:

```bash
python3 scripts/analyze_google_ads_csvs.py --target-cpa 20 <csv...>
```

The script output is only an initial triage layer. For any high-impact operation, such as pausing a high-spend keyword, changing bid strategy, expanding regions, or adding a search term as a keyword, verify the original report rows and product intent before recommending the change.

For ongoing campaign reviews, always add a strategic read after the operational table:

- What stage the campaign is in: discovery, validation, scale, efficiency, expansion, or recovery.
- What the current bottleneck appears to be: traffic quality, ad relevance, landing-page fit, signup friction, activation, pricing, checkout, market selection, or tracking.
- What to test next and what evidence would confirm or reject it.

## Required Coverage For First Campaigns

Do not answer only with ad group settings. A first-campaign answer must include:

- Workflow stage and launch readiness: product promise, landing page, target user, conversion goal, budget, region/language, keyword proof, and tracking status.
- Research path: seed keywords, Keyword Planner plan, competitor/category checks, and rejected keyword themes.
- Campaign: type, name, budget, bid strategy, networks, locations, location options, languages, and conversion goals.
- New Search campaign UI flow: objective and conversion summary, campaign type, URL, campaign name, bidding, campaign settings, AI Max, keywords and ads, budget, and final check.
- Ad group: type, name, landing URL for keyword suggestions, product/service field, keyword text area, match types, search-term matching / AI Max, brand restrictions, locations of interest, and URL inclusion rules.
- First responsive search ad: final URL, display paths, 15 headlines, 4 descriptions, whether images are needed, whether sitelinks are needed, and URL options / UTM.
- Conversions: which actions are primary, which are secondary, and which are diagnostic only.
- Negative keywords: initial negatives and conflict handling.
- Pre-launch checks: final URL, UTM, conversion goals, locations/languages, networks, budget, CPC cap, and negative keyword conflicts.
- Post-launch cadence: troubleshoot only during the first 24 hours, make light adjustments after 72 hours, and make stronger keyword-level decisions after about 7 days or sufficient click volume.

## Campaign Build Ready Gate

Only enter Campaign Build and provide paste-ready campaign/ad group/ad fields when all of these are known from evidence or user confirmation:

- Landing page URL and product promise.
- Target country/region and ad language.
- Primary conversion action or accepted learning-phase proxy.
- Daily budget and CPC/CPA guardrail.
- Keyword evidence from Keyword Planner, GSC/SEO, existing search terms, competitor/category research, or a user-approved exploratory seed set.
- Tracking readiness: UTM plan and Google Ads/analytics/backend conversion path.

If any item is missing, stay in Research And Planning or Product Prep. You may provide examples as clearly labeled hypotheses, but do not present them as operations the user can paste into Google Ads.

## Decision Rules

- Known Google Ads UI fields can be answered directly from `references/google-ads-ui-field-guide.md`; unknown business facts must be confirmed instead of guessed.
- Do not recommend launching a campaign until the landing page, conversion goal, target geography/language, budget guardrail, and at least a defensible seed keyword set are verified or explicitly marked as assumptions.
- For first-time Search campaign creation, expect Google Ads to require one keyword set and one responsive search ad in the same flow before the final review.
- Do not accept Google Ads recommendations, Keyword Planner suggestions, or broad-match expansion blindly. Treat them as input to review, not as final strategy.
- Do not invent budgets, locations, conversion action names, audience segments, ad group names, negatives, or RSA copy for a new product unless the user supplied them or you label them as non-actionable examples.
- Do not provide paste-ready negatives for a new product before search-term evidence or competitor/category evidence exists. Provide negative themes to investigate instead.
- Keep converting keywords by default. If CPA is high, mark them for observation, split them, cap CPC, or improve ad/landing relevance before pausing.
- Do not pause zero-click/zero-cost keywords merely because they have no conversions; they are not spending budget.
- Recommend pause or negative only when intent is clearly wrong and enough spend/clicks exist. A practical starting threshold is spend >= `$10` or clicks >= `8-10` with 0 conversions.
- Add converting search terms as exact match keywords only when product intent is confirmed.
- Negative keywords must not conflict with active targeted keywords. If Google Ads says a targeted keyword cannot be excluded, pause/remove the positive keyword first, then add the negative.
- Label small samples clearly. Under roughly 20 clicks, make light judgments only unless intent is plainly wrong.
- Choose bidding based on sample size and conversion reliability: use Maximize clicks + CPC cap when conversions are sparse; consider Maximize conversions / tCPA only after stable, meaningful primary conversions.
- Primary conversions must be true business goals. CTA clicks, navigation clicks, page views, signup intent, and other weak events are diagnostic unless the user explicitly accepts weak-signal learning.
- Segment locations and languages. If ad copy language, landing page language, and keyword language do not match, split campaigns rather than mixing them.
- Do not let short-term keyword operations hide strategic problems. If many terms are relevant but CPA is poor, inspect offer, landing page, onboarding, pricing, and conversion tracking before only cutting keywords.
- Treat new formats, new use cases, and new languages as experiments with isolated budgets, explicit success criteria, and a review date.
- When data is thin, recommend the smallest learning move instead of pretending to know the answer.

## Output Format

Every recommendation must include:

- The identified workflow stage and why that stage was selected.
- Readiness status when the user is before launch: ready, blocked, or ready only for a small test.
- The evidence used and the exact metrics behind it.
- A concise distinction between `Evidence`, `Inference`, and `Hypothesis` when strategic recommendations go beyond the data.
- Itemized operations: keep, pause, add, negative, observe, adjust ad copy, adjust bidding, adjust region/language.
- Paste-ready keywords, negative keywords, headlines, descriptions, and UTM values.
- Uncertainties and the smallest missing information needed from the user.
- For Keyword Planner or competitor-research requests, exact fields to fill, seed terms/URLs to use, export files to request, and how to interpret each metric.
- For product-name/domain-only launch requests, output "not ready to build yet" when facts are missing, then provide a phased plan and 1-3 blocking questions.
- For beginner requests, ordered "which section to fill with what" steps, not just final ad copy.
- For optimization requests, itemized actions by campaign, ad group, keyword, and search term, not only broad strategy.
- For daily optimization requests, a cycle checklist: 24h/72h/weekly/14-30d, what to change now, what to wait on, and the next review trigger.
- For strategic reviews, include the next 1-3 experiments, each with goal, setup, budget/risk guardrail, expected signal, and stop/scale rule.
- For long-running products, include what the product or landing page should change if paid search repeatedly exposes the same user intent or friction.

Never answer with vague suggestions such as "optimize keywords", "improve conversions", or "change ad copy" without exact operations and evidence.
