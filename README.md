# COMP730-LAB4
Lab 4
Some diagrams may be available as PlantUML text; to edit and render this text, please use https://www.plantuml.com. Images will be provided.

# Vision Statement: Farkle Game

## Vision
Deliver a fun, engaging, and accessible digital version of the classic dice game Farkle, enabling players to enjoy quick, competitive gameplay against the bot.

## Business Case
- **Customer Value:** Provides a familiar, easy-to-learn game that appeals to casual and competitive players.
- **Agile Benefits:** Rapid iterations allow for frequent feedback, ensuring the game meets user expectations and adapts to changing needs.
- **Market Opportunity:** Digital tabletop games are popular; Farkle’s simplicity and replayability make it ideal for mobile and desktop platforms.

## Goals
- Fast, intuitive gameplay
- VS. Bot Mode
- Clear scoring and rules

# Farkle — Environment Requirements & Configuration

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

## 3) Project Layout
```
.
├─ README.md                                 # this file
├─ documents/
│  ├─ class_diagram.png
│  ├─ class_diagram_plantuml.txt
│  ├─ domain_model.png
│  ├─ domain_model_plantuml.txt
│  ├─ glossary.png
│  ├─ glossary_plantuml.txt
│  ├─ meeting_notes.txt
│  ├─ use_case_model.png
│  ├─ use_case_model_plantuml.txt
│  ├─ use_case_scenarios.png
│  └─ use_case_scenarios_plantuml.txt
│
├─ implementation/
│  ├─ CalculateScore.py
│  ├─ DicePool.py
│  ├─ Die.py
│  ├─ Game.py
│  ├─ main.py
│  ├─ Player.py
│  └─ Setup.py
│
├─ farkle_game.py
└─ tests/
   └─ test_farkle.py                         # unit tests
```

## 4) Running the Game (Interactive CLI)
```bash
python farkle_game.py
```
On launch, the program prompts for:
- **Player name** (default: 'You')
- **Target score** (default: '10000')
- **Enable Hot Dice?** ('y'/'n', default 'y')

Configuration is stored on the 'Game' object:
- 'Game.target_score: int'
- 'Game.allow_hot_dice: bool'

## 5) Logging / Console Output
The game prints roll results, scoring breakdowns, Hot Dice notices, banking, and winner. No external logs.

## 6) Unit Testing
Use Python’s built‑in 'unittest' or 'pytest' (optional).

**Run tests**
```bash
# unittest
python -m unittest discover -s tests -p "test_*.py" -v
# pytest (if installed)
pytest -q
```

## 7) Diagram Rendering (optional)
Render the PlantUML files to PNG/SVG with PlantUML:
```bash
plantuml domain_model_plantuml.txt
plantuml glossary_plantuml.txt
plantuml use_case_model_plantuml.txt
plantuml use_case_scenarios_plantuml.txt
plantuml system_sequence_diagram_plantuml.txt
```

## 8) Troubleshooting
- **Python not found:** Install Python 3.10+ and ensure 'python'/'python3' on PATH.
- **PlantUML not found:** Install PlantUML (requires Java) or use an online renderer (https://www.plantuml.com).
