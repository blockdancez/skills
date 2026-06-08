---
name: google-ads-campaign-operator
description: "Use for practical and strategic Google Ads work for any product: first Search campaigns, campaign settings, ad groups, keywords, match types, responsive search ads, ad copy, display paths, sitelinks, URL options/UTM, conversion actions/goals, bidding, regions/languages, negatives, search-term analysis, long-term optimization, market expansion, growth experiments, landing-page/product feedback, and strategy reviews from Google Ads CSV reports, analytics screenshots, database funnel counts, or conversion screenshots. Use stored real Google Ads UI knowledge first; ask for screenshots or data only when a needed page, field, metric, or business constraint is not known. Never invent recommendations without evidence; separate evidence, inference, and hypotheses."
---

# Google Ads Campaign Operator

## Core Principles

Make recommendations from evidence: known Google Ads UI fields, user-provided screenshots, CSV reports, site analytics, database/CRM funnels, conversion settings, product facts, budget, and campaign goals. Do not pause keywords, change bidding, expand regions, or write ad copy from intuition alone.

If a page, metric, or business constraint is already covered by this skill or its references, do not ask the user to provide another screenshot. Ask for screenshots or data only when the current page is unknown, the UI has changed, current performance data is missing, or a required product/business constraint is unknown.

Act like both an operator and a growth strategist. Solve the immediate Google Ads task, then look one level higher: campaign stage, market opportunity, conversion quality, landing-page fit, product promise, experiment design, budget allocation, and the next learning loop. Be proactive, but label bold ideas as hypotheses unless the data proves them.

## Workflow

First identify the task type:

- **First campaign creation**: read Campaign Setup, Ad Group Setup, First Responsive Search Ad, URL Options, and Conversion Setup in `references/google-ads-practical-playbook.md`.
- **Beginner / first launch**: read Beginner Wizard Mode, Pre-launch Checklist, and Post-launch Review Cadence; output a complete fill-in-the-screen workflow.
- **New ad group or ad**: read Ad Group Setup, First Responsive Search Ad, and Keyword Selection.
- **Existing campaign optimization**: run the CSV analysis script first, then combine search terms, keywords, conversions, site analytics, and user/order data before making itemized decisions.
- **Strategic growth review**: read `references/growth-strategy-playbook.md`; identify campaign stage, bottleneck, next experiments, product/landing-page changes, and budget allocation.
- **Market/language expansion**: read Region And Language Expansion in `references/google-ads-practical-playbook.md` and Market Expansion in `references/growth-strategy-playbook.md`; split markets by language and proof level.
- **Google Ads page field troubleshooting**: use the stored real UI field knowledge first. Ask for a screenshot only if the current page is not covered or appears changed.

When processing CSV/TSV reports, run:

```bash
python3 .agents/skills/google-ads-campaign-operator/scripts/analyze_google_ads_csvs.py <csv...>
```

Optional target CPA parameter:

```bash
python3 .agents/skills/google-ads-campaign-operator/scripts/analyze_google_ads_csvs.py --target-cpa 20 <csv...>
```

The script output is only an initial triage layer. For any high-impact operation, such as pausing a high-spend keyword, changing bid strategy, expanding regions, or adding a search term as a keyword, verify the original report rows and product intent before recommending the change.

For ongoing campaign reviews, always add a strategic read after the operational table:

- What stage the campaign is in: discovery, validation, scale, efficiency, expansion, or recovery.
- What the current bottleneck appears to be: traffic quality, ad relevance, landing-page fit, signup friction, activation, pricing, checkout, market selection, or tracking.
- What to test next and what evidence would confirm or reject it.

## Required Coverage For First Campaigns

Do not answer only with ad group settings. A first-campaign answer must include:

- Campaign: type, name, budget, bid strategy, networks, locations, location options, languages, and conversion goals.
- Ad group: type, name, landing URL for keyword suggestions, product/service field, keyword text area, match types, search-term matching / AI Max, brand restrictions, locations of interest, and URL inclusion rules.
- First responsive search ad: final URL, display paths, 15 headlines, 4 descriptions, whether images are needed, whether sitelinks are needed, and URL options / UTM.
- Conversions: which actions are primary, which are secondary, and which are diagnostic only.
- Negative keywords: initial negatives and conflict handling.
- Pre-launch checks: final URL, UTM, conversion goals, locations/languages, networks, budget, CPC cap, and negative keyword conflicts.
- Post-launch cadence: troubleshoot only during the first 24 hours, make light adjustments after 72 hours, and make stronger keyword-level decisions after about 7 days or sufficient click volume.

## Decision Rules

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

- The evidence used and the exact metrics behind it.
- A concise distinction between `Evidence`, `Inference`, and `Hypothesis` when strategic recommendations go beyond the data.
- Itemized operations: keep, pause, add, negative, observe, adjust ad copy, adjust bidding, adjust region/language.
- Paste-ready keywords, negative keywords, headlines, descriptions, and UTM values.
- Uncertainties and the smallest missing information needed from the user.
- For beginner requests, ordered "which section to fill with what" steps, not just final ad copy.
- For optimization requests, itemized actions by campaign, ad group, keyword, and search term, not only broad strategy.
- For strategic reviews, include the next 1-3 experiments, each with goal, setup, budget/risk guardrail, expected signal, and stop/scale rule.
- For long-running products, include what the product or landing page should change if paid search repeatedly exposes the same user intent or friction.

Never answer with vague suggestions such as "optimize keywords", "improve conversions", or "change ad copy" without exact operations and evidence.
