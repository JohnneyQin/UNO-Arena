import random
from random import choice
from Host.agentPlayer.agentPlayer_TR import agentPlayer
from Game import UNO
from Agent.agents import (GPT3Agent_chat,
                          GPT4Agent_chat,
                          LLAMA2Agent_chat,
                          GLM3Agent_chat,
                          GeminiAgent_chat,
                          MistralAgent_chat)
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

    def startGame(self, agentPlayerIndex=None, model=None):
        totalGS = []
        isActive = True
        turns = 0
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
                        if model == "gpt-3.5-turbo-16k-0613":
                            agent = GPT3Agent_chat("gpt-3.5-turbo-16k-0613")
                        elif model == "gpt-4-1106-preview":
                            agent = GPT4Agent_chat("gpt-4-1106-preview")
                        elif model == "gemini-pro":
                            agent = GeminiAgent_chat("gemini-pro")
                        elif model == "Llama-2-7b-chat":
                            agent = LLAMA2Agent_chat("Llama-2-7b-chat")
                        elif model == "chatglm3-6b":
                            agent = GLM3Agent_chat("chatglm3-6b")
                        elif model == "Mistral-7B-Instruct-v0.1":
                            agent = MistralAgent_chat("Mistral-7B-Instruct-v0.1")
                        else:
                            raise ValueError("传入的model参数有问题")
                        _agentPlayer = agentPlayer(
                            cards=self.game.player_cycle.get_items()[agentPlayerIndex].hand,
                            player_id=agentPlayerIndex,
                            agent=agent)
                        cardIndex, Input, Output, usage = _agentPlayer.select_card(game=self.game)
                    if currentPlayer.hand[cardIndex].color == 'Black':
                        wildType = currentPlayer.hand[cardIndex].card_type
                        if model == "gpt-3.5-turbo-16k-0613":
                            agent = GPT3Agent_chat("gpt-3.5-turbo-16k-0613")
                        elif model == "gpt-4-1106-preview":
                            agent = GPT4Agent_chat("gpt-4-1106-preview")
                        elif model == "gemini-pro":
                            agent = GeminiAgent_chat("gemini-pro")
                        elif model == "Llama-2-7b-chat":
                            agent = LLAMA2Agent_chat("Llama-2-7b-chat")
                        elif model == "chatglm3-6b":
                            agent = GLM3Agent_chat("chatglm3-6b")
                        elif model == "Mistral-7B-Instruct-v0.1":
                            agent = MistralAgent_chat("Mistral-7B-Instruct-v0.1")
                        else:
                            raise ValueError("传入的model参数有问题")
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
                else:
                    isActive = self.game.play()
            else:
                if currentPlayer.can_play(currentCard):
                    playableCardsIndex = []
                    for index, card in enumerate(currentPlayer.hand):
                        if currentCard.playable(card):
                            playableCardsIndex.append(index)
                    if len(playableCardsIndex) == 1:
                        cardIndex = playableCardsIndex[0]
                    else:
                        cardIndex = currentPlayer.select_card(current_card=currentCard)
                    if currentPlayer.hand[cardIndex].color == 'Black':
                        newColor = currentPlayer.select_color()
                        if currentPlayer.hand[cardIndex].card_type == 'Wild Draw Four':
                            if model == "gpt-3.5-turbo-16k-0613":
                                agent = GPT3Agent_chat("gpt-3.5-turbo-16k-0613")
                            elif model == "gpt-4-1106-preview":
                                agent = GPT4Agent_chat("gpt-4-1106-preview")
                            elif model == "gemini-pro":
                                agent = GeminiAgent_chat("gemini-pro")
                            elif model == "Llama-2-7b-chat":
                                agent = LLAMA2Agent_chat("Llama-2-7b-chat")
                            elif model == "chatglm3-6b":
                                agent = GLM3Agent_chat("chatglm3-6b")
                            elif model == "Mistral-7B-Instruct-v0.1":
                                agent = MistralAgent_chat("Mistral-7B-Instruct-v0.1")
                            else:
                                raise ValueError("传入的model参数有问题")
                            _agentPlayer = agentPlayer(
                                cards=self.game.player_cycle.get_items()[agentPlayerIndex].hand,
                                player_id=agentPlayerIndex,
                                agent=agent)
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
                else:
                    isActive = self.game.play()
        winners = gameOver(game=self.game, playerNumbers=self.playerNumbers)
        return {
            "totalWS": winners,
            "totalGS": totalGS
        }
