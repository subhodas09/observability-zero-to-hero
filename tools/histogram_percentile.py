#!/usr/bin/env python3
"""Explain classic Prometheus histogram percentile interpolation step by step."""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from typing import Iterable


SAMPLE_RE = re.compile(
    r"^(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)"
    r"(?:\{(?P<labels>.*)\})?\s+"
    r"(?P<value>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[+-]?Inf|NaN)"
    r"(?:\s+\d+)?$"
)
LABEL_RE = re.compile(r'(\w+)="((?:\\.|[^"\\])*)"(?:,|$)')


@dataclass(frozen=True)
class Bucket:
    upper_bound: float
    cumulative_count: float


@dataclass(frozen=True)
class Estimate:
    percentile: float
    total: float
    target: float
    previous_bound: float
    previous_count: float
    current_bound: float
    current_count: float
    bucket_count: float
    position: float
    fraction: float
    width: float
    value: float
    infinite_bucket: bool = False


def parse_number(value: str, context: str) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"invalid {context}: {value!r}") from error
    if math.isnan(number):
        raise ValueError(f"{context} cannot be NaN")
    return number


def parse_percentiles(values: Iterable[str]) -> list[float]:
    parsed: list[float] = []
    for group in values:
        for raw_value in group.split(","):
            value = raw_value.strip().lower()
            if not value:
                raise ValueError("percentile list contains an empty value")
            if value.startswith("p"):
                value = value[1:]
            percentile = parse_number(value, "percentile")
            if percentile <= 0 or percentile > 100:
                raise ValueError("percentiles must be greater than 0 and at most 100")
            parsed.append(percentile)
    if not parsed:
        raise ValueError("provide at least one percentile")
    return parsed


def validate_buckets(buckets: list[Bucket]) -> list[Bucket]:
    if not buckets:
        raise ValueError("no histogram buckets were found")
    ordered = sorted(buckets, key=lambda bucket: bucket.upper_bound)
    previous_bound = -math.inf
    previous_count = 0.0
    for bucket in ordered:
        if bucket.upper_bound <= previous_bound:
            raise ValueError("bucket upper bounds must be strictly increasing")
        if not math.isfinite(bucket.cumulative_count):
            raise ValueError("cumulative bucket counts must be finite")
        if bucket.cumulative_count < 0:
            raise ValueError("cumulative bucket counts cannot be negative")
        if bucket.cumulative_count < previous_count:
            raise ValueError("cumulative bucket counts must not decrease")
        previous_bound = bucket.upper_bound
        previous_count = bucket.cumulative_count
    return ordered


def parse_direct_buckets(value: str) -> list[Bucket]:
    buckets: list[Bucket] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            raise ValueError("bucket list contains an empty item")
        if ":" not in item:
            raise ValueError(f"bucket {item!r} must use UPPER_BOUND:CUMULATIVE_COUNT")
        raw_bound, raw_count = item.split(":", 1)
        bound = parse_number(raw_bound.strip(), "bucket upper bound")
        count = parse_number(raw_count.strip(), "cumulative bucket count")
        buckets.append(Bucket(bound, count))
    return validate_buckets(buckets)


def unescape_label(value: str) -> str:
    return value.replace(r"\\", "\\").replace(r'\"', '"').replace(r"\n", "\n")


def parse_labels(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    labels: dict[str, str] = {}
    position = 0
    for match in LABEL_RE.finditer(value):
        if match.start() != position:
            raise ValueError(f"malformed Prometheus labels near {value[position:]!r}")
        labels[match.group(1)] = unescape_label(match.group(2))
        position = match.end()
    if position != len(value):
        raise ValueError(f"malformed Prometheus labels near {value[position:]!r}")
    return labels


def parse_label_filters(values: list[str]) -> dict[str, str]:
    filters: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"label filter {value!r} must use NAME=VALUE")
        name, label_value = value.split("=", 1)
        if not name or not label_value:
            raise ValueError(f"label filter {value!r} must use non-empty NAME=VALUE")
        filters[name] = label_value
    return filters


