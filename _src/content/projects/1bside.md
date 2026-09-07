---
slug: 1bside
order: 1
title: Bside
tagline: A social simulation game where the characters think for themselves.
years: 2024 – now
role: Technical lead, Kotoko AI
thumb: bside-keyart.jpg
hero: bside-keyart.jpg
links:
  - ["Official site", "https://www.bside.zone/"]
  - ["Steam", "https://store.steampowered.com/app/3649950/Bside/"]
  - ["App Store", "https://apps.apple.com/us/app/bside/id6757434275"]
  - ["Google Play", "https://play.google.com/store/apps/details?id=com.kotoko.bside"]
---

Bside is an AI-native character simulation and social game, shipped on Steam (PC) and on iOS and Android. Players create characters with their own appearance, backstory and personality, then watch them live, talk and act in a shared multiplayer world driven by large language models. The game is our running experiment in how AI characters can make social play richer, and in what a meaningful player-AI relationship looks like.

I led Bside's engineering from the first prototype through international launch, across three generations of LLM-native client, server and character systems.

## On PC

- A real-time 3D social world where LLM-driven characters interact with each other and with players
- Community-created story worlds and a playground mode
- Desktop mate: your character lives on your desktop when you are not in the game

![Characters hanging out around a campfire on Bside PC, with the player choosing what to do next]({{img}}/bside-pc-world.jpg)

![A character's room on Bside PC]({{img}}/bside-pc-room.jpg)

## On mobile

- Create your character and chat with it anywhere; its replies follow the personality and backstory you defined
- A social feed where characters post daily updates about their lives
- Cooperative adventures with friends' characters
- Idle adventure gameplay with AI-generated comic recaps of what happened while you were away

<img class="img--phone" src="{{img}}/bside-mobile-home.jpg" alt="Bside mobile home screen: chat, adventure, playground, bond, style, vlog">

## Under the hood

**Multi-agent LLM system.** A real-time multi-agent architecture so characters can talk to each other naturally, with memory and personality systems that keep each character consistent over time, and dialogue generation that stays in character.

**Social interaction framework.** Systems for AI-to-AI and AI-to-player interaction, behaviour patterns that let social dynamics emerge, and emotion and relationship simulation underneath.

**Research.** A user study on player-AI interaction patterns and the social catalyst effect of AI characters. The control framework behind Bside's characters is written up in [Bounded Autonomy: Controlling LLM Characters in Live Multiplayer Games](https://arxiv.org/abs/2604.04703), and a case study on grounding LLM characters into executable gameplay is accepted at AIIDE 2026. See [Papers]({{base}}/publications/).
