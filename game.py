from poker import *


def execute():
    # num_players = input("Please enter number of machine players: ")

    user_stack = 1000
    machine_stack = 1000

    while user_stack > 0 and machine_stack > 0:
        print(f"\nYour stack: {user_stack}  |   Machine stack: {machine_stack}\n")
        print(
            "______________________________________________________________________________________\n"
        )

        user_is_playing = input("Enter to play | Any key to exit: ")
        if user_is_playing != "":
            print("\nThanks for playing, bye...\n")
            break
        else:
            print("\nLet's go!\n")
            print("--------------------------------\n")

        blind = min(10, user_stack, machine_stack)
        user_stack -= blind
        machine_stack -= blind

        pot = blind * 2

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

        user_action = input("\nPlease take action (Bet[B] | Check[C]): ").upper()

        # ____________________________________Game Logic____________________________________#

        if user_action == "C":
            if machine_action == 1:  # Machine bets
                #############################################################

                player_reply = user_reply(machine_bet, user_stack, machine_stack)

                # Update players stack
                user_stack -= player_reply[0]
                machine_stack -= player_reply[0]
                # Update pot
                pot += player_reply[0] * 2

                if player_reply[1] == "F":
                    round_result = -1

            else:
                print("\nMachine also checked\n")

        elif user_action == "B":
            user_bet = int(
                input(f"\nYour stack: {user_stack}\nPlease enter bet amount: ")
            )

            if machine_action == 1:
                if machine_bet > user_bet:
                    print(f"\nMachine raised!")
                    ###################################################################
                    player_reply = user_reply(machine_bet, user_stack, machine_stack)

                    # Update players stack
                    user_stack -= player_reply[0]
                    machine_stack -= player_reply[0]
                    # Update pot
                    pot += player_reply[0] * 2

                    if player_reply[1] == "F":
                        round_result = -1

                elif machine_bet == user_bet:
                    print("Machine called\n")
                    # Update players stack
                    user_stack -= user_bet
                    machine_stack -= machine_bet
                    pot += user_bet * 2

                else:
                    print("Machine folded\n")
                    round_result = 1

            else:
                print("Machine folded\n")
                round_result = 1

        # ____________________________________End of Logic___________________________________#

        ###################################### Round Result ##################################

        # Show hands
        print(
            f"Your hand:    {HANDLEVEL[user_hand_result[0]]} {show_hand(user_hand_result[1])}"
        )
        print(
            f"Machine hand: {HANDLEVEL[machine_hand_result[0]]} {show_hand(machine_hand_result[1])}\n"
        )

        # Post show hand operations
        if round_result == 1:
            print("You won!\n")
            user_stack += pot
        elif round_result == 0:
            print("Everyone loves a chop!\n")
            user_stack += pot / 2
            machine_stack += pot / 2
        elif round_result == -1:
            print("You lost..\n")
            machine_stack += pot


def user_reply(machine_bet, user_stack, machine_stack):
    user_action = input(
        f"\nMachine betted {machine_bet}.\nPlease Choose your action (Call[C] | Raise(R) | Fold[F]): "
    ).upper()

    if user_action == "C":
        print("\nYou called")
        bet_plus = min(machine_bet, user_stack)

    elif user_action == "R":
        user_reraise = int(
            input(f"\nYour stack: {user_stack}\nPlease enter raise amount: ")
        )

        print("\nMachine called\n")
        bet_plus = min(user_reraise, machine_stack)

    elif user_action == "F":
        print("\nYou folded.\n")
        bet_plus = 0

    return bet_plus, user_action


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
