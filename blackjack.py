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
    money=100
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

        print(f'Bet: {bet}')
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            if getHandValue(playerHand) > 21:
                break
            
            move = getMove(playerHand, money - bet)

            if move == 'd'.upper():
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print(f'Bet increased to {bet}.')
                print(f'Bet: {bet}')

            if move in ('h'.upper(), 'd'.upper()):
                newCard = deck.pop()
                rank, suit = newCard
                print(f'You drew a {rank} of {suit}')
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    continue

            if move in ('s'.upper(), 'd'.upper()):
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

            if playerValue > 21:
                print('You busted everywhere hah!')
                money -= bet
            elif dealerValue > 21:
                print(f'Dealer Busts! You won ${bet}')
                money += bet
            elif (playerValue < dealerValue):
                print('You lost!')
                money -= bet
            elif playerValue > dealerValue:
                print(f'You won ${bet}')
                money += bet
            elif playerValue == dealerValue:
                print("It's a tie! Take your money back")

            input('Press enter to continue...')
            print('\n\n')


def getBet(maxBet):
    while True:
        print(f'How much do you bet? (1-{maxBet}) or QUIT)')
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing')
            sys.exit()
        if not bet.isdecimal():
            continue
        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2,11):
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    print()
    if showDealerHand:
        print(f'DEALER: {getHandValue(dealerHand)}')
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        displayCards(['backside'] + dealerHand[1:])

    print(f'PLAYER: {getHandValue(playerHand)}')
    displayCards(playerHand)

def getHandValue(cards):
    value = 0
    numberofAces = 0
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberofAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    value += numberofAces
    for i in range(numberofAces):
        if value + 10 <= 21:
            value += 10

    return value

def displayCards(cards):
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += ' ___  '
        if card == 'backside':
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            rank, suit = card
            rows[1] += f'|{rank.ljust(2)} | '
            rows[2] += f'| {suit} | '
            rows[3] += f"|_{rank.rjust(2,'_')}| "

    for row in rows:
        print(row)

def getMove(playerHand, money):
    while True:
        moves = ['(H)it', '(S)tand']
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')
        
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H','S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move

if __name__ == '__main__':
    main()