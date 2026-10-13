import pytest
from conecta_4.player import Player, HumanPlayer
from conecta_4.match import Match

@pytest.fixture
def humano():
    return HumanPlayer('Humano')
@pytest.fixture
def ordenador():
    return Player('Ordenador')

def test_different_players_have_different_chars():
    t = Match(humano, ordenador)
    assert humano.char != ordenador.char

def test_no_player_with_none_char():
    t = Match(humano, ordenador)

    assert humano.char != None
    assert ordenador.char != None

def test_next_player_is_round_robbin():
    t = Match(humano, ordenador)
    p1 = t.get_next_player
    p2 = t.get_next_player
    assert p1 != p2

def test_players_are_opponents(humano, ordenador):
    t = Match(humano, ordenador)
    p1 = t.get_next_player
    p2 = t.get_next_player
    assert p1.opponent is p2
    assert p2.opponent is p1