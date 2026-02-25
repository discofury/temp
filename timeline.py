"""Timeline computation engine for Spoon."""
from __future__ import annotations

import calendar
from collections import defaultdict
from datetime import date

from actions import Action


SEASON_MAP = {
    12: "winter", 1: "winter", 2: "winter",
    3: "spring", 4: "spring", 5: "spring",
    6: "summer", 7: "summer", 8: "summer",
    9: "autumn", 10: "autumn", 11: "autumn",
}


def month_to_season(month: int) -> str:
    return SEASON_MAP[month]


def generate_buckets(current_date: date, age_months: int) -> list[dict]:
    buckets = []
    year = current_date.year
    month = current_date.month

    for i in range(12):
        m = month + i
        y = year
        if m > 12:
            m -= 12
            y += 1
        label = f"{calendar.month_abbr[m]} {y}"
        buckets.append({
            "year": y,
            "month": m,
            "age_months": age_months + i,
            "season": month_to_season(m),
            "label": label,
        })
    return buckets


def action_matches_bucket(action: Action, bucket: dict) -> bool:
    if action.trigger_type == "age" and action.age_months is not None:
        lo, hi = action.age_months
        return lo <= bucket["age_months"] <= hi
    if action.trigger_type == "season" and action.seasons is not None:
        return bucket["season"] in action.seasons
    return False


def build_timeline(
    current_date: date,
    age_months: int,
    actions: list[Action],
) -> list[dict]:
    buckets = generate_buckets(current_date, age_months)
    for bucket in buckets:
        bucket["actions"] = [a for a in actions if action_matches_bucket(a, bucket)]
    return buckets


def group_by_swim_lane(actions: list[Action]) -> dict[str, list[Action]]:
    grouped: dict[str, list[Action]] = defaultdict(list)
    for a in actions:
        grouped[a.swim_lane].append(a)
    return dict(grouped)
