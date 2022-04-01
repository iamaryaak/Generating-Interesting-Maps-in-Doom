# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random

import numpy as np

WALL_TYPE = np.int8
WALL = 0
EMPTY = 1


######################
#
#   Code change notes by Tilun: 
#    1. add function set_text
#    2. add line set_text
#    3. add function enermy_set
#
######################



class Maze:
    def __init__(self, rows, columns):
        if rows < 1 or columns < 1:
            raise ValueError("Invalid number rows or columns, must be greater than 1.")

        self.nrows = rows
        self.ncolumns = columns
        self.board = np.zeros((rows, columns), dtype=WALL_TYPE)
        self.board.fill(EMPTY)

    def __str__(self):
        return os.linesep.join(''.join('X' if self.is_wall(i, j) else ' '
                                       for j in range(self.ncolumns))
                               for i in range(self.nrows))

    def __hash__(self):
        return hash(self.board.tostring())

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def set_borders(self):
        self.board[0, :] = self.board[-1, :] = WALL
        self.board[:, 0] = self.board[:, -1] = WALL

    def is_wall(self, x, y):
        assert self.in_maze(x, y)
        return self.board[x][y] == WALL

    def set_wall(self, x, y):
        assert self.in_maze(x, y)
        self.board[x][y] = WALL
        
    def set_text(self, x, y, text_typ = 2, density = 0.05):
        if random.random() <= density: 
            assert self.in_maze(x, y)
            self.board[x][y] = text_typ
            
    def set_enermy(self, x, y, enermy_type):
            assert self.in_maze(x, y)
            self.board[x][y] = enermy_type

    def remove_wall(self, x, y):
        assert self.in_maze(x, y)
        self.board[x][y] = EMPTY

    def in_maze(self, x, y):
        return 0 <= x < self.nrows and 0 <= y < self.ncolumns
    
    def in_map(self, x, y):
        return 

    def write_to_file(self, filename):
        f = open(filename, 'w')
        f.write(str(self))
        f.close()

    @staticmethod
    def create_maze(rows, columns, seed=None, complexity=.7, density=.8):
        rows = (rows // 2) * 2 + 1
        columns = (columns // 2) * 2 + 1

        if seed is not None:
            np.random.seed(seed)

        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (rows + columns)))
        density = int(density * ((rows // 2) * (columns // 2)))

        maze = Maze(rows, columns)
        maze.set_borders()

        # Make aisles
        for i in range(density):
            x = np.random.random_integers(0, rows // 2) * 2
            y = np.random.random_integers(0, columns // 2) * 2
            maze.set_wall(x, y)
            # If wall, set the texture by density. 
            maze.set_text(x, y)

            for j in range(complexity):
                neighbours = []

                if maze.in_maze(x - 2, y):
                    neighbours.append((x - 2, y))

                if maze.in_maze(x + 2, y):
                    neighbours.append((x + 2, y))

                if maze.in_maze(x, y - 2):
                    neighbours.append((x, y - 2))

                if maze.in_maze(x, y + 2):
                    neighbours.append((x, y + 2))

                if len(neighbours):
                    next_x, next_y = neighbours[np.random.randint(
                        0,
                        len(neighbours) - 1)]

                    if not maze.is_wall(next_x, next_y):
                        maze.set_wall(next_x, next_y)
                        maze.set_wall(next_x + (x - next_x) // 2,
                                      next_y + (y - next_y) // 2)
                        x, y = next_x, next_y

        return maze
    
    def enermy_set (maze, rows, columns, enermy_num = 1, enermy_type = 99): 
        """
        Parameters
        ----------
        maze : maze
            The input maze with walls.
        enermy_num: int, optional
            The number of enermy been set into the map. 
            The default is 1.
            

        Returns maze
        -------
        """
        count = 0
        while enermy_num != 0 and count < 50: 
            x = np.random.random_integers(0, rows // 2) * 2
            y = np.random.random_integers(0, columns // 2) * 2
            if not maze.is_wall(x, y) and count <50: 
                maze.set_text(x, y, enermy_type)
                enermy_num -= 1
                count = 0
            else: 
                maze.set_text(x, y, enermy_type)
            count += 1

            
        return maze
        
            
        


def generate_mazes(maze_id, num, rows=9, columns=9, seed=None, complexity=.7, density=.7):
    """
    args: 

    maze_id: 
    num: (int) number of maps to generate (default: 10)
    rows: (int) maps row size (default: 9)
    columns: (int) maps column size (default: 9)
    seed: seed of the maze to generate
    """
    counter = 0
    mazes = set()
    ath = list()

    if seed:
        random.seed(seed)

    while len(mazes) < num:
        if counter > 5:
            raise ValueError('Unable to create the desired number of unique maps')

        map_seed = random.randint(0, 2147483647)

        maze = Maze.create_maze(columns + 1, rows + 1, map_seed, complexity=complexity, density=density)
        maze = Maze.enermy_set(maze, rows, columns, enermy_num = 1, enermy_type = 99)

        if maze in mazes:
            counter += 1
        else:
            counter = 0
            mazes.add(maze)
            ath.append(maze.board)
            
        ##Line added: to print maze
        return ath

    for idx, maze in enumerate(sorted(mazes, key=lambda x: hash(x))):
        # prefix = 'TRAIN' if idx in train_indices else 'TEST'

        maze.write_to_file("{}_MAP{:02d}.txt".format(
            maze_id, idx + 1))

    return mazes
