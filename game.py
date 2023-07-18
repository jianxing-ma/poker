from poker import *
import math


def execute():
    # num_players = input("Please enter number of machine players: ")

    user_stack = 1000
    machine_stack = 1000

    while user_stack >= 0 and machine_stack >= 0:
        bet = 10
        user_stack -= bet
        machine_stack -= bet

        # Get new deck
        deck = new_deck()

        # deal hole cards to user
        user_hand = []
        deal_cards(deck, user_hand, 2)

        # deal hole cards to machine
        machine_hand = []
        deal_cards(deck, machine_hand, 2)

        # deal community cards
        community_cards = []
        deal_cards(deck, community_cards, 5)

        print(f"Your hole cards are: {show_hand(user_hand)}")
        print(f"Community cards are: {show_hand(community_cards)}\n")

        # user hand result
        user_hand += community_cards
        user_hand_result = get_hand_result(user_hand)
        user_win_ratio = calc_winning_possibility(
            user_hand_result, community_cards, deck
        )

        # machine hand result
        machine_hand += community_cards
        machine_hand_result = get_hand_result(machine_hand)
        machine_win_ratio = calc_winning_possibility(
            machine_hand_result, community_cards, deck
        )

        # compare hands result
        round_result = compare_hands(user_hand_result, machine_hand_result)

        machine_action = 0

        bet_ratio = random.randint(0, 100)
        if machine_win_ratio >= bet_ratio:
            machine_action = 1
            machine_bet = random.randint(1, machine_stack)

        user_action = input("Please take action (Bet[B] | Check[C]): ").upper()

        if user_action == "C":
            if machine_action == 1:
                user_action = input(
                    f"Machine betted {machine_bet}.\nPlease Choose your action (Call[C] | Raise(R) | Fold[F]): "
                ).upper()

                if user_action == "C":
                    print("You called")

                    bet += min(machine_bet, user_stack)

                    print_result_action(round_result)

                elif user_action == "R":
                    user_reraise = int(
                        input(f"Your stack: {user_stack}\nPlease enter raise amount: ")
                    )

                    print("Machine called")
                    bet += min(user_reraise, machine_stack)

                    print_result_action(round_result)
                elif user_action == "F":
                    round_result = -1
                    print("You folded.\n")

            else:
                print("Machine also checked\n")
                print_result_action(round_result)

        elif user_action == "B":
            user_bet = int(
                input(f"Your stack: {user_stack}\nPlease enter bet amount: ")
            )

            if machine_action == 1:
                if machine_bet > user_bet:
                    print(f"Machine raised!")
                    user_action = input(
                        f"Machine betted {machine_bet}. Please Choose your action (Call[C] | Raise  (R) | Fold[F])  : "
                    ).upper()

                    if user_action == "C":
                        print("You called\n")
                        bet += max(machine_bet, user_stack)

                        print_result_action(round_result)

                    elif user_action == "R":
                        bet += int(input("Please enter raise amount: "))

                        print("Machine called\n")

                        print_result_action(round_result)

                    elif user_action == "F":
                        print("You folded.\n")
                        bet += user_bet

                elif machine_bet == user_bet:
                    print("Machine called\n")
                    bet += user_bet

                    print_result_action(round_result)

                else:
                    print("Machine folded\n")
                    round_result = 1
                    print_result_action(round_result)

            else:
                print("Machine folded\n")
                round_result = 1
                print_result_action(round_result)
        print(
            f"Your hand: {HANDLEVEL[user_hand_result[0]]} {show_hand(user_hand_result[1])}"
        )
        print(
            f"Machine hand: {HANDLEVEL[machine_hand_result[0]]} {show_hand(machine_hand_result[1])}\n"
        )

        user_stack += round_result * bet
        machine_stack -= round_result * bet
        print(f"\nYour stack: {user_stack}  |   Machine stack: {machine_stack}\n")
        print(
            "______________________________________________________________________________________\n"
        )


def print_result_action(round_result):
    if round_result == -1:
        print("You lost..\n")
    elif round_result == 0:
        print("Everyone loves a chop!\n")
    elif round_result == 1:
        print("You won!\n")


def deal_cards(deck, target, num):
    for i in range(num):
        target.append(deal(deck))


# TODO TO BE DELTED
execute()
