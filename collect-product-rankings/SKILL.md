---
name: collect-product-rankings
description: Use when collecting today's products from Product Hunt, BetaList, Uneed, DevHunt, Microlaunch, Peerlist Launchpad, Fazier, Startup Fame, There Is An AI For That, Futurepedia, Toolify, AIToolHunt, or TopAI.tools into per-site JSON files.
metadata:
  short-description: Collect product-ranking sites into JSON
---

# Collect Product Rankings

Use this skill when the user asks to gather current/today's products from product launch boards, startup directories, developer-tool boards, or AI-tool directories and write one JSON file per source site.

## Output Contract

Each output file is named after the source site, for example:

- `producthunt.json`
- `devhunt.json`
- `aitoolhunt.co.json`
- `topai.tools.json`

Each file contains a JSON array. Every item must have exactly these fields:

```json
{
  "title": "",
  "url": "",
  "description": "",
  "category": ""
}
```

`category` means the collected product/site type, not the source website type and not necessarily the source site's raw tag. Use normalized coarse labels such as:

- `SAAS`
- `TOOL/AI`
- `TOOL/CMS`
- `TOOL/DEV`
- `TOOL/API`
- `TOOL/SEO`
- `TOOL/MARKETING`
- `TOOL/DESIGN`
- `TOOL/CONTENT`
- `TOOL/PRODUCTIVITY`
- `TOOL/SECURITY`
- `TOOL/WEB`

## Supported Sources

The bundled script supports:

- `https://www.producthunt.com`
- `https://betalist.com`
- `https://uneed.best`
- `https://devhunt.org`
- `https://microlaunch.net`
- `https://peerlist.io/projects`
- `https://fazier.com`
- `https://startupfa.me`
- `https://theresanaiforthat.com`
- `https://www.futurepedia.io`
- `https://www.toolify.ai`
- `https://aitoolhunt.co`
- `https://topai.tools`

Do not include `insanelycooltools.com`; it has no usable current ranking data in this workflow. If the user gives `aitoolhunt.com`, normalize it to `aitoolhunt.co`.

## Quick Start

Run from the user's target output directory:

```bash
python3 /path/to/collect-product-rankings/scripts/collect_product_rankings.py --date YYYY-MM-DD --output-dir .
```

If the user did not specify a date, use today's date.

Example from an installed skill:

```bash
python3 ~/.codex/skills/collect-product-rankings/scripts/collect_product_rankings.py --output-dir .
```

The script uses:

- Product Hunt Atom feed
- DevHunt Supabase RPC
- Peerlist public JSON response captured during page load
- Playwright-rendered DOM extraction for the remaining sites

## Verification

After running the script:

1. Confirm `aitoolhunt.co.json` exists.
2. Confirm `aitoolhunt.json` and `insanelycooltools.json` do not exist unless the user explicitly requested legacy files.
3. Validate JSON parsing and exact fields:

```bash
python3 - <<'PY'
import json, glob
for path in sorted(glob.glob('*.json')):
    data = json.load(open(path, encoding='utf-8'))
    bad = [i for i, item in enumerate(data) if set(item) != {'title', 'url', 'description', 'category'}]
    print(path, len(data), 'bad_fields=', bad[:3])
PY
```

4. Spot-check a few categories to make sure they describe the product/site type, e.g. `TOOL/CMS` for a WordPress publishing tool, `TOOL/DEV` for developer tooling, or `SAAS` for broad SaaS software.

## Maintenance Notes

These websites change often. If counts drop unexpectedly or descriptions look wrong:

- Prefer public feeds/RPC/API responses over HTML scraping.
- Use Playwright network logs to find JSON endpoints before adding brittle selectors.
- Keep output schema stable even when a source site changes.
- Keep source-specific categories out of `category`; normalize to product/site type labels.
