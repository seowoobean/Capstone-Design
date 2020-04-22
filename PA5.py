suits = 'CDHS'
ranks = '23456789TJQKA'
values = dict(zip(ranks, range(2, 2+len(ranks))))

from abc import ABCMeta, abstractmethod
import random

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

class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = []
        for i in cards:
            self.cards.append(PKCard(i))
        self.cards = sorted(self.cards, reverse=True)

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
                return list_value
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
        rank_dict = {8:'Straight Flush',7:'Four Card',6:'Full House',5:'Flush',4:'Straight',3:'Triple',2:'Two Pair',1:'One Pair',0:'High Card'}
        return f'{rank_dict[rank]}'

    def find_winner(self,other):
        self_hand_ranking = self.find_hand_ranking()
        other_hand_ranking = other.find_hand_ranking()
        if self_hand_ranking[0] > other_hand_ranking[0]:
            return True
        elif self_hand_ranking[0] < other_hand_ranking[0]:
            return False
        else:
            if self.cards[0].value() > other.cards[0].value():
                return True
            elif self.cards[0].value() < other.cards[0].value():
                return False
            else:
                if self_hand_ranking[0] == 2 or 1:
                    if self.cards[2].value() > other.cards[2].value():
                        return True
                    elif self.cards[2].value() < other.cards[2].value():
                        return False
                    else:
                        if self.cards[3].value() > other.cards[3].value():
                            return True
                        elif self.cards[3].value() < other.cards[3].value():
                            return False
                        else:
                            if self.cards[4].value() > other.cards[4].value():
                                return True
                            elif self.cards[4].value() < other.cards[4].value():
                                return False
                return None

if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()

    my_hand = []
    your_hand = []
    for i in range(5):
        for hand in (my_hand, your_hand):
            card = deck.pop()
            hand.append(card)
    print(my_hand)
    print(your_hand)


    #Test Straight Flush
    card = ['5C','6C', '7C', '8C', '9C']
    test(Hands(card).tell_hand_ranking() == 'Straight Flush')
    #Test Straight
    card = ['5C', '6H', '7C', '8C', '9S']
    test(Hands(card).tell_hand_ranking() == 'Straight')
    #Test flush
    card = ['5C', 'AC', 'QC', 'AC', 'TC']
    test(Hands(card).tell_hand_ranking() == 'Flush')
    #Test Four card
    card = ['AC', 'AH', 'AS', 'AD', '9S']
    test(Hands(card).tell_hand_ranking() == 'Four Card')
    #Test Full House
    card = ['2C', '2H', '2S', 'KH', 'KS']
    test(Hands(card).tell_hand_ranking() == 'Full House')
    #Test Triple
    card = ['3C', '3H', '3D', 'QH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'Triple')
    #Test Two Pair
    card = ['3C', '3H', 'QD', 'QH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'Two Pair')
    #Test One Pair
    card = ['AC', '7H', '3D', 'JH', 'JD']
    test(Hands(card).tell_hand_ranking() == 'One Pair')
    #Test One Pair
    card = ['8C', '9H', 'AD', 'TH', 'KD']
    test(Hands(card).tell_hand_ranking() == 'High Card')

    #Test same rank but value is different in Straight flush
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank but value is different in flush
    my_hand = Hands(['5C','6C', '7C', '8C', 'TC'])
    your_hand = Hands(['TH','AH', '7H', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank but value is different in Straight
    my_hand = Hands(['5C','6H', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7D', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank but value is different in Four card
    my_hand = Hands(['5C','5S', '5D', '5H', '9C'])
    your_hand = Hands(['2C','2S', '2D', '2H', '9H'])
    test(my_hand.find_winner(your_hand) == True)
    #Test same rank but value is different in Full House
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['TH','6H', '7H', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank but value is different in Triple
    my_hand = Hands(['5C','5H', '5D', '8C', '9C'])
    your_hand = Hands(['TH','TS', 'TD', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank first value but second value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '2H', '2D', '9H'])
    test(my_hand.find_winner(your_hand) == True)
    #Test same rank, first value and second value but last value is different in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', 'TH'])
    test(my_hand.find_winner(your_hand) == False)
    #Test same rank, all value in Two Pair
    my_hand = Hands(['AC','AD', '7C', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '7D', '9H'])
    test(my_hand.find_winner(your_hand) == None)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', '7H', '6D', '9H'])
    test(my_hand.find_winner(your_hand) == True)
    #Test same rank, value is Difference in One Pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '6D', '9H'])
    test(my_hand.find_winner(your_hand) == True)
    #Test same rank in One pair
    my_hand = Hands(['AC','AD', 'QC', '7S', '9C'])
    your_hand = Hands(['AH','AS', 'QH', '7D', '9H'])
    test(my_hand.find_winner(your_hand) == None)
    #Straight Flush vs High Card
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['8C', '9H', 'AD', 'TH', 'KD'])
    test(my_hand.find_winner(your_hand) == True)
    #if same rank and value, winner is None
    my_hand = Hands(['5C','6C', '7C', '8C', '9C'])
    your_hand = Hands(['5H','6H', '7H', '8H', '9H'])
    test(my_hand.find_winner(your_hand) == None)