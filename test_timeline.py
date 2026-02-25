"""RED/GREEN TDD tests for the Toddler Timeline Planner."""
from datetime import date
from collections import Counter
import pytest


# ── Data Model Tests ──────────────────────────────────────────────────────────

class TestActionDataclass:
    def test_create_age_triggered_action(self):
        from actions import Action
        a = Action(
            id="sleep-nap-transition",
            swim_lane="sleep",
            title="Time to start the 2-to-1 nap transition",
            big_picture="Most toddlers drop to one nap between 15-18 months.",
            steps=["Week 1: Push morning nap 15 mins later each day"],
            trigger_type="age",
            age_months=(15, 18),
            seasons=None,
            priority="essential",
        )
        assert a.id == "sleep-nap-transition"
        assert a.swim_lane == "sleep"
        assert a.trigger_type == "age"
        assert a.age_months == (15, 18)
        assert a.seasons is None
        assert a.priority == "essential"
        assert len(a.steps) == 1

    def test_create_season_triggered_action(self):
        from actions import Action
        a = Action(
            id="clothing-summer-gear",
            swim_lane="clothing",
            title="Get summer gear ready",
            big_picture="UV swimsuit, sun cream, lightweight sleeping bag.",
            steps=["Buy UV swimsuit", "Stock up on SPF 50 sun cream"],
            trigger_type="season",
            age_months=None,
            seasons=["summer"],
            priority="essential",
        )
        assert a.trigger_type == "season"
        assert a.seasons == ["summer"]
        assert a.age_months is None

    def test_action_swim_lane_must_be_valid(self):
        from actions import Action, VALID_SWIM_LANES
        assert "sleep" in VALID_SWIM_LANES
        assert "feeding" in VALID_SWIM_LANES
        assert "clothing" in VALID_SWIM_LANES
        assert "health" in VALID_SWIM_LANES
        assert "development" in VALID_SWIM_LANES
        assert "travel" in VALID_SWIM_LANES
        assert "childcare" in VALID_SWIM_LANES
        assert "safety" in VALID_SWIM_LANES
        assert len(VALID_SWIM_LANES) == 8


# ── Timeline Engine Tests ─────────────────────────────────────────────────────

class TestMonthlyBuckets:
    def test_generates_12_buckets(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 2, 25), age_months=14)
        assert len(buckets) == 12

    def test_first_bucket_is_current_month(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 2, 25), age_months=14)
        first = buckets[0]
        assert first["year"] == 2026
        assert first["month"] == 2
        assert first["age_months"] == 14

    def test_age_increments_each_month(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 2, 25), age_months=14)
        ages = [b["age_months"] for b in buckets]
        assert ages == [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    def test_months_wrap_around_year_boundary(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 10, 1), age_months=14)
        months = [(b["year"], b["month"]) for b in buckets]
        assert months[0] == (2026, 10)
        assert months[2] == (2026, 12)
        assert months[3] == (2027, 1)
        assert months[-1] == (2027, 9)

    def test_bucket_has_season(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 2, 25), age_months=14)
        seasons = [b["season"] for b in buckets]
        # Feb=winter, Mar-May=spring, Jun-Aug=summer, Sep-Nov=autumn, Dec-Feb=winter
        assert seasons[0] == "winter"   # Feb
        assert seasons[1] == "spring"   # Mar
        assert seasons[4] == "summer"   # Jun
        assert seasons[7] == "autumn"   # Sep
        assert seasons[10] == "winter"  # Dec

    def test_bucket_has_label(self):
        from timeline import generate_buckets
        buckets = generate_buckets(current_date=date(2026, 2, 25), age_months=14)
        assert buckets[0]["label"] == "Feb 2026"
        assert buckets[10]["label"] == "Dec 2026"
        assert buckets[11]["label"] == "Jan 2027"


class TestSeasonMapping:
    def test_month_to_season(self):
        from timeline import month_to_season
        assert month_to_season(12) == "winter"
        assert month_to_season(1) == "winter"
        assert month_to_season(2) == "winter"
        assert month_to_season(3) == "spring"
        assert month_to_season(4) == "spring"
        assert month_to_season(5) == "spring"
        assert month_to_season(6) == "summer"
        assert month_to_season(7) == "summer"
        assert month_to_season(8) == "summer"
        assert month_to_season(9) == "autumn"
        assert month_to_season(10) == "autumn"
        assert month_to_season(11) == "autumn"


