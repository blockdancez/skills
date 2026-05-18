#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import argparse
from pathlib import Path

ROOT = Path.cwd()


DEVHUNT_SUPABASE_URL = "https://xpdhqqwgprlqmqaqmnyx.supabase.co"
DEVHUNT_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhwZGhxcXdncHJscW1xYXFtbnl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQ4NTg0ODcsImV4cCI6MjAwMDQzNDQ4N30."
    "fwN6a_NzygrFxhj0GCxGnJJpHv8q8iNEjY1jvhL8Kv0"
)


def curl(url: str, *, method: str = "GET", data: dict | None = None, headers: dict | None = None) -> str:
    command = ["curl", "-L", "--max-time", "30", "-s"]
    if method != "GET":
        command.extend(["-X", method])
    for key, value in (headers or {}).items():
        command.extend(["-H", f"{key}: {value}"])
    if data is not None:
        command.extend(["--data", json.dumps(data)])
    command.append(url)
    return subprocess.check_output(command, text=True)


def write_json(output_dir: Path, name: str, rows: list[dict[str, str]]) -> None:
    normalized = []
    url_to_index = {}
    seen = set()
    for row in rows:
        item = {
            "title": clean_text(row.get("title", "")),
            "url": row.get("url", "").strip(),
            "description": clean_text(row.get("description", "")),
            "category": classify_site_type(row),
        }
        if not item["title"] or not item["url"]:
            continue
        existing_index = url_to_index.get(item["url"])
        should_merge_by_url = existing_index is not None and (
            len(item["title"]) > 100 or len(normalized[existing_index]["title"]) > 100
        )
        if should_merge_by_url:
            current = normalized[existing_index]
            if len(item["title"]) < len(current["title"]) and len(item["title"]) <= 80:
                current["title"] = item["title"]
            if len(item["description"]) > len(current["description"]):
                current["description"] = item["description"]
            if current["category"] == "TOOL/WEB" and item["category"] != "TOOL/WEB":
                current["category"] = item["category"]
            continue
        key = (item["title"].lower(), item["url"])
        if key in seen:
            current = normalized[url_to_index[item["url"]]]
            if len(item["title"]) < len(current["title"]) and len(item["title"]) <= 80:
                current["title"] = item["title"]
            if len(item["description"]) > len(current["description"]):
                current["description"] = item["description"]
            continue
        seen.add(key)
        url_to_index.setdefault(item["url"], len(normalized))
        normalized.append(item)
        if len(item["title"]) <= 100:
            url_to_index[item["url"]] = len(normalized) - 1
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def classify_site_type(row: dict[str, str]) -> str:
    text = " ".join(
        clean_text(row.get(key, ""))
        for key in ("title", "description", "category", "url")
    ).lower()

    rules = [
        ("TOOL/CMS", ["wordpress", "cms", "content management", "blog publisher"]),
        ("TOOL/API", [" api", "sdk", "graphql", "webhook", "endpoint", "inference", "rpc"]),
        ("TOOL/DEV", ["developer", "code", "coding", "github", "repository", "ci/cd", "devops", "boilerplate", "terminal", "shadcn", "component", "schema", "database", "debug", "localhost"]),
        ("TOOL/SEO", ["seo", "rank", "google", "indexed", "keyword", "serp", "llm visibility"]),
        ("TOOL/MARKETING", ["marketing", "sales", "lead", "campaign", "linkedin", "crm", "outreach", "ads", "advertising"]),
        ("TOOL/CONTENT", ["content", "writing", "blog", "newsletter", "copy", "caption", "transcript", "document", "pdf", "summarizer"]),
        ("TOOL/DESIGN", ["design", "image", "video", "photo", "thumbnail", "avatar", "ui", "color", "3d", "slideshow", "animation"]),
        ("TOOL/FINANCE", ["finance", "financial", "expense", "stock", "trading", "crypto", "payment", "revenue", "subscription", "billing"]),
        ("TOOL/PRODUCTIVITY", ["productivity", "workflow", "automation", "schedule", "calendar", "task", "note", "workspace", "assistant"]),
        ("TOOL/SECURITY", ["security", "privacy", "guardrail", "compliance", "identity", "scanner"]),
        ("TOOL/AI", [" ai", "chatbot", "agent", "llm", "gpt", "claude", "gemini", "prompt", "model"]),
        ("APP/MOBILE", ["android", "ios", "mobile app", "app store"]),
        ("PLATFORM/MARKETPLACE", ["marketplace", "directory", "community", "platform", "launchpad"]),
        ("HARDWARE", ["hardware", "device", "m5stack"]),
        ("GAME", ["game", "gaming", "bingo"]),
        ("EDUCATION", ["education", "course", "learning", "study", "interview practice"]),
        ("SAAS", ["saas", "software", "dashboard", "management", "portal", "platform"]),
    ]
    for category, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return category
    return "TOOL/WEB"


