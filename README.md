# Pacman agents
Analyzing some algorithms for a simplified game of Pacman with two ghosts. These algorithms are Random, MiniMax, Monte Carlo Tree Search and a hybrid between MiniMax and Monte Carlo Tree Search. This hybrid algorithm is similar to MCTS but uses MiniMax in the playout stage.


## Result
Because the results can be hard to read i will interpret every match-up. We are going to analyze the results after ten games on the second map. By X vs Y: score1(depth1), score2(depth2), score3(depth3) it is understood that Pacman uses algorithm X and ghosts use algorithm Y and got scores score1, score2, score3 for depths depth1, depth2, depth3.

Random vs Random: 0-10
* for random agents it hard for Pacman to eat all the food and not meet a ghost

MiniMax, MCTS, Hybrid vs Random: 10-0
* as expected every algorithm beats random ghosts

MiniMax vs MiniMax: 2-8(5), 1-9(6), 3-7(7), 2-8(8), 4-6 (9)
* seems like a bigger depth helps Pacman
* possible explanation: it is possible for Pacman to predict better where the ghosts are going to be

MiniMax vs MCTS: 7-3(5), 6-4(6), 6-4(7), 5-5(8), 5-5(9)
* with bigger depth MCTS starts to catch up
* possible explanation: MCTS explores more and can evaluate states better

MiniMax vs Hybrid: 3-7(5), 3-7(6), 2-8(7)
* the hybrid algorithm does quite well considering the fact that the ghosts are favored
* possible explanation: Hybrid is a better version of MiniMax, however it is slow

MCTS vs MiniMax:  1-9(5), 0-10(6), 0-10(7), 1-9(8), 1-9(9)
* for small depth MiniMax clearly dominates, but, with the depth growth, MCTS starts to manage
* possible explanation: the game favors the ghosts and MiniMax seems a better algorithm for smaller depths

MCTS vs MCTS: 2-8(5), 2-8(6), 3-7(7), 2-8(8), 3-7(9)
* the win-rate of Pacman stays at 20%-30%
* possible explanation: this win-rate may approach the real probability for Pacman to win
 
MCTS vs Hibrid: 2-8(5), 1-9(6), 1-9(7)
* with bigger depth the hybrid seems to be better
* possible explanation: the hybrid agent is better informed then MCTS and gets better with bigger depths
 
Hibrid vs MiniMax: 3-7(5), 4-6(6), 2-8(7)
* MiniMax and Hibrid seems to be relatively equal for small depths
* possible explanation: the hybrid can't get enough useful empirical information

Hibirid vs MCTS: 4-6(5), 2-8(6), 5-5(7)
* the hybrid is better than MCTS for these values of the depth
* possible explanation: information helps the hybrid get the edge

Hibrid vs Hibrid: 1-3(5)
* Pacman has 25% win-rate
* possible explanation: is in the expected win-rate of Pacman

## Conclusions

* relative ranking is Hibrid > MiniMax > MCTS > Random
* the game favors the ghosts because there are 2 of them and they can coordinate
* The hybrid is theoretically the best because it combines the empirical model of MCTS with the good state evaluation of MiniMax, but runs really slow.
* MiniMax is the algorithm i would choose because it runs relatively fast and it is good for this game because it is not as complicated(not like chess GO).
* MCTS is too complicated for this game, being beaten in most games by MiniMax and Hybrid. It gets better with bigger depths.
