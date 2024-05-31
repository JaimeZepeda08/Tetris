# Tetris

## Description

This is a **Tetris** game implemented in Python using the Pygame library. The game includes the following features:

- Different types of Tetris pieces with unique rotations.
- The ability to hold and swap the current piece.
- A grid-based layout for managing piece placement.
- Basic game mechanics like piece movement, rotation, and line clearing.

## Installation

To run the Tetris game, you need to have both Python and Pygame installed on your computer.

1. **Install Python**: Download and install the latest version of Python from the official [Python website](https://www.python.org/downloads/).

2. **Install Pygame**: Use `pip` to install Pygame by running the following command in your terminal or command prompt:

```
pip install pygame
```

## Running the Game

1. **Clone the Repository**: clone this repository to your local machine using the following command:

```
git clone https://github.com/JaimeZepeda08/Tetris.git
```

2. **Navigate to the Directory**: change to the directory containing the game code:

```
cd Tetris
```

3. **Run the Game**: execute the main python file to play the game:

```
python3 main.py
```

## Controls

`Up Arrow`: Rotate the current piece

`Down Arrow`: Move the piece down by one space

`Left Arrow`: Move the piece to the left by one space

`Right Arrow`: Move the piece to the right by one space

`Spacebar`: Drop the current piece to the bottom

`H`: hold the current piece for later use

## Game Features

### Grid

The game grid consists of a 10x20 layout where the Tetris pieces fall. The grid is managed by the `Grid` class, which handles the placement of pieces, checking for line clears, and managing the game state.

### Pieces

The game includes all the standard Tetris pieces:

- L-shaped
- Reverse L-shaped
- I-shaped
- Square
- T-shaped
- S-shaped
- Z-shaped

Each piece has its own class inheriting from the Piece class. The pieces can rotate, move left, right, and down, and interact with the grid.

### Holding Pieces

Players can hold the current piece for later use. Press the hold key to swap the current piece with the held piece.

### Clearing Lines

When a row is completely filled with pieces, it gets cleared, and all rows above it move down.

## Game Over

The game ends when a new piece cannot be placed at the starting position because of existing pieces in the grid.

## Possible Improvements

- Adding a scoring system.
- Implementing levels and increasing difficulty.
- Adding a graphical interface for displaying the score and level.
