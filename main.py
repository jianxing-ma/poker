#!/user/bin/python3

import math
import random

HANDLEVEL = {
    0: "HIGH-CARD",
    1: "ONE-PAIR",
    2: "TWO-PAIR",
    3: "TRIPS",
    4: "STRAIGHT",
    5: "FLUSH",
    6: "FULL-HOUSE",
    7: "QUADS",
    8: "STRAIGHT FLUSH",
}
CARDFIGURE = {
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
    14: "A",
}

# create card deck
deck = []
for i in ("♠", "♦", "♥", "♣"):
    for j in range(2, 15):
        deck.append((i, j))


def main():
    # deal player1 cards
    hand_player1 = []
    for i in range(2):
        hand_player1.append(deal(deck))
    # print(f"\nPlayer 1's hole cards: {show_hand(hand_player1)}\n")

    # deal community cards
    community_cards = []
    for i in range(5):
        community_cards.append(deal(deck))
    # print(f"\nCommunity cards are: {show_hand(community_cards)}\n")

    hand_player1 += community_cards

    # print(
    #     f"\nPlayer 1's hand is {HANDLEVEL[get_hand_result(hand_player1)[0]]}: {show_hand(get_hand_result(hand_player1)[1])}\n"
    # )

    dict_test_level_count = {}

    for i in range(1):  # number of test cases to run
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
        dict_test_level_count[HANDLEVEL[get_hand_result(test_hand)[0]]] = (
            dict_test_level_count.get(HANDLEVEL[get_hand_result(test_hand)[0]], 0) + 1
        )

        calc_winning_possibility(
            get_hand_result(test_hand), test_community_cards, test_deck
        )

        print("TEST PLAYER Hole cards: ", show_hand(test_hole_cards))
        print("Community cards: ", show_hand(test_community_cards))

        print(
            f"\n{HANDLEVEL[get_hand_result(test_hand)[0]]}: {show_hand(get_hand_result(test_hand)[1])}\n"
        )
    # print(
    #     dict(sorted(dict_test_level_count.items(), key=lambda kv: kv[1], reverse=True))
    # )


###########################################################################################
###################TODO CALCULATE POSSIBILITY OF WINNING HAND TODO#########################
###########################################################################################


### Calculate winning possibility
def calc_winning_possibility(self_hand_result, community_cards, deck):
    lose_count = 0

    case_check_count = 0

    for i in range(45):
        for j in range(i + 1, 45):
            # TODO Delete
            case_check_count += 1
            print("Case check #: ", case_check_count)

            oppo_cards = [card for card in community_cards]
            oppo_cards.append(deck[i])
            oppo_cards.append(deck[j])

            oppo_hand_result = get_hand_result(oppo_cards)
            print(
                "Oppo's hand: ",
                HANDLEVEL[oppo_hand_result[0]],
                " ",
                show_hand(oppo_hand_result[1]),
            )

            if self_hand_result[0] < oppo_hand_result[0]:
                lose_count += 1
                print("Different level, Count of losing cases: ", lose_count, "\n")
                continue
            elif self_hand_result[0] == oppo_hand_result[0]:
                for card in range(5):
                    if self_hand_result[1][card][1] < oppo_hand_result[1][card][1]:
                        lose_count += 1
                        print("Same level, Count of losing cases: ", lose_count, "\n")
                        break
                    elif self_hand_result[1][card][1] > oppo_hand_result[1][card][1]:
                        print("Same level, self won", "\n")
                        break

            else:
                print("Different level, Self won", "\n")

    winning_ratio = math.floor(
        100 * (1 - (lose_count / (len(deck) * (len(deck) - 1) / 2)))
    )

    print(f"Test Player's winning possibility is: {winning_ratio}%")
    return winning_ratio


### Get player's hand-level
def get_hand_result(hand):
    dict_suit = {}
    dict_repeated = {}

    for card in hand:
        # create suited cards count dictionary and get the most suited list
        dict_suit[card[0]] = dict_suit.get(card[0], []) + [card]
        list_cards_suited = max(dict_suit.values(), key=lambda i: len(i))

        # create repeated cards count dictionary and sort it
        dict_repeated[card[1]] = dict_repeated.get(card[1], []) + [card]
        dict_repeated_sorted = dict(
            sorted(
                dict_repeated.items(), key=lambda kv: (len(kv[1]), kv[0]), reverse=True
            )
        )
        list_repeated_count = [
            (key, len(dict_repeated_sorted[key])) for key in dict_repeated_sorted
        ]

    # Check if hand has straight
    list_figure_sorted = sorted(list(dict_repeated.keys()), reverse=True)
    check_figures_straight = is_straight(list_figure_sorted)

    if len(list_cards_suited) >= 5:
        list_figures_suited = [card[1] for card in list_cards_suited]
        list_figures_suited.sort(reverse=True)
        # Straight Flush
        if is_straight(list_figures_suited)[0]:
            hand_level = 8
            hand_result = [
                dict_repeated_sorted[figure][0]
                for figure in is_straight(list_figures_suited)[1]
            ]
        # Flush
        else:
            hand_level = 5
            hand_result = sorted(
                list_cards_suited, key=lambda card: card[1], reverse=True
            )[:5]
    # Straight
    elif check_figures_straight[0]:
        hand_level = 4
        hand_result = [
            dict_repeated_sorted[figure][0] for figure in check_figures_straight[1]
        ]
    else:
        # Quads
        if list_repeated_count[0][1] == 4:
            hand_level = 7
        # Full House
        elif list_repeated_count[0][1] == 3 and list_repeated_count[1][1] == 2:
            hand_level = 6
        elif len(list_repeated_count) <= 5:
            # Trips
            if list_repeated_count[0][1] == 3:
                hand_level = 3
            # Two Pair
            else:
                hand_level = 2
        # One Pair
        elif len(list_repeated_count) == 6:
            hand_level = 1
        # High Cards
        else:
            hand_level = 0
        hand_result = retrieve_hand_result(dict_repeated_sorted)

    return hand_level, hand_result


### helper function to check if cards are straight
def is_straight(list_cards):
    for i in range(len(list_cards) - 4):
        if list_cards[i] - list_cards[i + 4] == 4:
            return {0: True, 1: list_cards[i : i + 5]}
    return {0: False}


### helper function to get hand result
def retrieve_hand_result(dict_hand):
    hand_result = []

    # for i in range(n):
    #     hand_result += dict_hand[list_hand[i][0]]
    # return hand_result
    for key in dict_hand:
        hand_result += dict_hand[key]
    return hand_result[:5]


### helper function to deal cards
def deal(deck):
    return deck.pop(random.randrange(len(deck)))


### helper function to print cards
def show_hand(hand):
    hand_shown = ""
    for card in hand:
        hand_shown += CARDFIGURE[card[1]] + card[0] + " "
    return hand_shown


if __name__ == "__main__":
    while input("Enter to play or any key to exit: ") == "":
        main()
