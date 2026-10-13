import pytest

from conecta_4.settings import BOARD_LENGTH
from conecta_4.oracle import *
from conecta_4.square_board import SquareBoard
from conecta_4.player import Player


def test_base_oracle():
    board = SquareBoard.from_list([[None, None, None, None],
                                  ['x', 'o', 'x', 'o'],
                                  ['o', 'o', 'x', 'x'],
                                  ['o', None, None, None]])

    expected = [ColumnRecommendations(0, ColumnClassification.MAYBE),
                ColumnRecommendations(1, ColumnClassification.FULL),
                ColumnRecommendations(2, ColumnClassification.FULL),
                ColumnRecommendations(3, ColumnClassification.MAYBE)]

    rappel = BaseOracle()

    assert len(rappel._get_recommendation(board, None)) == len(expected)
    assert rappel._get_recommendation(board, None) == expected


def test_equality():
    cr = ColumnRecommendations(2, ColumnClassification.MAYBE)

    assert cr == cr  # SON INDÉNTICOS
    assert cr == ColumnRecommendations(2, ColumnClassification.MAYBE)  # SON EQUIVALENTES

    # NO EQUIVALENTES

    assert cr != ColumnRecommendations(2, ColumnClassification.FULL)
    assert cr != ColumnRecommendations(3, ColumnClassification.FULL)

    # DOS OBJETOS EQUIVALES DEBEN DE TENER EL MISMO HASH. SI IMPLEMENTAMOS
    # METODO __EQ__ HAY QUE IMPLEMENTAR EL MÉTODO __HASH__


def test_hash():
    cr = ColumnRecommendations(2, ColumnClassification.MAYBE)
    assert hash(cr) == hash(ColumnRecommendations(2, ColumnClassification.MAYBE))


def test_is_winning_move():
    winner = Player('Xavier', 'x')
    loser = Player('Otto', 'o')

    empty = SquareBoard()
    almost = SquareBoard.from_list([['o', 'x', 'o', None],
                                   ['o', 'x', 'o', None],
                                   ['x', None, None, None],
                                   [None, None, None, None]])
    oracle = SmartOracle()

    for i in range(0, BOARD_LENGTH):
        assert oracle._is_winning_bet(empty, i, winner) == False
        assert oracle._is_winning_bet(empty, i, loser) == False

    for i in range(0, BOARD_LENGTH):
        assert oracle._is_winning_bet(almost, i, loser) == False

    assert oracle._is_winning_bet(almost, 2, winner)


