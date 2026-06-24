#!/usr/bin/env python3
"""Validate a backlink-publisher JSON queue."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


VALID_STATUSES = {
    "pending",
    "in_progress",
    "needs_user",
    "submitted",
    "skipped",
    "failed",
}

REQUIRED_ITEM_FIELDS = {
    "id",
    "platform_name",
    "url",
    "free",
    "status",
    "login_method",
    "notes",
    "last_attempt_at",
    "result_url",
    "error",
}

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    return type(value).__name__


def validate_item(item: Any, index: int) -> list[str]:
    label = f"items[{index}]"
    errors: list[str] = []

    if not isinstance(item, dict):
        return [f"{label} must be an object, got {type_name(item)}"]

    missing = sorted(REQUIRED_ITEM_FIELDS - item.keys())
    for field in missing:
        errors.append(f"{label}.{field} is required")

    item_id = item.get("id")
    if not isinstance(item_id, str) or not item_id:
        errors.append(f"{label}.id must be a non-empty string")
    elif not ID_RE.match(item_id):
        errors.append(f"{label}.id must be a lowercase slug")

    platform_name = item.get("platform_name")
    if not isinstance(platform_name, str) or not platform_name.strip():
        errors.append(f"{label}.platform_name must be a non-empty string")

    url = item.get("url")
    if not isinstance(url, str) or not is_http_url(url):
        errors.append(f"{label}.url must be an absolute http(s) URL")

    if not isinstance(item.get("free"), bool):
        errors.append(f"{label}.free must be a boolean")
    elif item.get("free") is not True:
        errors.append(f"{label}.free must be true for this queue")

    status = item.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"{label}.status must be one of {sorted(VALID_STATUSES)}")

    login_method = item.get("login_method")
    if not isinstance(login_method, str) or not login_method:
        errors.append(f"{label}.login_method must be a non-empty string")

    if not isinstance(item.get("notes"), str):
        errors.append(f"{label}.notes must be a string")

    last_attempt_at = item.get("last_attempt_at")
    if last_attempt_at is not None and not isinstance(last_attempt_at, str):
        errors.append(f"{label}.last_attempt_at must be null or a string")

    result_url = item.get("result_url")
    if result_url is not None and (not isinstance(result_url, str) or not is_http_url(result_url)):
        errors.append(f"{label}.result_url must be null or an absolute http(s) URL")

    error = item.get("error")
    if error is not None and not isinstance(error, str):
        errors.append(f"{label}.error must be null or a string")

    return errors


def validate_document(data: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return [f"root must be an object, got {type_name(data)}"]

    if data.get("version") != 1:
        errors.append("version must be 1")

    if data.get("default_login_method") != "google":
        errors.append('default_login_method must be "google"')

    if data.get("requires_logged_in_chrome") is not True:
        errors.append("requires_logged_in_chrome must be true")

    if data.get("submit_policy") != "auto_submit_free_listings":
        errors.append('submit_policy must be "auto_submit_free_listings"')

    items = data.get("items")
    if not isinstance(items, list):
        errors.append("items must be an array")
        return errors

    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for index, item in enumerate(items):
        errors.extend(validate_item(item, index))
        if isinstance(item, dict):
            item_id = item.get("id")
            url = item.get("url")
            if isinstance(item_id, str):
                if item_id in seen_ids:
                    errors.append(f"items[{index}].id duplicates {item_id}")
                seen_ids.add(item_id)
            if isinstance(url, str):
                if url in seen_urls:
                    errors.append(f"items[{index}].url duplicates {url}")
                seen_urls.add(url)

    return errors


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a backlink-publisher JSON queue.")
    parser.add_argument("path", help="Path to the backlink JSON queue")
    args = parser.parse_args(argv)

    path = Path(args.path)
    try:
        data = load_json(path)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 1

    errors = validate_document(data)
    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(data['items'])} backlink items validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
