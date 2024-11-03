# Bouncing Ball Game

## Description
This project is a simple bouncing ball game developed using Pygame. Players interact with a ball that responds to gravity, damping, and friction. The goal is to score points by colliding the ball with the walls and the ground. The game features a visually appealing effect where the ball leaves a trail as it moves.

## Features
- Realistic ball physics with gravity and friction
- Scoring system based on collisions
- Configurable settings via an INI file
- Rotating ball texture based on movement
- Customizable display dimensions

## Requirements
- Python 3.x
- Pygame

## Installation

### 1. Clone the repository
To get a local copy of the project, run the following commands in your terminal:
```bash
git clone https://github.com/HouwyTwitch/bouncing-ball-game.git
cd bouncing-ball-game
```

### 2. Install dependencies
Once your virtual environment is activated, install the required packages using pip:
```bash
pip install -r requirements.txt
```

## Running the Game
To run the game, execute:
```bash
python main.py
```

## Configuration
You can adjust game settings by modifying the `config.ini` file. This includes:
- Display width and height
- Ball initial size
- Gravity, friction, and damping factors
- Scoring thresholds

## Project Structure
```
src/
├── assets/
│   ├── ball.png
│   └── background.png
├── config.ini
├── main.py
README.md
requirements.txt
