from random import choice
from math import sqrt, log
from representation import *


MAX, MIN = 1000, -1000


class Agent:
    def __init__(self, max_depth=0):
        self.max_depth = max_depth

    def get_action(self, state, player, last_action):
        pass


class Random(Agent):
    def random(self, state, player):
        return choice(state.get_available_actions(player))

    def get_action(self, state, player, last_action):
        return self.random(state, player)



class MiniMax(Agent):
    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def heuristic_pacman(self, state):
        food_distances  = [self.distance(state.pacman_pos, (i, j)) for i in range(1, state.height) for j in range(1, state.width) if state.maze[i][j] == 1]
        
        ghost_distances = [self.distance(state.pacman_pos, (i, j)) for (i, j) in state.ghosts_pos]        

        return min(ghost_distances) / ((1 + min(food_distances)) ** 2)

    def heuristic_ghosts(self, state):
        ghost_distances = [self.distance(state.pacman_pos, (i, j)) for (i, j) in state.ghosts_pos]

        return sum(ghost_distances)

    def minimax(self, state, depth, player, alpha, beta):        
        if depth == self.max_depth or state.is_final():
            if state.is_won():
                return MAX, None
            elif state.is_lost():
                return MIN, None

            return self.heuristic_pacman(state) if player == PACMAN else self.heuristic_ghosts(state), None

        best_action = None

        if player == PACMAN:
            action_cost = {}
            best = MIN

            for action in state.get_available_actions(player):
                new_state = state.apply_action(action, player)
                val, _ = self.minimax(new_state, depth + 1, 3 - player, alpha, beta)

                x, y = new_state.pacman_pos
                if state.maze[y][x] == 1 and new_state.maze[y][x] == 2:
                    val += 10

                if val > best:
                    best = val
                    best_action = action
  
                alpha = max(alpha, best)  
    
                if beta <= alpha:  
                    break 

            return best, best_action
        elif player == GHOSTS: 
            best = MAX 
    
            for action in state.get_available_actions(player):
                new_state = state.apply_action(action, player)
                val, _ = self.minimax(new_state, depth + 1, 3 - player, alpha, beta)

                val += choice([0, 1])

                if val < best:
                    best = val
                    best_action = action
  
                beta = min(beta, best)

                if beta <= alpha:  
                    break 
            
            return best, best_action

    def get_action(self, state, player, last_action):
        return self.minimax(state, 0, player, MIN, MAX)[1]


NEXT_PLAYER = 1
N = 'N'
Q = 'Q'

PARENT = 'parent'
ACTIONS = 'actions'

CP = 1.0 / sqrt(2.0)

class MCTS(Agent):
    memory = None

    def init_node(self, parent = None):
        return {N: 0, Q: 0, PARENT: parent, ACTIONS: {}}

    def select_action(self, node, c = CP):
        m = (-1, -1)
        
        N_node = node[N]

        for a in node[ACTIONS]:
            Q_a = node[ACTIONS][a][Q]
            N_a = node[ACTIONS][a][N]
            
            E = Q_a / N_a + c * sqrt(2 * log(N_node) / N_a)
            
            if E > m[1]:
                m = (a, E)

        return m[0]

    def get_next_state(self, state, player):
        return state.apply_action(choice(state.get_available_actions(player)), player)

    def mcts(self, state0, budget, tree, player, opponent_s_action = None):
        if opponent_s_action:
            opponent_s_action = tuple(opponent_s_action)

        if tree is not None and opponent_s_action in tree[ACTIONS]:
            tree = tree[ACTIONS][opponent_s_action]
        else:
            tree = self.init_node()

        for x in range(budget):
            state = state0
            node = tree
            
            while not state.is_final():
                actions = state.get_available_actions(player)
                
                if len(actions) > len(node[ACTIONS]):
                    break
                
                action = self.select_action(node)
                state = state.apply_action(action, player)
                node = node[ACTIONS][action]
                
            if not state.is_final():
                unexploredActions = []
                
                for action in state.get_available_actions(player):
                    if tuple(action) not in node[ACTIONS]:
                        unexploredActions.append(action)
                
                action = choice(unexploredActions)
                
                new_node = self.init_node(node)
                node[ACTIONS][tuple(action)] = new_node

                state = state.apply_action(action, player)
                node = new_node

            depth = 0
            current_player = player
            while not depth == budget and not state.is_final():
                state = self.get_next_state(state, current_player)
                current_player = 3 - current_player
                depth += 1

            if state.is_won():
                reward = 1
            elif state.is_lost():
                reward = 0.0
            else:
                reward = 0.5
            
            while node:
                node[Q] += reward
                node[N] += 1
                node = node[PARENT]
            
        if tree:
            final_action = self.select_action(tree, 0.0)
            return (final_action, tree[ACTIONS][final_action])

        if get_available_actions(state0):
            return (get_available_actions(state0)[0], init_node())
        return (0, None)

    def get_action(self, state, player, last_action):
        action, self.memory = self.mcts(state, 5 * self.max_depth, self.memory, player, last_action)

        return action


class Hibrid(MCTS):
    def __init__(self, max_depth=0):
        self.max_depth = max_depth
        self.minimax = MiniMax(max_depth)

    def get_next_state(self, state, player):
        action = self.minimax.get_action(state, player, None)
        return state.apply_action(action, player)