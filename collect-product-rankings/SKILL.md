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

`url` means the product's original website/source URL, not the ranking site's detail page. For example, use `https://intrip.me/` instead of `https://aitoolhunt.co/item/intripme`, and use `https://anyfrm.com` instead of a Product Hunt product page.

`category` means the collected product/site type, not the source website type and not necessarily the source site's raw tag. Use normalized coarse labels such as:

- `SAAS`
- `TOOL`
- `AI`
- `CMS`
- `DEV`
- `API`
- `SEO`
- `MARKETING`
- `DESIGN`
- `CONTENT`
- `PRODUCTIVITY`
- `SECURITY`
- `WEB`

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
- Product Hunt `Visit website` links via the `r.jina.ai` markdown view when Cloudflare blocks direct product-page scraping
- DevHunt Supabase RPC
- Peerlist public JSON response captured during page load
- Playwright-rendered DOM extraction for the remaining sites
- Detail-page JSON-LD and `Visit Website` links to replace ranking-site detail URLs with original product URLs

## Verification

After running the script, you must inspect all generated data before reporting completion. In particular, verify that every `url` is the product's original website/source URL rather than a ranking-site listing or detail URL. If any item does not meet the output contract, keep processing and correcting the data until all items comply.

1. Confirm `aitoolhunt.co.json` exists.
2. Validate JSON parsing and exact fields:

```bash
python3 - <<'PY'
import json, glob
for path in sorted(glob.glob('*.json')):
    data = json.load(open(path, encoding='utf-8'))
    bad = [i for i, item in enumerate(data) if set(item) != {'title', 'url', 'description', 'category'}]
    print(path, len(data), 'bad_fields=', bad[:3])
PY
```

3. Check every URL against its source site's host. If a URL still points to the ranking site, open the listing/detail page, follow visit/website/launch links or rendered external anchors, replace it with the original source URL, and rerun validation.
4. Check every `category` against the normalized labels in this document. If any category is missing, too raw, or outside the allowed labels, normalize it and rerun validation.
5. Do not stop at spot checks. Continue this validate-and-fix loop until all files parse, all items have exactly the required fields, all categories are normalized, and all resolvable product URLs point to source websites.
6. Example URL checks: `AnyFrame` should resolve to `anyfrm.com`; `InTrip.Me` should resolve to `intrip.me`.

## Maintenance Notes

These websites change often. If counts drop unexpectedly or descriptions look wrong:

- Prefer public feeds/RPC/API responses over HTML scraping.
- Use Playwright network logs to find JSON endpoints before adding brittle selectors.
- Keep output schema stable even when a source site changes.
- Treat listing-site URLs as temporary detail URLs only; replace them with source URLs whenever the detail page exposes an external website link or JSON-LD `sameAs`.
- Keep source-specific categories out of `category`; normalize to product/site type labels.
