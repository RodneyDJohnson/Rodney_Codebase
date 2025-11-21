# Week 1 Python Project Template
# MedTrans CSV Summary & Basic Route Analytics

import csv
from pathlib import Path
from collections import defaultdict


def summarize_csv(file_path: str) -> None:
    """
    Print basic information about a CSV file:
    - Total rows
    - Column names
    - On-time vs late delivery counts
    - Per-route delivery count and average miles
    - Route with the most deliveries
    """
    path = Path(file_path)

    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return

    try:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"\nFile: {path}")
        print(f"Total rows (excluding header): {len(rows)}")

        if not rows:
            print("No data rows found in this file.")
            return

        columns = list(rows[0].keys())
        print("Columns:", ", ".join(columns))

        # --- On-time vs late analytics ---
        on_time_count = 0
        late_count = 0

        for row in rows:
            status = row.get("delivered_on_time", "").strip().lower()
            if status == "yes":
                on_time_count += 1
            elif status == "no":
                late_count += 1

        total_with_status = on_time_count + late_count
        on_time_rate = (
            (on_time_count / total_with_status) * 100 if total_with_status > 0 else 0
        )

        print("\nDelivery Timeliness:")
        print(f"  On-time deliveries: {on_time_count}")
        print(f"  Late deliveries:    {late_count}")
        print(f"  On-time rate:       {on_time_rate:.1f}%")

        # --- Route-level analytics ---
        route_stats = defaultdict(lambda: {"count": 0, "total_miles": 0.0})

        for row in rows:
            route = row.get("route", "UNKNOWN").strip()
            miles_raw = row.get("miles", "").strip()

            try:
                miles = float(miles_raw) if miles_raw else 0.0
            except ValueError:
                miles = 0.0

            route_stats[route]["count"] += 1
            route_stats[route]["total_miles"] += miles

        print("\nRoute Analytics:")
        print("  Route       Count   Avg Miles")
        print("  ---------   -----   ---------")
        for route, stats in route_stats.items():
            count = stats["count"]
            avg_miles = stats["total_miles"] / count if count > 0 else 0.0
            print(f"  {route:<10} {count:<7} {avg_miles:>9.2f}")

        # --- Route with most deliveries ---
        most_route = None
        most_count = 0

        for route, stats in route_stats.items():
            if stats["count"] > most_count:
                most_count = stats["count"]
                most_route = route

        if most_route is not None:
            print(f"\nRoute with most deliveries: {most_route} ({most_count} stops)")

        print()

    except Exception as e:
        print("[ERROR] Something went wrong while reading the CSV:")
        print(e)


if __name__ == "__main__":
    # Change this path to the CSV you want to inspect
    sample_path = "sample.csv"
    summarize_csv(sample_path)
