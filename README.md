# COMP730-LAB4
Lab 4
Some diagrams may be available as PlantUML text; to edit and render this text, please use https://www.plantuml.com. Images will be provided.

## Vision
Farkle is a well known dice game, a game of chance and strategy. In our implementation, we will be delivering a fast paced and easy to use version of Farkle intended for singleplayer. 

## Business Case
- **Customer Value:** Provides a familiar, easy-to-learn game that appeals to casual and competitive players.
- **Agile Benefits:** Rapid iterations allow for frequent feedback, ensuring the game meets user expectations and adapts to changing needs.
- **Market Opportunity:** Digital tabletop games are popular; Farkle’s simplicity and replayability make it ideal for mobile and desktop platforms.

## Goals
- Fast, intuitive gameplay
- VS. Bot Mode
- Clear scoring and rules

# Environment Requirements & Configuration

## 1) Platform
- **OS:** Windows, macOS, or Linux
- **Python:** 3.10+ (tested with 3.10/3.11)
- **Shell:** Any (PowerShell, bash, zsh)

## 2) Dependencies
- **Runtime:** Python standard library only (no third‑party packages required).
- **Dev/Test (optional):**
  - 'unittest' (bundled with Python)
  - 'pytest' (optional)
  - 'plantuml' (optional, to render the '.plantuml' diagrams under documents folder)

### Optional dev setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest
```
> PlantUML is a separate Java tool; install via your package manager or download the jar.


