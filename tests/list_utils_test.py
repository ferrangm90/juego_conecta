import pytest
from conecta_4.list_utils import *

def test_find_n():
    #el pajar, la aguja y la cantidad de veces que está la aguja
    assert find_n([2, 3, 4, 5, 6], 2, -1) == False
    assert find_n([1, 2, 3, 4, 5], 42, 2) == False
    assert find_n([1, 2, 3, 4, 5], 2, 2) == False
    assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
    assert find_n([1, 2, 3, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)
    assert find_n([1, 2, 3, 4],'x' , 0)

def test_find_one():
    assert find_one([1, 2, 3, 4], 1)
    assert find_one([1, 2, 3, 4], 5) == False
    assert find_one([1, 2, 3, 4], 4)
    assert find_one([4, 4, 4, 4], 4)

def test_find_strike():
    assert find_strike([1, 2, 3, 4], 1, 3) == False
    assert find_strike([1, 1, 1, 4], 1, 3)
    assert find_strike([2, 1, 1, 1], 1, 3)
    assert find_strike([1, 2, 3, 4], 1, -3) == False
    assert find_strike([1, 2, 3, 4], 5, 3) == False
    assert find_strike([1, 1, 3, 1], 1, 3) == False

def test_make_list():
    assert make_list(4, None) == [None, None, None, None]

def test_index_first_element():
    assert index_first_element([1, 2, 3], 1) == 0
    assert index_first_element([1, 2, 3], 4) is None
