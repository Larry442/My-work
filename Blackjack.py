import random
import time

deck = ["A", "A", "A", "A", 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "J", "J", "J", "J", "Q", "Q", "Q", "Q", "K", "K", "K", "K"]
current_deck = deck
player_deck = []
player_deck_split = []
dealer_deck = []
money = 1000
bet = 0
play_round = True
end_round = False
play_game = True

def place_bet():
    global bet
    bet = int(input("Place your bet: "))
    global money
    if bet % 2 != 0 and bet < 2:
        bet = int(input("Place an even number amount of bet, no less than 2: "))
    if bet > money:
        print("not enough money")
    else:
        money -= bet
    

def draw_card(deck):
    global current_deck
    if len(current_deck) > 0:
        random_draw = int(random.random() * (len(current_deck)))
        deck.append(current_deck[random_draw])
        current_deck.pop(random_draw)
    else:
        current_deck = deck.copy()

def calc_sum(deck):
    card_sum = 0
    ace_count = 0
    
    for card in deck:
        if card in ["J", "Q", "K"]:
            card_sum += 10
        elif card == "A":
            ace_count += 1
            card_sum += 11
        else:
            card_sum += card
    
    # Adjust for aces if total sum is over 21
    while card_sum > 21 and ace_count > 0:
        card_sum -= 10
        ace_count -= 1
        
    return card_sum


def compare():
    global bet, money
    player_card_sum = calc_sum(player_deck)
    dealer_card_sum = calc_sum(dealer_deck)
    print("Comparing hands...")
    time.sleep(1.5)
    if player_card_sum > dealer_card_sum:
        money += 2 * bet
        print("Player wins")
    elif player_card_sum < dealer_card_sum:
        print("Dealer wins")
    else:
        money += bet
        print("Draw")

def compare_1_split():
    global bet, money
    player_card_sum = calc_sum(player_deck)
    dealer_card_sum = calc_sum(dealer_deck)
    print("Comparing hands...")
    time.sleep(1.5)
    if player_card_sum > dealer_card_sum:
        money += bet
        print("Player wins")
    elif player_card_sum < dealer_card_sum:
        print("Dealer wins")
    else:
        money += initial_bet
        print("Draw")

def compare_split():
    global bet, money
    player_card_split_sum = calc_sum(player_deck_split)
    dealer_card_sum = calc_sum(dealer_deck)
    print("Comparing hands...")
    time.sleep(1.5)
    if player_card_split_sum > dealer_card_sum:
        money += bet
        print("Player wins")
    elif player_card_split_sum < dealer_card_sum:
        print("Dealer wins")
    else:
        money += initial_bet
        print("Draw")

def double():
    global bet
    global money
    money -= bet
    bet *= 2

def insurance():
    global bet
    global money
    money -= bet/2
    bet += bet/2