def labels_match(labels: dict[str, str], filters: dict[str, str]) -> bool:
    return all(labels.get(name) == value for name, value in filters.items())


def series_name(labels: dict[str, str]) -> str:
    if not labels:
        return "(no labels)"
    return ",".join(f"{name}={value}" for name, value in sorted(labels.items()))


def parse_prometheus(
    text: str, metric: str, filters: dict[str, str]
) -> tuple[list[Bucket], float, dict[str, str]]:
    base_metric = metric.removesuffix("_bucket").removesuffix("_count")
    grouped_buckets: dict[tuple[tuple[str, str], ...], list[Bucket]] = {}
    grouped_counts: dict[tuple[tuple[str, str], ...], float] = {}

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = SAMPLE_RE.match(line)
        if not match:
            continue
        name = match.group("name")
        if name not in {f"{base_metric}_bucket", f"{base_metric}_count"}:
            continue
        try:
            labels = parse_labels(match.group("labels"))
            sample_value = parse_number(match.group("value"), f"sample on line {line_number}")
        except ValueError as error:
            raise ValueError(f"line {line_number}: {error}") from error
        if not labels_match(labels, filters):
            continue

        if name.endswith("_bucket"):
            if "le" not in labels:
                raise ValueError(f"line {line_number}: histogram bucket has no le label")
            bound = parse_number(labels.pop("le"), f"le label on line {line_number}")
            key = tuple(sorted(labels.items()))
            grouped_buckets.setdefault(key, []).append(Bucket(bound, sample_value))
        else:
            key = tuple(sorted(labels.items()))
            grouped_counts[key] = sample_value

    candidates = [key for key, buckets in grouped_buckets.items() if buckets]
    if not candidates:
        rendered_filters = ", ".join(f"{k}={v}" for k, v in filters.items()) or "none"
        raise ValueError(
            f"no {base_metric}_bucket samples matched; label filters: {rendered_filters}"
        )
    if len(candidates) > 1:
        choices = "; ".join(series_name(dict(key)) for key in candidates)
        raise ValueError(
            "more than one histogram series matched. Add --label filters to select one: "
            + choices
        )

    key = candidates[0]
    buckets = validate_buckets(grouped_buckets[key])
    count = grouped_counts.get(key)
    infinite = next(
        (bucket.cumulative_count for bucket in buckets if math.isinf(bucket.upper_bound)),
        None,
    )
    total = count if count is not None else infinite
    if total is None:
        raise ValueError(
            f"matched buckets have neither a {base_metric}_count sample nor a +Inf bucket"
        )
    if not math.isfinite(total):
        raise ValueError("histogram count must be finite")
    if total < 0:
        raise ValueError("histogram count cannot be negative")
    if buckets[-1].cumulative_count > total:
        raise ValueError("a cumulative bucket count is greater than the histogram count")
    return buckets, total, dict(key)


def estimate_percentile(
    buckets: list[Bucket], percentile: float, total: float | None = None
) -> Estimate:
    buckets = validate_buckets(buckets)
    if total is None:
        total = buckets[-1].cumulative_count
    if total <= 0:
        raise ValueError("cannot estimate a percentile from an empty histogram")
    if total < buckets[-1].cumulative_count:
        raise ValueError("total observations cannot be less than a cumulative bucket count")

    target = total * percentile / 100.0
    previous_bound = 0.0 if buckets[0].upper_bound > 0 else buckets[0].upper_bound
    previous_count = 0.0

    for bucket in buckets:
        if bucket.cumulative_count < target:
            previous_bound = bucket.upper_bound
            previous_count = bucket.cumulative_count
            continue

        bucket_count = bucket.cumulative_count - previous_count
        if bucket_count <= 0:
            raise ValueError(
                f"p{percentile:g} lands in an empty bucket ending at {bucket.upper_bound:g}"
            )
        position = target - previous_count
        fraction = position / bucket_count
        if math.isinf(bucket.upper_bound):
            value = previous_bound
            width = math.inf
            infinite_bucket = True
        else:
            width = bucket.upper_bound - previous_bound
            value = previous_bound + fraction * width
            infinite_bucket = False
        return Estimate(
            percentile=percentile,
            total=total,
            target=target,
            previous_bound=previous_bound,
            previous_count=previous_count,
            current_bound=bucket.upper_bound,
            current_count=bucket.cumulative_count,
            bucket_count=bucket_count,
            position=position,
            fraction=fraction,
            width=width,
            value=value,
            infinite_bucket=infinite_bucket,
        )
    raise ValueError(
        f"p{percentile:g} target count {target:g} is beyond the supplied cumulative buckets"
    )