def clean_text(value: str) -> str:
    return " ".join(html.unescape(str(value or "")).replace("\xa0", " ").split())


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or title.lower()


def split_lines(text: str) -> list[str]:
    return [clean_text(line) for line in text.splitlines() if clean_text(line)]


def product_hunt(date_value: dt.date) -> list[dict[str, str]]:
    body = curl("https://www.producthunt.com/feed")
    root = ET.fromstring(body)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    rows = []
    local_date = date_value
    previous_date = date_value - dt.timedelta(days=1)
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", default="", namespaces=ns)
        link = entry.find("atom:link", ns)
        content = entry.findtext("atom:content", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        updated = entry.findtext("atom:updated", default="", namespaces=ns)
        # Product Hunt resets on Pacific time; the feed may still show the previous
        # Pacific date for today's launch batch depending on where the agent runs.
        if not (
            published.startswith(local_date.isoformat())
            or updated.startswith(local_date.isoformat())
            or published.startswith(previous_date.isoformat())
            or updated.startswith(previous_date.isoformat())
        ):
            continue
        description = re.sub("<[^>]+>", " ", content).split("Discussion")[0]
        rows.append(
            {
                "title": title,
                "url": link.attrib.get("href", "") if link is not None else "",
                "description": description,
                "category": "Product Hunt today",
            }
        )
    return rows


def devhunt(date_value: dt.date) -> list[dict[str, str]]:
    headers = {
        "apikey": DEVHUNT_ANON_KEY,
        "Authorization": f"Bearer {DEVHUNT_ANON_KEY}",
        "Content-Type": "application/json",
    }
    week = int(
        curl(
            f"{DEVHUNT_SUPABASE_URL}/rest/v1/rpc/get_week_number",
            method="POST",
            headers=headers,
            data={"date_in": f"{date_value.isoformat()}T12:00:00.000Z", "start_day": 2},
        )
    )
    weeks = json.loads(
        curl(
            f"{DEVHUNT_SUPABASE_URL}/rest/v1/rpc/get_prev_launch_weeks",
            method="POST",
            headers=headers,
            data={"_year": date_value.year, "_start_day": 2, "_launch_week": week, "_limit": 1},
        )
    )
    rows = []
    for item in (weeks[0].get("products") if weeks else []) or []:
        product = item.get("product") or {}
        categories = " / ".join(c.get("name", "") for c in item.get("product_categories") or [])
        rows.append(
            {
                "title": product.get("name", ""),
                "url": product.get("demo_url")
                or product.get("github_url")
                or f"https://devhunt.org/tool/{product.get('slug', '')}",
                "description": product.get("slogan", ""),
                "category": categories or "Dev tool",
            }
        )
    return rows


def page_candidates(page, url: str, href_pattern: str) -> list[dict[str, str]]:
    page.goto(url, wait_until="domcontentloaded", timeout=45_000)
    page.wait_for_timeout(4_000)
    for _ in range(4):
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(700)
    return page.evaluate(
        """
        (pattern) => Array.from(document.querySelectorAll('a[href]'))
          .filter((a) => a.href.includes(pattern) && (a.innerText || '').trim())
          .map((a) => {
            let node = a;
            let context = a.innerText || '';
            for (let i = 0; i < 6 && node.parentElement; i++) {
              node = node.parentElement;
              const text = node.innerText || '';
              if (text.length > context.length && text.length < 1400) context = text;
            }
            return { href: a.href, text: a.innerText || '', context };
          })
        """,
        href_pattern,
    )


def parse_contextual(candidates: list[dict[str, str]], site: str, limit: int | None = None) -> list[dict[str, str]]:
    rows = []
    for candidate in candidates:
        href = candidate["href"].split("#")[0]
        lines = split_lines(candidate.get("context") or candidate.get("text") or "")
        link_lines = split_lines(candidate.get("text") or "")
        if not lines:
            continue

        title = link_lines[0] if link_lines else lines[0]
        if title.lower().startswith("more about "):
            title = title[11:]
        description = ""
        category = ""

        if site == "startupfame" and re.match(r"[A-Z][a-z]+ \\d{1,2}, 2026", lines[0]):
            title = lines[1] if len(lines) > 1 else title
            description = lines[2] if len(lines) > 2 else ""
            category = "Today"
        elif site == "theresanaiforthat":
            if "Featured" in title or re.fullmatch(r"[\d,]+( \| \d+.*)?", title):
                continue
            description = next((line for line in lines[1:] if not line.startswith("Free ") and not line.startswith("Released ")), "")
            category = next((line for line in lines[1:] if line and line not in {description} and not line.startswith("Released ")), "AI tool")
        elif site == "aitoolhunt":
            title = link_lines[0] if link_lines else lines[0]
            skipped = {
                "productivity",
                "artificial intelligence",
                "tech",
                "development",
                "games",
                "saas",
                "security",
                "developer tools",
                "task management",
                "marketing",
            }
            description = next(
                (
                    line
                    for line in lines[1:]
                    if len(line) > 35 and line.lower() not in skipped and line != title
                ),
                next((line for line in lines[1:] if line.lower() not in skipped and line != title), ""),
            )
            category = " / ".join(line for line in lines[1:] if line.lower() in skipped) or "AI tool"
        elif site in {"futurepedia", "toolify", "topaitools"}:
            title = link_lines[0] if link_lines else lines[0]
            if title.startswith("#") or title in {"Rated 0 out of 5", "Rated 5 out of 5"}:
                continue
            description = next((line for line in lines[1:] if not line.startswith("#") and "Rated " not in line), "")
            tags = [line.lstrip("#") for line in lines if line.startswith("#")]
            category = " / ".join(tags[:4]) or next((line for line in lines[1:] if line != description), "")
        elif site == "uneed":
            title = link_lines[0] if link_lines else lines[0]
            if title.startswith("#"):
                continue
            noise = {
                "free",
                "paid",
                "freemium",
                "premium",
                "deals",
                "live",
                "today",
            }
            description = next(
                (
                    line
                    for line in lines[1:]
                    if not line.startswith("#")
                    and not re.fullmatch(r"#?\d+", line)
                    and not re.fullmatch(r"\(\d+\)", line)
                    and line.lower() not in noise
                ),
                "",
            )
            tags = [line.strip("#•") for line in lines if line.startswith("#") and not re.fullmatch(r"#\d+", line)]
            category = " / ".join(tags[:5]) or "Daily"
        else:
            description = next(
                (
                    line
                    for line in lines[1:]
                    if not line.startswith("#")
                    and not re.fullmatch(r"#?\d+", line)
                    and line.lower() not in {"free", "paid", "freemium", "premium", "deals", "live"}
                ),
                "",
            )
            tags = [line.strip("#•") for line in lines if line.startswith("#") and not re.fullmatch(r"#\d+", line)]
            category = " / ".join(tags[:5]) or "Today"

        rows.append({"title": title, "url": href, "description": description, "category": category})
        if limit and len(rows) >= limit:
            break
    return rows


def betalist(page) -> list[dict[str, str]]:
    page.goto("https://betalist.com", wait_until="domcontentloaded", timeout=45_000)
    page.wait_for_timeout(4_000)
    text = page.locator("body").inner_text()
    lines = split_lines(text)
    try:
        start = next(i for i, line in enumerate(lines) if line.startswith("Today "))
    except StopIteration:
        return []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("Yesterday")), len(lines))
    rows = []
    chunk = lines[start + 1 : end]
    ignored = {"🔥", "Stay ahead of the curve", "Receive a daily digest of the newest startups."}
    i = 0
    while i + 1 < len(chunk):
        title = chunk[i]
        description = chunk[i + 1]
        if title in ignored or description in ignored or title.lower() in {"sign up", "submit startup"}:
            i += 1
            continue
        rows.append(
            {
                "title": title,
                "url": f"https://betalist.com/startups/{slugify(title)}",
                "description": description,
                "category": "Today",
            }
        )
        i += 2
    return rows


