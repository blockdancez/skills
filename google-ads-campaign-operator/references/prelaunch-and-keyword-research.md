# Prelaunch And Keyword Research

Use this reference when the user is preparing a product for Google Ads, researching keywords, using Keyword Planner, analyzing competitors, or deciding campaign structure before launch.

## Prelaunch Product Preparation

Do not recommend a live campaign until the launch basics are verified or explicitly labeled as assumptions.

Landing page checklist:

- First-screen headline states the exact job-to-be-done, not only the brand name.
- CTA is visible and matches the conversion goal.
- Page language matches ad language and target region.
- Product input/output workflow is clear: what the user gives, what the product returns, and how fast.
- Pricing, free plan, limits, or trial expectation are visible enough to avoid surprise clicks.
- Trust proof exists when the category needs it: screenshots, examples, docs, security/privacy notes, testimonials, or comparison.
- Mobile experience is acceptable when mobile traffic is expected.
- Page supports the claim in the ad. Do not advertise a feature only because it is in the keyword list.

Assets checklist:

- 15 responsive search ad headlines per main ad group.
- 4 descriptions per main ad group.
- Display paths with recognizable intent words.
- Sitelinks only for pages that help conversion: pricing, docs, guide, examples, signup, comparison.
- Structured snippets only when the values are real product capabilities.
- Product screenshots or images only when they clarify the offer; avoid generic images.

Conversion checklist:

- Primary conversion: the meaningful business goal, such as purchase, qualified lead, completed signup, or equivalent.
- Secondary conversion: activation or product usage, such as project/deployment created.
- Diagnostic events: CTA clicks, page views, form starts, signup intent, navigation, upgrade prompt viewed.
- Verify Google Ads conversion status, analytics event, and backend/CRM count if available.

## Keyword Research Workflow

Build keyword ideas from six sources:

- Product category: what the product is.
- Job-to-be-done: what the user wants to accomplish.
- Input/output: file type, object, source, destination, result.
- Problem language: errors, friction, "without X", "no setup", "fast", "free", "online".
- Alternatives: competitor, platform, manual method, category alternatives.
- Existing evidence: Google Search Console, site search, ads search terms, support tickets, sales calls, analytics landing pages.

Classify every keyword into one of:

- **Core high intent**: directly describes the product's strongest conversion path.
- **Adjacent high intent**: related use case that the product supports, but may need a dedicated landing page/ad group.
- **Research/learning**: relevant but earlier-stage or unclear monetization.
- **Content/SEO only**: useful query but too broad or expensive for ads.
- **Negative/reject**: wrong product, wrong workflow, wrong audience, unsupported feature, freebie-only with no business value, or likely support/login/navigation intent.

## Google Ads Keyword Planner

Use the user's Google Ads UI when possible. The two main cards/screens are:

### Discover New Keywords

Use this when the user needs keyword ideas.

Field guidance:

```text
Card: Discover new keywords (`发现新关键字`)
Use when: Need new keyword ideas from seed terms or a landing page.
Input method 1: Start with keywords (`首先输入关键字`)
Input method 2: Start with a website (`首先指定网站网址`)
Location: target country or region only; do not leave a default region if it mismatches the campaign.
Language: campaign language, not account UI language.
Website URL: final landing page or the closest relevant product page.
Scope: entire site only when the site is tightly focused; otherwise use only this page.
```

Seed term rules:

- Use 5-15 seed terms per theme.
- Keep one intent per plan. Do not mix brand, competitor, product category, and unrelated formats in one pull.
- Include localized phrases written by humans, not only literal translations.
- Include negative filters or excluded URL/page scope when the site contains unrelated products.

Export and interpret:

- Export keyword ideas with average monthly searches, 3-month change, YoY change, competition, top-of-page bid low/high, and keyword text.
- Mark high search volume but low intent as SEO/content or reject.
- Mark expensive terms as test candidates only if landing page and expected LTV justify them.
- Do not add all suggested broad keywords. Group and review manually.

### Get Search Volume And Forecasts

Use this when the user already has candidate keywords and needs traffic/cost estimates.

Field guidance:

```text
Card: Get search volume and forecasts (`获取搜索量和预测数据`)
Use when: Candidate keyword list exists and we need estimated clicks, CPC, cost, conversions, and budget pressure.
Paste: exact and phrase candidates, one per line. Keep broad candidates separate.
Location: same as planned campaign.
Language: same as planned campaign.
Bid/budget: use the user's current max CPC/daily budget or a stated test guardrail.
Export: forecast, historical metrics, and plan by keyword if available.
```

Interpret forecasts cautiously:

- Forecasts are directional, not truth.
- Compare top-of-page bid with max CPC and acceptable CPA.
- If forecast cost exceeds learning budget, narrow match types or split ad groups.
- If search volume is tiny but intent is perfect, keep exact match as a low-cost capture term.

## Competitor And Category Research

Use competitor research when the user asks for better keywords, market positioning, alternative pages, or category strategy.

Research checklist:

- Search results: ads shown, organic pages, SERP intent, country/language differences.
- Competitor landing pages: first-screen promise, CTA, supported workflow, proof, pricing, limits, onboarding friction.
- Keyword categories: product category, alternative/vs, integration, feature, problem, migration, pricing, free.
- Claim gaps: what competitors promise that the user's product can or cannot support.
- Landing-page gap: whether the user's page can safely answer the query.

Output competitor findings as:

```text
Competitor/category:
Evidence:
Possible keyword theme:
Can advertise now? Yes / No / Only with landing page change
Needed page/ad copy:
Risk:
```

Do not recommend competitor-conquest keywords unless:

- The competitor term appears in evidence or the user explicitly wants the test.
- The product has a clear alternative/comparison argument.
- The landing page does not mislead users.
- The budget is isolated and the stop rule is strict.

## Campaign Architecture From Research

Turn research into isolated ad groups:

- One ad group per intent cluster.
- One campaign per market/language when geography or language changes.
- Exact match for highest-confidence terms.
- Phrase match for controlled variations.
- Broad match only after conversion data, negatives, and tracking are reliable.

Initial output format:

```text
Campaign:
Market/language:
Landing page:
Ad group:
Intent:
Exact keywords:
[keyword]

Phrase keywords:
"keyword"

Initial negatives:
"bad intent"

Do not add:
- keyword/theme: reason
```

## First Launch Guardrails

For a new product or unproven market:

- Prefer small, controlled Search tests over full automation.
- Disable Display Network for controlled validation.
- Use presence-based location targeting when relevant.
- Use Maximize clicks with a CPC cap when primary conversion data is sparse.
- Review after 24 hours for tracking/spend issues, after 72 hours for obvious terms, and after about 7 days or sufficient clicks for stronger keyword decisions.

If readiness is incomplete, output a preparation plan instead of pretending the campaign is ready.
