"""Spoon – your toddler's 12-month game plan."""
from datetime import date

from fasthtml.common import (
    fast_app, serve,
    Html, Head, Body, Title, Meta, Style,
    Div, H1, H2, H3, P, Form, Input, Label, Button, Details, Summary, Ul, Li,
    Section, Header, Span, A, NotStr,
)

from actions import ALL_ACTIONS, VALID_SWIM_LANES
from timeline import build_timeline, group_by_swim_lane

app, rt = fast_app()

# ── Pixel mascot: elephant with a spoon for a nose ──────────────────────────

_MASCOT_ROWS = [
    "....########....",
    "...##########...",
    "..############..",
    "#.############.#",
    "#.##ew####we##.#",
    "#.############.#",
    "..############..",
    "...##########...",
    ".....######.....",
    "......####......",
    ".......##.......",
    ".......##.......",
    ".......ss.......",
    "......ssss......",
    ".....ssssss.....",
    "......ssss......",
]

_MASCOT_PAL = {'#': '#7b93a1', 'w': '#ffffff', 'e': '#2d3436', 's': '#e6a817'}


def _mascot_svg(px=3):
    w = max(len(r) for r in _MASCOT_ROWS) * px
    h = len(_MASCOT_ROWS) * px
    rects = []
    for ry, row in enumerate(_MASCOT_ROWS):
        for rx, ch in enumerate(row):
            if ch in _MASCOT_PAL:
                rects.append(
                    f'<rect x="{rx*px}" y="{ry*px}" '
                    f'width="{px}" height="{px}" fill="{_MASCOT_PAL[ch]}"/>'
                )
    return (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
        f'class="mascot" role="img" aria-label="Spoon mascot: pixel elephant '
        f'with spoon nose">{"".join(rects)}</svg>'
    )


MASCOT_SVG = _mascot_svg()

# ── Swim-lane styling ────────────────────────────────────────────────────────

SWIM_LANE_COLOURS = {
    "sleep":       ("#5c6bc0", "#edeef8"),
    "feeding":     ("#d4930d", "#fdf6e3"),
    "clothing":    ("#c2477c", "#faf0f4"),
    "health":      ("#c94040", "#fdf0f0"),
    "development": ("#2e8b6e", "#eef7f3"),
    "travel":      ("#3078c6", "#eff5fc"),
    "childcare":   ("#7e57c2", "#f4f1fa"),
    "safety":      ("#d4700d", "#fdf4eb"),
}

SWIM_LANE_LABELS = {
    "sleep": "Sleep",
    "feeding": "Feeding & Nutrition",
    "clothing": "Clothing & Gear",
    "health": "Health & Medical",
    "development": "Development",
    "travel": "Travel & Holidays",
    "childcare": "Childcare & Social",
    "safety": "Safety",
}

PRIORITY_ICONS = {
    "essential": "!",
    "recommended": "~",
    "nice_to_have": "?",
}

# ── Rendering helpers ────────────────────────────────────────────────────────


def render_action_card(action):
    fg, bg = SWIM_LANE_COLOURS[action.swim_lane]
    priority_label = PRIORITY_ICONS.get(action.priority, "")
    steps_list = Ul(*[Li(s) for s in action.steps], cls="action-steps")
    return Details(
        Summary(
            Span(priority_label, cls="priority-icon") if priority_label else "",
            action.title,
            cls="action-title",
        ),
        P(action.big_picture, cls="action-big-picture"),
        steps_list,
        cls="action-card",
        style=f"border-left: 3px solid {fg}; background: {bg};",
    )


def render_month_column(bucket):
    grouped = group_by_swim_lane(bucket["actions"])
    lane_sections = []
    for lane in VALID_SWIM_LANES:
        actions = grouped.get(lane, [])
        if not actions:
            continue
        fg, _ = SWIM_LANE_COLOURS[lane]
        lane_sections.append(
            Div(
                Span(SWIM_LANE_LABELS[lane], cls="lane-tag", style=f"background:{fg};"),
                *[render_action_card(a) for a in actions],
                cls="lane-group",
            )
        )
    return Div(
        H3(
            bucket["label"],
            Span(f" ({bucket['age_months']}mo)", cls="age-badge"),
            cls="month-header",
        ),
        *lane_sections if lane_sections else [P("No actions this month", cls="empty-month")],
        cls="month-column",
    )


def render_timeline(buckets):
    return Div(
        *[render_month_column(b) for b in buckets],
        cls="timeline-grid",
    )


