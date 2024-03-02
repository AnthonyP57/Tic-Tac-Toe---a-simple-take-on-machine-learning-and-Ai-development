# Tic Tac Toe - a simple take on machine learning and Ai development

game available at:
https://anthonyp57.itch.io/tic-tac-toe-a-simple-take-on-machine-learning-and-ai-development

As well as here in the form of Python code

# Initial plan
Creating an algorithm that has no applied logic, but instead learns from its previous attempts and improves (no direct game prediction such as MiniMax algorithm).
The best environment for that seemed to be Tic Tac Toe as the rules are plain, evaluation is easy and it is possible to supervise and interprete the process.

# Logic types
- Supervised Machine Learning - simply, if last time I won I should do the same if not I shouldn't do this...
- Neural Networks - a group of 'neurons' trained on the dataset obtained from the games played by SML
- Rule-based Ai - all the decisions are based on a given set of rules (only used in game, no measurements were performed)

# How they *think*

## Supervised Machine Learning

  <img src="https://github.com/AnthonyP57/Tic-Tac-Toe---a-simple-take-on-machine-learning-and-Ai-development/blob/main/photos/sml.png">
  
### *simplified logic*

## Neural Networks

### Neural networks are like virtual brains that learn from examples, adjusting connections between neurons to understand and solve problems, such as recognizing images or making predictions.

## Rule-based Ai

### Rule-based Ai is like a computer following a set of specific instructions or conditions to make decisions or take actions, operating on predefined rules and logic. For example: if the opponent moved here move there and only there.

# Performance

## Random moves - as comparison for logic evaluation
| Random moves vs Random moves | number of games played | percent of games won | percent of games not lost (win and draw) |
| --- | --- | --- | --- |
| on average for a random moves player | 500 | 44.8 | 55.3 |


## Supervised Machine Learning
| Supervised Machine Learning vs random moves | number of games played | percent of games won | percent of games not lost (win and draw) | average time for game [sec] |
| --- | --- | --- | --- | --- |
| moves based on frequency | 400 | 65.9 | 74.2 | 1.7 in power saving mode |
| moves based on frequency | 800 | 69.8 | 78.5 | 1.425 in power saving mode |
| moves based on length of games | 1200 | 75.1 | 82.6 | 1.5 in power saving mode |
| moves based on length of games | 1600 | 76.8 | 82.3 | 0.6 in high performance mode |
| moves based on length of games | 2600 | 79.5 | 86.5 | 0.7 in high performance mode |
| moves based on length of games | 3600 | 81.5 | 89.8 | 0.7 in high performance mode |


## Neural Networks
| Neural Networks vs random moves | number of games played | percent of games won | percent of games not lost (win and draw) | average time for game [sec] |
| --- | --- | --- | --- | --- |
| 1000 neurons, 1000 learning iterations | 1300 | 41.9 | 54.5 | 0.8 in power saving mode |
| 1000 neurons, 2000 learning iterations | 2600 | 53.4 | 63.9 | 0.23 in high performance mode |
| 1000 neurons, 2000 learning iterations | 12600 | 48.5 | 62.1 | 0.12 in high performance mode |
| 200 neurons, 1000 learning iterations | 13600 | 44.2 | 54.9 | 0.18 in high performance mode |
| adaptive learning Off | 14600 | 45.6 | 54.2 | 0.18 in high performance mode |
| 200 neurons, no draw possibility in training, solver change to lbfgs | 15100 | 90.2 | 91.0 | 0.15 in high performance mode |


## Neural Networks vs Supervised Machine Learning
| number of games played | percent of games won by NN | percent of games not lost (win and draw) by NN |
| --- | --- | --- |
| 200 | 50.8 | 50.8 |
| 400 | 53.1 | 53.1 |
| 500 | 51.5 | 51.5 |
| 600 | 53.2 | 53.2 |

# Perfomance summary
  The initial goal has been achieved by creating an Ai capable of winning more than 90% of the games (against a random moves player). Among the two models developed, not only did neural networks prove to be a better player, but also were significantly easier to implement and cut average game time by four in comparison to SML.

# Game as an interactive experience
  These logic types have been implemented into a standalone game, that is available both here as code and on itch.io as an executable file. I wanted to create someting unique and interesting in and of itself, so game art substitutes for the lack of excitement stemming from the game's nature. Player can choose from three game themes as well as three logic types to play against. More in game.

# Game rules
  As mentioned player is stacked against three various types of artificial intelligence, for simplicity's sake player's tag is always X and Ai's tag is always O. However it is always decided at random as to who moves first. As said there are three difficulties (in roughly descending order) to choose from, switching between them mid-game may cause a logic problem.

# Tactics against Ai s
## Neural Networks
### Always make the same set of moves, starting first gives them advantage. However, there is an obvious susceptibility.
## Supervised Machine Learning
### Often unpredictable, there is (manually added to make the game more exciting) 33% chance it will block opponents move. Keep in mind that it will always try using the quickest path to win so a long-term tactic may pay off.
## Rule-based Ai
### Number of games lost by it is exactly 0.

# Game installation
### From Github
  Download and unzip game file, run main.py to start game. Make sure not to move any folders and files within the main folder.

### From itch.io
  Download and unzip game file, initiate .exe file or its shortcut to start game. Make sure not to move any folders and files within the main folder and to change shortcut path if necessary.

# Disclamers
- Learning functions have been disabled so as to make the game less demanding.
- The game has been packed, not compiled which may cause a (very) slow start and explains why a tic tac toe game is ~182MB in size.
- Supervised machine learning Ai can be slow as it is has a CPU-heavy logic.
- Changing Ai mid-game may cause logic problems.

## Python Packages
| Python | 3.8 |
| --- | --- |
| pygame | 2.5.2 |
| pandas | 2.0.3 |
| random | - |
| numpy | 1.24.4 |
| joblib | 1.3.2 |
| scikit-learn | 1.3.2 |

## Hardware
### MSI Leopard GP72 7RE
  CPU: i7 - 7700HQ
  
  GPU: GTX 1050Ti
  
  RAM: 16GB DDR4 2133MHz