def format_number(value: float) -> str:
    if math.isinf(value):
        return "+Inf" if value > 0 else "-Inf"
    return f"{value:.6g}"


def print_estimate(estimate: Estimate) -> None:
    print(f"\np{estimate.percentile:g}")
    print(f"  total observations:           {format_number(estimate.total)}")
    print(
        "  target count:                 "
        f"{format_number(estimate.total)} × {format_number(estimate.percentile / 100)} "
        f"= {format_number(estimate.target)}"
    )
    print(
        "  previous bucket:              "
        f"le={format_number(estimate.previous_bound)}, "
        f"cumulative={format_number(estimate.previous_count)}"
    )
    print(
        "  current bucket:               "
        f"le={format_number(estimate.current_bound)}, "
        f"cumulative={format_number(estimate.current_count)}"
    )
    print(
        "  observations in this bucket:  "
        f"{format_number(estimate.current_count)} - "
        f"{format_number(estimate.previous_count)} = "
        f"{format_number(estimate.bucket_count)}"
    )
    print(
        "  position inside this bucket:  "
        f"{format_number(estimate.target)} - "
        f"{format_number(estimate.previous_count)} = "
        f"{format_number(estimate.position)}"
    )
    print(
        "  fraction through bucket:      "
        f"{format_number(estimate.position)} / {format_number(estimate.bucket_count)} "
        f"= {format_number(estimate.fraction)}"
    )
    print(f"  bucket width:                 {format_number(estimate.width)} seconds")
    if estimate.infinite_bucket:
        print(
            "  +Inf bucket rule:             use the previous finite upper bound; "
            "an infinite width cannot be interpolated"
        )
    print(
        "  estimated percentile:         "
        f"{format_number(estimate.value)} seconds"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Show the linear interpolation behind percentiles in a Prometheus "
            "classic histogram. Read exposition text from stdin with --metric, or "
            "supply cumulative buckets directly with --buckets."
        )
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--metric", help="classic histogram base metric name")
    source.add_argument(
        "--buckets",
        help='cumulative buckets such as "0.10:12,0.25:28,0.50:43,1.00:50"',
    )
    parser.add_argument(
        "--label",
        action="append",
        default=[],
        metavar="NAME=VALUE",
        help="label filter for --metric mode; repeat for multiple labels",
    )
    percentiles = parser.add_mutually_exclusive_group(required=True)
    percentiles.add_argument("--percentile", action="append", metavar="P")
    percentiles.add_argument(
        "--percentiles", action="append", metavar="P50,P95,..."
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        raw_percentiles = args.percentile or args.percentiles
        requested = parse_percentiles(raw_percentiles)
        if args.buckets is not None:
            if args.label:
                raise ValueError("--label can only be used with --metric")
            buckets = parse_direct_buckets(args.buckets)
            total = buckets[-1].cumulative_count
            print("Source: direct cumulative buckets")
        else:
            filters = parse_label_filters(args.label)
            buckets, total, matched_labels = parse_prometheus(
                sys.stdin.read(), args.metric, filters
            )
            print(f"Source: Prometheus classic histogram {args.metric}")
            print(f"Matched series: {series_name(matched_labels)}")

        print(
            "Buckets: "
            + ", ".join(
                f"{format_number(bucket.upper_bound)}:{format_number(bucket.cumulative_count)}"
                for bucket in buckets
            )
        )
        for percentile in requested:
            print_estimate(estimate_percentile(buckets, percentile, total))
        return 0
    except (BrokenPipeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
