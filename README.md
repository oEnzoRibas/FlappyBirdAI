# Flappy Bird AI

This project implements an AI to play the Flappy Bird game using the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. The AI learns to navigate between pipes and achieve higher scores through evolution over generations.

## 📌 Table of Contents
- [Showcase](#showcase)
- [Motivation](#-motivation)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Running the Game (Playable)](#-running-the-game-playable)
  - [Training the AI (Non-playable)](#-training-the-ai-non-playable)
  - [Visualizing Training Progress](#-visualizing-training-progress)
- [Game Elements](#-game-elements)
  - [Bird](#-bird)
  - [Pipe](#-pipe)
  - [Base](#-base)
  - [Score](#-score)
- [NEAT Algorithm Overview](#-neat-algorithm-overview)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

## Showcase
### NEAT Playing Flappy Bird:
![Gameplay Demo](media/Showcase/neat_run_reduzido.gif)

## 🎯 Motivation
This project was created as an exploration of the NEAT algorithm and its applications in reinforcement learning.

## 📁 Project Structure
### Files and Directories
- **.gitattributes**: Configuration file for Git attributes.
- **LICENSE**: MIT License for the project.
- **README.md**: This file.
- **media/**: Directory containing media files such as images and models.
- **models/**: Directory containing trained models and fitness graphs.
- **Project/**: Main project directory containing the game and AI implementation.
  - **neat_run.py**: Script to run the NEAT algorithm and train the AI.
  - **neat.config.txt**: Configuration file for the NEAT algorithm.
  - **run.py**: Script to run the Flappy Bird game manually.
  - **visualize.py**: Script to visualize training progress with graphs.
  - **assets/**: Directory containing game assets like images and audio.
  - **game/**: Directory containing game logic and classes.

## 🔍 Requirements
- Python 3.8.1 or above
- Pygame
- NEAT-Python
- Matplotlib

## 💻 Installation
1. Clone the repository:
```sh
    git clone https://github.com/yourusername/flappy-bird-ai.git
    cd flappy-bird-ai
```

2. Install the required packages:
```sh
    pip install pygame neat-python matplotlib
```

## 🚀 Usage
### 🔥 Running the Game (Playable)
To run the Flappy Bird game manually:
```sh
python run.py
```

### 🧩 Training the AI (Non-playable)
To train the AI using the NEAT algorithm:
```sh
python neat_run.py
```
When the training is completed, the best model will be saved in the `models/` directory.

### 📊 Visualizing Training Progress
To generate graphs showing training progress:
```sh
python visualize.py
```
The graphs are saved in the `models/` directory.

## 🎮 Game Elements
### 🐦 Bird
Responsible for the bird's movement, jumping, and collision detection.

### 🟢 Pipe
Controls the pipes' movement and handles collisions with the bird.

### 🟫 Base
Manages the moving base at the bottom of the screen.

### 🔢 Score
Tracks and renders the score on the screen.

## 🧠 NEAT Algorithm Overview
NEAT (NeuroEvolution of Augmenting Topologies) is a powerful AI algorithm that evolves neural networks using reinforcement learning. The process involves:
- Creating an initial population of birds, each with a unique genome and neural network.
- Evaluating birds based on survival time and pipe passages.
- Selecting top-performing birds, breeding them, and applying mutations.
- Repeating over generations to improve performance.

For more information, see the [NEAT documentation](https://neat-python.readthedocs.io/en/latest/).

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

## 💬 Acknowledgements
- The `NEAT-Python` library for implementing the NEAT algorithm.
- The `Pygame` library for creating the game.
- The original Flappy Bird game for inspiration.

