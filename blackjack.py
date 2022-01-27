import random, sys

HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

def main():
    print('''
    WELCOME TO BLACKJACK!

    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value.
        (H)it to take another card.
        (S)tand to stop taking cards.
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player.
        The dealer stops hitting at 17.
    ''')

    money = 100
    while True:
        if money <= 0:
            print("You're broke!")
            print("Good thing you weren't playing with real money.")
            print("Thanks for playing!")
            sys.exit()

        print(f'Money: {money}')
        bet = getBet(money)

        deck = getDeck()

        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        print('Bet:', bet)
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break
            
            move = getMove(playerHand, move-bet)

            if move == 'D':
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')
                print(f'Bet: {bet}')

            if move in ('H', 'D'):
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}')
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('S', 'D'):
                break

        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break
                input('Press Enter to continue...')
                print('\n\n')

            displayHands(playerHand, dealerHand, True)

            playerValue = getHandValue(playerHand)
            dealerValue = getHandValue(dealerHand)

            if dealerValue > 21:
                print(f'Dealer Busts! You Win {bet}!')
                money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):
                print('You lost!')
                money -= bet
            elif playerValue > dealerValue:
                print(f'You won ${bet}')
                money += bet
            elif playerValue == dealerValue:
                print("It's a tie! Take your money back")

            input('Press enter to continue...')
            print('\n\n')