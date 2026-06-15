# Google Ads UI Field Guide

This reference stores observed Google Ads UI fields and page order from real screenshots. Use it to answer "where do I click" and "what does this field mean" without asking the user for another screenshot. Business strategy, budgets, markets, conversion actions, and product claims still require user evidence or confirmation.

## Operating Rules

- Use known UI labels here first. Ask for a screenshot only when the current page is not covered, appears different, or has account-specific warnings that affect launch.
- Do not treat Google Ads recommended defaults as strategy. Recommendations, preselected networks, AI Max, broad expansion, and suggested budgets are inputs to review.
- For first-time Search campaign creation, Google Ads usually requires campaign settings, at least one ad group keyword set, and one responsive search ad before the final review.
- If the UI field is known but the value depends on the product, say the exact field name and ask only for the missing product/business fact.
- If the user only provides a product name or domain, do not jump to paste-ready keywords, ads, budgets, or conversion names. Guide research and readiness first.

## Keyword Planner Home

Path observed: left navigation `工具` -> `规划` -> `关键词规划工具`.

Home cards:

- `发现新关键字`: get keyword ideas to reach users interested in the product or service.
- `获取搜索量和预测数据`: get search volume, historical metrics, and forecast data for existing keyword candidates.

Plan table:

- Tabs: `由您创建的方案`, `与您共享的方案`.
- Common columns: `方案`, `状态`, `最后修改时间`, `预测期`.
- Controls: filter, `列`.

Use `发现新关键字` for early discovery. Use `获取搜索量和预测数据` when the user already has a candidate list and needs volume/CPC/forecast checks.

## Discover New Keywords: Start With Keywords

Modal title: `发现新关键字`.

Tabs:

- `首先输入关键字`.
- `首先指定网站网址`.

Fields and controls on `首先输入关键字`:

- Main input label: `输入与您的业务最相关的产品或服务`.
- Placeholder example: `尝试输入“送餐”或“皮靴”`.
- Language and location chips appear below the input, for example `繁体中文（台湾）（默认）` and `香港`.
- Optional URL field: `输入网站网址以过滤不相关的关键字`.
- URL placeholder: `https://`.
- Button: `获取结果`; disabled until enough input exists.

Operator guidance:

- Use 5-15 seed terms grouped by one intent, not a mixed bag of all product features.
- Set location and language to the intended test market before exporting.
- Add the landing page URL only when it accurately represents the offer; otherwise it can filter out useful adjacent ideas.
- If default location/language is wrong, tell the user to change it before trusting export metrics.

## Discover New Keywords: Start With Website

Fields and controls on `首先指定网站网址`:

- URL field label: `输入网站或网页网址，以查找与您的网站匹配的关键字`.
- Example text: `输入 domain.com（网站）或 domain.com/page（网页）`.
- Language and location chips appear below the URL field.
- Radio options:
  - `使用整个网站`.
  - `仅使用此页面`.
- Button: `获取结果`; disabled until enough input exists.

Operator guidance:

- Choose `使用整个网站` only when the site is focused on one product/category.
- Choose `仅使用此页面` for multi-product sites or when testing one landing page.
- Treat website-derived ideas as a first pass. Export and review by intent, search volume, competition, and CPC before building campaigns.

## Keyword Ideas Results

Observed results page elements:

- Breadcrumb: `关键词规划工具`.
- Plan title may show creation time, for example `6月 15, 2026, 5 下午 (GMT+08:00) 创建的方案`.
- Tabs: `关键字提示`, `预测`, `已保存的关键字`, `否定关键字`.
- Top context chips: website/source, location, language, network, and date range.
- Example chips observed: `网站: https://previewship.com`, `香港`, `繁体中文（台湾）`, `Google`, `2025年6月 - 2026年5月`.
- Download action: `下载关键字提示`.
- Filter row: filter icon, `排除含成人内容的提示`, `添加过滤条件`, keyword idea count such as `862 条可用的关键字提示`.
- Table controls: `列`, `关键字视图`.
- Right panel: `优化关键字`; it may show `无结果`, which is not necessarily an error.

