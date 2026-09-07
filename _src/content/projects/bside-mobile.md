---
slug: bside-mobile
order: 2
title: Bside Mobile
tagline: A character-raising game for iOS and Android, built around AI-native play.
years: 2025 – now
role: Technical lead, Kotoko AI
thumb: bside-mobile-home.jpg
hero: bside-mobile-home.jpg
hero_phone: true
links:
  - ["App Store", "https://apps.apple.com/us/app/bside/id6757434275"]
  - ["Google Play", "https://play.google.com/store/apps/details?id=com.kotoko.bside"]
  - ["bside.zone", "https://www.bside.zone/"]
---

Bside Mobile launched on iOS and Android in March 2026 and is the product I currently spend most of my time on. It shares a name, an art style and the character creator with [Bside for PC]({{base}}/portfolio/1bside/), and characters made on one can be used on the other, but it is a different game built for a different platform.

The core is not chat. It is: create a character, then raise it. There are no preset characters and no NPCs. You build yours from personality tags and free text, and that personality drives how it acts, what it posts and how it plays.

## What the character does

- **A feed.** Your character posts social-media-style updates about its day, so it keeps living between your sessions.
- **Adventures.** Scenarios the character plays out on its own, according to its personality, while you watch.
- **Playground.** Visual novels written by players, staging scenes from their characters' lives, with branches the authors wrote.
- **Vlogs.** Short clips that place your character into footage from your own phone.
- **Chat, dress-up and gifts.** Talk to it whenever you like; what you give it affects its mood.

## Why a separate design

Sessions on a phone are short and frequent, latency budgets are tight, and every interaction has to pay for itself. Instead of the real-time multi-agent simulation that Bside for PC runs, Bside Mobile is built around mobile-native loops: lightweight nurturing, asynchronous presence through the feed, and generative image and video content, which only became affordable enough for a core loop in the last couple of years. Same characters, different game.
