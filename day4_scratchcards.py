import re


def part1(file_name):
    # open file for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # our point sum counter will record how many points our scratchers generate overall
    point_sum = 0

    # proceed line by line
    for line in file:
        # As in the first day problem, we can discard everything before the ':' symbol, as that is an irrelevant card id
        card = line.split(':')[1]

        # we now need to split again, this time around the '|' symbol which divides winning numbers from assigned
        # numbers
        numbers = card.split('|')

        # Our final split will be along whitespace to give us the integer strings on both sides
        winning_numbers = numbers[0].split()
        assigned_numbers = numbers[1].split()

        # we can now count matches. Note that we don't need to cast to int here, as we don't care about the actual
        # value of a number, only if it appears on both sides of the '|' divider
        match_counter = 0
        for number in winning_numbers:
            if number in assigned_numbers:
                match_counter += 1

        # with the number of matches known, we can now add the point value to our points counter. Note that the number
        # of points on a card always equals 2^(number of matches - 1) (1 match = 1 points, 2 = 2, 3 = 4, etc)
        if match_counter > 0:
            point_sum += 2**(match_counter-1)

    return point_sum


def part2(file_name):
    # open file for input processing
    file = open(file_name, 'r', encoding="utf-8")

    card_matrix = []
    # read our file into a card matrix for rapid and recursive access
    for line in file:
        card_matrix.append(line)

    # call our recursive card calculator function on our constructed card matrix, one card at a time. Store the
    # winnings of each card in a card_counter
    card_counter = 0
    for card_index in range(len(card_matrix)):
        card_counter += calculate_cards(card_matrix[card_index:])

    return card_counter


def calculate_cards(card_matrix):
    # a recursive function for determining the number of cards each scratcher gives us. The current card is the first
    # line of the card_matrix.

    # calculate the number of cards won on the scratcher card. First, we'll split the card ID out of the data and then
    # split along the '|' delimiter, as in part1()
    card = card_matrix[0].split(':')[1]
    numbers = card.split('|')
    winning_numbers = numbers[0].split()
    assigned_numbers = numbers[1].split()

    # cards_won counter records how many subsequent cards to call this function on
    cards_won = 0

    # calculate how many cards we now get from the current card
    for number in winning_numbers:
        if number in assigned_numbers:
            cards_won += 1

    # now, recursively calculate how many future cards we get from the newly won cards.
    if cards_won > 0:
        # subsequent_totals counter keeps track of the return values of cards won because of this card
        subsequent_totals = 1 # accounting for having this card

        for card_index in range(cards_won):
            subsequent_totals += calculate_cards(card_matrix[card_index+1:])

        return subsequent_totals
    else:
        return 1 # base case


if __name__ == "__main__":
    print(part1("day4_input.txt"))
    print(part2("day4_input.txt"))