Observed table columns:

- `关键字（按相关性排序）`.
- `平均每月搜索量`.
- `三个月变化`.
- `年同比变化`.
- `竞争程度`.
- `广告展示次数份额`.
- `页首出价（低位区间）`.
- `页首出价（高位区间）`.
- `账号状态`.

Operator guidance:

- Ask the user to export/download keyword ideas when real keyword decisions are needed.
- Do not recommend final keywords only from screenshots unless the visible rows are sufficient and match the product.
- Use `平均每月搜索量` for rough demand, `三个月变化`/`年同比变化` for trend, `竞争程度` for auction crowding, and `页首出价` for CPC/budget expectations.
- `账号状态` can show whether a keyword already exists in the account; use this to avoid duplicate adds.

## New Campaign Entry

Observed campaign list entry:

- Left nav group: `广告系列`, with subitems `广告系列`, `广告组`, `广告`, `实验`.
- Click the plus button on the campaign list.
- Menu options:
  - `新广告系列`.
  - `继续修改广告系列草稿`.
  - `加载广告系列设置`.

Use `新广告系列` for a new campaign. Use draft/settings options only when continuing a saved draft or cloning known settings intentionally.

## New Campaign: Objective, Type, URL, Name

Page title: `您的广告系列目标是什么？`

Observed objective cards:

- `销售`: attract users to purchase on website, app, phone, or store.
- `潜在客户`: encourage users to act so you can get leads and other conversions.
- `网站流量`: attract target visitors to the website.
- `应用宣传`: get more app installs, interactions, and preregistrations.
- `YouTube 覆盖面、观看次数和互动次数`: improve awareness and consideration.
- `本地实体店光顾次数和促销表现`: improve local store visits and promotions.
- `在没有目标导向的情况下制作广告系列`: continue without a goal-driven setup.

Conversion summary section:

- Header pattern: `为了更好地实现上面选择的“网站流量”目标，可以选用以下转化目标`.
- Columns: `转化目标`, `转化来源`, `转化操作`, `值`.
- Observed rows include `互动（账号默认）`, `注册（账号默认）`, `网页浏览（账号默认）`, `购买（账号默认）`.
- Some rows can show warning icons and counts such as `1 项操作` or `2 项操作`.

Campaign type section:

- Header: `选择广告系列类型`.
- Cards observed: `效果最大化`, `搜索`, `需求开发`, `视频`, `展示`, `购物`.

Destination and name fields:

- Destination URL section: `选择您希望通过何种方式达成目标`.
- URL field can contain values like `https://lumi.new`.
- Campaign name section: `广告系列名称`.
- Auto-generated example: `Website traffic-Search-37`.
- Buttons: `取消`, `继续`.

Operator guidance:

- For SaaS direct response, prefer `销售` or `潜在客户` only when meaningful conversions are configured and reliable. Use `网站流量` only as a learning/traffic phase, and label it as such.
- Select `搜索` for controlled keyword-driven tests.
- Campaign name should encode product, market, language, intent, and month, for example `{Product}-{Market}-{Language}-{Intent}-{YYYYMM}`.
- Inspect conversion warnings before relying on those goals for bidding.

## New Search Campaign Flow

Observed left-step flow for a new Search campaign:

1. `出价`.
2. `广告系列设置`.
3. `AI Max`.
4. `关键字和广告`.
5. `预算`.
6. `检查`.

First launch guidance: prepare values for all six steps before starting. The `关键字和广告` step usually asks for both a keyword set and a first responsive search ad in the same flow.

## Bidding Page

Page/section: `出价`.

Observed fields:

- Question: `您希望着重实现的目标是什么？`
- Dropdown example: `转化次数`.
- Checkbox: `设置目标每次转化费用（可选）`.
- Input: `目标每次转化费用`, currency placeholder such as `US$`.
- Recommendation card with action button `应用`.
- Section: `客户获取`.
- Checkbox: `调整出价以便获取新客户`.

Operator guidance:

