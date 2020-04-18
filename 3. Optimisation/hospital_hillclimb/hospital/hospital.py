import random
random.seed(0)

class State():

    def __init__(self, board_h, board_w, n_houses, n_hospital):
        self.board_h = board_h
        self.board_w = board_w
        self.n_houses = n_houses

        self.board = self.create_empty_board(self.board_h, self.board_w)
        self.init_available_spots()

        self.add_houses(n_houses)
        self.init_hospitals(n_hospital)

        print(self.board)
        print(self.houses)
        print(self.hospitals)



    def create_empty_board(self, board_h, board_w):
        board = []

        for i in range(board_h):
            board.append([None] * board_w)

        return board

    def add_houses(self, n_houses):
        self.houses = set()

        for i in range(n_houses):
            spot = random.sample(self.available_spots, 1)[0]
            self.available_spots.remove(spot)

            self.houses.add(spot)
            self.board[spot[0]][spot[1]] = 'h'

    def init_hospitals(self, n_hospital):
        self.hospitals = set()

        for i in range(n_hospital):
            spot = random.sample(self.available_spots, 1)[0]
            self.available_spots.remove(spot)

            self.hospitals.add(spot)
            self.board[spot[0]][spot[1]] = 'H'

    def init_available_spots(self):
        self.available_spots = set()

        for i in range(self.board_h):
            for j in range(self.board_w):
                if self.board[i][j] is None:
                    self.available_spots.add((i,j))



    def calculate_cost(self, hospitals):
        cost = 0

        for house in self.houses:
            min = self.board_h + self.board_w
            for hosp in hospitals:
                dist = self.calculate_distance(house, hosp)
                min = dist if dist < min else min

            cost += min

        return cost

    def calculate_distance(self, pos1, pos2):
        x_dist = abs(pos1[1] - pos2[1])
        y_dist = abs(pos1[0] - pos2[0])

        return x_dist + y_dist

    def hill_climb(self, max):
        cost = self.calculate_cost(self.hospitals)

        steps = 0
        for hosp in self.hospitals:
            change = True

            while change:
                change = False

                print('Hospital', hosp)
                moves = self.find_possible_moves(hosp)
                print('Moves', moves)

                new_pos = self.hospitals
                for m in moves:
                    # Add new hospital position and calculate cost
                    proposed_pos = self.hospitals.union({m}) - {hosp}
                    new_cost = self.calculate_cost(proposed_pos)

                    if new_cost < cost:
                        cost = new_cost
                        new_pos = proposed_pos
                        change = True
                        steps += 1

                if new_pos is not None:
                    print('New Hospital Position', new_pos)
                    self.hospitals = new_pos


        print(f'Total steps {steps}. Final position {self.hospitals}')
        print('Total cost: ', self.calculate_cost(self.hospitals))




    def find_possible_moves(self, hospital):
        all_moves = set()

        for i in [-1, 1]:
            h = hospital[0] + i
            if 0 <= h < self.board_h:
                all_moves.add((h, hospital[1]))

            w = hospital[1] + i
            if 0 <= w < self.board_w:
                all_moves.add((hospital[0], w))

        print('All moves', all_moves)

        poss_moves = all_moves.intersection(self.available_spots)

        return poss_moves




s = State(10, 10, 15, 5)
s.hill_climb(1)