class TestActionMatching:
    def test_age_triggered_action_matches_when_in_range(self):
        from timeline import action_matches_bucket
        from actions import Action
        action = Action(
            id="test", swim_lane="sleep", title="T", big_picture="B",
            steps=[], trigger_type="age", age_months=(15, 18),
            seasons=None, priority="essential",
        )
        bucket = {"month": 3, "year": 2026, "age_months": 15, "season": "spring", "label": "Mar 2026"}
        assert action_matches_bucket(action, bucket) is True

    def test_age_triggered_action_no_match_outside_range(self):
        from timeline import action_matches_bucket
        from actions import Action
        action = Action(
            id="test", swim_lane="sleep", title="T", big_picture="B",
            steps=[], trigger_type="age", age_months=(15, 18),
            seasons=None, priority="essential",
        )
        bucket = {"month": 2, "year": 2026, "age_months": 14, "season": "winter", "label": "Feb 2026"}
        assert action_matches_bucket(action, bucket) is False

    def test_season_triggered_action_matches(self):
        from timeline import action_matches_bucket
        from actions import Action
        action = Action(
            id="test", swim_lane="clothing", title="T", big_picture="B",
            steps=[], trigger_type="season", age_months=None,
            seasons=["summer"], priority="essential",
        )
        bucket_jun = {"month": 6, "year": 2026, "age_months": 18, "season": "summer", "label": "Jun 2026"}
        bucket_feb = {"month": 2, "year": 2026, "age_months": 14, "season": "winter", "label": "Feb 2026"}
        assert action_matches_bucket(action, bucket_jun) is True
        assert action_matches_bucket(action, bucket_feb) is False

    def test_season_action_matches_multiple_seasons(self):
        from timeline import action_matches_bucket
        from actions import Action
        action = Action(
            id="test", swim_lane="clothing", title="T", big_picture="B",
            steps=[], trigger_type="season", age_months=None,
            seasons=["spring", "summer"], priority="essential",
        )
        bucket_apr = {"month": 4, "year": 2026, "age_months": 16, "season": "spring", "label": "Apr 2026"}
        assert action_matches_bucket(action, bucket_apr) is True

    def test_age_triggered_matches_single_month(self):
        from timeline import action_matches_bucket
        from actions import Action
        action = Action(
            id="test", swim_lane="health", title="T", big_picture="B",
            steps=[], trigger_type="age", age_months=(24, 24),
            seasons=None, priority="essential",
        )
        bucket_24 = {"month": 12, "year": 2026, "age_months": 24, "season": "winter", "label": "Dec 2026"}
        bucket_23 = {"month": 11, "year": 2026, "age_months": 23, "season": "autumn", "label": "Nov 2026"}
        assert action_matches_bucket(action, bucket_24) is True
        assert action_matches_bucket(action, bucket_23) is False


