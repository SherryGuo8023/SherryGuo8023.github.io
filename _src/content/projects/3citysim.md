---
slug: 3citysim
order: 5
title: Multi-layered city generation for crowd simulation
tagline: 3D cities from OpenStreetMap data, with bridges and tunnels handled properly.
years: 2021
role: Master's thesis, Utrecht University, with uCrowds
thumb: citysim-banner.png
hero: citysim-banner.png
links: []
---

Most city reconstruction pipelines flatten everything. This one keeps bridges and tunnels as separate walkable layers and connects them properly, so a crowd simulator gets an environment it can actually navigate.

## What it does

**Multi-layered environments.** A geometric processing pipeline analyses multi-layer structures, resolves the spatial overlaps caused by bridges and tunnels, and builds the ramps and transitions between layers, so every layer is non-overlapping and properly connected to its neighbours.

**Geographic data.** An OpenStreetMap parser extracts buildings, road networks and terrain for any location in the world, using tiled vector data for fast rendering and feature lookups.

**Simulation integration.** Walkable space and obstacles are divided automatically and an Explicit Corridor Map (ECM) is generated for navigation in multi-layered environments, feeding directly into the SimCrowds engine.

Validated on complex urban scenarios as part of my master's research at Utrecht University, in collaboration with uCrowds.
