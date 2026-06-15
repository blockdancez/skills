# Google Ads Practical Playbook

This reference stores reusable Google Ads operating knowledge learned from real campaign creation/editing screens and performance reviews. It is product-agnostic. Use product-specific data only as examples, not as universal truth.

For exact current Google Ads screen order, visible field labels, default checkboxes, and first-campaign page flow, read `references/google-ads-ui-field-guide.md` before applying this playbook. This playbook explains the operating logic behind those fields.

## Evidence Standard

Every recommendation must be tied to one of:

- Visible Google Ads UI fields from screenshots or known screens.
- Google Ads keyword/search-term CSV reports.
- Analytics data: pages, referrers, countries, devices, events.
- Database or CRM funnel data: signups, leads, purchases, activations.
- Product facts and landing page content.
- User-confirmed budget, risk level, region, language, or business goal.

If the needed page or account-specific option is unknown, ask for one screenshot. If data is missing, ask for the smallest useful report, usually keyword report + search-term report + conversions + analytics for the same period.

## Beginner Wizard Mode

Use this when the user is new to Google Ads, creating a first campaign, or asking "how do I fill this page".

Always output in this order:

1. Campaign settings to fill.
2. Ad group settings to fill.
3. Keyword box content, one keyword per line.
4. First responsive search ad fields.
5. URL options / UTM.
6. Conversion goal setup.
7. Initial negative keywords.
8. Pre-launch checklist.
9. First review schedule: 24 hours, 72 hours, 7 days.

For each field, use the visible Google Ads label when known, then provide the exact value to paste. If a field is unknown because the UI changed, ask for one screenshot of that page instead of guessing.

Use this concise format:

```text
Field: Campaign name (`广告系列名称`)
Fill: Product-US-EN-202606
Reason: Region, language, and month are clear, which makes later market-level review easier.
```

Do not answer only with ad copy or keywords when the user is building a first campaign. First launches need the full setup path.

## Campaign Setup

Use this when the user is creating a new Google Ads Search campaign.

Recommended controlled-test defaults:

- Campaign type: Search.
- Campaign name: `{Product}-{Regions}-{Language}-{YYYYMM}`.
- Budget: start small enough to learn without wasting spend; increase only after CPA/quality is acceptable.
- Bidding: start with Maximize clicks (Chinese UI may show `尽可能争取更多点击次数`) plus a CPC cap when conversion data is sparse. Use Maximize conversions (Chinese UI may show `尽可能提高转化次数`) only when reliable primary conversions exist and the user intentionally wants conversion bidding.
- Networks: Google Search only for controlled tests. Disable Display Network and Search Partners unless explicitly testing expansion.
- Locations: split by market/language. Do not mix unrelated languages in one campaign.
- Location option: people in or regularly in targeted locations, not merely people interested in those places.
- Languages: match the landing page and ad copy language.
- Conversion goals: optimize to meaningful primary conversions, not diagnostic clicks.

Do not assume adding conversion actions automatically changes bidding. Verify campaign settings, Google Ads recommendations/auto-apply, and campaign/account-default goals.

## Bidding Decision Tree

Use this before recommending or changing bid strategy.

- **No reliable primary conversions yet**: use Maximize clicks (Chinese UI may show `尽可能争取更多点击次数`) with a CPC cap. Goal is controlled query discovery.
- **Reliable primary conversion exists but weekly volume is low**: keep Maximize clicks or run Maximize conversions only as a deliberate test with small budget. Do not treat one good day as enough evidence.
- **Stable primary conversions and acceptable CPA**: consider Maximize conversions (Chinese UI may show `尽可能提高转化次数`).
- **Stable CPA target and enough conversion volume**: consider Target CPA (Chinese UI may show `目标每次转化费用`).
- **Revenue or subscription value is tracked reliably**: consider value-based bidding later, not at first launch.

Decision output must include:

- Current conversion actions used for bidding.
- Whether each action is primary or secondary.
- Conversion count and CPA for the same reporting period.
- Why the selected strategy fits the current sample size.

