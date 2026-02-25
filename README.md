# Toddler Timeline Planner

A personalised 12-month action plan for toddler parents. Enter your toddler's age and today's date, hit Go, and get a month-by-month timeline across 8 categories: sleep, feeding, clothing, health, development, travel, childcare, and safety.

UK-focused (NHS schedule, UK seasons).

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Then open [http://localhost:5001](http://localhost:5001) in your browser.

## Usage

1. Set the current date (defaults to today)
2. Enter your toddler's age in months (e.g. 14)
3. Click **Go**

You'll get a scrollable timeline with expandable action cards grouped by category. Each card has:
- A headline (what to do)
- Big picture context (why it matters)
- Concrete weekly steps (how to do it)

Bookmarkable URLs: `http://localhost:5001/timeline?current_date=2026-02-25&age_months=14`

## Running Tests

```bash
pip install -r requirements.txt
python -m pytest test_timeline.py -v
```

## Project Structure

```
main.py            # FastHTML app (routes, UI rendering, CSS)
actions.py         # Action dataclass + 40 curated actions across 8 swim lanes
timeline.py        # Timeline computation engine (buckets, matching, grouping)
test_timeline.py   # 40 tests (data model, engine, action data, routes)
requirements.txt   # python-fasthtml, pytest
PRD.md             # Product requirements document
```
