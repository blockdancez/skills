#!/usr/bin/env python3
"""
Capture a project profile folder from a landing page URL using Firecrawl.
"""

import argparse
import json
import mimetypes
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

FIRECRAWL_SCRAPE_URL = "https://api.firecrawl.dev/v2/scrape"
# Optional local shortcut. If you intentionally want the key in this script,
# replace the empty string with your Firecrawl key, e.g. "fc-...".
HARDCODED_FIRECRAWL_API_KEY = "fc-d1698603cd514d51bcdef6eac881f559"
DEFAULT_FORMATS: List[Any] = [
    "markdown",
    "summary",
    "branding",
    "product",
    {"type": "screenshot", "fullPage": False},
]


def normalize_url(url: str) -> str:
    value = url.strip()
    if not value:
        raise ValueError("URL is required")
    if "://" not in value:
        value = f"https://{value}"
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")
    return value


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return re.sub(r"-{2,}", "-", slug)


def first_text(values: Iterable[Any]) -> Optional[str]:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def domain_from_url(url: str) -> str:
    parsed = urlparse(normalize_url(url))
    host = parsed.netloc.split("@")[-1].split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host or "project"


def project_name(data: Dict[str, Any], source_url: str) -> str:
    product = data.get("product") if isinstance(data.get("product"), dict) else {}
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return first_text(
        [
            product.get("title"),
            metadata.get("title"),
            metadata.get("ogSiteName"),
            domain_from_url(source_url),
        ]
    ) or "Project"


def project_slug(data: Dict[str, Any], source_url: str) -> str:
    product = data.get("product") if isinstance(data.get("product"), dict) else {}
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    for candidate in [
        product.get("title"),
        metadata.get("title"),
        metadata.get("ogSiteName"),
        domain_from_url(source_url),
    ]:
        if isinstance(candidate, str):
            slug = slugify(candidate)
            if slug:
                return slug
    return "project"


def logo_url(data: Dict[str, Any]) -> Optional[str]:
    branding = data.get("branding") if isinstance(data.get("branding"), dict) else {}
    images = branding.get("images") if isinstance(branding.get("images"), dict) else {}
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return first_text(
        [
            branding.get("logo"),
            images.get("logo"),
            images.get("favicon"),
            metadata.get("favicon"),
            metadata.get("ogImage"),
            metadata.get("og:image"),
        ]
    )


def screenshot_url(data: Dict[str, Any]) -> Optional[str]:
    screenshot = data.get("screenshot")
    if isinstance(screenshot, str) and screenshot.strip():
        return screenshot.strip()
    actions = data.get("actions") if isinstance(data.get("actions"), dict) else {}
    screenshots = actions.get("screenshots")
    if isinstance(screenshots, list):
        return first_text(screenshots)
    return None


def resolved_url(data: Dict[str, Any], source_url: str) -> str:
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    return first_text([metadata.get("sourceURL"), metadata.get("ogUrl"), source_url]) or source_url


def http_json_post(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout_seconds: int) -> Tuple[int, str, bytes]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return response.status, response.headers.get("content-type", ""), response.read()
    except HTTPError as exc:
        return exc.code, exc.headers.get("content-type", ""), exc.read()
    except URLError as exc:
        raise RuntimeError(f"HTTP request failed: {exc.reason}") from exc


def http_get_bytes(url: str, timeout_seconds: int) -> Tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": "project-profile-capture/1.0"})
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return response.read(), response.headers.get("content-type", "")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:300]
        raise RuntimeError(f"Asset download failed: HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Asset download failed: {exc.reason}") from exc


def call_firecrawl(url: str, api_key: Optional[str], timeout_seconds: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "project-profile-capture/1.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    status_code, _content_type, body = http_json_post(
        FIRECRAWL_SCRAPE_URL,
        headers=headers,
        payload={
            "url": url,
            "formats": DEFAULT_FORMATS,
            "timeout": timeout_seconds * 1000,
        },
        timeout_seconds=timeout_seconds + 10,
    )

    try:
        raw = json.loads(body.decode("utf-8"))
    except ValueError as exc:
        raise RuntimeError(f"Firecrawl returned non-JSON response: HTTP {status_code}") from exc

    if not isinstance(raw, dict):
        raise RuntimeError(f"Firecrawl returned unexpected JSON response: HTTP {status_code}")

    if status_code >= 400:
        message = raw.get("error") or raw.get("message") or body.decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Firecrawl request failed: HTTP {status_code}: {message}")

    if raw.get("success") is False:
        message = raw.get("error") or raw.get("message") or "unknown Firecrawl error"
        raise RuntimeError(f"Firecrawl request failed: {message}")

    data = raw.get("data", raw)
    if not isinstance(data, dict):
        raise RuntimeError("Firecrawl response did not contain a data object")
    return raw, data