- Do not apply `目标每次转化费用` just because the checkbox appears. Use it only when the campaign has enough reliable primary conversions and a defensible CPA target.
- For sparse or new conversion data, prefer a controlled learning strategy such as maximize clicks with a CPC cap or a small deliberate maximize-conversions test.
- Do not enable new-customer acquisition bidding unless the user has confirmed new vs returning customer tracking and value.

## Campaign Settings Page

Page/section: `广告系列设置`.

Observed substeps:

- `网络`.
- `地理位置`.
- `语言`.
- `受众群体`.

### Networks

Section: `投放网络`.

Observed checkboxes, both shown selected by default:

- `Google 搜索合作伙伴网络（推荐）`.
- `Google 展示广告网络（推荐）`.

Operator guidance:

- For controlled Search launch, usually turn off `Google 展示广告网络`.
- Consider turning off `Google 搜索合作伙伴网络` unless the user intentionally wants expansion and accepts lower query transparency.
- If the user wants maximum reach and has strong negatives/conversions, document that this is an expansion choice.

### Locations

Section: `地理位置`.

Observed choices:

- `所有国家和地区`.
- A selected specific location, for example `香港`.
- `自行指定地理位置`.
- Expandable `地理位置选项`.

Observed location option choices:

- `所在地或兴趣：位于您已包含的地理位置、经常身处这些位置或对这些位置表现出兴趣的用户（推荐）`.
- `所在地：位于您已包含的地理位置或经常身处这些位置的用户`.

Operator guidance:

- For controlled market validation, prefer `所在地` instead of the broader `所在地或兴趣`.
- Use interest-based reach only when the user intentionally wants people outside the market who show interest in that market.

### Languages

Section: `语言`.

Observed fields:

- Input: `开始输入或选择一种语言`.
- Selected chip example: `英语`.
- Right-side suggestions can include `繁体中文`, `简体中文`, and `全部添加`.

Operator guidance:

- Language must match ad copy and landing page language.
- Split campaigns when market language, ad language, and landing page language differ.

### Audience Segments

Section: `细分受众群`.

Observed controls:

- Tabs: `搜索`, `浏览`.
- Search input with suggested text such as `试着搜一下“科技”`.
- Left list can show recent audiences and suggestions.
- Right panel shows selected audiences, initially `未选择任何项`.
- Campaign targeting setting:
  - `定位`.
  - `观察（推荐）`.

Operator guidance:

- For Search first launch, use `观察（推荐）` unless the user explicitly wants audience-restricted serving.
- Add audiences only when they support observation or deliberate bid adjustments.

## AI Max Search Campaign Page

Page title: `AI Max 搜索广告系列`.

Observed controls:

- Toggle: `利用 AI Max 优化广告系列`.
- Section: `优化素材资源`.
- Checkbox: `文案适配`.
- Checkbox: `最终到达网址扩展`.
- Links/actions: `添加文案准则`, `查看素材资源示例`, `添加网址排除对象`.
- Section: `品牌搜索`.
- Brand search options:
  - `针对所有相关搜索展示广告`.
  - `通过限定的品牌和品牌排除设置来控制品牌搜索`.
  - `仅针对不含品牌名称的搜索展示广告`.

Operator guidance:

- If the user wants strict keyword and landing page control, recommend turning AI Max off or limiting it carefully.
- If AI Max is enabled, review URL exclusions and brand search settings before launch.
- Do not accept `最终到达网址扩展` if the site has pages that would misrepresent the offer or route paid users to low-intent content.
- Do not let brand expansion or competitor terms run without a deliberate brand policy.

## Keywords And Ads Page

Page title: `关键字和广告`.

Observed substeps:

- `关键字`.
- `AI Max 设置`.
- `广告`.

First launch rule: expect to fill both a keyword set and one responsive search ad before review.

### Keyword Section

Observed fields:

- `获取建议的关键字（可选）`.
- Website URL field.
- Product/service field.
- Button/link: `获取建议的关键字`.
- Textarea: `输入关键字`.

Keyword textarea rules:

```text
[exact match keyword]
"phrase match keyword"
broad match keyword
```

One keyword per line is safest.

