# Terminal Catacomb Crawler

A classic roguelike catacomb/dungeons crawler game built for the terminal using Python and the `blessed` library.

## Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Development](#development)
  - [Running Tests](#running-tests)
  - [Code Style](#code-style)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- **Classic ASCII Graphics**: Retro-style dungeon visualization with colored tiles
- **Smooth Movement**: Navigate with WASD keys or arrow keys
- **Real-time Rendering**: Efficient viewport-based rendering system
- **Player Stats**: Health, experience, level, and combat stats tracking
- **Inventory System**: Basic inventory management (expandable)
- **Cross-platform**: Works on Windows, macOS, and Linux terminals

## Screenshots

```
###############################
###############.......#########
#######......##@......#.......#
###...................#.......#
#.............#.......#.......#
#..>...####.....#######.......#
#......####................####
...........................####

==================================================
Health: ████████████████████ (100/100)
EXP:    ░░░░░░░░░░░░░░░░░░░░ (0/100)
Level: 1 | Attack: 10 | Defense: 5 | Position: (24, 4)

--------------------------------------------------
Controls: WASD/Arrows=Move | Q=Quit | I=Inventory
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/terminal-dungeon-crawler.git
   cd terminal-dungeon-crawler
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Start the game:
   ```bash
   python main.py
   ```

2. **Controls**:
   - `W/A/S/D` or `Arrow Keys` - Move your character (@)
   - `I` - Open inventory
   - `Q` - Quit game

3. **Game Elements**:
   - `@` - Your character (player)
   - `#` - Walls (impassable)
   - `.` - Floor (walkable)
   - `+` - Doors
   - `>` - Stairs going down
   - `<` - Stairs going up

## Project Structure

```
terminal-dungeon-crawler/
├── main.py              # Game entry point
├── requirements.txt     # Python dependencies
├── game/
│   ├── __init__.py
│   ├── engine.py        # Main game loop and engine
│   ├── player.py        # Player character logic
│   ├── level.py         # Level generation and management
│   └── ui.py           # User interface and rendering
└── README.md
```

## Technical Details

- **Game Engine**: Custom event-driven game loop with input handling
- **Terminal Library**: `blessed` for cross-platform terminal control
- **Rendering**: Viewport-based rendering with configurable view radius
- **Architecture**: Modular design with separated concerns (engine, UI, player, level)

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. Format code with:
```bash
black game/ main.py
```

## Roadmap

- [X] **Combat System** - Enemies and turn-based combat
- [ ] **Items & Equipment** - Weapons, armor, and consumables
- [ ] **Multiple Levels** - Procedural dungeon generation
- [ ] **Save/Load** - Game state persistence
- [ ] **Sound Effects** - Terminal beeps and audio feedback
- [ ] **Advanced UI** - Message log, minimap, help screens

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic roguelike games like Rogue, NetHack, and Angband
- Built with the excellent `blessed` Python library
- ASCII art and terminal graphics tradition

---

*Happy dungeon crawling!*