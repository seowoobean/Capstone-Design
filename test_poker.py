import pytest
from PA5 import Hands, Ranking, PKCard
import random

non_flush_suit = 'CHSDS'
flush_suit = 'SSSSS'
test_cases = {
    Ranking.Straight_Flush: (
        tuple(zip('AKQJT', flush_suit)),
        tuple(zip('KQJT9', flush_suit)),
    ),
    Ranking.Four_Card: (
        tuple(zip('TTTTQ', non_flush_suit)),
        tuple(zip('9999A', non_flush_suit)),
    ),
    Ranking.Full_House: (
        tuple(zip('88877', non_flush_suit)),
        tuple(zip('22299', non_flush_suit)),
    ),
    Ranking.Flush: (
        tuple(zip('AJT98', flush_suit)),
        tuple(zip('AJ987', flush_suit)),
    ),
    Ranking.Straight: (
        tuple(zip('AKQJT', non_flush_suit)),
        tuple(zip('KQJT9', non_flush_suit)),
        tuple(zip('5432A', non_flush_suit)),
    ),
    Ranking.Triple: (
        tuple(zip('888A9', non_flush_suit)),
        tuple(zip('888A7', non_flush_suit)),
    ),
    Ranking.Two_Pair: (
        tuple(zip('AA998', non_flush_suit)),
        tuple(zip('AA778', non_flush_suit)),
        tuple(zip('JJTTK', non_flush_suit)),
    ),
    Ranking.One_Pair: (
        tuple(zip('88AT9', non_flush_suit)),
        tuple(zip('88AT7', non_flush_suit)),
        tuple(zip('77AKQ', non_flush_suit)),
    ),
    Ranking.High_Card: (
        tuple(zip('AJT98', non_flush_suit)),
        tuple(zip('AJT97', non_flush_suit)),
        tuple(zip('QJT97', non_flush_suit)),
    ),
}

def cases(*rankings):
    if not rankings:
        rankings = test_cases.keys()
    return \
        [ ([r+s for r, s in case], ranking) 
                    for ranking in rankings
                        for case in test_cases[ranking]
        ]

@pytest.mark.parametrize("faces, expected", cases(Ranking.Straight))
def test_is_straight(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_straight()
    assert result != None
    assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", cases(Ranking.Flush))
def test_is_flush(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_flush()
    assert result == True
    assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", 
        cases(Ranking.Four_Card, Ranking.Triple, 
            Ranking.Two_Pair, Ranking.One_Pair))
def test_is_find_a_kind(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.find_a_kind()
    assert result == expected
    assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", cases(Ranking.High_Card))
def test_is_find_a_kind_None(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.find_a_kind()
    assert result == 0
    assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", cases())
def test_eval(faces, expected):
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    hand.eval()
    assert hand.ranking == expected

def test_who_wins():
    hand_cases = [Hands(faces) for faces, ranking in cases()]
    for hand in hand_cases:
        hand.eval()
    print(hand_cases)
    sorted_cases = sorted(hand_cases, reverse=True)
    print(sorted_cases)
    assert sorted_cases == hand_cases
    print('\nHigh to low order:')
    for i, hand in enumerate(hand_cases):
        print(i, hand)
