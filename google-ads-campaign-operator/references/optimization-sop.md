# Optimization SOP

Use this reference for running campaigns, daily reviews, search-term cleanup, negative keyword decisions, funnel diagnosis, bidding/budget changes, product/landing-page/operations feedback, and weekly/longer strategic optimization.

## Review Cadence

### First 24 Hours

Only fix clearly broken or risky items:

- Campaign/ad/ad group status, disapprovals, limited serving, policy issues.
- Final URL, UTM, redirect, page language, mobile loading, 404/500.
- Spend pacing versus daily budget.
- Bid strategy or CPC cap accidentally changed by recommendations or auto-apply.
- Conversion actions firing, duplicate counting, primary/secondary/diagnostic classification.
- Wrong country, language, network, or search partner/display leakage.
- Search terms with obvious bad intent and meaningful spend.
- Product/landing issues that are obviously breaking paid traffic: page outage, mobile layout failure, wrong language, slow auth, broken verification, broken upload/deploy flow, checkout failure, or conversion events not firing.

Avoid heavy keyword pruning in the first 24 hours unless intent is plainly wrong.

### 72 Hours

Make light, evidence-based changes:

- Add exact keywords from converting search terms that match product intent.
- Add phrase keywords for repeated relevant variations.
- Add ad group or campaign negatives for clearly irrelevant terms.
- Split a theme into a new ad group if the query intent is good but ad/landing page mismatch is obvious.
- Update ad copy only when search terms reveal repeated intent that the current ad underserves.
- Check CPC spikes and search-term quality before changing bids.
- Record product, landing-page, or operations hypotheses exposed by search terms and funnel behavior. Fix only obvious breakages; otherwise queue them for weekly review.

### Weekly

Make stronger decisions:

- Keyword/ad group CPA, conversion rate, CTR, CPC, and spend.
- Search-term waste by theme.
- Country/language/device performance.
- Landing page path: ad click -> landing page -> CTA -> signup intent -> register success -> activation -> checkout/revenue.
- Conversion quality: primary business event versus weak diagnostic event.
- Budget allocation: winners, weak tests, experiments.
- Bid strategy fit: sample size, conversion reliability, CPA stability.
- Product and operations backlog: landing-page clarity, onboarding friction, activation gaps, pricing/upgrade friction, docs/support gaps, localization/device issues, tracking gaps, and manual ops that slow feedback loops.

### Every 14-30 Days

Review structural changes:

- New language/country campaigns.
- New landing pages for repeated query themes.
- Competitor/alternative pages.
- SEO/content pages for expensive but informative queries.
- Product/onboarding/pricing changes exposed by paid traffic.
- Whether to scale, cap, pause, or redesign experiment cells.
- Whether paid-search learnings should become product roadmap items, landing-page tests, SEO/content pages, instrumentation work, support macros, or automated reporting.

## Required Data Merge

For optimization, combine at least the available pieces:

- Google Ads keyword report.
- Google Ads search-term report.
- Google Ads campaign/ad group screenshots for budget, bidding, status, conversion rate, CPA.
- Google Search Console performance if the user provides it.
- Analytics: pages, referrers, countries, devices, events, bounce rate.
- Backend/CRM: created users, qualified leads, register success, activation, purchase.
- Conversion setup screenshots: primary/secondary status, source, counts, values.

If date ranges differ, state the mismatch and use the closest comparable window. Do not hide partial-day data.

## Funnel Diagnosis

Map performance through this funnel:

```text
Impression -> Click -> Landing page visit -> CTA/signup intent -> Verification/form step -> Primary conversion -> Activation -> Checkout/revenue
```

Diagnose by symptom:

- High CTR, low landing-page engagement: ad promise or query may be curiosity/misaligned.
- Good landing page visits, low signup intent: offer, CTA, trust, pricing, or page clarity issue.
- High signup intent, low register success: auth/verification/friction/tracking issue.
- Good register success, low activation: onboarding or product fit issue.
- Good activation, low checkout: pricing, limit, value communication, or payment friction.
- Ads conversions differ greatly from analytics/backend: conversion counting, attribution window, duplicate counting, or event definition issue.

Do not solve funnel problems only by adding negatives.

## Product And Operations Feedback Loop

Every optimization review must include a product/landing/operations read, even when the immediate ad actions are small. Paid search is a fast source of product research: queries, click behavior, registration friction, activation events, support needs, and checkout behavior reveal what the product and operations should improve.

Separate follow-ups from ad operations:

- `Ad operation`: keywords, negatives, ads, bids, budgets, regions, languages, networks.
- `Landing-page follow-up`: page copy, first-screen promise, proof, pricing/limits, examples, comparison pages, docs links, mobile layout, localization.
- `Product follow-up`: feature gap, onboarding, upload/deploy flow, activation moment, error handling, free/pro limit, checkout, account creation, import/export workflow.
- `Tracking follow-up`: conversion definition, duplicate counting, primary/secondary status, event naming, attribution, UTM, backend reconciliation.
- `Operations follow-up`: reporting cadence, support macros, sales/CRM handling, data dashboard, daily anomaly alerts, experiment log, handoff notes.
- `Content/SEO follow-up`: expensive but informative queries, repeated how-to intent, docs gaps, comparison/alternative pages, glossary pages.

Map evidence to follow-ups:

