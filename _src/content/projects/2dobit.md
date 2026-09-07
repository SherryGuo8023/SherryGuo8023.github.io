---
slug: 2dobit
order: 3
title: Dobit
tagline: A multiplayer life simulation on mobile where players' AI characters and NPCs live together in a small town.
years: 2023 – 2024
role: Technical lead, Kotoko AI
thumb: dobit-screenshot.jpg
hero: dobit-screenshot.jpg
links:
  - ["Review on YouTube", "https://www.youtube.com/watch?v=8hRC9d4-f5c"]
  - ["Another review", "https://www.youtube.com/watch?v=LvezYDDMTI4"]
---

Dobit was the first of the three products I have led at Kotoko AI: a multiplayer life simulation for iOS and Android, run as a closed beta in 2023 and 2024. Each player created a Dobit, their own AI character, which then lived in the town of Mystereal alongside other players' Dobits and a cast of named NPCs. Players did not steer their character with a joystick. They told it what they hoped it would do, and it usually did, but not always.

## How it worked

**One system for every character.** A multi-agent system drove players' Dobits and the NPCs alike: planning the day, moving around town, working, talking and remembering. Several specialised language models were combined to balance cost and quality.

**Memory as a graph.** Each Dobit kept short-term and long-term memory in a graph store, including its relationships with other Dobits and with places in town. The agents read that memory when they planned and talked.

**Daily letters.** Every day your Dobit wrote you a letter about what it had done. Beta players told us the letters were the moment the character felt alive.

**Character generation.** One sentence of description became a game-ready character: artist-drawn parts and outfits were combined, rigged and animated automatically.

**Staged conversations.** When one character decided to talk to another, a single model call wrote the whole exchange and the participants acted it out face to face. Coherent little scenes, and the reason the next product changed how conversation works.

## What it taught us

Open-ended generation produced signs of life: rumours that spread through the whole town, a shopkeeper who could think of nothing but her cats. It also showed that characters need rules the model cannot give itself, about interruption, about ending a conversation, about which actions the game can actually execute. Those lessons became the runtime in [Bside: Desktop Mate]({{base}}/portfolio/1bside/), and the road from one to the other is the subject of a case study accepted at AIIDE 2026. See [Papers]({{base}}/publications/).

Built with Unity, Stable Diffusion and a custom LLM integration layer.
