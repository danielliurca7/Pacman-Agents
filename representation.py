from copy import deepcopy


PACMAN, GHOSTS = 1, 2


class State:
    def __init__(self, height, width, maze, pacman_pos, ghosts_pos):
        self.height      = height
        self.width       = width
        self.maze        = maze
        self.pacman_pos  = pacman_pos
        self.ghosts_pos  = ghosts_pos


    def is_won(self):
        return [row for row in self.maze if 1 in row] == []


    def is_lost(self):
        return self.pacman_pos in self.ghosts_pos


    def is_final(self):
        return self.is_won() or self.is_lost()


    def get_available_moves(self, position):
        moves = []

        if self.maze[position[0]][position[1] - 1] != 0:
            moves.append('up')
        if self.maze[position[0]][position[1] + 1] != 0:
            moves.append('down')
        if self.maze[position[0] - 1][position[1]] != 0:
            moves.append('left')
        if self.maze[position[0] + 1][position[1]] != 0:
            moves.append('right')

        return moves


    def get_available_actions(self, player):
        if player == PACMAN:
            return self.get_available_moves(self.pacman_pos)
        elif player == GHOSTS:
            return [
                [move1, move2]
                for move1 in self.get_available_moves(self.ghosts_pos[0])
                for move2 in self.get_available_moves(self.ghosts_pos[1])
            ]


    def get_move(self, position, move):
        if move == 'up':
            return (position[0], position[1] - 1)
        if move == 'down':
            return (position[0], position[1] + 1)
        if move == 'left':
            return (position[0] - 1, position[1])
        if move == 'right':
            return (position[0] + 1, position[1])

        return None


    def move_pacman(self, action):
        if action in self.get_available_actions(PACMAN):
            self.pacman_pos = self.get_move(self.pacman_pos, action)

        x, y = self.pacman_pos

        if self.maze[y][x] == 1:
            self.maze[y][x] = 2

    def move_ghosts(self, actions):
        if actions in self.get_available_actions(GHOSTS):
            for ghost, action in enumerate(actions):
                self.ghosts_pos[ghost] = self.get_move(self.ghosts_pos[ghost], action)


    def apply_action(self, action, player):
        new_state = deepcopy(self)

        if player == PACMAN:
            new_state.move_pacman(action)
        elif player == GHOSTS:
            new_state.move_ghosts(action)

        return new_state