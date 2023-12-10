# Tetris AI

An engine for playing Tetris, as well as several different AIs that can play the game on this engine.

![Brief demo of the game.](https://github.com/calebabutler/tetris_ai_project/blob/main/photos/demo.gif)

# Dependencies

This collection of programs require the following dependencies:

* Python 3, preferrably 3.10 or newer
* pygame
* numpy
* tensorflow

# Which Program for Which Purpose

For a playable demo of the tetris engine, run the following program:

    python3 playable.py

For a demo that executes random moves and creates new games when old ones end forever, run this program:

    python3 random_game.py

For an AI that uses tensorflow for machine learning, run this program:

    python3 agent.py

For a simple AI that does not use machine learning or any complex techniques, but simply makes decisions based on the calculations for bumpiness, aggregate height, and amount of holes used by the machine learning AI, run this program:

    python3 simple_ai.py

