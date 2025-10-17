# 🚀 Space Invaders: Retro Edition

A modern take on the classic Space Invaders arcade game, built with Python and Pygame. Features advanced AI, power-ups, wave progression, and retro aesthetics.

## ✨ Features

### 🎮 **Core Gameplay**
- **Smooth 60 FPS** gameplay with frame-rate independent movement
- **10 Different Enemy AI Patterns** - from basic waves to tactical positioning
- **Wave-Based Progression** - structured levels with formation spawning
- **Combo System** - chain kills for up to 5x score multipliers
- **7 Unique Power-Ups** - from rapid fire to bullet time

### 🎯 **Power-Ups**
- **Rapid Fire** 🔴 - Faster shooting
- **Shield** 🔵 - Absorbs one hit  
- **Multi-Shot** 🟡 - 3-bullet spread
- **Speed Boost** 🟢 - 1.5x movement
- **Score Multiplier** 🟣 - 2x points
- **Screen Clear** 🟠 - Destroy all enemies
- **Bullet Time** ⏰ - Slow down enemies 70%

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Pygame

### Installation
```bash
# Clone the repository
git clone https://github.com/depressoboi/Space-Invaders
cd space-invaders-retro

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## 🎮 Controls

- **Movement**: Arrow Keys or WASD
- **Shoot**: Spacebar
- **Pause**: P
- **Test Mode**: T (spawn power-ups for testing)

### Game Over Screen
- **R** - Restart game
- **ESC** - Return to menu
- **Q** - Quit

## 🏗️ Architecture

The game is built with a modular architecture for maintainability and extensibility:

```
├── main.py              # Entry point
├── game.py              # Main game loop
├── player.py            # Player mechanics
├── enemy.py             # Enemy AI patterns
├── powerup_system.py    # Power-up mechanics
├── wave_system.py       # Wave progression
├── combo_system.py      # Combo and visual effects
├── menu_system.py       # Main menu and high scores
└── [other modules]      # Additional game systems
```

## 🎯 Game Design Philosophy

- **Respect the Classic** - Maintains core Space Invaders gameplay
- **Modern Enhancements** - Adds depth without complexity
- **Smooth Performance** - 60 FPS with delta-time movement
- **Visual Feedback** - Satisfying effects and animations

## 🛠️ Development Features

### Testing Mode
Press `T` during gameplay to enter test mode:
- Spawn any power-up instantly
- Infinite lives for safe testing
- Visual power-up descriptions
- Quick balance iteration

### Modular Design
- Each system is self-contained
- Easy to add new features
- Clean separation of concerns
- Comprehensive settings configuration

## 📊 Technical Highlights

- **Frame-Rate Independent Movement** - Consistent gameplay across hardware
- **Advanced Enemy AI** - 10 different behavioral patterns
- **Efficient Collision Detection** - Multiple threshold system
- **State Machine Architecture** - Clean game flow management
- **Geometric Power-Ups** - No external image dependencies

## 🎓 Learning Outcomes

This project demonstrates:
- **Game Architecture** - Modular, maintainable code structure
- **Game Design** - Balanced progression and feedback systems
- **Performance Optimization** - Smooth 60 FPS gameplay
- **User Experience** - Polish and professional presentation

## 🚀 Future Enhancements

- Sound system and background music
- Boss fights every 5th wave
- Local co-op multiplayer
- Achievement system
- Weapon variants and upgrades

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

**Enjoy the game!** 🚀👾

*Built with ❤️ using Python and Pygame*