If a campaign unexpectedly changes to Maximize conversions, check:

1. Campaign bid strategy setting.
2. Account-default goals.
3. Auto-applied recommendations.
4. Accepted Google recommendations.
5. Whether the user recently changed primary conversion actions.

## Ad Group Setup Screen

Known Google Ads fields from the real setup screen:

- Ad group type (Chinese UI: `广告组类型`): choose Standard (`标准`) unless the user has a specific reason for another type.
- Ad group name (Chinese UI: `广告组名称`): name by search intent, not by generic group number.
- Final URL (Chinese UI: `最终到达网址`): paste the real landing page URL for keyword suggestions.
- Product or service to advertise (Chinese UI: `输入要宣传的产品或服务`): enter a concise service/product phrase, such as `HTML file hosting`, `Markdown file hosting`, `CRM lead routing`, or a localized equivalent.
- Get keyword suggestions (Chinese UI: `获取建议的关键字`): use only for discovery. Do not accept suggestions blindly.
- Keyword text area: paste selected keywords. One keyword per line is safest.
- Match types:
  - `[keyword]` = exact match.
  - `"keyword"` = phrase match.
  - `keyword` = broad match.
- Search-term matching / AI Max (Chinese UI: `搜索字词匹配 / AI Max`): for controlled tests, use only your keywords and match types. Enable expansion only after search terms and negatives are under control.
- Brand restrictions (Chinese UI: `限定的品牌`): leave empty unless building a brand-only or competitor campaign.
- Locations of interest (Chinese UI: `感兴趣的地理位置`): usually leave empty at ad group level; control locations at campaign level.
- URL inclusion objects (Chinese UI: `网址包含对象`): leave empty unless intentionally restricting serving to URL patterns.

First ad group must include enough keywords to serve, but not so many that intent becomes mixed. Prefer exact/phrase for new tests.

## Keyword Selection

Use phrase and exact match for first launch:

- Use exact for high-confidence, high-intent queries.
- Use phrase for moderate variation around a clear intent.
- Avoid broad match until the account has strong conversion data and a mature negative keyword list.

Decision rules:

- Keep: keywords with conversions or clear intent and low sample size.
- Pause: wrong intent with spend and no conversions. Practical starting threshold: spend >= `$10` or clicks >= `8-10`, 0 conversions.
- Monitor: has clicks/cost but too little sample or has conversions with high CPA.
- Add: converting search terms that directly match the product promise.
- Do not pause: zero-click/zero-cost terms only because they have no conversions.

When analyzing search terms:

- Add exact keywords from converting terms if they match product intent.
- Add negatives from costly zero-conversion terms if they are irrelevant.
- Do not add a negative that is still an active targeted keyword in the same scope.

When giving keyword operations, classify every material term:

- `Keep`: conversions, good CPA, or clearly relevant with insufficient sample.
- `Add exact`: converting search term with exact product intent.
- `Add phrase`: recurring relevant search term variation that needs controlled expansion.
- `Pause`: active keyword has wrong intent with spend or enough clicks and no conversion.
- `Negative`: irrelevant search term. State scope: ad group, campaign, or account list.
- `Observe`: too little data, mixed signal, or high CPA but not enough evidence to stop.

Never pause a keyword only because it has no conversion if it has no spend or too few clicks. Never keep a keyword only because it has clicks if the search terms prove wrong intent.

## Negative Keywords

Google Ads may reject negatives with the message that you cannot exclude targeted keywords. This means the negative term is currently active as a targeted keyword.

Fix sequence:

1. Check whether the term exists as a keyword in the same ad group/campaign.
2. If data says it should not serve, pause or remove that targeted keyword.
3. Add the negative keyword afterward.

Use scope carefully:

- Ad group negative: intent is bad only for this ad group.
- Campaign negative: intent is bad for the whole campaign.
- Account/shared negative list: intent is bad for all campaigns.

Negative examples by category, adapt to product:

```text
"editor"
"runner"
"template"
"builder"
"generator"
"viewer"
"pdf"
"login"
"download"
"source code"
"github"
"localhost"
```

