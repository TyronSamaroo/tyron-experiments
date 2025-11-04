from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Static,
    TabPane,
    TabbedContent,
)

DATA_FILE = Path.home() / ".macro_tracker.json"


def _default_data() -> Dict[str, Any]:
    return {
        "profile": {
            "name": "",
            "age": 0,
            "height": 0,
            "weight": 0,
            "goal": "maintain",
            "daily_calories": 0,
            "daily_protein": 0,
            "daily_carbs": 0,
            "daily_fat": 0,
        },
        "weight_history": [],
        "daily_logs": {},
    }


def load_data() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return _default_data()
    try:
        with DATA_FILE.open("r") as handle:
            return json.load(handle)
    except Exception:
        return _default_data()


def save_data(data: Dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w") as handle:
        json.dump(data, handle, indent=2)


@dataclass
class MacroTotals:
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fat: float = 0

    @classmethod
    def from_day(cls, day_data: Dict[str, Any]) -> "MacroTotals":
        if not day_data:
            return cls()
        return cls(
            calories=day_data.get("total_calories", 0),
            protein=day_data.get("total_protein", 0),
            carbs=day_data.get("total_carbs", 0),
            fat=day_data.get("total_fat", 0),
        )


class SummaryPanel(Static):
    """Renders high-level macro stats for the selected day."""

    totals: reactive[MacroTotals | None] = reactive(None)
    profile: reactive[Dict[str, Any]] = reactive({})

    def render(self) -> RenderableType:
        profile = self.profile or {}
        totals = self.totals or MacroTotals()

        table = Table.grid(padding=(0, 1))
        table.add_column("Label", justify="left")
        table.add_column("Value", justify="right")
        table.add_column("Target", justify="right")
        table.add_column("Remaining", justify="right")

        def make_row(label: str, consumed: float, target: float, unit: str) -> None:
            remaining = max(target - consumed, 0)
            pct = f"{(consumed / target * 100):.0f}%" if target else "—"
            value = f"{consumed:.0f} {unit} ({pct})" if target else f"{consumed:.0f} {unit}"
            table.add_row(label, value, f"{target:.0f} {unit}" if target else "—", f"{remaining:.0f} {unit}")

        make_row("Calories", totals.calories, float(profile.get("daily_calories") or 0), "kcal")
        make_row("Protein", totals.protein, float(profile.get("daily_protein") or 0), "g")
        make_row("Carbs", totals.carbs, float(profile.get("daily_carbs") or 0), "g")
        make_row("Fat", totals.fat, float(profile.get("daily_fat") or 0), "g")

        name = profile.get("name") or "Macro Tracker"
        subtitle = Text.from_markup(
            f"Goal: [b]{profile.get('goal', 'maintain').title()}[/b] • Weight: [b]{profile.get('weight', 0)} kg[/b]"
        )
        return Panel(table, title=f"Daily Snapshot — {name}", subtitle=subtitle)


class FoodTable(DataTable):
    def on_mount(self) -> None:  # type: ignore[override]
        self.add_columns("Time", "Food", "Calories", "Protein", "Carbs", "Fat", "Qty")
        self.cursor_type = "row"
        self.zebra_stripes = True

    def update_entries(self, foods: Iterable[Dict[str, Any]]) -> None:
        self.clear()
        for food in foods:
            self.add_row(
                food.get("time", "—"),
                food.get("name", "Unknown"),
                f"{food.get('calories', 0):.0f}",
                f"{food.get('protein', 0):.0f}",
                f"{food.get('carbs', 0):.0f}",
                f"{food.get('fat', 0):.0f}",
                food.get("quantity", "1"),
            )


class WeightTrend(Static):
    weights: reactive[List[Dict[str, Any]]] = reactive([])

    def render(self) -> RenderableType:
        if not self.weights:
            return Panel("No weight history yet.", title="Weight Trend")

        entries = sorted(self.weights, key=lambda item: item.get("date", ""))[-12:]
        values = [float(entry.get("weight", 0)) for entry in entries]
        if not values:
            return Panel("No weight data found.", title="Weight Trend")

        min_w, max_w = min(values), max(values)
        span = max(max_w - min_w, 0.1)
        blocks = "▁▂▃▄▅▆▇█"
        scale = (len(blocks) - 1) / span
        chars = [blocks[int((value - min_w) * scale)] for value in values]
        trend = Text("".join(chars), style="bold green")

        start = values[0]
        end = values[-1]
        delta = end - start
        subtitle = f"Change: {delta:+.1f} kg"
        body = Text("  ".join(f"{entry['date']}: {weight:.1f}kg" for entry, weight in zip(entries, values)))
        return Panel(Text.assemble(trend, "\n", body), title="Weight Trend", subtitle=subtitle)


class QuickLogScreen(ModalScreen[Optional[Dict[str, Any]]]):
    class Submitted(Message):
        def __init__(self, food: Dict[str, Any]) -> None:
            self.food = food
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Vertical(
                Label("Quick Log Entry", id="modal-title"),
                Input(placeholder="Food name", id="food-name"),
                Input(placeholder="Calories", id="calories"),
                Input(placeholder="Protein (g)", id="protein"),
                Input(placeholder="Carbs (g)", id="carbs"),
                Input(placeholder="Fat (g)", id="fat"),
                Input(placeholder="Quantity", id="quantity"),
                Horizontal(
                    Button("Cancel", id="cancel"),
                    Button("Save", id="save", variant="primary"),
                    id="modal-actions",
                ),
                id="modal-body",
            ),
            id="modal",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
            return
        if event.button.id == "save":
            food = {
                "name": self.query_one("#food-name", Input).value.strip() or "Quick entry",
                "calories": _to_float(self.query_one("#calories", Input).value),
                "protein": _to_float(self.query_one("#protein", Input).value),
                "carbs": _to_float(self.query_one("#carbs", Input).value),
                "fat": _to_float(self.query_one("#fat", Input).value),
                "quantity": self.query_one("#quantity", Input).value or "1 serving",
                "time": datetime.now().strftime("%H:%M"),
            }
            self.dismiss(food)


class HabitHubApp(App):
    CSS = """
    #body {
        height: 1fr;
    }

    #sidebar {
        width: 32;
        border: round $surface 50%;
        padding: 1 1;
        background: $boost;
    }

    #sidebar-title {
        text-style: bold;
        padding-bottom: 1;
    }

    #main {
        padding: 0 1;
    }

    DataTable {
        height: 1fr;
    }

    #modal {
        width: 60;
        border: round $accent 50%;
        padding: 1 2;
        background: $surface-darken-1;
    }

    #modal-title {
        text-style: bold;
        padding-bottom: 1;
    }

    #modal-actions {
        padding-top: 1;
        content-align: right middle;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "reload", "Reload data"),
        ("n", "new_entry", "Quick log"),
    ]

    selected_date: reactive[str | None] = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        self.data: Dict[str, Any] = load_data()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="body"):
            with Horizontal():
                with Vertical(id="sidebar"):
                    yield Label("Days", id="sidebar-title")
                    yield ListView(id="date-list")
                    yield Button("New Quick Log", id="new-entry-button", variant="primary")
                with Vertical(id="main"):
                    with TabbedContent():
                        with TabPane("Daily Summary", id="summary-tab"):
                            with Vertical(id="summary-container"):
                                yield SummaryPanel(id="summary-panel")
                                yield FoodTable(id="food-table")
                        with TabPane("Weight Trend", id="weight-tab"):
                            yield WeightTrend(id="weight-trend")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_data()

    def refresh_data(self) -> None:
        self.data = load_data()
        dates = sorted((self.data.get("daily_logs") or {}).keys(), reverse=True)
        list_view = self.query_one("#date-list", ListView)
        list_view.clear()
        if not dates:
            list_view.append(ListItem(Label("No entries yet")))
            self.selected_date = None
        else:
            for index, day in enumerate(dates):
                label = datetime.fromisoformat(day).strftime("%a %d %b %Y") if _is_iso_date(day) else day
                list_item = ListItem(Label(label))
                setattr(list_item, "day_key", day)
                list_view.append(list_item)
            self.selected_date = dates[0]
            list_view.index = 0
        self.update_views()

    def update_views(self) -> None:
        profile = self.data.get("profile", {})
        day_data = {}
        foods: List[Dict[str, Any]] = []
        if self.selected_date:
            day_data = self.data.get("daily_logs", {}).get(self.selected_date, {})
            foods = day_data.get("foods", [])

        summary = self.query_one("#summary-panel", SummaryPanel)
        summary.profile = profile
        summary.totals = MacroTotals.from_day(day_data)

        food_table = self.query_one("#food-table", FoodTable)
        food_table.update_entries(foods)

        weight_panel = self.query_one("#weight-trend", WeightTrend)
        weight_panel.weights = self.data.get("weight_history", [])

    @on(ListView.Selected)
    def handle_date_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id != "date-list":
            return
        selected_day = getattr(event.item, "day_key", None)
        if selected_day:
            self.selected_date = selected_day
            self.update_views()

    def action_reload(self) -> None:
        self.refresh_data()

    def action_new_entry(self) -> None:
        self.push_screen(QuickLogScreen(), self.handle_quick_entry)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new-entry-button":
            self.action_new_entry()

    def handle_quick_entry(self, food: Optional[Dict[str, Any]]) -> None:
        if not food:
            return
        today = date.today().isoformat()
        logs = self.data.setdefault("daily_logs", {})
        day = logs.setdefault(
            today,
            {
                "foods": [],
                "total_calories": 0,
                "total_protein": 0,
                "total_carbs": 0,
                "total_fat": 0,
            },
        )
        day["foods"].append(food)
        day["total_calories"] += food["calories"]
        day["total_protein"] += food["protein"]
        day["total_carbs"] += food["carbs"]
        day["total_fat"] += food["fat"]
        save_data(self.data)
        self.refresh_data()
        today_label = date.today().isoformat()
        self.selected_date = today_label
        self.update_views()


def _is_iso_date(value: str) -> bool:
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def _to_float(value: Optional[str]) -> float:
    try:
        return float(value) if value else 0.0
    except (TypeError, ValueError):
        return 0.0


def run() -> None:
    HabitHubApp().run()


if __name__ == "__main__":
    run()
