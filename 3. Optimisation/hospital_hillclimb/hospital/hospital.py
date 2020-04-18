import random
random.seed(0)

class State():

    def __init__(self, board_h, board_w, n_houses, n_hospital):
        self.board_h = board_h
        self.board_w = board_w
        self.n_houses = n_houses

        self.board = self.create_empty_board(self.board_h, self.board_w)

        self.add_houses(n_houses)
        self.init_hospitals(n_hospital)



    def create_empty_board(self, board_h, board_w):
        board = []

        for i in range(board_h):
            board.append([None] * board_w)

        return board

    def add_houses(self, n_houses):
        spots = self.find_available_spots()
        self.houses = set()

        for i in range(n_houses):
            spot = random.sample(spots, 1)[0]
            spots.remove(spot)

            self.houses.add(spot)
            self.board[spot[0]][spot[1]] = 'h'

    def init_hospitals(self, n_hospital):
        spots = self.find_available_spots()
        self.hospitals = set()

        for i in range(n_hospital):
            spot = random.sample(spots, 1)[0]
            spots.remove(spot)

            self.hospitals.add(spot)
            self.board[spot[0]][spot[1]] = 'H'

    def find_available_spots(self):
        spots = set()

        for i in range(self.board_h):
            for j in range(self.board_w):
                if self.board[i][j] is None:
                    spots.add((i,j))

        return spots

    def calculate_cost(self):
        cost = 0

        for house in self.houses:
            min = self.board_h + self.board_w
            for hosp in self.hospitals:
                print(house, hosp)
                dist = self.calculate_distance(house, hosp)
                print(dist)
                min = dist if dist < min else min

            cost += min

        return cost

    def calculate_distance(self, pos1, pos2):
        x_dist = abs(pos1[1] - pos2[1])
        y_dist = abs(pos1[0] - pos2[0])

        return x_dist + y_dist




s = State(3, 3, 3, 1)
