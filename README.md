# Connect 4

2 player and battle against advanced AI Connect 4 game built using Python


#### Demo

<p align="center">
  <img alt="Connect 4 game play" src='https://user-images.githubusercontent.com/39765499/56462040-26ef7080-63b4-11e9-8f5a-7f0b4dec216d.gif'>
</p>

<p align="center">
  <img alt="Winning screen" src='https://user-images.githubusercontent.com/39765499/56461893-f9092c80-63b1-11e9-9a9e-d46439a6365a.png'>
</p>

### Features

* Replica of original game
* 2 player mode or play against computer using AI
* AI uses advanced algorithm ([Minimax](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/))

### How to Run

**_To Run 2 player game_**

```
$ git clone https://github.com/barclayd/Connect-4
$ cd Connect-4
$ python connect_4_two_player.py
```

**_To run vs AI game_**

```
$ git clone https://github.com/barclayd/Connect-4
$ cd Connect-4
$ python connect_4_with_ai.py
```

### Future Improvements

* Settings screen with options to configure
    * Difficulty of AI (depth level of recursive algorithm)
    * Game mode - toggle between 2 player and vs Computer
    * Customisation of game in settings and allow for players to choose player colour pieces
    * Limits for time user can spend on making a move
* Deploy as installable .exe/.dmg
