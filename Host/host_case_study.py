import copy
import random
from random import choice
from Game import UNO
from Game.UNO import COLORS
from Game.UNO import CHALLENGE_BLACK
from workflow.utils import gameOver
from Host.agentPlayer.agentPlayer_SA import agentPlayer


class host:
    def __init__(self, deck=None, playerNumbers=None):
        if not isinstance(deck, list):
            raise ValueError("the deck should be a list. ")
        if not isinstance(playerNumbers, int) or not (2 <= playerNumbers <= 7):
            raise ValueError("the value of playerNumbers should be an int of size 2 to 7. ")
        self.playerNumbers = playerNumbers
        self.deck = deck
        self.discard_pile = []
        self.players = [UNO.rulePlayer(self.deal_cards(), index) for index in range(self.playerNumbers)]
        self.create_discard_pile()
        self.player_cycle = UNO.ReversibleCycle(self.players)
        self.game = UNO.UnoGame(deck=self.deck,
                                discard_pile=self.discard_pile,
                                player_cycle=self.player_cycle)

    def deal_cards(self):
        return [self.deck.pop(0) for _ in range(7)]

    def create_discard_pile(self):
        while True:
            card = self.deck.pop(0)
            self.discard_pile.append(card)
            if isinstance(card.card_type, int):
                break

    def startGame(self, agentPlayerIndex=None, agent=None):
        isActive = True
        turns = 0
        totalSD = []
        while isActive:
            turns += 1
            currentPlayer = self.game.current_player
            currentCard = self.game.current_card
            if currentPlayer.player_id == agentPlayerIndex:
                if currentPlayer.can_play(currentCard):
                    playableCardsIndex = []
                    for index, card in enumerate(currentPlayer.hand):
                        if currentCard.playable(card):
                            playableCardsIndex.append(index)
                    if len(playableCardsIndex) == 1:
                        cardIndex = playableCardsIndex[0]
                    else:
                        _agentPlayer = agentPlayer(
                                cards=self.game.player_cycle.get_items()[agentPlayerIndex].hand,
                                player_id=agentPlayerIndex,
                                agent=agent)
                        cardIndex, Input, Output, usage = _agentPlayer.select_card(game=self.game)
                    if currentPlayer.hand[cardIndex].color == 'Black':
                        wildType = currentPlayer.hand[cardIndex].card_type
                        _agentPlayer = agentPlayer(
                                cards=self.game.player_cycle.get_items()[agentPlayerIndex].hand,
                                player_id=agentPlayerIndex,
                                agent=agent)
                        newColor, Input, Output, usage = _agentPlayer.select_color(game=self.game, wild_type=wildType)
                        if currentPlayer.hand[cardIndex].card_type == 'Wild Draw Four':
                            challengeFlag = choice(CHALLENGE_BLACK)
                        else:
                            challengeFlag = None
                    else:
                        newColor = None
                        challengeFlag = None
                    isActive = self.game.play(card_id=cardIndex,
                                              new_color=newColor,
                                              challenge_flag=challengeFlag)
                    totalSD.append({
                        "turns": turns,
                        "game": copy.deepcopy(self.game),
                        "flag": True
                    })
                else:
                    isActive = self.game.play()
                    totalSD.append({
                        "turns": turns,
                        "game": copy.deepcopy(self.game),
                        "flag": True
                    })
            else:
                if currentPlayer.can_play(currentCard):
                    playableCardsIndex = []
                    for index, card in enumerate(currentPlayer.hand):
                        if currentCard.playable(card):
                            playableCardsIndex.append(index)
                    if len(playableCardsIndex) == 1:
                        cardIndex = playableCardsIndex[0]
                    else:
                        cardIndex = random.choice(playableCardsIndex)
                    if currentPlayer.hand[cardIndex].color == 'Black':
                        newColor = random.choice(COLORS)
                        _agentPlayer = agentPlayer(
                                cards=self.game.player_cycle.get_items()[agentPlayerIndex].hand,
                                player_id=agentPlayerIndex,
                                agent=agent)
                        if currentPlayer.hand[cardIndex].card_type == 'Wild Draw Four':
                            challengeFlag, Input, Output, usage = _agentPlayer.select_challenge_black(game=self.game,
                                                                                                     new_color=newColor)
                        else:
                            challengeFlag = None
                    else:
                        newColor = None
                        challengeFlag = None
                    isActive = self.game.play(card_id=cardIndex,
                                              new_color=newColor,
                                              challenge_flag=challengeFlag)
                    totalSD.append({
                        "turns": turns,
                        "game": copy.deepcopy(self.game),
                        "flag": False
                    })
                else:
                    isActive = self.game.play()
                    totalSD.append({
                        "turns": turns,
                        "game": copy.deepcopy(self.game),
                        "flag": False
                    })
        winners = gameOver(game=self.game, playerNumbers=self.playerNumbers)
        return {
            "totalWS": winners,
            "totalSD": totalSD
        }
