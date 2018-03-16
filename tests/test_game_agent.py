"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import sample_players
from importlib import reload
import competition_agent

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_example(self):
        # TODO: All methods must start with "test_"
        count_victory = 0
        count_forfeit = 0
        total = 100
        for i in range(total):
            player2 = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score_2)
            player1 = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score)
            #player2 = sample_players.GreedyPlayer()
            game = isolation.Board(player1, player2)
            game.apply_move((2, 3))
            game.apply_move((0, 5))
            print(game.to_string())
            # players take turns moving on the board, so player1 should be next to move
            assert (player1 == game.active_player)

            # play the remainder of the game automatically -- outcome can be "illegal
            # move", "timeout", or "forfeit"
            winner, history, outcome = game.play()
            print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
            print(game.to_string())
            print("Move history:\n{!s}".format(history))

            if winner == player1:
                count_victory += 1

            if outcome == "forfeit" and winner != player1:
                count_forfeit += 1

        print("Won {} times in a total of {} games, representing {} % of victory rate. "
              "{} forfeits occurred".format(count_victory, total, float((count_victory/total) * 100), count_forfeit))

if __name__ == '__main__':
    unittest.main()