- Repeated relevant search terms with no matching landing section -> landing-page copy or dedicated page.
- Repeated relevant search terms for unsupported workflow/file type/integration -> product roadmap hypothesis.
- High CTR but high bounce or low page engagement -> ad promise mismatch, page clarity, load speed, or low-intent query.
- Good landing visits but low CTA/signup intent -> offer clarity, trust proof, pricing/limits, CTA, examples, or localized copy issue.
- High signup intent but low register success -> auth, verification, form friction, blocked emails, mobile UX, or tracking issue.
- Good register success but low activation -> onboarding, first action, template/example, import/upload/deploy flow, or empty-state guidance.
- Good activation but low checkout/upgrade -> pricing, plan limits, upgrade prompt timing, payment methods, or value communication.
- One country/language clicks but does not activate -> localization, region support, payment/support availability, or wrong location option.
- Device gap, especially mobile traffic with weak activation -> mobile UX, page speed, file upload constraints, or layout issue.
- Ads conversions disagree with analytics/backend -> tracking follow-up before budget/bid decisions.
- Informational queries are relevant but expensive -> content/SEO follow-up instead of continuing to buy all of them.

Prioritize follow-ups:

```text
Now fix:
- Only clear breakages or tracking issues that can invalidate spend.

Experiment:
- Evidence-backed landing/product changes that can be tested with one page, one flow, one event, or one campaign cell.

Backlog:
- Plausible ideas with weak data, large build cost, or no direct campaign impact yet.

Do not do yet:
- Large product pivots, pricing changes, or broad roadmap work supported only by a tiny sample.
```

For each product/operations recommendation, state:

- Evidence: exact search terms, funnel metric, country/device/page/event, or user data.
- Inference: what the evidence likely means.
- Action: the smallest product, landing, content, tracking, or ops change.
- Owner/type: product, growth, engineering, content, support, analytics, or ops.
- Verification: which metric should move and by when.
- Risk: what could go wrong or what not to over-interpret.

## Negative Keyword SOP

Before adding any negative:

1. Confirm the exact search term and campaign/ad group scope.
2. Check whether the negative would conflict with an active targeted keyword.
3. Decide match type:
   - Exact negative `[term]`: block only the exact irrelevant query.
   - Phrase negative `"term"`: block queries containing that phrase.
   - Broad negative `term`: use cautiously; it can block many variants.
4. Decide scope:
   - Ad group: bad for only one intent cluster.
   - Campaign: bad for the whole campaign.
   - Account/shared list: bad for all campaigns and future tests.
5. Add variants only if they appeared in search terms or are obvious language/plural/misspell variants.

Conflict rule:

```text
If Google Ads says a targeted keyword cannot be excluded:
1. Pause/remove the active positive keyword first if data supports exclusion.
2. Then add the negative.
3. If the positive keyword should stay active, do not add the conflicting negative at that scope.
```

Negative output must be split:

```text
Can add now:
"bad term"
[bad exact term]

Do not add because it conflicts with active keywords:
"conflicting term" -> first pause/remove positive keyword: "conflicting term"

Need more evidence:
"uncertain term" -> reason
```

Never output only a plain text negative list without scope, match type, and conflict notes.

## Keyword Operation Rules

Classify material keywords/search terms:

- **Keep**: conversions, strong relevance, low sample, or strategically important exact intent.
- **Add exact**: converting search term with direct product intent.
- **Add phrase**: repeated relevant variation that needs controlled expansion.
- **Pause**: active keyword has wrong intent or enough spend/clicks with no meaningful conversion.
- **Negative**: search term is irrelevant, unsupported, wrong language, wrong product, or bad for the whole scope.
- **Observe**: low sample, mixed signal, high CPA with conversions, or attribution lag.
- **Split**: intent is good but deserves its own ad copy/landing page/ad group.

Use practical thresholds as starting points, not hard law:

- Under about 20 clicks: usually observe unless intent is plainly wrong.
- 8-10 clicks with 0 conversion and bad intent: pause/negative can be justified.
- Spend above target CPA with 0 conversion: inspect search terms and landing behavior before pausing.
- Converting but expensive: keep while testing split/ad/landing/CPC improvements.

## Bidding And Budget SOP

Before changing bids or budget, state:

- Current bid strategy.
- Daily budget and whether it is constrained.
- CPC cap or target CPA if any.
- Primary conversion action and reliability.
- Conversion volume and CPA for the same window.
- Whether the campaign is discovery, validation, scale, efficiency, expansion, or recovery.

Decision guide:

- Sparse or unreliable primary conversions: Maximize clicks with CPC cap is usually safer.
- Stable meaningful conversions but low weekly volume: test Maximize conversions only with a small guardrail.
- Stable CPA and enough conversion volume: consider Maximize conversions or target CPA.
- Budget constrained but CPA acceptable: increase budget gradually, not all at once.
- Budget spending on weak tests: cap weak tests and protect proven intent.
- CPC too high with low query quality: tighten match types and negatives before only lowering CPC.

Avoid stacking many changes in one day. Prefer one meaningful change set, then review after the next conversion/search-term window.

## Paste-Ready Optimization Output

Every optimization answer should include:

```text
Stage:
Date range:
Evidence used:
Main bottleneck:

Operations by ad group:
Ad group | Object | Action | Evidence | Exact content | Scope/risk

Exact keywords to add:
[keyword]

Phrase keywords to add:
"keyword"

Ad group negatives:
"negative phrase"
[negative exact]

Campaign negatives:
"negative phrase"
[negative exact]

Pause keywords:
"keyword" -> reason

Observe:
"keyword/search term" -> reason and next trigger

Bidding/budget:
Action:
Reason:
Review trigger:

Do not change yet:
- Item: reason

Product / landing / operations follow-ups:
Type | Priority | Evidence | Action | Verification | Owner

What this means for product quality or operations efficiency:
- Insight:
- Why it matters:
- Next smallest test:
```

For strategic reviews, append experiments from `growth-strategy-playbook.md`.
