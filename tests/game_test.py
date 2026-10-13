import pytest
from conecta_4.game import Game
from conecta_4.match import Match
from conecta_4.player import Player
from conecta_4.square_board import *


def test_creation():
    g = Game()

    assert g is not None


def test_is_game_over():
    g = Game()
    g.match = Match(Player('Chip'), Player('Chop'))

    win_x = SquareBoard.from_list([['x', 'o', None, None],
                                  ['o', 'x', 'o', 'o'],
                                  ['o', 'x', 'x', 'o'],
                                  ['o', None, None, None]])

    win_o = SquareBoard.from_list([['o', 'x', None, None],
                                  ['x', 'o', 'o', 'o'],
                                  ['o', 'x', 'x', None],
                                  [None, None, None, None]])

    tie = SquareBoard.from_list([['x', 'o', 'x', 'o'],
                                ['o', 'x', 'o', 'x'],
                                ['o', 'x', 'o', 'x'],
                                ['x', 'o', 'x', 'o']])

    unfinished = SquareBoard.from_list([['x', 'o', None, None],
                                       [None, None, None, None],
                                       [None, None, None, None],
                                       [None, None, None, None]])

    g.board = win_x
    assert g._winner_or_tie() == True

    g.board = win_o
    assert g._winner_or_tie() == True

    g.board = tie
    assert g._winner_or_tie() == True

    g.board = unfinished
    assert g._winner_or_tie() == False

