COLORS = ['Red', 'Yellow', 'Blue', 'Green']
ALL_COLORS = COLORS + ['Black']
NUMBERS = list(range(10)) + list(range(1, 10))
SPECIAL_CARD_TYPES = ['Skip', 'Reverse', 'Draw Two']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES * 2
BLACK_CARD_TYPES = ['Wild', 'Wild Draw Four']
CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES
CHALLENGE_BLACK = [True, False]


class ReversibleCycle:
    def __init__(self, iterable):
        self._items = list(iterable)
        self._pos = None
        self._reverse = False

    def __next__(self):
        if self.pos is None:
            self.pos = -1 if self._reverse else 0
        else:
            self.pos = self.pos + self._delta
        return self._items[self.pos]

    @property
    def _delta(self):
        return -1 if self._reverse else 1

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value % len(self._items)

    def reverse(self):
        self._reverse = not self._reverse

    def get_next_item(self, playerNumbers=None):
        pos = (self.pos + (-1 if self._reverse else 1)) % playerNumbers
        return self._items[pos]

    def get_items(self):
        return self._items


class UnoCard:
    def __init__(self, color, card_type):
        self._validate(color, card_type)
        self.color = color
        self.card_type = card_type
        self.temp_color = None

    def __repr__(self):
        return '<UnoCard object: {} {}>'.format(self.color, self.card_type)

    def __eq__(self, other):
        return self.color == other.color and self.card_type == other.card_type

    @staticmethod
    def _validate(color, card_type):
        if color not in ALL_COLORS:
            raise ValueError('Invalid color')
        if color == 'Black' and card_type not in BLACK_CARD_TYPES:
            raise ValueError('Invalid card type')
        if color != 'Black' and card_type not in COLOR_CARD_TYPES:
            raise ValueError('Invalid card type')

    def get_color(self):
        return self.temp_color if self.temp_color else self.color

    def set_temp_color(self, color):
        self.temp_color = color

    def playable(self, other):
        return (
                self.get_color() == other.color or
                self.card_type == other.card_type or
                other.color == 'Black'
        )


class rulePlayer:
    def __init__(self, cards, player_id=None):
        self.hand = cards
        self.player_id = player_id

    def can_play(self, current_card):
        return any(current_card.playable(card) for card in self.hand)

    def select_card(self, current_card=None):
        while True:
            for index, card in enumerate(self.hand):
                if card.card_type == current_card.card_type and card.color != 'Black':
                    return index
            for index, card in enumerate(self.hand):
                if card.color == current_card.get_color():
                    return index
            for index, card in enumerate(self.hand):
                if card.card_type == 'Wild':
                    return index
            for index, card in enumerate(self.hand):
                if card.card_type == 'Wild Draw Four':
                    return index

    def select_color(self):
        color_dict = {}
        for color in COLORS:
            color_dict[color] = 0
        for card in self.hand:
            if card.color != 'Black':
                color_dict[card.color] += 1
        max_value = color_dict['Red']
        max_value_color = 'Red'
        for key in color_dict:
            if color_dict[key] > max_value:
                max_value = color_dict[key]
                max_value_color = key
        return max_value_color


class UnoGame:
    def __init__(self, deck: list, discard_pile: list, player_cycle):
        self.deck = deck
        self.discard_pile = discard_pile
        self.player_cycle = player_cycle
        self.current_player = next(self.player_cycle)
        self.history = []
        self.played_cards = [self.discard_pile[-1]]
        self.rounds = 0

    def __next__(self):
        self.current_player = next(self.player_cycle)

    def pick_up(self, player, n):
        if len(self.deck) < n:
            return False
        else:
            penaltyCards = [self.deck.pop(0) for _ in range(n)]
            player.hand.extend(penaltyCards)
            return True

    @property
    def current_card(self):
        return self.discard_pile[-1]

    def play(self, card_id=None, new_color=None, challenge_flag=None):
        self.rounds += 1
        player = self.current_player
        if card_id is None:
            if self.pick_up(player, 1):
                history_info = f"it is No.{self.rounds} turn, the player{player.player_id} drew a card. "
                self.history.append(history_info)
                next(self)
                return True
            else:
                return False
        played_card = player.hand.pop(card_id)
        if len(player.hand) == 0:
            return False
        self.discard_pile.append(played_card)
        card_color = played_card.color
        card_type = played_card.card_type
        flag = True
        challenge_succeed_flag = False
        history_info = None
        if card_color == 'Black':
            self.current_card.set_temp_color(color=new_color)
            if card_type == 'Wild Draw Four':
                next(self)
                if challenge_flag:
                    for card in player.hand:
                        if card.color == self.discard_pile[-2].get_color():
                            challenge_succeed_flag = True
                            break
                    if challenge_succeed_flag:
                        flag = self.pick_up(player, 4)
                        history_info = (f"it is No.{self.rounds} round, "
                                        f"the player{player.player_id} played a Wild Draw Four card, "
                                        f"and declared the next color to be matched is {new_color}. "
                                        f"The player{self.current_player.player_id} "
                                        f"selected to challenge the use of the Wild Draw Four card, "
                                        f"and he succeeded. So, the player{player.player_id} drew 4 cards. ")
                    else:
                        flag = self.pick_up(self.current_player, 6)
                        history_info = (f"it is No.{self.rounds} round, "
                                        f"the player{player.player_id} played a Wild Draw Four card, "
                                        f"and declared the next color to be matched is {new_color}. "
                                        f"The player{self.current_player.player_id} "
                                        f"selected to challenge the use of the Wild Draw Four card, "
                                        f"but he failed. So, the player{self.current_player.player_id} drew 6 cards. ")
                else:
                    flag = self.pick_up(self.current_player, 4)
                    history_info = (f"it is No.{self.rounds} turn, "
                                    f"the player{player.player_id} played a Wild Draw Four card, "
                                    f"and declared the next color to be matched is {new_color}.  "
                                    f"The player{self.current_player.player_id} "
                                    f"selected not to challenge the use of the Wild Draw Four card. "
                                    f"So, the player{self.current_player.player_id} drew 4 cards. ")
            else:
                history_info = (f"it is No.{self.rounds} turn, "
                                f"the player{player.player_id} played a Wild card, "
                                f"and declared the next color to be matched is {new_color}. ")
        elif card_type == 'Reverse':
            self.player_cycle.reverse()
        elif card_type == 'Skip':
            next(self)
        elif card_type == 'Draw Two':
            next(self)
            flag = self.pick_up(player=self.current_player, n=2)
        if history_info is None:
            history_info = (f"it is No.{self.rounds} turn, "
                            f"the player{player.player_id} played a {played_card.color} {played_card.card_type} card. ")
        if flag:
            if challenge_succeed_flag:
                pass
            else:
                next(self)
            self.history.append(history_info)
            return True
        else:
            return False
