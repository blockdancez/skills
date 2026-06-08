# Google Ads Growth Strategy Playbook

Use this reference when the user needs more than field-filling or keyword triage: long-term paid-search strategy, market expansion, product feedback, budget allocation, experiment design, or a second brain for what to try next.

## Strategic Posture

Every strategic recommendation must be tagged as one of:

- **Evidence**: directly supported by reports, analytics, conversion data, product facts, or screenshots.
- **Inference**: a reasonable interpretation of the evidence, but not directly proven.
- **Hypothesis**: a testable idea that may improve growth, but needs a controlled experiment.

Do not present hypotheses as facts. Do not hide behind caution either: propose useful experiments when the upside is plausible and the risk is bounded.

## Campaign Stage Diagnosis

Before giving strategic advice, classify the current stage:

- **Discovery**: few conversions, unknown query quality, or new market. Optimize for learning with controlled spend.
- **Validation**: some conversions, enough search terms to see intent, but CPA or activation is still unstable.
- **Scale**: repeatable conversions with acceptable CPA and enough high-intent search inventory.
- **Efficiency**: conversions exist but CPC/CPA is rising, wasted queries appear, or budget is limited.
- **Expansion**: a core market works and the user is testing new languages, countries, formats, or use cases.
- **Recovery**: performance dropped after bid, keyword, landing-page, tracking, or market changes.

Output the stage and the reason. Example:

```text
Stage: Validation
Evidence: 43 conversions, CPA $19.05, but most conversions come from one ad group and secondary activation is uneven.
Implication: protect the winning ad group, keep testing adjacent intents with isolated budgets, and do not over-scale weak ad groups yet.
```

## Growth Bottleneck Map

Map the bottleneck before changing many keywords:

- **Traffic quality**: search terms are irrelevant, wrong language, wrong country, or too broad.
- **Ad relevance**: CTR is weak for relevant terms or ad copy does not mirror query intent.
- **Landing-page fit**: clicks arrive, but visitors do not move to signup or the top page does not answer the query.
- **Signup friction**: signup intent is high, verification/register success is low.
- **Activation friction**: register success is fine, but product usage events are low.
- **Revenue friction**: activation exists, but checkout/purchase/subscription is low.
- **Tracking weakness**: Ads conversions, analytics events, and database counts disagree.
- **Market mismatch**: one country/language gets traffic but does not activate or pay.
- **Product promise mismatch**: search demand points to a feature, format, or workflow the product does not fully support.

For each bottleneck, recommend one paid-search action and one product/landing-page action when relevant.

## Long-Term Review Cadence

Use this cadence unless the user asks for a different operating rhythm:

- **Daily during launch**: broken URLs, spend pacing, countries, networks, search terms with obvious bad intent, tracking fire rate.
- **Every 72 hours**: add obvious negatives, add exact matches from converting search terms, tune ad copy around high-intent queries.
- **Weekly**: judge ad groups, keyword clusters, CPA, conversion quality, activation, and regional mix.
- **Every 14-30 days**: reallocate budget, retire weak experiments, launch new experiment cells, review landing-page/product opportunities.
- **Monthly**: compare paid-search learnings with SEO/content roadmap, competitor pages, feature roadmap, pricing, and onboarding.

Avoid heavy optimization within the first 24 hours unless something is clearly broken or wasteful.

## Experiment Portfolio

Maintain a balanced experiment portfolio instead of only optimizing the existing campaign:

- **Core intent**: proven high-intent search terms. Protect budget and quality.
- **Adjacent intent**: search terms close to the core promise, tested with phrase/exact match.
- **New format or feature**: newly supported file type, workflow, integration, or audience.
- **Competitor/alternative intent**: "{competitor} alternative", "{competitor} vs {product}", or category alternatives.
- **Market/language expansion**: isolated campaigns by country/language.
- **Landing-page variant**: same intent, different message, proof, demo, pricing, or friction removal.
- **Monetization test**: discount, pricing proof, plan messaging, checkout flow, or trial/free limit.
- **Content/SEO feedback loop**: queries that are useful but too expensive for Ads become SEO pages or docs.

For each proposed experiment, output:

```text
Experiment:
Goal:
Setup:
Budget/risk guardrail:
Primary signal:
Secondary signal:
Stop rule:
Scale rule:
```

## Market Expansion

Do not recommend new countries only because they are cheap. Check:

- Localized landing page exists and matches the ad language.
- Search terms are in the local language and represent product intent.
- Signup, verification, activation, billing, and support work for that country.
- CPC is affordable relative to expected value.
- Early funnel quality is not just page views.

Expansion strategy:

- Start with one language/region campaign per market group.
- Use small isolated budget until search terms and conversions prove quality.
- Prefer exact/phrase match at first.
- Track country-level visitors, page views, signup intent, register success, activation, and purchase.
- Scale a market only when it has meaningful conversion or activation, not just high CTR.

If a market produces high page views but few users, suspect low-quality traffic, wrong language, or curiosity clicks.

## Budget Allocation

Allocate budget by learning value and proof:

- **Protect winner**: keep the proven high-intent ad group funded.
- **Cap weak tests**: do not let low-proof experiments spend like winners.
- **Reserve experiment budget**: keep a fixed small portion for new markets/features.
- **Use guardrails**: define max daily spend, max CPC, max CPA, and stop rules.
- **Avoid blended averages**: review by campaign/ad group/country/device/landing page.

Suggested early split when one core group is clearly best:

```text
70-80% core proven intent
10-20% adjacent/new feature tests
5-10% market/language expansion
0-5% competitor or speculative tests
```

Change the split only after enough data shows a new cell deserves more budget.

## Product And Landing-Page Feedback

Paid search is also product research. If search terms repeat a demand, suggest product or content work:

- **Feature gap**: users search for a format/workflow not supported.
- **Promise clarity gap**: users search for exactly what the product does, but the landing page hides it.
- **Education gap**: users confuse source code, build output, files, previews, hosting, or deployment.
- **Trust gap**: users hesitate without examples, screenshots, pricing, limits, privacy, or proof.
- **Activation gap**: users register but do not complete the first meaningful action.
- **Monetization gap**: users activate but do not start checkout.

Output product/landing-page ideas separately from ad operations and mark them as `Product follow-up` or `Landing-page follow-up`.

## Competitor And Category Thinking

Use competitor analysis when:

- The user references a competitor.
- Search terms include competitor names.
- The product has a clear alternative page.
- The market category is unclear and competitors reveal better positioning.

Compare:

- Product promise and first-screen clarity.
- Supported input/output workflow.
- Pricing and limits.
- Social proof and trust.
- SEO landing pages and comparison pages.
- Ad language and likely search intent.

Do not suggest competitor conquest campaigns if the landing page cannot clearly explain why the product is a better fit.

## Strategic Output Template

For strategic reviews, include this after tactical keyword/ad operations:

```text
Strategic read
Stage:
Main bottleneck:
Evidence:
Inference:
Hypotheses:

Next experiments
1. Experiment:
   Goal:
   Setup:
   Budget/risk guardrail:
   Stop rule:
   Scale rule:

Product / landing-page follow-ups
- Item:
  Why:
  Evidence or hypothesis:

What not to do yet
- Item:
  Reason:
```

Keep it concise. The goal is to expand the user's thinking without burying exact operational steps.