def resolve_api_key(cli_api_key: Optional[str]) -> Optional[str]:
    return first_text([cli_api_key, HARDCODED_FIRECRAWL_API_KEY, os.environ.get("FIRECRAWL_API_KEY")])


def extension_from_response(url: str, content_type: str, default_extension: str) -> str:
    clean_content_type = content_type.split(";", 1)[0].strip().lower()
    guessed = mimetypes.guess_extension(clean_content_type) if clean_content_type else None
    if guessed == ".jpe":
        guessed = ".jpg"
    if guessed:
        return guessed

    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix and re.fullmatch(r"\.[a-z0-9]{1,8}", suffix):
        return suffix
    return default_extension


def download_asset(url: Optional[str], output_dir: Path, stem: str, default_extension: str) -> Optional[Path]:
    if not url:
        return None
    content, content_type = http_get_bytes(url, timeout_seconds=60)
    extension = extension_from_response(url, content_type, default_extension)
    path = output_dir / f"{stem}{extension}"
    path.write_bytes(content)
    return path


def unique_warnings(warnings: Iterable[str]) -> List[str]:
    result = []
    seen = set()
    for warning in warnings:
        if warning and warning not in seen:
            result.append(warning)
            seen.add(warning)
    return result


def markdown_excerpt(markdown: Any, limit: int = 2400) -> str:
    if not isinstance(markdown, str) or not markdown.strip():
        return "_No markdown content returned._"
    text = markdown.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n\n..."


def format_price(price: Any) -> str:
    if not isinstance(price, dict):
        return "n/a"
    formatted = first_text([price.get("formatted")])
    if formatted:
        return formatted
    parts = [str(item) for item in [price.get("amount"), price.get("currency")] if item is not None and str(item).strip()]
    return " ".join(parts) if parts else "n/a"


def format_availability(availability: Dict[str, Any]) -> str:
    text = availability.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()
    if "inStock" in availability:
        return str(availability["inStock"])
    return "n/a"


def format_product(product: Any) -> str:
    if not isinstance(product, dict) or not product:
        return "_No product data returned._"

    lines = [
        f"- Title: {product.get('title') or 'n/a'}",
        f"- Brand: {product.get('brand') or 'n/a'}",
        f"- Category: {product.get('category') or 'n/a'}",
        f"- URL: {product.get('url') or 'n/a'}",
        f"- Description: {product.get('description') or 'n/a'}",
    ]
    variants = product.get("variants")
    if isinstance(variants, list) and variants:
        lines.append("")
        lines.append("### Variants")
        for index, variant in enumerate(variants, start=1):
            if not isinstance(variant, dict):
                continue
            availability = variant.get("availability") if isinstance(variant.get("availability"), dict) else {}
            sale = variant.get("sale") if isinstance(variant.get("sale"), dict) else {}
            original_price = sale.get("originalPrice") if isinstance(sale.get("originalPrice"), dict) else None
            images = variant.get("images")
            image_urls = []
            if isinstance(images, list):
                image_urls = [image.get("url") for image in images if isinstance(image, dict) and image.get("url")]
            lines.extend(
                [
                    f"- Variant {index}: {variant.get('title') or variant.get('sku') or variant.get('id') or 'n/a'}",
                    f"  - Price: {format_price(variant.get('price'))}",
                    f"  - Original price: {format_price(original_price)}",
                    f"  - Availability: {format_availability(availability)}",
                    f"  - Images: {', '.join(image_urls) if image_urls else 'n/a'}",
                ]
            )
    return "\n".join(lines)


