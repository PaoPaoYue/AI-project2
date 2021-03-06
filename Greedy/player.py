from _404NotFound_.algorithm.minimax import *
from _404NotFound_.env.board import *
from _404NotFound_.env.pos import *

from functools import reduce


class Player:

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.
        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        self.color = Color.white if colour == "white" else Color.black
        self.board = Board(True)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        color = self.color
        board = self.board

        def eval(board):
            self_pieces = board.get_pieces(color)
            other_pieces = board.get_pieces(opposite(color))
            self_pieces_num = sum(stack[1] for stack in self_pieces)
            other_pieces_num = sum(stack[1] for stack in other_pieces)

            boom_component = board.get_boom_component()
            boom_reward = []
            boom_penalty = []
            for i in range(len(boom_component[Color.white])):
                delta = self_pieces_num / other_pieces_num * boom_component[opposite(color)][i] - boom_component[color][
                    i]
                if delta > 0:
                    boom_reward.append(delta)
                else:
                    boom_penalty.append(-delta)

            ft = self_pieces_num / 0.01 if (other_pieces_num == 0) else self_pieces_num / other_pieces_num
            if other_pieces_num - sum(boom_reward) == 0:
                f0 = (self_pieces_num - sum(boom_penalty)) / 0.01
            else:
                f0 = (self_pieces_num - sum(boom_penalty)) / (other_pieces_num - sum(boom_reward))
            return (ft, f0)

        all_state = [(eval(s[0]), s) for s in board.all_possible_states(color)]
        all_state.sort(key=lambda pair: pair[0], reverse=True)
        largets_eval = all_state[0][0]
        best_states = [pair[1] for pair in all_state if pair[0] == largets_eval]
        import random
        return best_states[random.randint(0, len(best_states) - 1)][1]

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.
        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.
        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.
        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        self.board = self.board.apply_action(action)
