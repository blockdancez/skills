---
name: website-ux-seo-analysis
description: Create a logged-in user-experience and SEO analysis report for any website URL supplied by the user. Use when asked to analyze a live website, SaaS product, web app, landing page, competitor site, or AI tool after hands-on browsing, especially when the user requests login-based feature testing, SEO/keyword analysis, competitor comparison, or a Markdown website analysis report saved locally.
---

# Website UX SEO Analysis

## Overview

Produce evidence-based website analysis reports from real browsing, not guesses. The target is always the website URL or domain supplied by the user; do not treat any prior analyzed site as fixed. Cover the logged-in product experience when required, avoid dangerous/payment actions, verify SEO facts from live pages, and include only keyword metrics with external data sources.

## Workflow

1. Confirm the target URL supplied in the current user request, required login state, output path/name, and any forbidden actions.
2. Use the browser requested by the user. Prefer Chrome when the task needs existing cookies, Google login, authenticated sessions, or profile-dependent pages.
3. Browse like a real user: public pages first, then login, then dashboard/workspace/core flows.
4. Avoid irreversible or high-risk actions unless explicitly requested:
   - Do not purchase, subscribe, upgrade, enter payment details, configure Stripe/checkout, delete projects, publish live content, change domains, invite users, or modify billing.
   - You may observe these entry points and record that they exist.
5. Capture factual evidence: visible UI text, URLs, page states, error messages, module names, metadata, robots, sitemap, headers, and source links.
6. Write the report in the user’s requested language and format, usually Markdown.
7. Save the report to the requested directory. If no filename is specified, use a concise snake_case filename derived from the domain.

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
- For every numeric keyword metric, record the source and query scope:
  - keyword
  - country/market
  - date checked
  - metric provider
  - monthly volume
  - CPC
  - paid competition or PPC competition
  - Organic keyword difficulty only when an external tool returns it
- Never invent or model global volume, country splits, or keyword difficulty.
- If a metric is unavailable, write “未获取到可验证外部数据” or equivalent in the user’s language.
- Do not convert PPC competition into Organic KD. Keep them separate.
- If only one country is retrieved, report only that country’s numbers and list other countries as unavailable.
- Strategy labels such as priority, intent, and recommended landing page may be based on judgment, but label them as strategic recommendations rather than external metrics.

## Report Structure

Use the structure the user requested. When unspecified, use:

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

## 三、结论与优先级建议
## 四、参考来源
```

## Quality Bar

Before finalizing:

- Verify the report file exists and inspect key sections.
- Search the report for leaked sensitive data such as email addresses, tokens, cookies, or Bearer strings.
- Search for unsupported keyword phrases such as “估算”, “model”, “KD估算”, “主要国家流量估算”, or any numeric keyword metric without a source.
- If a flow was blocked, state exactly what happened and how it affects confidence.
- Do not claim “all functions were fully tested” if payment, deletion, publishing, domain changes, or other unsafe actions were intentionally avoided.
