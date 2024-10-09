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

select_card_calibration_first = ("f\""
                                 f"Here is the statistical data of the game history: \\n"
                                 f"{{history_summary}} \\n"

                                 f"Now, in order to win the game, "
                                 f"you must consider the statistical data carefully "
                                 f"and reflect the action you just selected. \\n"

                                 f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                 f"The value corresponding to the 'reflection' key is your reflection. "
                                 f"The value corresponding to the 'action' key "
                                 f"is the card index you currently select. "
                                 f"\"")

select_color_calibration_first = ("f\""
                                  f"Here is the statistical data of the game history: \\n"
                                  f"{{history_summary}} \\n"

                                  f"Now, in order to win the game, "
                                  f"you must consider the statistical data carefully "
                                  f"and reflect the action you just selected. \\n"

                                  f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                  f"The value corresponding to the 'reflection' key is your reflection. "
                                  f"The value corresponding to the 'action' key "
                                  f"is the color you currently select."
                                  f"\"")

select_challenge_calibration_first = ("f\""
                                      f"Here is the statistical data of the game history: \\n"
                                      f"{{history_summary}} \\n"

                                      f"Now, in order to win the game, "
                                      f"you must consider the statistical data carefully "
                                      f"and reflect the action you just selected. \\n"

                                      f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                      f"The value corresponding to the 'reflection' key is your reflection. "
                                      f"The value corresponding to the 'action' key "
                                      f"is the choice you currently select."
                                      f"\"")

select_card_calibration_second = ("f\""
                                  f"Here is an useful tip that you can follow: \\n"
                                  f"The card values range from low to high, starting with number cards 0, followed by number cards (1-9), reverse cards, skip cards and wild cards. It is better to start with low-value cards before playing high-value cards. Unless your opponent is on the verge of victory, it is time to play some high-value cards to disrupt your opponent's strategy. \\n"

                                  f"Now, in order to win the game, "
                                  f"you should reflect the action you just selected based on the tip. "

                                  f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                  f"The value corresponding to the 'reflection' key is your reflection. "
                                  f"The value corresponding to the 'action' key "
                                  f"is the final card index you currently select."
                                  f"\"")

select_color_calibration_second = ("f\""
                                   f"Here are some useful tips that you can follow: \\n"
                                   f"1. It is better to select the color with the highest frequency of occurrence in your hand. \\n"
                                   f"2. It is better to avoid selecting the color with the lowest frequency of occurrence in your hand. \\n"
                                   f"3. Consider carefully which color of cards is relatively more frequent in your opponent's hand and try to avoid selecting that color. \\n"

                                   f"Now, in order to win the game, "
                                   f"you should reflect the action you just selected based on these tips. "

                                   f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                   f"The value corresponding to the 'reflection' key is your reflection. "
                                   f"The value corresponding to the 'action' key "
                                   f"is the final color you currently select."
                                   f"\"")

select_challenge_calibration_second = ("f\""
                                       f"Here are some useful tips that you can follow: \\n"
                                       f"1. Please remember the penalty for a failed challenge: you must draw 6 cards. \\n"
                                       f"2. Please remember the benefits of a successful challenge: your opponent must draw 4 cards. \\n"
                                       f"3. Wild Draw Four is only illegal if your opponent has cards of {{old_color}} color in his hand. Please carefully consider whether your opponent's Wild Draw Four card is genuinely illegal. \\n"

                                       f"Now, in order to win the game, "
                                       f"you should reflect the action you just selected based on these tips. "

                                       f"You should strictly output a JSON object with two keys: 'reflection' and 'action'. "
                                       f"The value corresponding to the 'reflection' key is your reflection. "
                                       f"The value corresponding to the 'action' key "
                                       f"is the final choice you currently select."
                                       f"\"")