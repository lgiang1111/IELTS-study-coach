# API Reference: Model Context Protocol (MCP) Server

The IELTS Study Coach exposes its core Genetic Algorithm optimization engine via the Model Context Protocol (MCP) using a standard stdio transport layer.

---

## Tool: `optimize_schedule`

Optimizes a 7-day IELTS study schedule based on user scores, target scores, and study duration.

### Request Arguments

| Argument | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `initial_bands_str` | `string` | Yes | Comma-separated initial scores for Listening, Reading, Writing, Speaking (e.g. `"6.0, 6.5, 5.5, 6.0"`). Bands must be between 0.0 and 9.0. |
| `target_bands_str` | `string` | Yes | Comma-separated target scores for Listening, Reading, Writing, Speaking (e.g. `"7.0, 7.0, 6.5, 6.5"`). Bands must be between 0.0 and 9.0. |
| `total_days` | `integer` | Yes | Total study duration in days (must be at least `7`). |

### Response Schema

Returns a JSON string containing the status, fitness value, weekly study schedule, and forecasted scores:

```json
{
  "status": "success",
  "fitness": 25.2746,
  "schedule": [
    [["L", 1.5], ["R", 2.0]],     // Day 1: Session list of [Skill, Duration in hours]
    [["W", 1.0]],                 // Day 2
    [["S", 1.5], ["L", 1.0]],     // Day 3
    [],                           // Day 4 (Rest day)
    [["R", 2.0], ["W", 1.5]],     // Day 5
    [["S", 2.0]],                 // Day 6
    [["L", 1.0], ["R", 1.0]]      // Day 7
  ],
  "forecasted_scores": {
    "L": 7.21,
    "R": 6.89,
    "W": 6.12,
    "S": 6.45,
    "overall": 6.5
  }
}
```

---

## Programmatic Usage (Python API)

You can import and execute the engine programmatically in python:

```python
from ielts_coach.ga_engine import run_ga

initial_bands = {"L": 6.0, "R": 6.5, "W": 5.5, "S": 6.0}
target_bands = {"L": 7.0, "R": 7.0, "W": 6.5, "S": 6.5}
total_days = 30

result = run_ga(initial_bands, target_bands, total_days)
print("Forecasted Overall Band:", result["forecasted_scores"]["overall"])
```
