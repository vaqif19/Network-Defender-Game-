# Network Defender

A cyberpunk-style action game made with **Python** and **Pygame**.
You are the security admin of a central server: ban the red **hacker** packets before they
reach it, and let the green **user** packets through.

## Features
- Animated cyberpunk menu (falling code, network nodes, glitch title)
- Server and packet figures drawn with Pygame (virus vs. envelope)
- 3 difficulty levels, pause menu (ESC / P), TOP 5 high scores saved in `highscores.json`
- 4 languages: English, Azerbaijani, Turkish, Russian

## How to play
| Packet | What to do | Result |
|---|---|---|
| Red spiky virus (hacker) | Click it | +15 points |
| Red virus reaches the server | - | -1 life |
| Green envelope (user) | Let it pass | +5 points |
| Green envelope clicked | - | -1 life |

You have 3 lives on Normal (Easy = 5, Hard = 2). The game gets faster over time.

## Run
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/macOS: source venv/bin/activate)
pip install -r requirements.txt
python main.py
```

## Project structure
```
main.py                  # entry point + core game loop
requirements.txt
network_defender/
├── config.py            # constants, colours, difficulty levels
├── texts.py             # 4-language text dictionary
├── utils.py             # helper functions, lambdas, decorator
├── ui.py                # Button class
├── entities.py          # Particle, Packet, MatrixRain, Node classes
├── game.py              # GameApp class (states, logic, drawing)
└── storage.py           # high score save/load (json)
```

## Author
Vaqif Ismayilov
