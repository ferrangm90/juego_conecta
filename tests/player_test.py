import pytest
from conecta_4.square_board import SquareBoard
from conecta_4.player import *


def test_valid_column():
    board = SquareBoard.from_list([['x', None, None, None],
                                  ['x', 'o', 'x', 'x'],
                                  ['o', 'o', 'x', 'x'],
                                  ['o', None, None, None]])

    assert HumanEntryVerifications._is_not_full(board, 0)
    assert HumanEntryVerifications._is_not_full(board, 1) == False
    assert HumanEntryVerifications._is_not_full(board, 2) == False
    assert HumanEntryVerifications._is_not_full(board, 0)

    assert HumanEntryVerifications._is_in_range(board, 0)
    assert HumanEntryVerifications._is_in_range(board, 1)
    assert HumanEntryVerifications._is_in_range(board, 2)
    assert HumanEntryVerifications._is_in_range(board, 3)
    assert HumanEntryVerifications._is_in_range(board, 5) == False
    assert HumanEntryVerifications._is_in_range(board, -5) == False
    assert HumanEntryVerifications._is_in_range(board, 15) == False


def test_is_int():
    assert HumanEntryVerifications._is_int('42')
    assert HumanEntryVerifications._is_int('0')
    assert HumanEntryVerifications._is_int('-40')
    assert HumanEntryVerifications._is_int('hola') == False
    assert HumanEntryVerifications._is_int('1.618') == False