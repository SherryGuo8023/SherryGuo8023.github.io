---
title: "Bounded Autonomy: Controlling LLM Characters in Live Multiplayer Games"
collection: publications
category: preprints
permalink: /publication/2026-04-06-bounded-autonomy
excerpt: 'A control framework for LLM-driven characters in a live multiplayer social game: agent-to-agent communication, world action execution, and player steering.'
date: 2026-04-06
status: 'Preprint,'
venue: 'arXiv:2604.04703 [cs.HC]'
paperurl: 'https://arxiv.org/abs/2604.04703'
citation: 'Yunjia Guo, Jinghan Zhu, Siyu Wang, Haixin Qiao. (2026). &quot;Bounded Autonomy: Controlling LLM Characters in Live Multiplayer Games.&quot; <i>arXiv:2604.04703</i> [cs.HC].'
---

Large language models are bringing richer dialogue and social behaviour into games, but they also expose a control problem that existing game interfaces do not directly address: how should LLM characters participate in live multiplayer interaction while remaining executable in the shared game world, socially coherent with other active characters, and steerable by players when needed?

This paper presents a control framework that organises LLM character management around three interfaces:

- **Agent-to-agent communication**, kept stable with probabilistic reply-chain decay so that conversations between characters converge instead of running away.
- **World action execution**, using embedding-based action grounding with fallbacks so that what a character says it does is something the game can actually execute.
- **Player steering**, through a "whisper" mechanism that lets players nudge a character without overriding its autonomy.

The framework is deployed in [Bside](https://www.bside.zone/), a live multiplayer social simulation game. A formative analysis of the deployment shows how the architecture keeps interaction stable, grounds actions reliably, and supports successful player interventions.

[Read on arXiv](https://arxiv.org/abs/2604.04703)
