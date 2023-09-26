# Animal Shogi AI

## Overview

Welcome to the Animal Shogi AI project! This endeavor aims to develop a sophisticated AI model trained through reinforcement learning to play the game of Animal Shogi, also known as Dobutsu Shogi or Let's Catch the Lion! It's a simpler and more accessible version of the traditional Japanese board game, shogi, designed specifically for children and beginners. With this project, we aim to introduce a digital, AI-based opponent to the world of Animal Shogi.

## Setup and Installation

1. **Clone the Repository**: Start by cloning this repository to your local machine.
2. **Install Dependencies**: Navigate to the project directory and run the following command to install all the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Features

Our AI model incorporates the following features:

1. **Board Reading Mechanism**: Can accurately represent the game's state at any given time.
2. **Game Rules**: All the rules of Animal Shogi are meticulously implemented to ensure a fair game.
3. **Win/Loss Determination**: Can determine the end game conditions accurately.
4. **Reward Function**: Defined for effective reinforcement learning training of the AI model.

Additionally, the project features a user-friendly graphical interface developed using Python and Pygame.

## Development Stages

### Phase 1: Pre-Reinforcement Learning

In this phase, we established the game's foundation:

- Developed a graphical user interface (GUI) for interactive gameplay.
- Implemented piece movement based on the game's rules.
- Introduced a system to manage player turns.
- Designed a system to determine win/loss conditions.

### Phase 2: Reinforcement Learning

In the reinforcement learning phase, we utilized the Stable Baselines3 library to develop and train the AI model using the Proximal Policy Optimization (PPO) algorithm.

## Testing and Evaluation

Once the AI model is trained, it can be tested and evaluated against human players or other AI opponents to gauge its performance.

## Technologies Used

- **Python**: Serves as the primary language for backend development and AI modeling.
- **Pygame**: Used for GUI development, offering an intuitive and interactive gameplay experience.
- **Stable Baselines3**: A reinforcement learning library utilized to train the AI model.

## Contributing

Contributions are welcome! If you're interested in contributing or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Contact

For any questions, suggestions, or feedback, please contact us.

Thank you for your interest in our project!
