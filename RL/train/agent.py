from _404NotFound_ import player
from _404NotFound_.env.board import Color
from manual import player as human
import pickle
from timeit import default_timer as time

class Agent(player.Player):
    def __init__(self, color):
        super().__init__(color)
        self.lr = 0.2
        self.history = []

    def add_state_value(self, v):
        if v[0] not in self.state_values:
            self.state_values[v[0]] = v[1]

    def add_history(self, h):
        self.history.append(h)

    def reset_history(self):
        self.history = []

    def update_state_values(self, referee):
        reward = referee.reward(self.color)
        target = reward
        for prev in reversed(self.history):
            # Monte-Carlo learning
            value = self.state_values[prev] + self.lr*(target - self.state_values[prev])
            self.state_values[prev] = value
            target = value
        self.reset_history()
        self.board.__init__(True)

class Referee:
    def __init__(self):
        self.winner = None
        self.timer = time()

    def game_over(self, board):
        white_num = board.get_white()
        black_num = board.get_black()
        if (not white_num and not black_num) or (time() - self.timer > 80):
            return True
        elif not white_num:
            self.winner = Color.black
            return True
        elif not black_num:
            self.winner = Color.white
            return True
        else:
            return False

    def reward(self, color):
        return 1 if self.winner == color else 0



def play_game(p1, p2, referee, plot=False):
    current_player = None

    while True:
        current_player = p2 if current_player == p1 else p1

        # current_player.board.print()

        action = current_player.action()

        p1.update(current_player.color, action)
        p2.update(current_player.color, action)

        state = tuple(current_player.board.cells)
        p1.add_history(state)
        p2.add_history(state)

        if not referee.game_over(current_player.board):
            p1.add_state_value((state, 0.5))
            p2.add_state_value((state, 0.5))
            continue
        break

    p1.add_state_value((p1.history[-1], 1 if referee.winner == p1.color else -1))
    p2.add_state_value((p2.history[-1], 1 if referee.winner == p2.color else -1))

    p1.update_state_values(referee)
    p2.update_state_values(referee)

    # current_player.board.print()

def self_train(instance=5000, filename="", save_model=1):
    p1 = Agent('white')
    p2 = Agent('black')

    for t in range(instance):
        if t % 10 == 0:
            print(t)
        play_game(p1, p2, Referee())

    if save_model:
        with open(filename, 'wb') as f:
            # pickle.dump([p1, p2], f)
            pickle.dump([p1.state_values, p2.state_values], f)

def play_with_human(human_first, agent_name="Agents_N_4000_lr=05.pickle"):
    p1, p2 = pickle.load(open(agent_name, "rb"))
    if human_first:
        h = human.Player(Color.white)
        while True:
            play_game(h, p2, Referee(), plot=human_first)
    else:
        h = human.Player(Color.black)
        while True:
            play_game(p1, h, Referee(), plot=human_first)

if __name__ == "__main__":
    self_train(instance=100, filename="100_lr=02.pickle")
    # state_values_1, state_values_2 = pickle.load(open("100_lr=02.pickle", "rb"))
    # print(state_values_1)
    # print(state_values_2)
    # print(p1.state_values)