while play_game:
    while play_round:
        
        print()
        player_deck = []
        player_deck_split = []
        dealer_deck = []

        place_bet()
            
        print("Money left:", money)
        time.sleep(0.5)

        draw_card(player_deck)
        draw_card(player_deck)

        player_card_sum = calc_sum(player_deck)        
        print("Player deck:", end = " ")
        print(str(player_deck[0]) + " " + str(player_deck[1]))
        time.sleep(0.5)

        draw_card(dealer_deck)
        draw_card(dealer_deck)
        dealer_card_sum = calc_sum(dealer_deck)

        if dealer_card_sum != 21:
            print("Dealer deck: " + str(dealer_deck[0]) + " ?")
            time.sleep(0.5)

        if player_card_sum == 21 and dealer_card_sum == 21:
            print("Dealer deck: " + str(banker_deck[0]) + " " + str(banker_deck[1]))
            print("Draw")
            time.sleep(1)
            money += bet
            bet = 0
            print("Money left:", money)
            break

        elif player_card_sum == 21:
            print("Blackjack! Player wins.")
            time.sleep(1)
            money += 2 * bet
            print("Money left:", money)
            bet = 0
            break
        elif dealer_card_sum == 21:
            print("Dealer deck: " + str(dealer_deck[0]) + " " + str(dealer_deck[1]))
            time.sleep(0.5)
            print("Blackjack! Dealer wins!")
            print("Money left:", money)
            bet = 0
            break
        
        action_i = ""
        
        if dealer_deck[0] == "A":
            while True:
                action_i = input("Buy insurance? Type 'yes' or 'no': ").strip().lower()
                if action_i in ["yes", "no"]:
                    break
                print("Invalid input. Please type 'yes' or 'no'.")

            if action_i == "yes":
                insurance()
                print("New bet:", bet)
                print("Money left:", money)
                time.sleep(0.5)

            if dealer_card_sum == 21:
                print("Dealer deck:", str(dealer_deck[0]) + " " + str(dealer_deck[1]))
                if action_i == "yes":
                    money += bet * 2 / 3
                    bet = 0
                    print("Blackjack! Dealer wins! Insurance gained!")
                else:
                    bet = 0
                    print("Blackjack! Dealer wins!")
                print("Money left:", money)
                break
            else:
                if action_i == "yes":
                    bet = 0
                    print("Dealer doesn't have a blackjack! Insurance lost!")
                    break
                else:
                    print("Dealer doesn't have a blackjack, continue.")

        action = ""
        if player_deck[0] == player_deck[1] and money - bet * 2 >= 0:
            action = input("Type your next action: 'stand', 'hit', 'double', 'split': ").strip().lower()
        else:
            action = input("Type your next action: 'stand', 'hit', 'double': ").strip().lower()
        time.sleep(0.5)

        if action == "stand":
            print("Dealer deck after hit:", end = " ")
            while dealer_card_sum < 17:
                draw_card(dealer_deck)
                dealer_card_sum = calc_sum(dealer_deck)
            for card in dealer_deck:
                print(str(card), end = " ")
                time.sleep(1)
            print()

            dealer_card_sum = calc_sum(dealer_deck)
            if dealer_card_sum > 21:
                print("Dealer busted, player wins!")
                time.sleep(0.5)
                money += 2 * bet
                print("Money left:", money)
                bet = 0
                break
            else:
                compare()
                print("Money left:", money)
                bet = 0
                break
                    
        #Player chooses to draw a new card
        elif action == "hit":
            while True:
                draw_card(player_deck)
                player_card_sum = calc_sum(player_deck)
                print("Player's deck:")
                for cards in player_deck:
                    print(cards, end=" ")
                    time.sleep(1)
                print()
                if player_card_sum == 21:
                    print("Blackjack! Player wins!")
                    money += bet * 2
                    time.sleep(0.5)
                    print("Money left: " + str(money))
                    bet = 0
                    end_round = True
                    break
                if player_card_sum > 21:
                    print("Player busted!")
                    time.sleep(0.5)
                    print("Money left: " + str(money))
                    bet = 0
                    end_round = True
                    break
         
                action = input("Type your next action: 'stand' or 'hit': ")
                if action == "stand":
                    break
                elif action != "hit":
                    print("Invalid input. Please type 'stand' or 'hit'.")
                    time.sleep(0.5)
                    action = input("Type your next action: 'stand' or 'hit': ")
            if end_round:
                break
            if action == "stand":
                while calc_sum(dealer_deck) < 17:
                    draw_card(dealer_deck)
                    dealer_card_sum = calc_sum(dealer_deck)
                
                print("Dealer deck after hit:")
                for card in dealer_deck:
                    print(str(card), end =" ")
                    time.sleep(1)
                print()
         
                dealer_card_sum = calc_sum(dealer_deck)  
                if dealer_card_sum > 21:
                    print("Dealer busted, player wins!")
                    money += 2 * bet
                else:
                    compare()
                print("Money left: " + str(money))
                bet = 0
                break
               
        elif action == "double":
            double()
            print("New bet: " + str(bet) + "\nMoney left: " + str(money))
            time.sleep(0.5)
            draw_card(player_deck)
            print("Player deck: ")
            for card in player_deck:
                print(str(card), end = " ")
                time.sleep(1)
            print()
            player_card_sum = calc_sum(player_deck)

            if player_card_sum == 21:
                print("Blackjack! Player wins!")
                money += bet * 2
                time.sleep(0.5)
                print("Money left: " + str(money))
                bet = 0
                break
            if player_card_sum > 21:
                print("Player busted, dealer wins!")
                print("Money left: " + str(money))
                bet = 0
                break
        
            while dealer_card_sum < 17:
                draw_card(dealer_deck)
                dealer_card_sum = calc_sum(dealer_deck)

            print("Dealer deck after hit: ")
            for card in dealer_deck:
                print(str(card), end =" ")
                time.sleep(1)
            print()
        
            dealer_card_sum = calc_sum(dealer_deck)  
            if dealer_card_sum > 21:
                print("Dealer busted, player wins!")
                money += 2 * bet
                print("Money left: " + str(money))
                bet = 0
                break
                
            #Check if both player and banker get a black jack
            if ("A" in player_deck and ("J" in player_deck or "Q" in player_deck or "K" in player_deck or 10 in player_deck)) and ("A" in dealer_deck and ("J" in dealer_deck or "Q" in dealer_deck or "K" in dealer_deck or 10 in dealer_deck)):
                print(str(dealer_deck[0]) + " " + str(dealer_deck[1]))
                print("Draw")
                money += bet
                bet = 0
                print("Money left: " + str(money))
        
            #Check if player gets a black jack
            elif "A" in player_deck and ("J" in player_deck or "Q" in player_deck or "K" in player_deck or 10 in player_deck):
                print("Blackjack! Player wins.")
                money += 2 * bet
                print("Money left: " + str(money))
                bet = 0
             
            #Check if banker gets a black jack
            elif "A" in dealer_deck and ("J" in dealer_deck or "Q" in dealer_deck or "K" in dealer_deck or 10 in dealer_deck) and (dealer_deck[0] == "J" or "Q" or "K" or 10):
                print(str(dealer_deck[0]) + " " + str(dealer_deck[1]))
                print("Blackjack! Dealer wins!")
                print("Money left: " + str(money))
                bet = 0

            else:
                compare()
                print("Money left:", money)
            break

        elif action == "split":
            initial_bet = bet
            bet *= 2
            print("New bet:", bet)
            money = money - initial_bet
            print("Money left:", money)
            player_deck_split.append(player_deck[0])
            player_deck.pop(0)
            player_card_sum = calc_sum(player_deck)
            player_card_split_sum = calc_sum(player_deck_split)
            print("First deck:", player_deck[0], "\nSecond deck:", player_deck_split[0])
            print()
            action = input("Next action for the first deck: 'stand', 'hit': ").strip().lower()
            if action == "stand":
                pass
            elif action == "hit":
                while True:
                    draw_card(player_deck)
                    player_card_sum = calc_sum(player_deck)
                    print("Player's first deck:", end=" ")
                    for cards in player_deck:
                        print(cards, end=" ")
                        time.sleep(1)
                    print()
                    if player_card_sum == 21:
                        print("Blackjack! Player wins!")
                        money += bet * 2
                        time.sleep(0.5)
                        print("Money left: " + str(money))
                        bet = 0
                        break
                    if player_card_split_sum > 21:
                        print("Player's first deck busted!")
                        time.sleep(0.5)
                        print("Money left:", money)
                        break
                    action = input("Type your next action: 'stand', 'hit': ").strip().lower()
                    if action == "stand":
                        break
                    elif action != "hit":
                        print("Invalid input. Please type 'stand' or 'hit'.")
                        time.sleep(0.5)
                        action = input("Type your next action: 'stand', 'hit': ").strip().lower()
                if action == "stand":
                    pass
            action = input("Next action for the second deck: 'stand', 'hit': ").strip().lower()
            if action == "stand":
                pass
            elif action == "hit":
                while True:
                    draw_card(player_deck_split)
                    player_card_split_sum = calc_sum(player_deck_split)
                    print("Player's second deck:", end=" ")
                    for cards in player_deck_split:
                        print(cards, end=" ")
                        time.sleep(1)
                    print()
                    if player_card_split_sum == 21:
                        print("Blackjack! Player wins!")
                        money += bet * 2
                        time.sleep(0.5)
                        print("Money left: " + str(money))
                        bet = 0
                        break
                    if player_card_split_sum > 21:
                        print("Player's second deck busted!")
                        time.sleep(0.5)
                        print("Money left:", money)
                        break
                    action = input("Type your next action: 'stand', 'hit': ").strip().lower()
                    if action == "stand":
                        break
                    elif action != "hit":
                        print("Invalid input. Please type 'stand' or 'hit'.")
                        time.sleep(0.5)
                        action = input("Type your next action: 'stand', 'hit': ").strip().lower()
                if action == "stand":
                    pass

            else:
                print("Invalid input. Please type 'stand' or 'hit'.")
                time.sleep(0.5)
                action = input("Type your next action: 'stand', 'hit': ").strip().lower()
            if ("A" in player_deck and any(card in ["J", "Q", "K", 10] for card in player_deck)) and len(player_deck) == 2 and len(player_deck_split) == 2 and player_card_split and (any(card in ["J", "Q", "K", 10] for card in player_deck)):
                break
            if player_card_sum == 21 and player_card_split_sum == 21:
                break
            if player_card_sum > 21 and player_card_split_sum > 21:
                break
            while dealer_card_sum < 17:
                draw_card(dealer_deck)
                dealer_card_sum = calc_sum(dealer_deck)
            print("Dealer deck after hit:", end = " ")
            for card in dealer_deck:
                print(str(card), end = " ")
                time.sleep(1)
            print()
            dealer_card_sum = calc_sum(dealer_deck)
            if dealer_card_sum > 21 and (player_card_sum <= 21 and player_card_split_sum <= 21):
                print("Dealer busted, both hands win!")
                time.sleep(0.5)
                money += 2 * bet
                print("Money left:", money)
                bet = 0
            elif dealer_card_sum > 21 and (player_card_sum <= 21 or player_card_split_sum <= 21):
                print("Banker busted!")
                time.sleep(0.5)
                money += bet
                print("Money left:", money)
                bet = 0
            elif player_card_sum <= 21 and player_card_split_sum <= 21:
                if player_card_sum != 21:
                    compare_1_split()
                    print("Money left:", money)
                else:
                    print("Blackjack! Player wins!")
                    money += bet
                    print("Money left:", money)
                    bet = 0
                if player_card_split_sum != 21:
                        compare_split()
                        print("Money left:", money)
                else:
                    print("Blackjack! Player wins!")
                    money += 2 * bet
                    print("Money left:", money)
                    bet = 0
            elif player_card_sum <= 21:
                if palyer_card_sum != 21:
                    compare_1_split()
                    print("Money left:", money)
                else:
                    print("Blackjack! Player wins!")
                    money += bet
                    print("Money left:", money)
                    bet = 0                    
            elif player_card_split_sum <= 21:
                if palyer_card_split_sum != 21:
                    compare_split()
                    print("Money left:", money)
                else:
                    print("Blackjack! Player wins!")
                    money += 2 * bet
                    print("Money left:", money)
                    bet = 0
            break
        
        elif player_deck[0] == player_deck[1]:
            print("Invaild input.")
            action = input("Type your next action: 'stand', 'hit', 'double', 'split': ").strip().lower()
        else:
            print("Invaild input.")
            action = input("Type your next action: 'stand', 'hit', 'double', 'split': ").strip().lower()

    play = input("Type 'c' to continue or 'quit' to quit: ").strip().lower()
    if play == "quit":
        play_game = False
        break
    elif play == "c":
        continue
    else:
        print("Invaild input!")
        play = input("Type 'c' to continue or 'quit' to quit: ").strip().lower()

    if money < 2:
        play_game = False
        print("Not enough money, quit.") 
    
            




