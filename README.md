# Chinese Chess AI
## Introduction
This project is a Chinese Chess (Xiangqi) AI engine that can simulate and evaluate game states, generate possible moves, and make intelligent decisions using the Minimax algorithm with alpha-beta pruning. The engine also incorporates position-based evaluations and piece values to optimize gameplay decisions.

## Features
Move Generation: Generate all possible moves for the current game state.
Minimax Algorithm with Alpha-Beta Pruning: Perform decision-making using the Minimax algorithm with alpha-beta pruning to reduce search space and improve performance.
Position and Piece Value Evaluation: The AI evaluates game states based on a combination of piece values and positional values, accounting for early, mid, and late game phases.
Game End Detection: Detects terminal states (win/loss) by checking the presence of generals on both sides.
Arc Consistency: Implements arc consistency to simplify the decision space by filtering invalid moves.

## How It Works
The AI evaluates the board using piece values and position values, which vary depending on the stage of the game (opening, midgame, or endgame). It generates all legal moves and applies the Minimax algorithm with alpha-beta pruning to search for the optimal move. Additionally, the AI ensures arc consistency by eliminating invalid move choices, further optimizing decision-making.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/chinese-chess-ai.git
cd chinese-chess-ai
```

2. Run the project:
```bash
python main.py
```

## Usage
Move Generation: Generate possible moves for any given game state.
AI Decision Making: The AI will use the Minimax algorithm to make the best possible move based on the current board state.
Game End Detection: Detects if one of the players has won the game by checking if the generals are still present on the board.


## Technologies
Python: The entire project is built using Python.

Minimax Algorithm: For AI decision-making.

Alpha-Beta Pruning: To optimize the decision-making process and reduce unnecessary computations.

Arc Consistency: Used to simplify decision-making by filtering out invalid moves.