Never paste a generic negative list without checking whether it conflicts with active keywords or blocks valid product intent.

Negative matching cautions:

- Negative broad, phrase, and exact are not the same as positive keyword matching.
- Add obvious variants, plurals, misspellings, and translations if they appear in search terms.
- Do not add single-token negatives such as `[html]` or `[url]` unless that token is always bad for the whole scope.
- If a negative conflicts with a targeted keyword, first decide whether the targeted keyword should remain active.

## First Responsive Search Ad

Known fields from the real Google Ads RSA editor:

- Final URL (Chinese UI: `最终到达网址`): landing page URL.
- Display path (Chinese UI: `显示路径`): two optional path fields, each up to 15 characters. Use intent words, not decoration.
- Headlines (Chinese UI: `标题`): up to 15 headlines, 30 characters each.
- Descriptions (Chinese UI: `广告内容描述`): up to 4 descriptions, 90 characters each.
- Image assets (Chinese UI: `图片`): optional. Use real product screenshots when available; avoid generic art.
- Sitelinks (Chinese UI: `站内链接`): optional at launch. Add only if strong pages exist.
- Structured snippets (Chinese UI: `结构化摘要`): optional; useful for feature/support-type lists.
- Lead form / app assets (Chinese UI: `潜在客户表单` / `应用`): leave empty unless the campaign is explicitly built for those assets.
- Ad URL options (Chinese UI: `广告网址选项`): tracking template, final URL suffix, custom parameters, mobile final URL checkbox.

Headline rules:

- Put the dominant query intent in the first 3-5 headlines.
- Include product category, action, and outcome.
- Include constraints when they prevent bad clicks, such as "No Build Step" or "Upload Build Output".
- Avoid overusing vague claims like "AI-powered" unless the query explicitly asks for AI.

Description rules:

- Say what the user can submit/upload/share.
- Say what they receive.
- Mention major limitations that filter bad traffic.
- Keep language matched to campaign language.

Ad quality checks:

- First 3-5 headlines must mirror the dominant keyword intent.
- At least one headline should state the output/result.
- At least one headline should filter bad clicks when needed, such as "No Git Needed", "No Build Step", or "Upload Build Output".
- Descriptions must match landing page content. Do not promise features not visible on the landing page.
- Display path should use intent words users recognize.
- If ad strength is weak, improve relevance before adding generic slogans.

Generic English headline templates:

```text
{Action} {File/Product} Online
{Product} To Public URL
Upload {File/Product} Fast
Share {File/Product} As Link
No Setup Required
Public HTTPS Link
Built For {Audience}
{Product} Hosting
Deploy In Seconds
Try {Product} Free
```

Generic English description templates:

```text
Upload or paste {input}. Get a public HTTPS link you can share instantly.
Built for quick previews, client review, and static file sharing. No server setup.
Publish {file/product} online without Git, FTP, or manual hosting steps.
Start free, then upgrade when you need more previews, storage, or custom workflows.
```

## URL Options And UTM

For normal Google Ads usage, leave the tracking template (Chinese UI: `跟踪模板`) empty unless the account uses an external tracker.

Use final URL suffix:

```text
utm_source=google&utm_medium=cpc&utm_campaign={campaign_slug}&utm_adgroup={adgroup_slug}&utm_term={keyword}&utm_matchtype={matchtype}&utm_device={device}
```

Optionally add:

```text
utm_content={creative}
```

Use a separate mobile final URL only if there is a real mobile-specific landing page. Otherwise leave the mobile checkbox off.

## Conversion Preflight

Before launching or changing bidding, verify conversion actions:

- Primary conversion: the event that should guide bidding and budget decisions.
- Secondary conversion: useful activation signal, but not the main optimization target.
- Diagnostic event: click, page view, navigation, signup intent, form start, or other weak signal.

Checklist:

1. Confirm the primary conversion name, status, and source in Google Ads.
2. Confirm the same event appears in site analytics or backend data.
3. Check duplicate counting: one user should not create multiple fake conversions unless the business wants that.
4. Check conversion lag before judging one-day data.
5. Keep diagnostic events out of primary goals unless the user explicitly accepts weak-signal bidding.

When the product has a funnel, report it as:

```text
Visitors -> signup intent -> verification sent -> register success -> activation -> checkout/purchase
```

Use `register_success`, qualified lead, purchase, subscription, or equivalent as primary when available. Use activation events such as deployment/project created as secondary until volume and value are understood.

## Conversion Setup

Classify conversion actions by business value:

- Primary: purchase, subscription, qualified lead, completed signup, or another event the business truly wants to optimize for.
- Secondary: activation/product usage, such as deployment created, project created, onboarding completed.
- Diagnostic only: page view, CTA click, signup intent, navigation click, form start.

For early campaigns:

- Use the most reliable meaningful conversion as primary.
- Keep sparse but higher-value events as secondary until there is enough data.
- Do not optimize bidding toward diagnostic click events unless there is no better signal and this is explicitly a learning phase.

If the campaign seems to change to Maximize conversions:

- Verify current campaign bid strategy.
- Check whether account-default goals include primary conversion actions.
- Check whether auto-apply recommendations changed bidding.
- Check whether the user accepted a Google recommendation.

## Pre-launch Checklist

Before telling the user to publish a campaign, check:

- Final URL returns 200 and matches the ad language.
- Landing page headline matches the ad group intent.
- Display path matches the keyword theme.
- URL suffix has `utm_source`, `utm_medium`, `utm_campaign`, `utm_adgroup`, `utm_term`, `utm_matchtype`, and `utm_device`.
- Campaign networks are intentionally selected. For controlled tests, use Google Search only.
- Location targeting and language match the landing page.
- Location option is set intentionally, preferably presence-based for controlled SaaS tests.
- Budget and CPC cap are explicit.
- Primary/secondary conversions are correct.
- Initial negative keywords do not conflict with active positive keywords.
- Auto-apply recommendations are reviewed, especially bid strategy changes.

## Post-launch Review Cadence

Use this rhythm for new campaigns:

- **First 24 hours**: check tracking, spend pacing, broken URLs, obvious wrong countries/languages, and search terms with clearly bad intent. Do not over-optimize small samples.
- **After 72 hours**: add obvious negatives, add exact keywords from converting search terms, adjust ad copy if query intent is clear, and check CPC spikes.
- **After 7 days or 100+ clicks**: make keyword-level keep/pause decisions, evaluate CPA by ad group, and consider budget shifts.

Minimum data rules:

- Under 20 clicks per keyword/search term: usually observe unless intent is plainly wrong.
- 8-10 clicks with 0 conversion and wrong intent: pause or negative is acceptable.
- Spend above the target CPA with 0 conversion: inspect intent and landing behavior before pausing.
- Converting but expensive: keep and monitor; consider query split, ad copy, landing page, or CPC cap before pausing.

## Region And Language Expansion

Use separate campaigns when markets differ by language, price sensitivity, or landing page.

For each candidate country/language, check:

- Localized landing page exists and returns 200.
- Ad copy language matches landing page language.
- Keywords are written in the target language, not machine-translated blindly.
- Billing, signup, and product usage work for that country.
- Time zone and support expectations are acceptable.
- Budget is small enough for a test and isolated from the main campaign.

Expansion decision:

- Keep or scale when CTR, CPC, conversion rate, and activation are better than or close to the main market.
- Pause or cap when traffic is cheap but does not reach the meaningful conversion.
- Do not mix a new language into a mature English campaign.

## Optimization Workflow

For each reporting cycle:

1. Read keyword report and search-term report for each ad group.
2. Compare with analytics for the same or closest date range.
3. Compare with database/CRM funnel counts if available.
4. Segment by campaign, ad group, keyword, search term, country, language, device, landing page, and conversion action.
5. Produce exact operations with evidence.

Metrics to compute:

