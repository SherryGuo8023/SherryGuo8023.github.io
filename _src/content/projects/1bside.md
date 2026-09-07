---
slug: 1bside
order: 1
title: Bside for PC
tagline: A multiplayer social world on Steam. Every character belongs to a player and is run by AI.
years: 2024 – 2025
role: Technical lead, Kotoko AI
thumb: bside-keyart.jpg
hero: bside-keyart.jpg
links:
  - ["Steam", "https://store.steampowered.com/app/3649950/Bside/"]
  - ["bside.zone", "https://www.bside.zone/"]
---

Bside for PC is a social simulation game released on Steam in Early Access in October 2025. There are no NPCs. Every character in the world, called a Biibit, belongs to a real player, but the player does not control it directly: a multi-agent runtime built on large language models decides what each Biibit does, who it talks to and how it reacts. Players shape their character through its personality and backstory, watch it live alongside other players' characters in shared rooms, and nudge it with a whisper when they want to.

The game also runs as a desktop mate: your Biibit lives on your desktop while you work, and steps back into the world when you open the game.

## What players do

- Create a Biibit with its own look, backstory and personality
- Join or host a Space, a shared room where up to a couple of dozen characters live together in real time
- Watch characters talk, cook, camp, dance and get into each other's business
- Whisper to your character to steer it without taking it over
- Community-created story worlds and a playground mode

![Characters around a campfire in a shared Space, with the player choosing what to suggest to their character]({{img}}/bside-pc-world.jpg)

![A Biibit's room]({{img}}/bside-pc-room.jpg)

## Under the hood

This is the version the three-layer architecture in our research refers to, and the hardest engineering of the three products I have led at Kotoko AI.

**Behaviours as bundles.** Characters run behaviour bundles with priority, mutual-exclusion and interruption rules, similar in spirit to an ability system in an action game. The model proposes what a character wants to do next; the runtime decides whether that can interrupt what it is doing, and whether the interrupted behaviour resumes or is dropped.

**Turn-by-turn conversation.** Conversations unfold one line at a time, and each participant decides for itself whether to reply, decline, leave or go back to what it was doing. A bounded conversational decay winds exchanges down so two characters do not talk forever.

**A bounded action pool.** Characters do not emit engine commands. The runtime selects from hand-authored, executable actions, with fallbacks, and the model voices the choice in character. Open language, but only actions the game can actually execute and read back.

**Whisper.** The player-steering interface: a suggestion the character will usually follow, never a command with a guaranteed effect.

The control framework is written up in [Bounded Autonomy: Controlling LLM Characters in Live Multiplayer Games](https://arxiv.org/abs/2604.04703). Bside for PC and [Bside Mobile]({{base}}/portfolio/bside-mobile/) are platform-specific designs rather than versions of one game: PC carries the real-time multi-agent simulation suited to long sessions; mobile is built around lighter daily loops.
