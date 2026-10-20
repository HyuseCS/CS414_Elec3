#!/usr/bin/env python3
"""Greedy (Nearest Neighbor) TSP for five real Cagayan de Oro landmarks.

Metric: rounded straight-line Haversine distances in TSP_Distance_Matrix.csv.
These are NOT measured road/walking distances. Source coordinates are in
TSP_Locations.csv. No third-party Python packages required.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATRIX_FILE = BASE / "TSP_Distance_Matrix.csv"
LOCATIONS_FILE = BASE / "TSP_Locations.csv"
START = "A"  # Gaston Park


def load_data():
    with LOCATIONS_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    names = {r["location_id"]: r["location_name"] for r in rows}
    with MATRIX_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        labels = header[1:]
        distances = {}
        for row in reader:
            distances[row[0]] = {k: float(v) for k, v in zip(labels, row[1:])}
    if set(labels) != set(names) or set(distances) != set(labels):
        raise ValueError("Mismatched location IDs in the CSV files.")
    for x in labels:
        if distances[x][x] != 0:
            raise ValueError(f"Diagonal for {x} must be zero.")
        for y in labels:
            if distances[x][y] < 0:
                raise ValueError("Distances cannot be negative.")
            if abs(distances[x][y] - distances[y][x]) > 1e-9:
                raise ValueError("This example assumes undirected, symmetric weights.")
    return labels, names, distances


def nearest_neighbor(labels, distances, start):
    """Make the locally smallest move until all vertices have been visited."""
    if start not in labels:
        raise ValueError("Starting vertex not found.")
    unvisited = set(labels) - {start}
    route = [start]
    steps = []
    while unvisited:
        current = route[-1]
        # Lexicographic tie break keeps results reproducible.
        next_city = min(unvisited, key=lambda v: (distances[current][v], v))
        steps.append((current, next_city, distances[current][next_city]))
        route.append(next_city)
        unvisited.remove(next_city)
    route.append(start)
    return route, steps


def validate_and_total(route, labels, distances, start):
    if route[0] != start or route[-1] != start:
        raise ValueError("The tour must start and finish at the depot.")
    if len(route) != len(labels) + 1 or set(route[:-1]) != set(labels):
        raise ValueError("Tour does not include every vertex exactly once.")
    if len(set(route[:-1])) != len(labels):
        raise ValueError("A location was revisited before closing the tour.")
    legs = [(a, b, distances[a][b]) for a, b in zip(route, route[1:])]
    return legs, round(sum(x[2] for x in legs), 3)


def main():
    labels, names, distances = load_data()
    print("=" * 66)
    print("GREEDY TSP: NEAREST NEIGHBOR / CAGAYAN DE ORO")
    print("=" * 66)
    print("Objective: MINIMIZE total straight-line distance (km)")
    print("Model: 5 real landmarks; symmetric, undirected, complete graph")
    print("WARNING: weights are calculated straight-line proxies, NOT road km")
    print("\nINPUT LOCATIONS")
    for key in labels:
        print(f"  {key} = {names[key]}")
    print("\nINPUT DISTANCE MATRIX (kilometers)")
    print("       " + "".join(f"{k:>9}" for k in labels))
    for a in labels:
        print(f"  {a:<5}" + "".join(f"{distances[a][b]:>9.3f}" for b in labels))

    tour, steps = nearest_neighbor(labels, distances, START)
    print("\nGREEDY SELECTIONS")
    for i, (a, b, d) in enumerate(steps, 1):
        print(f"  {i}. From {a}, select nearest UNVISITED {b}: {d:.3f} km")
    print(f"  Return to start: {tour[-2]} -> {START}")
    legs, total = validate_and_total(tour, labels, distances, START)
    print("\nRESULTING CLOSED TOUR")
    print("  " + " -> ".join(tour))
    print("  " + " -> ".join(names[x] for x in tour))
    print("\nINDEPENDENT DISTANCE CHECK")
    for a,b,d in legs:
        print(f"  {a} -> {b}: {d:.3f} km")
    print(f"  TOTAL: {total:.3f} km")
    print("  All locations visited exactly once: YES")
    print("  Returned to starting point: YES")
    print("  This greedy heuristic is NOT globally optimal in general.")
    print("=" * 66)


if __name__ == "__main__":
    main()