- Impressions, clicks, CTR, CPC, spend.
- Conversions, conversion rate, CPA.
- Search-term quality: product match, language match, funnel match.
- Landing page behavior: bounce rate, pages visited, signup, activation, purchase.

Output operation taxonomy:

- `Keep`: converting or strong-intent terms.
- `Add`: converting search terms or newly supported product intent.
- `Pause`: wrong-intent spend with enough evidence.
- `Negative`: irrelevant search terms, with scope and match type.
- `Observe`: small sample, mixed intent, high CPA but some promise.
- `Revise ad copy`: ad copy does not match winning query/landing page.
- `Adjust region/language`: mismatched traffic or a market needs a separate campaign.
- `Adjust bidding`: CPC/CPA trend justifies cap or strategy change.

Recommended optimization output table:

```text
Ad group | Object | Action | Evidence | Exact add/remove content | Risk/notes
```

The table must be followed by paste-ready blocks:

```text
Exact keywords to add:
[example keyword]

Phrase keywords to add:
"example keyword"

Ad group negatives:
"bad intent"

Campaign negatives:
"bad for all groups"
```

If the CSV script suggests an action but product intent is unknown, label it `Needs intent review`, not `Pause`.

## Real Case Study: PreviewShip

Use this only as an example of applying the framework.

Product facts:

- Supports publishing static preview URLs from ZIP build outputs, single HTML files, pasted HTML, `.md`, and `.markdown`.
- Supports console, CLI, MCP, and editor extension flows.
- Does not build source-code ZIPs; users should upload build output, single HTML, pasted HTML, or Markdown.

Historical signals from 2026-05-29 to 2026-06-07:

- `HTML File Hosting - High Intent`: 5,119 impressions, 413 clicks, 8.07% CTR, `$940.05` spend, 56 conversions, CPA `$16.79`. This was the main winner.
- `AI HTML To Live URL`: 755 impressions, 27 clicks, `$60.50` spend, 1 conversion, CPA `$60.50`. Weak; should not dominate budget without better evidence.
- `Static Hosting Alternatives`: 67 impressions, 2 clicks, `$11.52` spend, 0 conversions. Paused.
- `Markdown File Hosting - Test`: 13 impressions, 1 click, `$1.83` spend, 0 conversions. Too small to judge.
- `PreviewShip-BR-PT-Portuguese-202606`: 118 impressions, 22 clicks, 18.64% CTR, `$44.67` spend, 4 conversions, CPA `$11.17`. Strong early signal but small sample.

PreviewShip conversion setup used in prior analysis:

- `register_success`: primary.
- `deployment_created`: secondary.
- `signup_intent` / CTA clicks: diagnostics.

PreviewShip reusable field examples:

- English HTML final URL: `https://previewship.com/upload-html-file-to-website/`
- English display path: `html-file` / `hosting`
- Portuguese HTML final URL: `https://previewship.com/pt/guides/upload-html-file-to-website`
- Portuguese display path: `hospedar-html` / `gratis`
- Markdown final URL: `https://previewship.com/upload-markdown-file-to-website/`
- Markdown display path: `markdown` / `hosting`

PreviewShip English HTML UTM:

```text
utm_source=google&utm_medium=cpc&utm_campaign=us_ca_gb_au_202606&utm_adgroup=html_file_hosting&utm_term={keyword}&utm_matchtype={matchtype}&utm_device={device}
```

PreviewShip BR/PT UTM:

```text
utm_source=google&utm_medium=cpc&utm_campaign=br_pt_portuguese_202606&utm_adgroup=html_hosting_pt&utm_term={keyword}&utm_matchtype={matchtype}&utm_device={device}
```

## When To Ask The User

Ask for more information only when it changes the recommendation:

- Unknown landing page URL or product promise.
- Unknown target region/language.
- Unknown budget or risk tolerance.
- Unknown conversion action names/status.
- No keyword/search-term CSV for an optimization request.
- Google Ads page is not one of the known screens above or appears changed.
- A proposed operation would remove significant spend or a converting keyword and the evidence is incomplete.
