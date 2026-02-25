# Toddler Timeline Planner - PRD

## Context

New parents face an overwhelming amount of things to track, prepare for, and act on as their toddler grows. Information is scattered across blogs, books, and NHS pages. This app gives you a single, personalised 12-month action timeline based on your toddler's current age and today's date - combining developmental milestones, seasonal prep, health appointments, and day-to-day transitions into one scannable view.

---

## Product Overview

**One-liner:** Enter your toddler's age and today's date, hit Go, and get a month-by-month action plan for the next year across every category that matters.

**Target user:** First-time parent of a toddler (12-30 months).

### Inputs
| Field | Type | Default |
|-------|------|---------|
| Current date | Date picker | Today |
| Toddler age | Months (number) | — |
| Sex | Male / Female | — |
| Go button | — | — |

### Output
A 12-month scrollable timeline (current month + 11 ahead) with actions organised into **swim lanes** (categories). Each action card shows:
- **What** to do (short title)
- **Why** it matters (1-2 sentence description)
- **When** - the month it falls in (derived from toddler's age-at-that-month and/or calendar season)

---

## Swim Lanes (Categories)

### 1. Sleep
Actions triggered by **toddler age**:
- **14-18 months:** Watch for signs of 2-to-1 nap transition (refusing morning nap, late afternoon meltdowns). Start pushing morning nap later by 15 min every few days.
- **15-18 months:** Complete the transition to one midday nap (12:30-2:30pm typical).
- **18-24 months:** Potential sleep regression around 18 months (separation anxiety, teething molars). Stick to routine.
- **24+ months:** Consider toddler bed transition if climbing out of cot. No rush - cot is safer.

### 2. Feeding & Nutrition
- **14-15 months:** If still on bottles, plan the transition to open cup / straw cup. Drop daytime bottles first.
- **15-16 months:** Drop the bedtime bottle (replace with milk in cup before teeth-brushing).
- **16-18 months:** Expect peak fussiness / food refusal. Keep offering variety without pressure.
- **18-24 months:** Introduce cutlery skills (fork first). Expect mess.
- **24-26 months:** Most toddlers can self-feed reasonably well. Portions roughly 1/4 of adult size.

### 3. Clothing & Gear
Actions triggered by **calendar season + age**:
- **Spring (Mar-May):** Lightweight layers, puddle suit, wellies for outdoor play. Sun hat.
- **Summer (Jun-Aug):** UV swimsuit, swim nappy, sun cream (SPF 50), sun hat with neck flap. Lightweight sleeping bag / summer grobag (0.5-1 tog).
- **Autumn (Sep-Nov):** Transition to warmer sleeping bag (2.5 tog). Waterproof jacket. Check shoe size (feet grow fast at this age - measure every 6-8 weeks).
- **Winter (Dec-Feb):** Snowsuit / pramsuit if needed. Warm sleeping bag. Avoid loose blankets in cot.
- **Ongoing:** Size up every 2-3 months. Buy one size ahead for next season in sales.

### 4. Health & Medical
- **12-13 months (may already be done):** MMR vaccine + Hib/MenC booster + pneumococcal booster (NHS schedule).
- **15 months:** Check developmental review with health visitor.
- **18 months:** Register with NHS dentist if not already. First dental check-up.
- **2 years (24 months):** Schedule 2-year developmental review with health visitor (integrated review).
- **Ongoing:** Teething - canines and molars come through 16-24 months. Stock up on Calpol/Nurofen.

### 5. Development & Milestones
- **14-16 months:** Walking confidently (if not already). First words emerging. Pointing at things they want.
- **16-18 months:** Word explosion begins. Expect 10-50 words. Loves posting/stacking/emptying games.
- **18-20 months:** Follows simple instructions ("get your shoes"). Starting to show frustration / tantrums as communication lags behind understanding.
- **20-24 months:** Two-word combinations ("more milk"). Pretend play emerges. Can kick a ball.
- **24-26 months:** Sentences forming. Knows some colours. Can jump with both feet.

### 6. Travel & Holidays
- **3-4 months before summer trip (Mar-Apr):** Book flights/accommodation for a beach holiday. Check passport validity (apply/renew via HMPO - takes 4-6 weeks currently). Research child-friendly beach destination.
- **2 months before (May):** Buy travel car seat or check airline car seat policy. Get UV pop-up tent for beach. Travel blackout blind (e.g. Gro Anywhere Blind) for hotel room. Swim nappies.
- **1 month before (Jun):** Pack list - travel pharmacy (Calpol, Nurofen, plasters, thermometer, Piriton), snacks, tablet loaded with CBeebies downloads, sticker books, favourite comforter. EHIC/GHIC card check.
- **Trip month (Jul-Aug):** Stick to routine as much as possible (nap time, bedtime). Allow extra time for everything. Reapply sun cream every 2 hours.

### 7. Childcare & Social
- **Any time:** If starting nursery, begin settling-in sessions 2-4 weeks before start date.
- **14-18 months:** Toddler groups / music classes - good for socialisation and routine.
- **18-24 months:** Parallel play is normal (playing alongside, not with, other children). Don't worry about sharing yet.
- **24+ months:** Consider pre-school / increased nursery hours if desired.

### 8. Safety & Childproofing
- **14-16 months (walking):** Re-check all childproofing at toddler height. Stair gates, corner guards, socket covers, cupboard locks. Anchor furniture to walls (bookcase, TV).
- **18-20 months (climbing):** They will climb everything. Remove chairs from near countertops/windows. Window locks essential.
- **20-24 months:** Can reach higher surfaces now. Move medicines, cleaning products, sharp objects higher. Toilet lock if exploring bathrooms.
- **24+ months:** Can open doors. Door handle covers or chains for exterior doors.

---

## Technical Approach

### Stack
- **FastHTML** (Python) - single-file app using the FastHTML framework
- Python for all logic: timeline computation, trigger evaluation, HTML rendering
- Data stored as Python dataclass/dict structures in-module
- Deployed as a standard Python web app (`python main.py`)

### Data Model (Python)

```python
@dataclass
class Action:
    id: str
    swim_lane: str        # "sleep" | "feeding" | "clothing" | "health" | "development" | "travel" | "childcare" | "safety"
    title: str            # Alert-style headline: "Time to start the 2-to-1 nap transition"
    big_picture: str      # Why this matters, what to expect (2-3 sentences)
    steps: list[str]      # Ordered concrete weekly actions: ["Week 1: Push morning nap 15 mins later...", ...]
    trigger_type: str     # "age" | "season" | "relative_to_date"
    age_months: tuple[int, int] | None  # e.g. (15, 18) = show when toddler is 15-18 months
    seasons: list[str] | None           # e.g. ["summer"]
    priority: str         # "essential" | "recommended" | "nice_to_have"
```

### Timeline Computation
1. User enters current date + toddler age in months.
2. Generate 12 monthly buckets: `[currentMonth, currentMonth+1, ..., currentMonth+11]`.
3. For each bucket, compute the toddler's age in that month.
4. For each action, evaluate its trigger against the bucket's (age, season) and assign it to matching month(s).
5. Render swim lanes as horizontal rows, months as columns.

### UI Layout
- **Header:** Date picker, age input, Go button.
- **Timeline grid:**
  - X-axis = months (scrollable horizontally if needed)
  - Y-axis = swim lanes (colour-coded rows)
  - Cards placed in the appropriate cell(s)
- **Mobile:** Collapse to vertical month-by-month list with swim lane tags on each card.
- Colour scheme per swim lane for visual scanning.

---

## Implementation Plan

### Phase 1: Data & Core Logic
1. Set up `main.py` with FastHTML app scaffold and dependencies (`requirements.txt`).
2. Define the `Action` dataclass and populate ~40-60 actions across 8 swim lanes as a Python list.
3. Build the timeline computation engine: given (current_date, age_months) → 12 monthly buckets, each with matched actions.

### Phase 2: UI
4. Build the FastHTML routes: `GET /` renders the input form, `POST /timeline` computes and renders the timeline.
5. Style the swim lanes with distinct colours using inline CSS / `<style>` block. Horizontal grid layout (months = columns, swim lanes = rows).
6. Action cards show title + expandable description on click (use HTMX or `<details>` element for simplicity).

### Phase 3: Polish
7. Mobile responsive layout - collapse to vertical month-by-month list with swim lane colour tags.
8. Print-friendly stylesheet.
9. Add a "share" feature: permalink with query params (`?date=2026-02-25&age=14`) so the URL is bookmarkable.

---

## Verification
- Run `python main.py`, open in browser.
- Set date to Feb 2026, age to 14 months, click Go.
- Confirm: "2-to-1 nap transition" appears in Sleep lane around months 1-4.
- Confirm: Summer clothing/swim gear appears in Jun-Aug columns.
- Confirm: Travel prep cards appear 3-4 months before summer.
- Confirm: 2-year developmental review appears in Dec 2026 / Jan 2027 (when child is ~24-25 months).
- Resize to mobile width - confirm vertical layout works.
- Confirm bookmarkable URL works: `/?date=2026-02-25&age=14`.

---

## Future Vision: iPhone App

The web app is the v1 proving ground for the data and logic. The long-term product is a **native iPhone app** with:

- **Push notification alerts** triggered at the right time: *"Your little one is 15 months - it's time to start thinking about moving to one nap a day."*
- **Drill-down flow**: Alert → Big picture overview of the transition → Concrete steps for this week → Follow-up steps for next week.
- The data model is designed with this in mind from day one (each action has a summary, detail, and weekly steps).

### Implications for v1 data model
Each action needs more than just a title and description. Structure it as:
- **Title**: Short alert-style headline (*"Time to start the 2-to-1 nap transition"*)
- **Big picture**: Why this matters, what to expect, how long it takes (2-3 sentences)
- **Steps**: Ordered list of concrete weekly actions (*"Week 1: Push morning nap 15 mins later each day..."*)

The web v1 renders all of this in expandable cards. The future iPhone app uses the same data to power notifications + drill-down screens.

---

## Decisions Made
- **UK-based**: NHS schedule, UK seasons, HMPO passport, EHIC/GHIC.
- **Fixed curated list** for v1 - no user editing of actions.
- **Generic beach holiday** assumed for travel swim lane.
- **FastHTML (Python)** for the tech stack.
