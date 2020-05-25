suits = 'CDHS'
ranks = '23456789TJQKA'
values = dict(zip(ranks, range(2, 2+len(ranks))))

from abc import ABCMeta, abstractmethod
import random
from enum import IntEnum

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()

class PKCard(Card):
    def __init__(self, Card):
        self.card = Card 
    
    def value(self):
        return values[self.card[0]]

    def __getitem__(self, index):
        return self.card[index]

class Deck:
    def __init__(self, cls):
        self.deck = [k+suit for  suit in suits for k in ranks]
        self.deck = [PKCard(i) for i in self.deck]

    def __str__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, index):
        return self.deck[index]

    def shuffle(self):
        random.shuffle(self.deck)

    def pop(self):
        return self.deck.pop()

class Ranking(IntEnum):
    High_Card = 0
    One_Pair = 1
    Two_Pair = 2
    Triple = 3
    Straight = 4
    Flush = 5
    Full_House = 6
    Four_Card = 7
    Straight_Flush = 8

class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = []
        for i in cards:
            self.cards.append(PKCard(i))
        self.cards = sorted(self.cards, reverse=True)
        self.ranking = None

    def _check(self,other):
        if self.ranking is None or other.ranking is None:
            raise AttributeError('not evaluated. call eval() method')

    def __repr__(self):
        return '-'.join([repr(c) for c in self.cards]) + ': ' + repr(self.ranking)

    def __eq__(self, other):
        self._check(other)
        return (self.ranking, self.cards) == (other.ranking, other.cards)

    def __gt__(self, other):
        self._check(other)
        return (self.ranking, self.cards) > (other.ranking, other.cards)

    def __lt__(self, other):
        self._check(other)
        return (self.ranking, self.cards) < (other.ranking, other.cards)

    def __ne__(self, other): return not self.__eq__(other)
    def __le__(self, other): return not self.__gt__(other)
    def __ge__(self, other): return not self.__lt__(other)

    def eval(self):
        flush = self.is_flush()
        if flush:
            if self.is_straight():
                self.ranking = Ranking.Straight_Flush
            else:
                self.ranking = Ranking.Flush
        elif self.is_straight():
            self.ranking = Ranking.Straight
        else:
            ranking = self.find_a_kind()
            self.ranking = Ranking(ranking)

    def is_flush(self):
        flush_suit = self.cards[0][1]
        count = 0
        for i in self.cards:
            if i[1] == flush_suit:
                count += 1
        if count == 5:
            return True 
        return False

    def is_straight(self):
        list_value = []
        for i in self.cards:
            list_value.append(i.value())
        list_value = list(set(list_value))
        list_value.sort(reverse=True)
        if len(list_value) == 5:
            if list_value[0]-list_value[4] == 4 :
                return list_value
            elif list_value[0]-list_value[4] == 12 and list_value[0]==14 and list_value[1]==5: # A, 2, 3, 4, 5 straight일 떄
                self.cards[0],self.cards[1],self.cards[2],self.cards[3],self.cards[4] = self.cards[1],self.cards[2],self.cards[3],self.cards[4],self.cards[0]
                return self.cards
        return None
    
    def classify_by_rank(self):
        dict_card = {}
        for i in self.cards:
            if i[0] in dict_card:
                dict_card[i[0]].append(i)
            else:
                dict_card[i[0]] = [i]
        if len(dict_card)==5:
            return None
        return dict_card

    def find_a_kind(self):
        classify_by_ranks = self.classify_by_rank()
        if classify_by_ranks == None:
            return 0
        else:
            sorted_c_b_r = sorted(classify_by_ranks.values(), key = lambda x: len(x),reverse=True)
            sorted_list = []
            for i in sorted_c_b_r:
                for j in i:
                    sorted_list.append(j)
            self.cards = sorted_list
            if len(classify_by_ranks) == 4:
                return 1
            elif len(classify_by_ranks) == 3:
                for i in classify_by_ranks.values():
                    if(len(i)==3):
                        return 3
                return 2
            elif len(classify_by_ranks) == 2:
                for i in classify_by_ranks.values():
                    if(len(i)==3):
                        return 6
                return 7

    def find_hand_ranking(self):
        straight = self.is_straight()
        flush = self.is_flush()
        if flush is True and straight is not None:
            return (8, self.cards)
        elif straight is not None:
            return (4, self.cards)
        elif flush is True:
            return (5, self.cards)
        else:
            return (self.find_a_kind(), self.cards)

    def tell_hand_ranking(self):
        hand_ranking = self.find_hand_ranking()
        rank = hand_ranking[0]
        rank_dict = {8:'Straight_Flush',7:'Four_Card',6:'Full_House',5:'Flush',4:'Straight',3:'Triple',2:'Two_Pair',1:'One_Pair',0:'High_Card'}
        return f'{rank_dict[rank]}'