#!/user/bin/python3

import random

HANDLEVEL = {
    0: "high card",
    1: "one pair",
    2: "two pair",
    3: "trips",
    4: "straight",
    5: "flush",
    6: "full house",
    7: "quads",
    8: "straight flush",
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


def main():
    # create card deck
    deck = []
    for i in ("♠", "♦", "♥", "♣"):
        for j in range(2, 15):
            deck.append((i, j))

    # deal player1 cards
    hand_player1 = []
    for i in range(2):
        hand_player1.append(deal(deck))
    print(f"\nPlayer 1's hole cards: {show_hand(hand_player1)}\n")

    # deal community cards
    community_cards = []
    for i in range(5):
        community_cards.append(deal(deck))
    print(f"\nCommunity cards are: {show_hand(community_cards)}\n")

    hand_player1 += community_cards

    print(
        f"\nPlayer 1's hand is {HANDLEVEL[get_hand_level(hand_player1)[0]]}: {show_hand(get_hand_level(hand_player1)[1])}\n"
    )


### Get player1's hand-level
def get_hand_level(hand):
    dict_suit = {}
    dict_repeated = {}

    for card in hand:
        # create suited cards count dictionary and sort it
        dict_suit[card[0]] = dict_suit.get(card[0], []) + [card]
        # TODO Don't need this dict sorted, only need the monst suited element
        dict_suit_sorted = dict(
            sorted(dict_suit.items(), key=lambda kv: len(kv[1]), reverse=True)
        )
        # TODO Don't need this list, only need the most suited element
        list_suit_count = [
            (key, len(dict_suit_sorted[key])) for key in dict_suit_sorted
        ]
        ############################
        list_most_suited = [(key, len(dict_suit[key])) for key in dict_suit]
        list_most_suited.sort(key=lambda e: e[1])
        most_suited_cards = dict_suit[list_most_suited[0][0]]
        most_suited_cards.sort(key=lambda e: e[1])
        ############################
        list_cards_suited = max(dict_suit.values(), key=lambda i: len(i))
        ##############################

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

    list_figure_sorted = sorted(list(dict_repeated.keys()), reverse=True)
    check_figures_straight = is_straight(list_figure_sorted)

    # Straight Flush
    if len(list_cards_suited) >= 5:
        ##################TODO to be deleted TODO##################
        # list_suited_figures = [
        #     card[1] for card in dict_suit_sorted[list_suit_count[0][0]]
        # ]
        # list_suited_figures.sort(reverse=True)
        ###########################################################
        list_figures_suited = [card[1] for card in list_cards_suited]
        list_figures_suited.sort(reverse=True)
        ###########################################################
        if is_straight(list_figures_suited)[0]:
            hand_level = 8
            hand_result = [
                dict_repeated_sorted[figure][0]
                for figure in is_straight(list_figures_suited)[1]
            ]
        # Flush
        else:
            hand_level = 5
            ###############################################
            # hand_result = sorted(
            #     dict_suit_sorted[list_suit_count[0][0]],
            #     key=lambda card: card[1],
            #     reverse=True,
            # )[:5]
            ################################################
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
