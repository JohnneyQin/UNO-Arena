# coding=utf-8
import copy

from Host.agentPlayer.agentPlayer_SA_Arena import agentPlayer as SA
from Game import UNO
from Agent.agents import (GPT3Agent,
                          GPT4Agent,
                          LLAMA2Agent,
                          GLM3Agent,
                          GeminiAgent,
                          MistralAgent)

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

    def startGame(self, agentPlayerIndex=None):
        totalSD = {
            "gpt-3.5-turbo-16k-0613": [],
            "gpt-4-1106-preview": [],
            "gemini-pro": [],
            "Llama-2-7b-chat": [],
            "chatglm3-6b": [],
            "Mistral-7B-Instruct-v0.1": []
        }
        totalGS = {
            "gpt-3.5-turbo-16k-0613": [],
            "gpt-4-1106-preview": [],
            "gemini-pro": [],
            "Llama-2-7b-chat": [],
            "chatglm3-6b": [],
            "Mistral-7B-Instruct-v0.1": []
        }
        totalIO = {
            "gpt-3.5-turbo-16k-0613": [],
            "gpt-4-1106-preview": [],
            "gemini-pro": [],
            "Llama-2-7b-chat": [],
            "chatglm3-6b": [],
            "Mistral-7B-Instruct-v0.1": []
        }
        isActive = True
        turns = 0
        while isActive:
            turns += 1
            currentPlayer = self.game.current_player
            currentCard = self.game.current_card
            if currentPlayer.can_play(currentCard):
                playableCardsIndex = []
                for index, card in enumerate(currentPlayer.hand):
                    if currentCard.playable(card):
                        playableCardsIndex.append(index)
                if len(playableCardsIndex) == 1:
                    cardIndex = playableCardsIndex[0]
                else:
                    model = None
                    for key in agentPlayerIndex:
                        if agentPlayerIndex[key] == currentPlayer.player_id:
                            model = key
                            break
                    if model == "gpt-3.5-turbo-16k-0613":
                        agent = GPT3Agent("gpt-3.5-turbo-16k-0613")
                    elif model == "gpt-4-1106-preview":
                        agent = GPT4Agent("gpt-4-1106-preview")
                    elif model == "gemini-pro":
                        agent = GeminiAgent("gemini-pro")
                    elif model == "Llama-2-7b-chat":
                        agent = LLAMA2Agent("Llama-2-7b-chat")
                    elif model == "chatglm3-6b":
                        agent = GLM3Agent("chatglm3-6b")
                    elif model == "Mistral-7B-Instruct-v0.1":
                        agent = MistralAgent("Mistral-7B-Instruct-v0.1")
                    else:
                        raise ValueError("传入的model有问题")
                    agentPlayer = SA(cards=currentPlayer.hand,
                                     player_id=currentPlayer.player_id,
                                     agent=agent)
                    print(model)
                    cardIndex, Input, Output, usage = agentPlayer.select_card(game=self.game)
                    totalIO[model].append({
                        "turns": turns,
                        "select_card": {
                            "input": Input,
                            "output": Output,
                            "usage": usage
                        }
                    })
                    SD = agentPlayer.returnStatisticalData()
                    totalSD[model].append(SD)
                    if (SD["choose_error_numbers"] + SD["json_error_numbers"]) == 0:
                        totalGS[model].append({
                            "game": copy.deepcopy(self.game),
                            "flag": "select_card",
                            "turns": turns,
                            "data": {
                                "cardIndex": cardIndex
                            }
                        })
                if currentPlayer.hand[cardIndex].color == 'Black':
                    wildType = currentPlayer.hand[cardIndex].card_type
                    model = None
                    for key in agentPlayerIndex:
                        if agentPlayerIndex[key] == currentPlayer.player_id:
                            model = key
                            break
                    if model == "gpt-3.5-turbo-16k-0613":
                        agent = GPT3Agent("gpt-3.5-turbo-16k-0613")
                    elif model == "gpt-4-1106-preview":
                        agent = GPT4Agent("gpt-4-1106-preview")
                    elif model == "gemini-pro":
                        agent = GeminiAgent("gemini-pro")
                    elif model == "Llama-2-7b-chat":
                        agent = LLAMA2Agent("Llama-2-7b-chat")
                    elif model == "chatglm3-6b":
                        agent = GLM3Agent("chatglm3-6b")
                    elif model == "Mistral-7B-Instruct-v0.1":
                        agent = MistralAgent("Mistral-7B-Instruct-v0.1")
                    else:
                        raise ValueError("传入的model有问题")
                    agentPlayer = SA(cards=currentPlayer.hand,
                                     player_id=currentPlayer.player_id,
                                     agent=agent)
                    print(model)
                    newColor, Input, Output, usage = agentPlayer.select_color(game=self.game, wild_type=wildType)
                    totalIO[model].append({
                        "turns": turns,
                        "select_color": {
                            "input": Input,
                            "output": Output,
                            "usage": usage
                        }
                    })
                    SD = agentPlayer.returnStatisticalData()
                    totalSD[model].append(SD)
                    if (SD["choose_error_numbers"] + SD["json_error_numbers"]) == 0:
                        totalGS[model].append({
                            "game": copy.deepcopy(self.game),
                            "flag": "select_color",
                            "turns": turns,
                            "data": {
                                "cardIndex": cardIndex,
                                "color": newColor
                            }
                        })
                    if currentPlayer.hand[cardIndex].card_type == 'Wild Draw Four':
                        next_player = self.game.player_cycle.get_next_item(playerNumbers=self.playerNumbers)
                        model = None
                        for key in agentPlayerIndex:
                            if agentPlayerIndex[key] == next_player.player_id:
                                model = key
                                break
                        if model == "gpt-3.5-turbo-16k-0613":
                            agent = GPT3Agent("gpt-3.5-turbo-16k-0613")
                        elif model == "gpt-4-1106-preview":
                            agent = GPT4Agent("gpt-4-1106-preview")
                        elif model == "gemini-pro":
                            agent = GeminiAgent("gemini-pro")
                        elif model == "Llama-2-7b-chat":
                            agent = LLAMA2Agent("Llama-2-7b-chat")
                        elif model == "chatglm3-6b":
                            agent = GLM3Agent("chatglm3-6b")
                        elif model == "Mistral-7B-Instruct-v0.1":
                            agent = MistralAgent("Mistral-7B-Instruct-v0.1")
                        else:
                            raise ValueError("传入的model有问题")
                        agentPlayer = SA(cards=currentPlayer.hand,
                                         player_id=currentPlayer.player_id,
                                         agent=agent)
                        print(model)
                        challengeFlag, Input, Output, usage = agentPlayer.select_challenge_black(game=self.game, ID=next_player.player_id)
                        totalIO[model].append({
                            "turns": turns,
                            "select_challengeFlag": {
                                "input": Input,
                                "output": Output,
                                "usage": usage
                            }
                        })
                        SD = agentPlayer.returnStatisticalData()
                        totalSD[model].append(SD)
                        if (SD["choose_error_numbers"] + SD["json_error_numbers"]) == 0:
                            totalGS[model].append({
                                "game": copy.deepcopy(self.game),
                                "flag": "challengeFlag",
                                "turns": turns,
                                "data": {
                                    "cardIndex": cardIndex,
                                    "newColor": newColor,
                                    "challengeFlag": challengeFlag
                                }
                            })
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
            "totalGS": totalGS,
            "totalIO": totalIO,
            "totalSD": totalSD
        }
