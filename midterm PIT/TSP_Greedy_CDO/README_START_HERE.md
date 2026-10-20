# Greedy TSP — Cagayan de Oro City

## Quick start (Python 3 only; no installations needed)

1. Keep all project files in the same folder.
2. Open a command prompt / terminal in this folder.
3. Run `python TSP_Greedy_Implementation.py` (or `py TSP_Greedy_Implementation.py` on some Windows PCs).
4. Show the printed input matrix, Greedy selections, closed tour, and verification.
5. Optional audit: `python TSP_Optional_Exact_Audit.py`. This independent brute-force check is *not* the assigned greedy method.
6. Record the PowerPoint slides and the actual live Python execution following `TSP_Recording_Guide.pdf`.

## Problem description

A visitor plans a hypothetical photograph/documentation tour of five real urban landmarks in Cagayan de Oro, beginning and ending at Gaston Park. Choose the sequence of visits using the nearest-neighbor form of the Greedy Algorithm for TSP. Objective: minimize the SUM of the straight-line distances between designated landmark center points, measured in kilometers. The route need not coincide with shortest real-world walking/driving directions.

## Assumptions and data provenance (read before presenting)

- The geographic landmark identities and approximate coordinates come from public web references listed below. These are published location estimates.
- All **edge weights** were **calculated**, not copied from a Google Maps directions result: Haversine great-circle distances from latitude/longitude with Earth radius 6371.0088 km, individually rounded to 0.001 km.
- The completed *distance matrix is a mathematical proxy* for the tour. It is NOT a measured road or walking distance matrix; barriers, traffic, access points, and one-way roads are ignored.
- We treat the graph as complete, undirected, with symmetric nonnegative distances. There is no imposed arrival order, time window, or transport cost.
- Google Maps is supplied for viewing the locations and examining the suggested itinerary. Its walking route and distance may differ from the proxy model. Google Maps is **not** cited as the source of numerical edge weights. The original assignment says to use Google Maps: show/open the live Google Maps link during the presentation for context, and do not pass the computed model distances off as Google Maps measurements.

## Published coordinate sources

- A: Gaston Park — `8.47542, 124.64214` — https://mapcarta.com/W581430595
- B: Plaza Divisoria — `8.47775, 124.643778` — https://en.wikipedia.org/wiki/Plaza_Divisoria
- C: Ayala Malls Centrio — `8.485127, 124.651201` — https://en.wikipedia.org/wiki/Ayala_Malls_Centrio
- D: SM CDO Downtown — `8.4843833, 124.6543222` — https://www.wikidata.org/wiki/Q29586843
- E: Limketkai Mall — `8.48197, 124.65657` — https://mapcarta.com/W129409508

## Primary reference for the algorithm

R. Luna-Garcia, T. M. C. Candano, and R. L. Caga-anan, “Performance Analysis of Classical Algorithms for the Traveling Salesman Problem,” *The Mindanawan Journal of Mathematics*, vol. 6, no. 2, pp. 79–111, 2024. https://doi.org/10.62071/tmjm.v6i2.716 (Section 2.7, Algorithm 2.7, Theorem 2.7, pp. 88–89)

## Other references

- Google Maps "Measure distance between points": https://support.google.com/maps/answer/1628031?hl=en
- Google Maps URL documentation: https://developers.google.com/maps/documentation/urls/get-started
- Preview our landmark order on Google Maps: https://www.google.com/maps/dir/?api=1&origin=Gaston+Park%2C+Cagayan+de+Oro%2C+Philippines&destination=Gaston+Park%2C+Cagayan+de+Oro%2C+Philippines&travelmode=walking&waypoints=Plaza+Divisoria%2C+Cagayan+de+Oro%2C+Philippines%7CAyala+Malls+Centrio%2C+Cagayan+de+Oro%2C+Philippines%7CSM+CDO+Downtown%2C+Cagayan+de+Oro%2C+Philippines%7CLimketkai+Mall%2C+Cagayan+de+Oro%2C+Philippines

## Expected results

- Nearest Neighbor starting at A: `A -> B -> C -> D -> E -> A`
- Route segments: 0.316 + 1.157 + 0.353 + 0.365 + 1.746 km
- **Total: 3.937 km** (rounded matrix)
- Exact audit of 24 fixed-start tours: model minimum **3.937 km**, tied by reverse route symmetry.
- Greedy *matches* the model minimum on this dataset. That does **not** imply the heuristic always returns the optimum.

## Files to submit

- `TSP_Greedy_Implementation.py` — runnable assigned algorithm.
- `TSP_Locations.csv` and `TSP_Distance_Matrix.csv` — full identifiable dataset; `TSP_Distance_Edges.csv` additionally provides explicit edge definitions.
- Recorded 10–15-minute audio-video presentation with **actual live execution**.
- PowerPoint slides are provided as an aid, though the rubric only explicitly requires the recording, source, and dataset.

## Important academic note

Use the slide deck and narration as a scaffold, but make sure you can answer what “nearest unvisited” and “straight-line distance proxy” mean. The professor can ask why Google Maps walking directions show a different distance than the Python model: it is because walking routing follows real roads and paths while this model assumes straight-line edges.
