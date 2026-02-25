"""Toddler Timeline Planner - FastHTML app."""
from datetime import date

from fasthtml.common import (
    fast_app, serve,
    Html, Head, Body, Title, Meta, Style,
    Div, H1, H2, H3, P, Form, Input, Label, Button, Details, Summary, Ul, Li,
    Section, Header, Span, A,
)

from actions import ALL_ACTIONS, VALID_SWIM_LANES
from timeline import build_timeline, group_by_swim_lane

app, rt = fast_app()

SWIM_LANE_COLOURS = {
    "sleep":       ("#6366f1", "#eef2ff"),  # indigo
    "feeding":     ("#f59e0b", "#fffbeb"),  # amber
    "clothing":    ("#ec4899", "#fdf2f8"),  # pink
    "health":      ("#ef4444", "#fef2f2"),  # red
    "development": ("#10b981", "#ecfdf5"),  # emerald
    "travel":      ("#3b82f6", "#eff6ff"),  # blue
    "childcare":   ("#8b5cf6", "#f5f3ff"),  # violet
    "safety":      ("#f97316", "#fff7ed"),  # orange
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
        style=f"border-left: 4px solid {fg}; background: {bg};",
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
    today = date.today().isoformat()
    return Html(
        Head(
            Title("Toddler Timeline Planner"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Style(CSS),
        ),
        Body(
            Header(
                H1("Toddler Timeline Planner"),
                P("Enter your toddler's age and today's date to get a personalised 12-month action plan.",
                  cls="subtitle"),
                cls="page-header",
            ),
            *content,
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


CSS = """
/* ── Reset & base ─────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f8fafc;
    color: #1e293b;
    line-height: 1.5;
    padding: 0 1rem;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
.page-header {
    max-width: 900px;
    margin: 2rem auto 1rem;
    text-align: center;
}
.page-header h1 { font-size: 1.8rem; color: #0f172a; }
.subtitle { color: #64748b; margin-top: 0.25rem; }

/* ── Form ─────────────────────────────────────────────────────────────────── */
.input-form {
    max-width: 900px;
    margin: 1rem auto;
    background: #fff;
    padding: 1.25rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.form-row {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
    flex-wrap: wrap;
}
.form-field { display: flex; flex-direction: column; gap: 0.25rem; }
.form-field label { font-size: 0.85rem; font-weight: 600; color: #475569; }
.form-field input {
    padding: 0.5rem 0.75rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    font-size: 0.95rem;
}
.go-btn {
    padding: 0.5rem 2rem;
    background: #6366f1;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
}
.go-btn:hover { background: #4f46e5; }

/* ── Timeline ─────────────────────────────────────────────────────────────── */
.timeline-section {
    max-width: 900px;
    margin: 2rem auto;
}
.timeline-section h2 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
    color: #0f172a;
}
.timeline-grid {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
.month-column {
    background: #fff;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.month-header {
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e2e8f0;
    color: #0f172a;
}
.age-badge {
    font-size: 0.8rem;
    font-weight: 400;
    color: #64748b;
}
.empty-month { color: #94a3b8; font-style: italic; font-size: 0.9rem; }

/* ── Swim lane groups ─────────────────────────────────────────────────────── */
.lane-group { margin-bottom: 0.75rem; }
.lane-tag {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    color: #fff;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

/* ── Action cards ─────────────────────────────────────────────────────────── */
.action-card {
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    cursor: pointer;
}
.action-card[open] { padding-bottom: 1rem; }
.action-title {
    font-weight: 600;
    font-size: 0.95rem;
    list-style: none;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.action-title::-webkit-details-marker { display: none; }
.action-title::before {
    content: "▸";
    font-size: 0.8rem;
    color: #64748b;
    transition: transform 0.15s;
}
.action-card[open] .action-title::before {
    transform: rotate(90deg);
}
.priority-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 1.2rem;
    height: 1.2rem;
    border-radius: 50%;
    font-size: 0.7rem;
    font-weight: 700;
    background: #ef4444;
    color: #fff;
    flex-shrink: 0;
}
.action-big-picture {
    margin: 0.5rem 0;
    font-size: 0.9rem;
    color: #475569;
    line-height: 1.6;
}
.action-steps {
    margin: 0.5rem 0 0 1.25rem;
    font-size: 0.85rem;
    color: #475569;
}
.action-steps li { margin-bottom: 0.3rem; }

/* ── Mobile ───────────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
    .form-row { flex-direction: column; }
    .page-header h1 { font-size: 1.4rem; }
    .month-column { padding: 1rem; }
}

/* ── Print ────────────────────────────────────────────────────────────────── */
@media print {
    .input-form, .go-btn { display: none; }
    .action-card { break-inside: avoid; }
    .action-card[open] .action-big-picture,
    .action-card[open] .action-steps { display: block; }
    body { padding: 0; }
    .month-column { box-shadow: none; border: 1px solid #e2e8f0; }
}
"""


if __name__ == "__main__":
    serve()
