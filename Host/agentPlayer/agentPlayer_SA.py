# coding=utf-8
import random
import json
from time import sleep

from Host.agentPlayer.prompt.prompt_SA import (select_card_prompt,
                                               select_color_prompt,
                                               select_challenge_prompt)

from Game.UNO import COLORS


class agentPlayer:
    def __init__(self, cards, player_id=None, agent=None):
        if agent is None:
            raise ValueError(
                'Invalid agent: agent is None'
            )
        if cards is None:
            raise ValueError(
                'Invalid cards: cards is None'
            )
        if player_id is None:
            raise ValueError(
                'Invalid player_id: player_id is None'
            )
        self.agent = agent
        self.hand = cards
        self.player_id = player_id
        self.choose_error_numbers = 0
        self.json_error_numbers = 0
        self.success_api_numbers = 0

    def __repr__(self) -> str:
        return '<AgentPlayer {}>'.format(self.player_id)

    def __str__(self) -> str:
        return str(self.player_id)

    def can_play(self, current_card) -> bool:
        return any(current_card.playable(card) for card in self.hand)

    def select_card(self, game=None):
        player_id = self.player_id
        opponent_id = (player_id + 1) % 2
        len_deck = len(game.deck)
        len_discard_pile = len(game.discard_pile)
        players = game.player_cycle.get_items()
        len_opponent_hand = len(players[opponent_id].hand)
        len_history = 20
        if len(game.history) == 0:
            history = "Details Currently Unknown"
        elif len(game.history) <= 20:
            len_history = len(game.history)
            history = game.history
        else:
            history = game.history[-20:]
        playable_card_index = []
        for index in range(len(self.hand)):
            if game.current_card.playable(self.hand[index]):
                playable_card_index.append(index)
        playable_card = []
        for index in playable_card_index:
            playable_card.append(f'{self.hand[index].color} {self.hand[index].card_type} [card index:{index}]')
        opponent_hand = []
        for card in players[opponent_id].hand:
            opponent_hand.append(f'{card.color} {card.card_type}')
        hand = []
        for card in self.hand:
            hand.append(f'{card.color} {card.card_type}')
        top_card = f"{game.current_card.get_color()} {game.current_card.card_type}"
        _select_card_prompt = self.create_select_card_prompt(player_id=player_id,
                                                             opponent_id=opponent_id,
                                                             len_deck=len_deck,
                                                             len_discard_pile=len_discard_pile,
                                                             len_opponent_hand=len_opponent_hand,
                                                             len_history=len_history,
                                                             history=history,
                                                             playable_card=playable_card,
                                                             hand=hand,
                                                             top_card=top_card)
        msg = {
            "role": 'user',
            "content": _select_card_prompt
        }
        self.success_api_numbers += 1
        while True:
            try:
                result, usage = self.agent.sse_invoke(msg=msg)
                break
            except Exception as e:
                print(f"SA error:{e}")
        JSON = self.analyze_JSON(result)
        if JSON is None:
            self.json_error_numbers += 1
            card_index = random.choice(playable_card_index)
        else:
            if JSON['action'] in playable_card_index:
                card_index = JSON['action']
            else:
                self.choose_error_numbers += 1
                card_index = random.choice(playable_card_index)
        return card_index, _select_card_prompt, result, usage

    def select_color(self, game=None, wild_type=None):
        player_id = self.player_id
        opponent_id = (player_id + 1) % 2
        len_deck = len(game.deck)
        len_discard_pile = len(game.discard_pile)
        players = game.player_cycle.get_items()
        len_opponent_hand = len(players[opponent_id].hand)
        len_history = 20
        if len(game.history) == 0:
            history = "Details Currently Unknown"
        elif len(game.history) <= 20:
            len_history = len(game.history)
            history = game.history
        else:
            history = game.history[-20:]
        playable_card_index = []
        for index in range(len(self.hand)):
            if game.current_card.playable(self.hand[index]):
                playable_card_index.append(index)
        playable_card = []
        for index in playable_card_index:
            playable_card.append(f'{self.hand[index].color} {self.hand[index].card_type} [card index:{index}]')
        hand = []
        for card in self.hand:
            hand.append(f'{card.color} {card.card_type}')
        opponent_hand = []
        for card in players[opponent_id].hand:
            opponent_hand.append(f'{card.color} {card.card_type}')
        top_card = f"{game.current_card.get_color()} {game.current_card.card_type}"
        _select_color_prompt = self.create_select_color_prompt(player_id=player_id,
                                                               opponent_id=opponent_id,
                                                               len_deck=len_deck,
                                                               len_discard_pile=len_discard_pile,
                                                               len_opponent_hand=len_opponent_hand,
                                                               len_history=len_history,
                                                               history=history,
                                                               hand=hand,
                                                               wild_type=wild_type,
                                                               top_card=top_card)
        msg = {
            "role": 'user',
            "content": _select_color_prompt
        }
        self.success_api_numbers += 1
        while True:
            try:
                result, usage = self.agent.sse_invoke(msg=msg)
                break
            except Exception as e:
                print(f"SA error:{e}")
        JSON = self.analyze_JSON(result)
        if JSON is None:
            self.json_error_numbers += 1
            new_color = random.choice(COLORS)
        else:
            if JSON['action'] in COLORS:
                new_color = JSON['action']
            else:
                self.choose_error_numbers += 1
                new_color = random.choice(COLORS)
        return new_color, _select_color_prompt, result, usage

    def select_challenge_black(self, game=None, new_color=None):
        player_id = self.player_id
        opponent_id = (player_id + 1) % 2
        len_deck = len(game.deck)
        len_discard_pile = len(game.discard_pile)
        players = game.player_cycle.get_items()
        len_opponent_hand = len(players[opponent_id].hand)
        len_history = 20
        if len(game.history) == 0:
            history = "Details Currently Unknown"
        elif len(game.history) <= 20:
            len_history = len(game.history)
            history = game.history
        else:
            history = game.history[-20:]
        playable_card_index = []
        for index in range(len(self.hand)):
            if game.current_card.playable(self.hand[index]):
                playable_card_index.append(index)
        playable_card = []
        for index in playable_card_index:
            playable_card.append(f'{self.hand[index].color} {self.hand[index].card_type} [card index:{index}]')
        hand = []
        for card in self.hand:
            hand.append(f'{card.color} {card.card_type}')
        opponent_hand = []
        for card in players[opponent_id].hand:
            opponent_hand.append(f'{card.color} {card.card_type}')
        old_color = game.current_card.get_color()
        top_card = f"{game.current_card.get_color()} {game.current_card.card_type}"
        _select_challenge_prompt = self.create_select_challenge_black_prompt(player_id=player_id,
                                                                             opponent_id=opponent_id,
                                                                             len_deck=len_deck,
                                                                             len_discard_pile=len_discard_pile,
                                                                             len_opponent_hand=len_opponent_hand,
                                                                             len_history=len_history,
                                                                             history=history,
                                                                             hand=hand,
                                                                             old_color=old_color,
                                                                             new_color=new_color,
                                                                             top_card=top_card)
        msg = {
            "role": 'user',
            "content": _select_challenge_prompt
        }
        self.success_api_numbers += 1
        while True:
            try:
                result, usage = self.agent.sse_invoke(msg=msg)
                break
            except Exception as e:
                print(f"SA error:{e}")
        JSON = self.analyze_JSON(result)
        if JSON is None:
            self.json_error_numbers += 1
            challenge_flag = random.choice([True, False])
        else:
            if JSON['action'] in ['Yes', 'No']:
                if JSON['action'] == 'Yes':
                    challenge_flag = True
                else:
                    challenge_flag = False
            else:
                self.choose_error_numbers += 1
                challenge_flag = random.choice([True, False])
        return challenge_flag, _select_challenge_prompt, result, usage

    @staticmethod
    def create_select_card_prompt(player_id=None,
                                  opponent_id=None,
                                  len_deck=None,
                                  len_discard_pile=None,
                                  len_opponent_hand=None,
                                  len_history=None,
                                  history=None,
                                  playable_card=None,
                                  hand=None,
                                  top_card=None):
        return eval(select_card_prompt)

    @staticmethod
    def create_select_color_prompt(player_id=None,
                                   opponent_id=None,
                                   len_deck=None,
                                   len_discard_pile=None,
                                   len_opponent_hand=None,
                                   len_history=None,
                                   history=None,
                                   hand=None,
                                   wild_type=None,
                                   top_card=None):
        return eval(select_color_prompt)

    @staticmethod
    def create_select_challenge_black_prompt(player_id=None,
                                             opponent_id=None,
                                             len_deck=None,
                                             len_discard_pile=None,
                                             len_opponent_hand=None,
                                             len_history=None,
                                             history=None,
                                             hand=None,
                                             old_color=None,
                                             new_color=None,
                                             top_card=None):
        return eval(select_challenge_prompt)

    @staticmethod
    def analyze_JSON(result):
        try:
            prefix_index = result.index('{')
            suffix_index = result.index('}')
            json_text = result[prefix_index:suffix_index + 1]
            JSON = json.loads(json_text)
            _ = JSON['action']
            return JSON
        except Exception as e:
            print(f"JSON error:{e}")
            return None

    def returnStatisticalData(self):
        return {
            "choose_error_numbers": self.choose_error_numbers,
            "json_error_numbers": self.json_error_numbers,
            "success_api_numbers": self.success_api_numbers
        }
