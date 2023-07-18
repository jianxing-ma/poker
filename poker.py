import math
import random
import crayons

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


### Calculate winning possibility
def calc_winning_possibility(self_hand_result, community_cards, deck):
    lose_count = 0

    for i in range(len(deck)):
        for j in range(i + 1, len(deck)):
            oppo_cards = [card for card in community_cards]
            oppo_cards.append(deck[i])
            oppo_cards.append(deck[j])

            oppo_hand_result = get_hand_result(oppo_cards)

            compare_hands_result = compare_hands(self_hand_result, oppo_hand_result)

            if compare_hands_result == -1:
                lose_count += 1

    winning_ratio = math.floor(
        100 * (1 - (lose_count / (len(deck) * (len(deck) - 1) / 2)))
    )

    return winning_ratio


### Compare two players' hands
def compare_hands(self_hand_result, oppo_hand_result):
    if self_hand_result[0] < oppo_hand_result[0]:
        return -1
    elif self_hand_result[0] == oppo_hand_result[0]:
        for card in range(5):
            if self_hand_result[1][card][1] < oppo_hand_result[1][card][1]:
                return -1
            elif self_hand_result[1][card][1] > oppo_hand_result[1][card][1]:
                return 1
            else:
                pass
        return 0
    else:
        return 1


### Get player's hand-level
def get_hand_result(hand):
    dict_suited = {}
    dict_repeated = {}

    for card in hand:
        # create suited cards count dictionary and get the most suited list
        dict_suited[card[0]] = dict_suited.get(card[0], []) + [card]
        # create repeated cards count dictionary and sort it
        dict_repeated[card[1]] = dict_repeated.get(card[1], []) + [card]

    list_cards_suited = max(dict_suited.values(), key=lambda i: len(i))

    dict_repeated_sorted = dict(
        sorted(dict_repeated.items(), key=lambda kv: (len(kv[1]), kv[0]), reverse=True)
    )
    list_repeated_count = [
        (key, len(dict_repeated_sorted[key])) for key in dict_repeated_sorted
    ]

    # Check if hand has straight
    list_figure_sorted = sorted(list(dict_repeated.keys()), reverse=True)
    check_figures_straight = is_straight(list_figure_sorted)

    # At least Flush
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
        # Full-House
        elif list_repeated_count[0][1] == 3 and list_repeated_count[1][1] >= 2:
            hand_level = 6
        # Three Pairs Still counts as Two-Pair
        elif len(list_repeated_count) == 4:
            hand_level = 2
            # Single card's figure is larger than the smallest pair
            if list_repeated_count[2][0] < list_repeated_count[3][0]:
                return (
                    hand_level,
                    dict_repeated_sorted[list_repeated_count[0][0]]
                    + dict_repeated_sorted[list_repeated_count[1][0]]
                    + dict_repeated_sorted[list_repeated_count[3][0]],
                )
        elif len(list_repeated_count) == 5:
            # Trips
            if list_repeated_count[0][1] == 3:
                hand_level = 3
            # Two-Pair
            else:
                hand_level = 2
        # One-Pair
        elif len(list_repeated_count) == 6:
            hand_level = 1
        # High-Cards
        else:
            hand_level = 0
        hand_result = repeated_hand_result(dict_repeated_sorted)

    return hand_level, hand_result


### helper function to check if cards are straight
def is_straight(list_cards):
    for i in range(len(list_cards) - 4):
        if list_cards[i] - list_cards[i + 4] == 4:
            return {0: True, 1: list_cards[i : i + 5]}
    return {0: False}


### helper function to get hand result
def repeated_hand_result(dict_hand):
    hand_result = []

    for key in dict_hand:
        hand_result += dict_hand[key]
    return hand_result[:5]


### helper function to deal cards
def deal(deck):
    return deck.pop(random.randrange(len(deck)))


### create a fresh set of deck
def new_deck():
    deck = []
    for i in ("♠", "♥", "♣", "♦"):
        for j in range(2, 15):
            deck.append((i, j))
    return deck


### helper function to print cards
def show_hand(hand):
    hand_shown = ""

    for card in hand:
        colored_card = CARDFIGURE[card[1]] + card[0] + " "

        if card[0] == "♠":
            hand_shown += crayons.black(colored_card, bold=True)
        elif card[0] == "♥":
            hand_shown += crayons.red(colored_card, bold=True)
        elif card[0] == "♣":
            hand_shown += crayons.green(colored_card, bold=True)
        elif card[0] == "♦":
            hand_shown += crayons.blue(colored_card, bold=True)

        # hand_shown += colored_card

    return hand_shown