def page_shell(*content):
    return Html(
        Head(
            Title("Spoon"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Style(CSS),
        ),
        Body(
            Header(
                Div(
                    NotStr(MASCOT_SVG),
                    Div(
                        Span("Spoon", cls="brand-name"),
                        P("Your toddler's 12-month game plan", cls="brand-tagline"),
                        cls="brand-text",
                    ),
                    cls="top-bar-inner",
                ),
                cls="top-bar",
            ),
            Div(*content, cls="main-content"),
        ),
    )


def render_form(current_date=None, age_months=None):
    today = current_date or date.today().isoformat()
    age = age_months or ""
    return Form(
        Div(
            Div(
                Label("Current date", _for="current_date"),
                Input(type="date", name="current_date", id="current_date", value=today, required=True),
                cls="form-field",
            ),
            Div(
                Label("Toddler age (months)", _for="age_months"),
                Input(type="number", name="age_months", id="age_months", min="12", max="36",
                      value=str(age), placeholder="e.g. 14", required=True),
                cls="form-field",
            ),
            Div(
                Button("Go", type="submit", cls="go-btn"),
                cls="form-field",
            ),
            cls="form-row",
        ),
        method="post",
        action="/timeline",
        cls="input-form",
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@rt("/")
def get():
    return page_shell(render_form())


@rt("/timeline")
def post(current_date: str, age_months: int):
    d = date.fromisoformat(current_date)
    buckets = build_timeline(d, age_months, ALL_ACTIONS)
    return page_shell(
        render_form(current_date, age_months),
        Section(
            H2(f"Your 12-month plan (starting age {age_months} months)"),
            render_timeline(buckets),
            cls="timeline-section",
        ),
    )


@rt("/timeline")
def get(current_date: str = "", age_months: int = 0):
    if not current_date or not age_months:
        return page_shell(render_form())
    d = date.fromisoformat(current_date)
    buckets = build_timeline(d, age_months, ALL_ACTIONS)
    return page_shell(
        render_form(current_date, age_months),
        Section(
            H2(f"Your 12-month plan (starting age {age_months} months)"),
            render_timeline(buckets),
            cls="timeline-section",
        ),
    )


# ── Stylesheet (Basecamp-inspired) ──────────────────────────────────────────

CSS = """
/* ── Reset & base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Helvetica, Arial, sans-serif;
    background: #f1efe9;
    color: #1a1a1a;
    line-height: 1.5;
}

/* ── Top bar ──────────────────────────────────────────────────────────────── */
.top-bar {
    background: #fff;
    border-bottom: 3px solid #e6a817;
    padding: 0.65rem 1.25rem;
}
.top-bar-inner {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.mascot {
    width: 48px;
    height: auto;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    flex-shrink: 0;
}
.brand-text { display: flex; flex-direction: column; }
.brand-name {
    font-size: 1.35rem;
    font-weight: 800;
    color: #1a1a1a;
    letter-spacing: -0.03em;
    line-height: 1.2;
}
.brand-tagline {
    font-size: 0.8rem;
    color: #6b6b6b;
    line-height: 1.3;
}

/* ── Main content ─────────────────────────────────────────────────────────── */
.main-content {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* ── Form card ────────────────────────────────────────────────────────────── */
.input-form {
    margin: 1.5rem 0;
    background: #fff;
    padding: 1.25rem;
    border: 1px solid #d5d3ca;
    border-radius: 4px;
}
.form-row {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    flex-wrap: wrap;
}
.form-field { display: flex; flex-direction: column; gap: 0.3rem; }
.form-field label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.form-field input {
    padding: 0.45rem 0.65rem;
    border: 1px solid #ccc8bc;
    border-radius: 3px;
    font-size: 0.95rem;
    background: #fff;
}
.form-field input:focus {
    outline: none;
    border-color: #4a90d9;
    box-shadow: 0 0 0 2px rgba(74, 144, 217, 0.15);
}
.go-btn {
    padding: 0.5rem 2rem;
    background: #1d6ce0;
    color: #fff;
    border: none;
    border-radius: 3px;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s;
}
.go-btn:hover { background: #1557b8; }
.go-btn:active { background: #0e4a9a; }

/* ── Timeline section ─────────────────────────────────────────────────────── */
.timeline-section {
    margin: 1.5rem 0 2.5rem;
}
.timeline-section h2 {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #1a1a1a;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e6a817;
}
.timeline-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* ── Month cards ──────────────────────────────────────────────────────────── */
.month-column {
    background: #fff;
    border: 1px solid #d5d3ca;
    border-radius: 4px;
    padding: 1rem 1.25rem;
}
.month-header {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #e8e6df;
    color: #1a1a1a;
}
.age-badge {
    font-size: 0.78rem;
    font-weight: 400;
    color: #888;
}
.empty-month { color: #999; font-style: italic; font-size: 0.85rem; }

/* ── Swim-lane groups ─────────────────────────────────────────────────────── */
.lane-group { margin-bottom: 0.75rem; }
.lane-tag {
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 3px;
    color: #fff;
    font-size: 0.7rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── Action cards ─────────────────────────────────────────────────────────── */
.action-card {
    border-radius: 3px;
    padding: 0.6rem 0.85rem;
    margin: 0.35rem 0;
    cursor: pointer;
}
.action-card[open] { padding-bottom: 0.85rem; }
.action-title {
    font-weight: 600;
    font-size: 0.9rem;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    color: #1a1a1a;
}
.action-title::-webkit-details-marker { display: none; }
.action-title::before {
    content: "\u25b8";
    font-size: 0.75rem;
    color: #888;
    transition: transform 0.15s;
}
.action-card[open] .action-title::before { transform: rotate(90deg); }
.priority-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.1rem;
    height: 1.1rem;
    border-radius: 3px;
    font-size: 0.65rem;
    font-weight: 800;
    background: #c94040;
    color: #fff;
    flex-shrink: 0;
}
.action-big-picture {
    margin: 0.4rem 0;
    font-size: 0.85rem;
    color: #555;
    line-height: 1.6;
}
.action-steps {
    margin: 0.4rem 0 0 1.25rem;
    font-size: 0.82rem;
    color: #555;
}
.action-steps li { margin-bottom: 0.25rem; }

/* ── Mobile ───────────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .form-row { flex-direction: column; }
    .brand-name { font-size: 1.2rem; }
    .month-column { padding: 0.75rem 1rem; }
    .mascot { width: 40px; }
}

/* ── Print ────────────────────────────────────────────────────────────────── */
@media print {
    .input-form, .go-btn { display: none; }
    .action-card { break-inside: avoid; }
    .action-card[open] .action-big-picture,
    .action-card[open] .action-steps { display: block; }
    body { padding: 0; background: #fff; }
    .top-bar { border-bottom-color: #ccc; }
    .month-column { border-color: #ddd; }
}
"""


if __name__ == "__main__":
    import os
    serve(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
