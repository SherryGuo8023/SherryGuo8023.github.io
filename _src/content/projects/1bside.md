---
slug: 1bside
order: 2
title: "Bside: Desktop Mate"
tagline: A multiplayer world on Steam where every character belongs to a real player. No joysticks.
years: 2024 – 2025
role: Technical lead, Kotoko AI
thumb: bside-keyart.jpg
hero: bside-keyart.jpg
links:
  - ["Steam", "https://store.steampowered.com/app/3649950/Bside/"]
  - ["bside.zone", "https://www.bside.zone/"]
---

<video class="clip" controls playsinline preload="metadata" poster="/video/bside-desktop-mate-poster.jpg" src="/video/bside-desktop-mate.mp4"></video>

There are no NPCs. Every character in the world belongs to a real player, but you never control yours directly. A multi-agent system decides what your Biibit does, who it talks to, and how it reacts. You shape it through personality and backstory, watch it live alongside other players' characters, and whisper when you want to nudge it somewhere.

It also works as a desktop mate: your Biibit hangs out on your screen while you work, and steps back into the world when you open the game.

## What players do

- Create a Biibit with its own look, backstory and personality
- Join or host a Space, a shared room where up to a couple of dozen characters live together in real time
- Watch characters talk, cook, camp, dance and get into each other's business
- Whisper to your character to steer it without taking it over
- Community-created story worlds and a playground mode

![Characters around a campfire in a shared Space, with the player choosing what to suggest to their character]({{img}}/bside-pc-world.jpg)

![A Biibit's room]({{img}}/bside-pc-room.jpg)

## Under the hood

This is the version our research papers describe.

**Behaviour bundles.** Characters run prioritised behaviour bundles with interruption rules, like an ability system in an action game. The model proposes what a character wants to do; the runtime decides whether it can interrupt what's already happening.

**Turn-by-turn conversation.** Each line is its own decision. A character can reply, decline, walk away, or go back to what it was doing. A decay function winds exchanges down so nobody talks forever.

**Bounded actions.** Characters never emit raw engine commands. The runtime picks from hand-authored, executable actions with fallbacks; the model voices the choice in character.

**Whisper.** A suggestion the character will usually follow. Never a command with a guaranteed effect.

The framework is written up in [Bounded Autonomy](https://arxiv.org/abs/2604.04703). [Bside]({{base}}/portfolio/bside/) on mobile and Desktop Mate are different games for different platforms, not ports of each other.