def build_profile_markdown(record: Dict[str, Any], markdown: Any) -> str:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    assets = record.get("assets") if isinstance(record.get("assets"), dict) else {}
    warnings = record.get("warnings") if isinstance(record.get("warnings"), list) else []

    return "\n".join(
        [
            f"# {record['project_name']}",
            "",
            "## Overview",
            "",
            f"- Source URL: {record['source_url']}",
            f"- Resolved URL: {record['resolved_url']}",
            f"- Captured at: {record['captured_at']}",
            f"- Logo URL: {assets.get('logo_url') or 'n/a'}",
            f"- Local logo: {assets.get('logo_path') or 'n/a'}",
            f"- Screenshot URL: {assets.get('screenshot_url') or 'n/a'}",
            f"- Local screenshot: {assets.get('screenshot_path') or 'n/a'}",
            "",
            "## Summary",
            "",
            str(record.get("summary") or "No summary returned."),
            "",
            "## Page Metadata",
            "",
            f"- Title: {metadata.get('title') or 'n/a'}",
            f"- Description: {metadata.get('description') or 'n/a'}",
            f"- OG title: {metadata.get('ogTitle') or 'n/a'}",
            f"- OG description: {metadata.get('ogDescription') or 'n/a'}",
            f"- OG site name: {metadata.get('ogSiteName') or 'n/a'}",
            "",
            "## Product",
            "",
            format_product(record.get("product")),
            "",
            "## Markdown Excerpt",
            "",
            markdown_excerpt(markdown),
            "",
            "## Warnings",
            "",
            "\n".join(f"- {warning}" for warning in warnings) if warnings else "- None",
            "",
        ]
    )


def write_outputs(
    data: Dict[str, Any],
    source_url: str,
    output_dir: Path,
    raw_response: Dict[str, Any],
    logo_path: Optional[Path],
    screenshot_path: Optional[Path],
    warnings: Iterable[str],
) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_warnings = list(warnings)
    if not data.get("product"):
        all_warnings.append("Product data was not returned by Firecrawl.")

    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    record = {
        "source_url": source_url,
        "resolved_url": resolved_url(data, source_url),
        "project_name": project_name(data, source_url),
        "project_slug": project_slug(data, source_url),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "summary": data.get("summary"),
        "metadata": metadata,
        "branding": data.get("branding"),
        "product": data.get("product"),
        "assets": {
            "logo_url": logo_url(data),
            "logo_path": str(logo_path) if logo_path else None,
            "screenshot_url": screenshot_url(data),
            "screenshot_path": str(screenshot_path) if screenshot_path else None,
        },
        "warnings": unique_warnings(all_warnings),
    }

    (output_dir / "raw-firecrawl.json").write_text(
        json.dumps(raw_response, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "metadata.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "profile.md").write_text(
        build_profile_markdown(record, data.get("markdown")),
        encoding="utf-8",
    )
    return record


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture a project profile from a URL with Firecrawl.")
    parser.add_argument("url", help="Project landing page or product URL")
    parser.add_argument("--project-root", default=".", help="Project root for default <project-slug>/ output")
    parser.add_argument("--output-dir", help="Exact output directory. Overrides --project-root/<project-slug>")
    parser.add_argument("--api-key", help="Firecrawl API key. Overrides the script key and FIRECRAWL_API_KEY")
    parser.add_argument("--overwrite", action="store_true", help="Allow writing into an existing non-empty output directory")
    parser.add_argument("--timeout", type=int, default=120, help="Firecrawl request timeout in seconds")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    source_url = normalize_url(args.url)
    api_key = resolve_api_key(args.api_key)
    warnings: List[str] = []
    if not api_key:
        warnings.append("FIRECRAWL_API_KEY was not set; request used unauthenticated Firecrawl access.")

    raw_response, data = call_firecrawl(source_url, api_key=api_key, timeout_seconds=args.timeout)
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else (
        Path(args.project_root).expanduser().resolve() / project_slug(data, source_url)
    )
    if output_dir.exists() and any(output_dir.iterdir()) and not args.overwrite:
        raise SystemExit(f"Output directory already exists and is not empty: {output_dir}. Use --overwrite.")
    output_dir.mkdir(parents=True, exist_ok=True)

    local_logo_path = None
    local_screenshot_path = None
    try:
        local_logo_path = download_asset(logo_url(data), output_dir, "logo", ".png")
    except Exception as exc:  # pragma: no cover - depends on remote asset hosts
        warnings.append(f"Logo download failed: {exc}")
    try:
        local_screenshot_path = download_asset(screenshot_url(data), output_dir, "screenshot", ".png")
    except Exception as exc:  # pragma: no cover - depends on signed screenshot URL
        warnings.append(f"Screenshot download failed: {exc}")

    record = write_outputs(
        data=data,
        source_url=source_url,
        output_dir=output_dir,
        raw_response=raw_response,
        logo_path=local_logo_path,
        screenshot_path=local_screenshot_path,
        warnings=warnings,
    )
    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "profile_path": str(output_dir / "profile.md"),
                "metadata_path": str(output_dir / "metadata.json"),
                "raw_firecrawl_path": str(output_dir / "raw-firecrawl.json"),
                **record,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def cli(argv: Optional[List[str]] = None) -> int:
    try:
        return main(argv)
    except (RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(cli())
