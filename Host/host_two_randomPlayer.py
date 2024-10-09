import copy
import random
from random import choice
from Game import UNO
from Game.UNO import COLORS
from Game.UNO import CHALLENGE_BLACK
from workflow.utils import gameOver


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

    def startGame(self):
        isActive = True
        while isActive:
            currentPlayer = self.game.current_player
            currentCard = self.game.current_card
            if currentPlayer.can_play(currentCard):
                playableCardsIndex = []
                for index, card in enumerate(currentPlayer.hand):
                    if currentCard.playable(card):
                        playableCardsIndex.append(index)
                cardIndex = random.choice(playableCardsIndex)
                if currentPlayer.hand[cardIndex].color == 'Black':
                    newColor = random.choice(COLORS)
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
            else:
                isActive = self.game.play()
        return gameOver(game=self.game, playerNumbers=self.playerNumbers)