Operator guidance:

- Paste only reviewed keywords from Keyword Planner, existing reports, Search Console, competitor/category research, or a user-approved exploratory seed set.
- Do not accept all Google suggestions blindly.
- Use exact/phrase for controlled launch; broad match only when the account has enough conversion data and negatives.
- If Google suggests improving relevance, inspect whether the keywords, ad copy, and landing page are actually aligned before accepting automated changes.

### Ad Group AI Max Settings

Observed accordion: `广告组的 AI Max 设置`.

Account-specific rows can vary. If the user asks about a specific row not visible in this reference, ask for a screenshot of that section.

### Responsive Search Ad Editor

Observed ad creation section: `制作广告以获取更多网站流量`.

Fields and assets:

- `最终到达网址`: landing page URL.
- `显示路径`: two optional path fields, each up to 15 characters.
- `标题`: multiple headline fields, each up to 30 characters; link/button `+ 标题`.
- `广告内容描述`: description fields, each up to 90 characters.
- `图片`: optional image assets.
- `商家名称`: business name area may appear.
- `徽标`: logo area may appear.
- `站内链接`: can add multiple sitelink assets.
- Additional asset sections can include `促销`, `价格`, `致电`, `潜在客户表单`, `结构化摘要`, and related assets depending on account/campaign.
- `广告网址选项`: tracking template, final URL suffix, custom parameters, link test, and optional mobile final URL checkbox.

Operator guidance:

- Final URL must match the promise in the ad and keywords.
- Display path should describe user intent, not internal navigation.
- First 3-5 headlines should mirror the main keyword cluster.
- Descriptions should say what the user submits, what they get, and major constraints.
- Do not promise features not visible on the landing page.
- URL suffix should carry UTM tracking when the user has a tracking plan.

## Budget Page

Page title: `预算`.

Observed text: `决定您愿意支出多少费用。`

Important info box:

- After campaign starts, the budget type cannot be changed between `每日预算` and `广告系列总预算`.
- The budget amount can still be changed later.

Observed budget type choices:

- `平均每日预算`.
- Suggested amount cards, for example `US$116.44`, `US$97.03 推荐`, `US$77.62`.
- `设置自定义预算`.
- `广告系列总预算`.

Observed explanation:

- Recommended budgets are based on campaign settings such as bidding, location, keywords, ads, and similar advertisers.
- Monthly actual spend will not exceed the daily budget multiplied by the average number of days in a month.
- Some days can spend less than the daily budget; some days can spend up to about twice the daily budget.

Button: `下一步`.

Operator guidance:

- Do not choose Google recommended budget by default.
- Use the user's risk budget, test period, expected CPC, and required click volume.
- Confirm budget type before launch because budget type is locked after launch.

## Review / Check Page

Observed left-step label: `检查`.

No detailed screenshot was provided. If warnings appear on the review page, ask for that screenshot before telling the user to publish.

Review checklist:

- Objective and campaign type.
- Conversion goals and primary/secondary status.
- Bid strategy and any target CPA.
- Networks.
- Locations and location options.
- Languages.
- Audience targeting mode.
- AI Max, URL expansion, and brand search settings.
- Keywords and match types.
- Responsive search ad fields and assets.
- Final URL, display path, and UTM/url suffix.
- Budget type and budget amount.
- Initial negatives and conflicts.

## Conversion Goals And Summary

Known locations:

- The objective page can show conversion goal rows under the selected objective.
- The bidding page can optimize for `转化次数`.
- The conversion goal rows may use account-default goals.

Operator guidance:

- Ask for conversion action names/status when the visible page does not show them.
- Do not invent conversion action names such as `purchase_success` or `signup_success`; use only user-provided or visible action names.
- Treat page views, interactions, CTA clicks, navigation clicks, and signup-intent events as diagnostic unless the user explicitly accepts weak-signal learning.
- Use true business outcomes as primary conversions when available, such as registration success, purchase/subscription success, qualified lead, or deployment/project creation when it represents activation.
- Warning counts such as `1 项操作` or `2 项操作` need inspection before relying on them.