def peerlist(page, date_value: dt.date) -> list[dict[str, str]]:
    peerlist_week = int(date_value.strftime("%V"))
    peerlist_year = int(date_value.strftime("%G"))
    with page.expect_response(
        lambda response: "/api/v1/users/projects/spotlight" in response.url
        and f"year={peerlist_year}" in response.url
        and f"week={peerlist_week}" in response.url,
        timeout=30_000,
    ) as response_info:
        page.goto("https://peerlist.io/launchpad", wait_until="domcontentloaded", timeout=45_000)
    response = response_info.value
    data = response.json()
    payload = data.get("data") if isinstance(data, dict) else data
    items = payload.get("spotlight") if isinstance(payload, dict) else payload
    rows = []
    for item in items or []:
        project = item.get("project") or item
        slug = project.get("slug") or project.get("projectSlug") or slugify(project.get("name", ""))
        rows.append(
            {
                "title": project.get("name") or project.get("title", ""),
                "url": f"https://peerlist.io/projects/{slug}",
                "description": project.get("tagline") or project.get("description", ""),
                "category": project.get("category", {}).get("name") if isinstance(project.get("category"), dict) else f"Launchpad Week {peerlist_week}",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect current product ranking/listing sites into per-site JSON files.")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="Date to collect, in YYYY-MM-DD format.")
    parser.add_argument("--output-dir", default=".", help="Directory where JSON files will be written.")
    args = parser.parse_args()

    date_value = dt.date.fromisoformat(args.date)
    output_dir = Path(args.output_dir).resolve()

    write_json(output_dir, "producthunt", product_hunt(date_value))
    write_json(output_dir, "devhunt", devhunt(date_value))

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as error:
        raise SystemExit("Playwright is required for browser-rendered sources. Install it with: python3 -m pip install playwright && python3 -m playwright install chromium") from error

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
            )
        )
        page.set_default_timeout(12_000)

        write_json(output_dir, "betalist", betalist(page))
        write_json(output_dir, "peerlist", peerlist(page, date_value))

        site_specs = [
            ("uneed", "https://uneed.best", "/tool/", "uneed", None),
            ("microlaunch", "https://microlaunch.net", "/p/", "microlaunch", None),
            ("fazier", "https://fazier.com", "/launches/", "fazier", 43),
            ("startupfa.me", "https://startupfa.me", "/s/", "startupfame", None),
            ("theresanaiforthat", "https://theresanaiforthat.com", "/ai/", "theresanaiforthat", 40),
            ("futurepedia", "https://www.futurepedia.io", "/tool/", "futurepedia", 20),
            ("toolify", "https://www.toolify.ai", "/tool/", "toolify", 30),
            ("aitoolhunt.co", "https://aitoolhunt.co", "/item/", "aitoolhunt", 30),
            ("topai.tools", "https://topai.tools", "/t/", "topaitools", 40),
        ]
        for filename, url, pattern, site, limit in site_specs:
            candidates = page_candidates(page, url, pattern)
            write_json(output_dir, filename, parse_contextual(candidates, site, limit))

        browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
