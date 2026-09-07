---
slug: 5urbanpcg
order: 7
title: Procedural urban generation
tagline: A 4 km² city from a heightmap, with roads that follow the terrain and buildings built by Wave Function Collapse.
years: 2020
role: NetEase Games
thumb: urbanpcg-banner.png
hero: urbanpcg-banner.png
links:
  - ["Building generation demo", "https://youtu.be/cAl7qkdw154?si=VoFKmW13eHUvR1U1"]
  - ["City generation demo", "https://youtu.be/tl7diOhRB3s?si=lHhq8DKpQgdva_OE"]
---

A procedural pipeline for generating 4 km² urban environments at NetEase Games. Given a heightmap, the system lays out road networks, places buildings and shapes terrain into a coherent, varied cityscape.

## How it works

**Road networks.** Built in Houdini, adapting to the terrain, with a multi-level road hierarchy, intersection planning, and different distribution patterns for city centres and suburbs.

**Buildings.** Wave Function Collapse with bitmask constraints assembles buildings from a modular, parametric architecture kit, so the city is varied but architecturally coherent.

**Integration.** Terrain-adaptive placement and construction, with rendering optimised for large-scale real-time visualisation.
