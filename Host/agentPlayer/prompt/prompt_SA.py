select_card_prompt = ("f\""
                      f"You are playing a two-player UNO game. \\n"
                      f"You are the player{{player_id}}, and your opponent is the player{{opponent_id}}. \\n"

                      f"Currently, there are {{len_deck}} cards in the deck, "
                      f"and the discard pile has {{len_discard_pile}} cards. \\n"
                      f"The number of cards in the hand of your opponent is {{len_opponent_hand}}. \\n"
                      f"The game history of the last {{len_history}} rounds is {{history}}. \\n"
                      f"Your entire hand consists of {{hand}}. \\n"
                      f"The cards you can play are: {{playable_card}}. \\n"

                      f"Please note that you are not playing a normal UNO game, "
                      f"if the cards in the deck are depleted, "
                      f"the person who has the minimum cards will win directly. \\n"
                      f"The goal of the game is to minimize the number of cards in your possession. \\n"

                      f"In order to win the UNO game, "
                      f"you must consider all the provided information and select "
                      f"the best card from the cards you can play. \\n"

                      f"The output should strictly be a JSON object with two keys: 'thoughts' and 'action'.\\n "
                      f"In this context, "
                      f"the value corresponding to the 'thoughts' key represents your thoughts and considerations, "
                      f"with its data type being a string. \\n"
                      f"Simultaneously, the value corresponding to the 'action' key is a int which "
                      f"represents the card index of the card you have selected."
                      f"\"")
select_color_prompt = ("f\"You are playing a two-player UNO game. \\n"
                       f"You are the player{{player_id}}, and your opponent is the player{{opponent_id}}. \\n"

                       f"Currently, there are {{len_deck}} cards in the deck, "
                       f"and the discard pile has {{len_discard_pile}} cards. \\n"
                       f"The number of cards in the hand of your opponent is {{len_opponent_hand}}. \\n"
                       f"The game history of the last {{len_history}} rounds is {{history}}. \\n"
                       f"Your entire hand consists of {{hand}}. "

                       f"Please note that you are not playing a normal UNO game, "
                       f"if the cards in the deck are depleted, "
                       f"the person who has the minimum cards will win directly. "
                       f"The goal of the game is to minimize the number of cards in your possession. "

                       f"In order to win the UNO game, you just played a {{wild_type}} card, "
                       f"and you must consider all the provided information and select the best color from "
                       f"Red, Yellow, Blue and Green to switch. "

                       f"The output should strictly be a JSON object with two keys: 'thoughts' and 'action'. "
                       f"In this context, the value corresponding to the 'thoughts' key represents "
                       f"your thoughts and considerations, "
                       f"with its data type being a string. "
                       f"Simultaneously, the value corresponding to the 'action' key is one of "
                       f"Red, Yellow, Blue or Green, indicating the color you have selected.\"")

select_challenge_prompt = ("f\"You are playing a two-player UNO game. \\n "
                           f"You are the player{{player_id}}, and your opponent is the player{{opponent_id}}. \\n"

                           f"Currently, there are {{len_deck}} cards in the deck, "
                           f"and the discard pile has {{len_discard_pile}} cards. \\n"
                           f"The number of cards in the hand of your opponent is {{len_opponent_hand}}. \\n"
                           f"The game history of the last {{len_history}} rounds is {{history}}. \\n"
                           f"Your entire hand consists of {{hand}}. "

                           f"Your opponent played a Wild Draw Four card, "
                           f"and changed the color of the current discard pile's top card to {{new_color}}. "
                           f"But the use of the Wild Draw Four card may be illegal,"
                           f"when your opponent still has cards in {{old_color}}. \\n"

                           f"Please note that you are not playing a normal UNO game, "
                           f"if the cards in the deck are depleted, "
                           f"the person who has the minimum cards will win directly. "
                           f"The goal of the game is to minimize the number of cards in your possession. "

                           f"In order to win the UNO game, "
                           f"you must consider all the provided information and select whether to "
                           f"challenge the use of the Wild Draw Four card which played by your opponent. "

                           f"The output should strictly be a JSON object with two keys: 'thoughts' and 'action'. "
                           f"In this context, the value corresponding to the 'thoughts' key represents "
                           f"your thoughts and considerations, with its data type being a string. "
                           f"Simultaneously, the value corresponding to the 'action' key is 'Yes' or 'No', "
                           f"indicating that you select to challenge or not to challenge, respectively.\"")