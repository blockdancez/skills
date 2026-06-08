#!/usr/bin/env python3
"""Analyze Google Ads Chinese/English CSV or TSV reports and produce triage actions."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class Options:
    target_cpa: float | None
    cost_threshold: float
    click_threshold: float
    top: int


@dataclass
class RowMetrics:
    label: str
    campaign: str
    ad_group: str
    status: str
    match_type: str
    clicks: float
    impressions: float
    cost: float
    conversions: float
    all_conversions: float

    @property
    def conversion_signal(self) -> float:
        return self.conversions or self.all_conversions

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0.0

    @property
    def cpc(self) -> float:
        return self.cost / self.clicks if self.clicks else 0.0

    @property
    def cpa(self) -> float:
        return self.cost / self.conversion_signal if self.conversion_signal else 0.0


STATUS_TRANSLATIONS = {
    "有效": "Eligible",
    "符合条件": "Eligible",
    "已暂停": "Paused",
    "已移除": "Removed",
    "不符合条件": "Not eligible",
    "受限": "Limited",
    "正在审核": "Under review",
    "已添加": "Added",
    "已排除": "Excluded",
}


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-16", "utf-8-sig", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def split_line(line: str) -> list[str]:
    delimiter = "\t" if "\t" in line else ","
    return next(csv.reader([line], delimiter=delimiter))


def find_header(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        cells = split_line(line)
        has_dimension = any(name in cells for name in ("关键字", "搜索字词", "Keyword", "Search term"))
        has_metric = any(name in cells for name in ("点击次数", "展示次数", "Clicks", "Impr."))
        if has_dimension and has_metric:
            return index
    raise ValueError("Could not find a Google Ads header row. Confirm this is a keyword or search-term report.")


def parse_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = read_text(path)
    lines = [line for line in text.splitlines() if line.strip()]
    header_index = find_header(lines)
    delimiter = "\t" if "\t" in lines[header_index] else ","
    reader = csv.DictReader(lines[header_index:], delimiter=delimiter)
    rows: list[dict[str, str]] = []
    for row in reader:
        if not row:
            continue
        values = [str(value or "") for value in row.values()]
        if any("总计" in value or "Total" in value for value in values):
            continue
        if all(not value.strip() for value in values):
            continue
        rows.append({str(key): str(value or "").strip() for key, value in row.items() if key is not None})
    return list(reader.fieldnames or []), rows


def to_float(value: str) -> float:
    if not value or value in {"--", "—", "-"}:
        return 0.0
    cleaned = value.replace(",", "").replace("US$", "").replace("$", "").replace("%", "").strip()
    cleaned = cleaned.replace("<", "")
    match = re.search(r"-?\d+(?:\.\d+)?", cleaned)
    return float(match.group(0)) if match else 0.0


def get(row: dict[str, str], names: Iterable[str]) -> str:
    for name in names:
        if name in row:
            return row[name]
    return ""


def metric(row: dict[str, str], names: Iterable[str]) -> float:
    return to_float(get(row, names))


def label(row: dict[str, str]) -> str:
    return get(row, ("关键字", "搜索字词", "Keyword", "Search term")) or "(unknown)"


def status(row: dict[str, str]) -> str:
    value = get(row, ("状态", "Status", "添加/排除", "Added/Excluded"))
    return STATUS_TRANSLATIONS.get(value, value)


def detect_report_type(fields: list[str]) -> str:
    if any(name in fields for name in ("搜索字词", "Search term")):
        return "search_term"
    return "keyword"


def row_metrics(row: dict[str, str]) -> RowMetrics:
    return RowMetrics(
        label=label(row),
        campaign=get(row, ("广告系列", "Campaign")),
        ad_group=get(row, ("广告组", "Ad group")),
        status=status(row),
        match_type=get(row, ("匹配类型", "Match type", "Keyword match type")),
        clicks=metric(row, ("点击次数", "Clicks")),
        impressions=metric(row, ("展示次数", "Impr.", "Impressions")),
        cost=metric(row, ("费用", "Cost")),
        conversions=metric(row, ("转化次数", "Conversions")),
        all_conversions=metric(row, ("所有转化次数", "All conv.")),
    )


def money(value: float) -> str:
    return f"${value:.2f}"


def percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def evidence(metrics: RowMetrics) -> str:
    parts = [
        f"clicks {metrics.clicks:.0f}",
        f"impr {metrics.impressions:.0f}",
        f"CTR {percent(metrics.ctr)}",
        f"cost {money(metrics.cost)}",
    ]
    if metrics.conversion_signal:
        parts.append(f"conv {metrics.conversion_signal:.2f}")
        parts.append(f"CPA {money(metrics.cpa)}")
    return "; ".join(parts)


def classify(metrics: RowMetrics, report_type: str, options: Options) -> tuple[str, str, str, int]:
    """Return action, paste-ready content, note, and sort priority."""
    if metrics.conversion_signal:
        if options.target_cpa and metrics.cpa > options.target_cpa * 1.5:
            action = "Keep; monitor CPA" if report_type == "keyword" else "Add exact cautiously"
            paste = f"[{metrics.label}]" if report_type == "search_term" else ""
            note = "Has conversions but CPA is far above target; verify intent, ad copy, and landing page before pausing."
            return action, paste, note, 10
        if report_type == "search_term":
            return "Add exact", f"[{metrics.label}]", "Search term has conversions; add only after product intent is confirmed and no negative conflict exists.", 5
        return "Keep", "", "Keyword has conversions; keep by default, then split or improve ad/landing relevance if needed.", 5

    enough_bad_sample = metrics.cost >= options.cost_threshold or metrics.clicks >= options.click_threshold
    if enough_bad_sample:
        if report_type == "search_term":
            return "Review then negative", f'"{metrics.label}"', "Spent or received clicks with no conversion; if intent is irrelevant, add a negative at ad group or campaign scope.", 20
        return "Review then pause", "", "Keyword has spend/clicks and no conversion; inspect underlying search-term intent before pausing.", 20

    if metrics.impressions >= 50 and metrics.clicks == 0:
        return "Observe or improve ad copy", "", "Has impressions but no clicks; check ad relevance, bidding, and keyword intent first.", 40

    if metrics.clicks > 0:
        return "Observe", "", "Has clicks but sample is too small; do not pause only because conversions are currently 0.", 30

    return "No action", "", "No clicks or spend; it is not consuming budget.", 90


def table_row(cells: Iterable[str]) -> str:
    return "| " + " | ".join(str(cell).replace("\n", " ").replace("|", "\\|") for cell in cells) + " |"


def summarize(path: Path, options: Options) -> str:
    fields, rows = parse_rows(path)
    report_type = detect_report_type(fields)
    metrics_rows = [row_metrics(row) for row in rows]
    clicks = sum(row.clicks for row in metrics_rows)
    impressions = sum(row.impressions for row in metrics_rows)
    cost = sum(row.cost for row in metrics_rows)
    conversions = sum(row.conversions for row in metrics_rows)
    all_conversions = sum(row.all_conversions for row in metrics_rows)
    conv_metric = conversions or all_conversions
    cpa = cost / conv_metric if conv_metric else 0.0

    converting = sorted(
        [row for row in metrics_rows if row.conversion_signal > 0],
        key=lambda row: (row.conversion_signal, -row.cost),
        reverse=True,
    )
    costly_zero = sorted(
        [
            row
            for row in metrics_rows
            if row.cost >= options.cost_threshold
            and row.conversions == 0
            and row.all_conversions == 0
        ],
        key=lambda row: row.cost,
        reverse=True,
    )
    no_cost = [row for row in metrics_rows if row.cost == 0 and row.clicks == 0]
    actions = []
    for row in metrics_rows:
        action, paste, note, priority = classify(row, report_type, options)
        if action != "No action":
            actions.append((priority, row.cost, row.clicks, action, row, paste, note))
    actions.sort(key=lambda item: (item[0], -item[1], -item[2]))

    lines: list[str] = []
    lines.append(f"## {path.name}")
    lines.append(f"- report type: {report_type}; rows: {len(rows)}; no-cost/no-click rows: {len(no_cost)}")
    if conv_metric:
        lines.append(
            f"- clicks: {clicks:.0f}; impressions: {impressions:.0f}; cost: ${cost:.2f}; "
            f"conversions: {conv_metric:.2f}; CPA: ${cpa:.2f}"
        )
    else:
        lines.append(f"- clicks: {clicks:.0f}; impressions: {impressions:.0f}; cost: ${cost:.2f}; conversions: 0")
    lines.append("")

    if converting:
        lines.append("### Converting rows")
        for row in converting[: options.top]:
            lines.append(
                f"- {row.label} | clicks {row.clicks:.0f} | cost {money(row.cost)} | "
                f"conv {row.conversion_signal:.2f} | CPA {money(row.cpa)} | {row.status}"
            )
        lines.append("")

    if costly_zero:
        lines.append("### Costly zero-conversion rows")
        for row in costly_zero[: options.top]:
            lines.append(f"- {row.label} | clicks {row.clicks:.0f} | cost {money(row.cost)} | {row.status}")
        lines.append("")

    if actions:
        lines.append("### Suggested action table")
        lines.append(table_row(["Object", "Ad group", "Action", "Evidence", "Paste-ready content", "Notes"]))
        lines.append(table_row(["---", "---", "---", "---", "---", "---"]))
        for _, _, _, action, row, paste, note in actions[: options.top]:
            lines.append(table_row([row.label, row.ad_group or "-", action, evidence(row), paste or "-", note]))
        lines.append("")

    add_exact = [paste for _, _, _, action, _, paste, _ in actions if action.startswith("Add exact") and paste]
    review_negatives = [paste for _, _, _, action, _, paste, _ in actions if action == "Review then negative" and paste]
    review_pauses = [row.label for _, _, _, action, row, _, _ in actions if action == "Review then pause"]

    if add_exact or review_negatives or review_pauses:
        lines.append("### Paste-ready draft blocks")
        if add_exact:
            lines.append("Exact keywords to add (review product intent first):")
            lines.extend(add_exact[: options.top])
            lines.append("")
        if review_negatives:
            lines.append("Candidate negatives (check conflicts with active keywords first):")
            lines.extend(review_negatives[: options.top])
            lines.append("")
        if review_pauses:
            lines.append("Candidate keywords to pause (open raw search terms and verify intent first):")
            lines.extend(f"- {item}" for item in review_pauses[: options.top])
            lines.append("")

    lines.append("### Safety notes")
    lines.append("- The script cannot fully judge business intent; verify raw search terms and landing-page promises before pausing, negating, expanding locations, or changing bids.")
    lines.append("- Terms with conversions but high CPA should be observed, split, or improved before being paused.")
    lines.append("- Zero-click/zero-cost keywords do not waste budget; do not pause them only because conversions are 0.")
    lines.append("")

    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Google Ads keyword/search-term reports and produce an initial action table.")
    parser.add_argument("files", nargs="+", help="Path(s) to Google Ads CSV/TSV reports")
    parser.add_argument("--target-cpa", type=float, default=None, help="Target CPA used to flag high-CPA converting terms")
    parser.add_argument("--cost-threshold", type=float, default=10.0, help="High-spend threshold for zero-conversion rows; default is 10 USD")
    parser.add_argument("--click-threshold", type=float, default=10.0, help="High-click threshold for zero-conversion rows; default is 10 clicks")
    parser.add_argument("--top", type=int, default=40, help="Maximum action rows to output per table")
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])
    options = Options(
        target_cpa=args.target_cpa,
        cost_threshold=args.cost_threshold,
        click_threshold=args.click_threshold,
        top=args.top,
    )
    outputs = []
    for arg in args.files:
        path = Path(arg).expanduser()
        try:
            outputs.append(summarize(path, options))
        except Exception as exc:  # noqa: BLE001
            outputs.append(f"## {path.name}\n- ERROR: {exc}\n")
    print("\n".join(outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
