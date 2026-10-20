#!/usr/bin/env python3
"""Optional independent audit: exhaustively check the small five-vertex dataset.
This is NOT the assigned greedy algorithm and should not be presented as such.
"""
from itertools import permutations
from TSP_Greedy_Implementation import load_data, nearest_neighbor, validate_and_total, START


def main():
    labels, names, matrix = load_data()
    greedy, _ = nearest_neighbor(labels, matrix, START)
    _, greedy_cost = validate_and_total(greedy, labels, matrix, START)
    other = sorted(set(labels) - {START})
    candidates = []
    for p in permutations(other):
        route = [START, *p, START]
        _, cost = validate_and_total(route, labels, matrix, START)
        candidates.append((cost, route))
    min_cost = min(x[0] for x in candidates)
    best_routes = [route for cost, route in candidates if abs(cost-min_cost) < 1e-9]
    print("INDEPENDENT BRUTE-FORCE AUDIT (NOT GREEDY ALGORITHM)")
    print(f"Examined {len(candidates)} possible tours from fixed start {START}.")
    print(f"Greedy tour: {' -> '.join(greedy)} | {greedy_cost:.3f} km")
    print(f"Best total: {min_cost:.3f} km")
    print(f"One minimum tour: {' -> '.join(best_routes[0])}")
    print(f"Greedy reaches dataset minimum: {abs(greedy_cost-min_cost)<1e-9}")
    print("This finding applies ONLY to the present distance matrix.")


if __name__ == '__main__':
    main()