class TestBuildTimeline:
    def test_build_timeline_returns_buckets_with_actions(self):
        from timeline import build_timeline
        from actions import Action
        actions = [
            Action(id="a1", swim_lane="sleep", title="Nap", big_picture="B",
                   steps=[], trigger_type="age", age_months=(14, 15),
                   seasons=None, priority="essential"),
            Action(id="a2", swim_lane="clothing", title="Swim", big_picture="B",
                   steps=[], trigger_type="season", age_months=None,
                   seasons=["summer"], priority="essential"),
        ]
        timeline = build_timeline(date(2026, 2, 25), 14, actions)
        assert len(timeline) == 12
        # a1 should appear in Feb (age 14) and Mar (age 15)
        feb_actions = timeline[0]["actions"]
        assert any(a.id == "a1" for a in feb_actions)
        mar_actions = timeline[1]["actions"]
        assert any(a.id == "a1" for a in mar_actions)
        # a1 should NOT appear in Apr (age 16)
        apr_actions = timeline[2]["actions"]
        assert not any(a.id == "a1" for a in apr_actions)
        # a2 should appear in Jun-Aug (summer)
        jun_actions = timeline[4]["actions"]
        assert any(a.id == "a2" for a in jun_actions)

    def test_build_timeline_groups_by_swim_lane(self):
        from timeline import build_timeline, group_by_swim_lane
        from actions import Action
        actions = [
            Action(id="a1", swim_lane="sleep", title="Nap", big_picture="B",
                   steps=[], trigger_type="age", age_months=(14, 14),
                   seasons=None, priority="essential"),
            Action(id="a2", swim_lane="feeding", title="Cup", big_picture="B",
                   steps=[], trigger_type="age", age_months=(14, 14),
                   seasons=None, priority="essential"),
        ]
        timeline = build_timeline(date(2026, 2, 25), 14, actions)
        grouped = group_by_swim_lane(timeline[0]["actions"])
        assert "sleep" in grouped
        assert "feeding" in grouped
        assert len(grouped["sleep"]) == 1
        assert len(grouped["feeding"]) == 1

    def test_empty_actions_produces_empty_buckets(self):
        from timeline import build_timeline
        timeline = build_timeline(date(2026, 2, 25), 14, [])
        assert len(timeline) == 12
        for bucket in timeline:
            assert bucket["actions"] == []


# ── Action Data Completeness Tests ────────────────────────────────────────────

class TestActionData:
    def test_all_actions_list_is_populated(self):
        from actions import ALL_ACTIONS
        assert len(ALL_ACTIONS) >= 40

    def test_every_swim_lane_has_actions(self):
        from actions import ALL_ACTIONS, VALID_SWIM_LANES
        lanes_with_actions = {a.swim_lane for a in ALL_ACTIONS}
        for lane in VALID_SWIM_LANES:
            assert lane in lanes_with_actions, f"No actions for swim lane: {lane}"

    def test_each_swim_lane_has_at_least_3_actions(self):
        from actions import ALL_ACTIONS, VALID_SWIM_LANES
        from collections import Counter
        counts = Counter(a.swim_lane for a in ALL_ACTIONS)
        for lane in VALID_SWIM_LANES:
            assert counts[lane] >= 3, f"Swim lane '{lane}' has only {counts[lane]} actions"

    def test_all_actions_have_valid_swim_lanes(self):
        from actions import ALL_ACTIONS, VALID_SWIM_LANES
        for a in ALL_ACTIONS:
            assert a.swim_lane in VALID_SWIM_LANES, f"Invalid swim lane: {a.swim_lane}"

    def test_all_actions_have_non_empty_fields(self):
        from actions import ALL_ACTIONS
        for a in ALL_ACTIONS:
            assert a.id, f"Action missing id"
            assert a.title, f"Action {a.id} missing title"
            assert a.big_picture, f"Action {a.id} missing big_picture"
            assert len(a.steps) >= 1, f"Action {a.id} has no steps"

    def test_all_action_ids_are_unique(self):
        from actions import ALL_ACTIONS
        ids = [a.id for a in ALL_ACTIONS]
        assert len(ids) == len(set(ids)), "Duplicate action IDs found"

    def test_age_actions_have_valid_age_range(self):
        from actions import ALL_ACTIONS
        for a in ALL_ACTIONS:
            if a.trigger_type == "age":
                assert a.age_months is not None, f"Action {a.id}: age trigger but no age_months"
                lo, hi = a.age_months
                assert 12 <= lo <= 36, f"Action {a.id}: age_months lo={lo} out of range"
                assert lo <= hi, f"Action {a.id}: age_months lo > hi"

    def test_season_actions_have_valid_seasons(self):
        from actions import ALL_ACTIONS
        valid_seasons = {"spring", "summer", "autumn", "winter"}
        for a in ALL_ACTIONS:
            if a.trigger_type == "season":
                assert a.seasons is not None, f"Action {a.id}: season trigger but no seasons"
                for s in a.seasons:
                    assert s in valid_seasons, f"Action {a.id}: invalid season '{s}'"

    def test_14mo_feb_scenario_sleep_nap_transition(self):
        """The key scenario: 14-month-old in Feb. Nap transition should appear."""
        from actions import ALL_ACTIONS
        from timeline import build_timeline
        timeline = build_timeline(date(2026, 2, 25), 14, ALL_ACTIONS)
        # Nap transition actions should appear somewhere in months 1-4
        all_action_ids = set()
        for bucket in timeline[:6]:
            for a in bucket["actions"]:
                all_action_ids.add(a.id)
        assert any("nap" in aid for aid in all_action_ids), \
            f"No nap-related action found in first 6 months. IDs: {all_action_ids}"

    def test_14mo_feb_scenario_summer_clothing(self):
        """Summer clothing should appear in Jun-Aug columns."""
        from actions import ALL_ACTIONS
        from timeline import build_timeline
        timeline = build_timeline(date(2026, 2, 25), 14, ALL_ACTIONS)
        jun_aug_actions = []
        for bucket in timeline[4:7]:  # Jun, Jul, Aug
            jun_aug_actions.extend(bucket["actions"])
        clothing_actions = [a for a in jun_aug_actions if a.swim_lane == "clothing"]
        assert len(clothing_actions) >= 1, "No clothing actions in summer months"

    def test_14mo_feb_scenario_2year_review(self):
        """2-year developmental review should appear around month 24."""
        from actions import ALL_ACTIONS
        from timeline import build_timeline
        timeline = build_timeline(date(2026, 2, 25), 14, ALL_ACTIONS)
        # Age 24 = Dec 2026 (index 10)
        dec_actions = timeline[10]["actions"]
        health_actions = [a for a in dec_actions if a.swim_lane == "health"]
        assert any("2-year" in a.title.lower() or "two year" in a.title.lower() or "2 year" in a.title.lower()
                    for a in health_actions), \
            f"No 2-year review in Dec 2026. Health actions: {[a.title for a in health_actions]}"

    def test_14mo_feb_scenario_travel_prep_before_summer(self):
        """Travel prep should appear in spring, before summer trip."""
        from actions import ALL_ACTIONS
        from timeline import build_timeline
        timeline = build_timeline(date(2026, 2, 25), 14, ALL_ACTIONS)
        spring_actions = []
        for bucket in timeline[1:4]:  # Mar, Apr, May
            spring_actions.extend(bucket["actions"])
        travel_actions = [a for a in spring_actions if a.swim_lane == "travel"]
        assert len(travel_actions) >= 1, "No travel prep actions in spring"


