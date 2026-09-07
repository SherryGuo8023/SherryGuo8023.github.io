---
slug: 2dobit
order: 3
title: Dobit
tagline: A small town where AI characters lived together. The game that taught us everything we got wrong.
years: 2023 – 2024
role: Technical lead, Kotoko AI
thumb: dobit-screenshot.jpg
hero: dobit-screenshot.jpg
links:
  - ["Review on YouTube", "https://www.youtube.com/watch?v=8hRC9d4-f5c"]
  - ["Another review", "https://www.youtube.com/watch?v=LvezYDDMTI4"]
---

Dobit was where everything started. A multiplayer life sim for mobile, closed beta in 2023–2024. You created a character, it moved into the town of Mystereal, and it lived there alongside other players' characters and a cast of NPCs. You didn't control it with a joystick. You told it what you hoped it would do, and it usually did. Usually.

## How it worked

**One system for every character.** The same multi-agent system drove players' Dobits and NPCs alike: planning, moving, talking, remembering.

**Memory as a graph.** Each Dobit kept short- and long-term memory in a graph store, tracking relationships with other characters and places. The agents read that memory when they planned and talked.

**Daily letters.** Every day your Dobit wrote you a letter about what it had been up to. Beta players told us that was the moment the character felt real.

**Character generation.** One sentence of description turned into a game-ready character: artist-drawn parts combined, rigged and animated automatically.

**Staged conversations.** When one character wanted to talk to another, a single model call wrote the whole exchange and they acted it out face to face. Coherent little scenes, and the reason the next product overhauled how conversation works.

## What it taught us

Open-ended generation gave us signs of life we didn't expect: rumours that spread through the whole town, a shopkeeper who could think of nothing but her cats. It also showed us everything characters can't figure out on their own — when to stop talking, what actions the game can actually execute, how to interrupt gracefully. Those lessons became the runtime in [Bside: Desktop Mate]({{base}}/portfolio/1bside/), and the journey is written up in a case study accepted at AIIDE 2026. See [Papers]({{base}}/publications/).

Built with Unity, Stable Diffusion, and a custom LLM integration layer.
