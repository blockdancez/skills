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

If a reasonable default exists and risk is low, proceed with a labeled assumption instead of stopping.

## Artifact To Workflow Map

Use these routes:

- Product URL only -> inspect landing page promise, then use `prelaunch-and-keyword-research.md`.
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