# ── FastHTML Route Tests ──────────────────────────────────────────────────────

class TestRoutes:
    @pytest.fixture()
    def client(self):
        from main import app
        from fasthtml.common import Client
        return Client(app)

    def test_homepage_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_homepage_has_form_inputs(self, client):
        resp = client.get("/")
        html = resp.text
        assert 'name="current_date"' in html
        assert 'name="age_months"' in html
        assert "Go" in html

    def test_homepage_has_title(self, client):
        resp = client.get("/")
        assert "Toddler Timeline" in resp.text

    def test_timeline_post_returns_200(self, client):
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        assert resp.status_code == 200

    def test_timeline_shows_month_headers(self, client):
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        html = resp.text
        assert "Feb 2026" in html
        assert "Mar 2026" in html
        assert "Jan 2027" in html

    def test_timeline_shows_swim_lane_labels(self, client):
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        html = resp.text
        assert "Sleep" in html
        assert "Feeding" in html
        assert "Safety" in html

    def test_timeline_shows_action_titles(self, client):
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        html = resp.text
        assert "nap transition" in html.lower()

    def test_timeline_shows_age_in_months(self, client):
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        html = resp.text
        # Should show toddler age for each month
        assert "14 months" in html.lower() or "14mo" in html.lower() or "14 mo" in html.lower()

    def test_timeline_via_get_with_query_params(self, client):
        """Bookmarkable URL support."""
        resp = client.get("/timeline?current_date=2026-02-25&age_months=14")
        assert resp.status_code == 200
        assert "Feb 2026" in resp.text

    def test_timeline_actions_have_details(self, client):
        """Each action should show expandable big_picture and steps."""
        resp = client.post("/timeline", data={"current_date": "2026-02-25", "age_months": "14"})
        html = resp.text
        # Details/summary elements for expand/collapse
        assert "<details" in html
        assert "<summary" in html
