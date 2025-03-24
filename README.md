# Isometric-Snake

Isometric-Snake is a Python game that recreates the classic Snake experience in an isometric view using the Pygame library.

## Features

- **Isometric Graphics**: Provides a unique visual perspective to the traditional Snake game.
- **Customizable Assets**: Allows users to integrate their own isometric block graphics.
- **Original Sound Effects**: Features sounds created by the developer.

## Requirements

- **Python**: Ensure you have Python installed on your system.
- **Pygame**: This library is essential for running the game. Install it using pip:

  ```bash
  pip install pygame
  ```

## Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/cyptrix12/Isometric-Snake.git
   cd Isometric-Snake
   ```

2. **Add Isometric Block Graphics**:

   - Obtain or create an isometric block PNG image.
   - Place the image in the project directory.
   - Update the `block_resolution` variable in the code to match the resolution of your PNG (32 pixels is recommended).

3. **Run the Game**:

   Execute the main script to start the game:

   ```bash
   python main.py
   ```

## Gameplay

- **Objective**: Navigate the snake to collect points without colliding with itself or the boundaries.
- **Controls**: Use the arrow keys to change the snake's direction.
- **Scoring**: Each collected point increases the snake's length and score.
