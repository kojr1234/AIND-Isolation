"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
from math import sqrt

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y_me, x_me = game.get_player_location(player)

    dist_center = sqrt((h - y_me) ** 2 + (w - x_me) ** 2)
    future_moves = 0

    for move in game.get_legal_moves(player):
        _ = len(game.forecast_move(move).get_legal_moves(player))
        if _ > future_moves:
            future_moves = _

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(2*future_moves + (own_moves - opp_moves)/(1 + dist_center))


class CustomPlayer:

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left, it_dp=True):
        self.time_left = time_left
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            if it_dp:
                total_depth = 1
                while True:
                    depth = total_depth
                    best_move = self.alphabeta(game, depth)
                    total_depth += 1
            else:
                best_move = self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float("-inf")
        best_move = None
        for move in game.get_legal_moves():
            v = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if v > best_score:
                best_score = v
                best_move = move
            alpha = max(alpha, v)
        return best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        v = float('-inf')
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        v = float('inf')
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v