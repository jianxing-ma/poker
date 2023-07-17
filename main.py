#!/user/bin/python3

import math
import random

from poker import *

# HANDLEVEL = {
#     0: "HIGH-CARD",
#     1: "ONE-PAIR",
#     2: "TWO-PAIR",
#     3: "TRIPS",
#     4: "STRAIGHT",
#     5: "FLUSH",
#     6: "FULL-HOUSE",
#     7: "QUADS",
#     8: "STRAIGHT FLUSH",
# }
# CARDFIGURE = {
#     2: "2",
#     3: "3",
#     4: "4",
#     5: "5",
#     6: "6",
#     7: "7",
#     8: "8",
#     9: "9",
#     10: "10",
#     11: "J",
#     12: "Q",
#     13: "K",
#     14: "A",
# }


def main():
    # fresh card deck
    deck = new_deck()

    ######################  TEST WINNING POSSIBILITY ####################

    dict_test_level_count = {}

    for i in range(50):  # number of test cases to run
        # create deck
        test_deck = []
        for j in ("♠", "♦", "♥", "♣"):
            for k in range(2, 15):
                test_deck.append((j, k))

        # deal cards to test player
        test_hole_cards = []
        test_community_cards = []
        for l in range(2):
            test_hole_cards.append(deal(test_deck))
        for m in range(5):
            test_community_cards.append(deal(test_deck))
        test_hand = test_hole_cards + test_community_cards

        # add test hand level result to dict
        # dict_test_level_count[HANDLEVEL[get_hand_result(test_hand)[0]]] = (
        #     dict_test_level_count.get(HANDLEVEL[get_hand_result(test_hand)[0]], 0) + 1
        # )

        print(
            f"Test Player's winning possibility is: {calc_winning_possibility(get_hand_result(test_hand), test_community_cards, test_deck)}%"
        )

        print(f"{show_hand(test_hole_cards)}  |  {show_hand(test_community_cards)}")

        print(
            f"{HANDLEVEL[get_hand_result(test_hand)[0]]}: {show_hand(get_hand_result(test_hand)[1])}\n"
        )

    # print(
    #     dict(sorted(dict_test_level_count.items(), key=lambda kv: kv[1], reverse=True))
    # )


if __name__ == "__main__":
    while input("Enter to play or any key to exit: \n") == "":
        main()
