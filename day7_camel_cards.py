import copy
from enum import IntEnum

class hand_values(IntEnum):
    # enum ranking the various hand values
    HIGH_CARD=1
    ONE_PAIR=2
    TWO_PAIR=3
    THREE_OF_A_KIND=4
    FULL_HOUSE=5
    FOUR_OF_A_KIND=6
    FIVE_OF_A_KIND=7

def part1(file_name):
    # open file stream for input reading
    file = open(file_name, 'r', encoding="utf-8")

    # read in each hand and bid and store the hands and bids as tuples for later reference
    hands_bids_list = []
    for line in file:
        # the first segment is always the hand and the second segment is always the bid
        hands_bids_list.append((line.split()[0], int(line.split()[1])))

    # with our hands now read into a list, we're going to iterate hand by hand. Our algorithm will check how many times
    # each unique card identifier occurs in the input and then use that to calculate the hand value.
    ranks_hands_bids_list = []
    for hand, bid in hands_bids_list:
        # our hand set divides our hand into unique cards, which we can than use to find the counts of each card
        hand_set = list(set(list(hand)))
        card_counter = {}
        for card in hand_set:
            card_counter[card] = hand.count(card)

        # with our count of each unique card, we can now append our hand to our ranks tracker list with the enum value
        # of the hand rank. We'll check our set for all possible hand values.
        if 5 in card_counter.values():
            ranks_hands_bids_list.append((hand_values.FIVE_OF_A_KIND, hand, bid))
        elif 4 in card_counter.values():
            ranks_hands_bids_list.append((hand_values.FOUR_OF_A_KIND, hand, bid))
        elif 3 in card_counter.values():
            if 2 in card_counter.values():
                ranks_hands_bids_list.append((hand_values.FULL_HOUSE, hand, bid,))
            else:
                ranks_hands_bids_list.append((hand_values.THREE_OF_A_KIND, hand, bid))
        elif sum(count == 2 for count in card_counter.values()) == 2:
            ranks_hands_bids_list.append((hand_values.TWO_PAIR, hand, bid))
        elif 2 in card_counter.values():
            ranks_hands_bids_list.append((hand_values.ONE_PAIR, hand, bid))
        else:
            ranks_hands_bids_list.append((hand_values.HIGH_CARD, hand, bid))

    # now, we can divide our list along the lines of hand type. Once we have our hand type lists, we can order our lists
    # once again by internal ranking (e.g. 324TT > 234TT)
    high_card_hands = []
    pair_hands = []
    two_pair_hands = []
    three_of_a_kind_hands = []
    full_house_hands = []
    four_of_a_kind_hands = []
    five_of_a_kind_hands = []

    for rank, hand, bid in ranks_hands_bids_list:
        # we need to replace all values of face cards T J Q K A with ascii characters that will resolve to proper
        # ordering for the purposes of sorting the hands
        sortable_hand = (hand.replace('A', 'Z')
                .replace('K', 'Y')
                .replace('Q', 'X')
                .replace('J', 'W')
                .replace('T', 'V'))
        if rank == hand_values.HIGH_CARD:
            high_card_hands.append((sortable_hand, bid))
        elif rank == hand_values.ONE_PAIR:
            pair_hands.append((sortable_hand, bid))
        elif rank == hand_values.TWO_PAIR:
            two_pair_hands.append((sortable_hand, bid))
        elif rank == hand_values.THREE_OF_A_KIND:
            three_of_a_kind_hands.append((sortable_hand, bid))
        elif rank == hand_values.FULL_HOUSE:
            full_house_hands.append((sortable_hand, bid))
        elif rank == hand_values.FOUR_OF_A_KIND:
            four_of_a_kind_hands.append((sortable_hand, bid))
        else:
            five_of_a_kind_hands.append((sortable_hand, bid))

    # with the hands now partitioned, we can add our lists back together in sorted form to give us our final hand
    # ranking
    high_card_hands.sort()
    pair_hands.sort()
    two_pair_hands.sort()
    three_of_a_kind_hands.sort()
    full_house_hands.sort()
    four_of_a_kind_hands.sort()
    five_of_a_kind_hands.sort()
    ordered_hands = (high_card_hands + pair_hands + two_pair_hands + three_of_a_kind_hands + full_house_hands +
                     four_of_a_kind_hands + five_of_a_kind_hands)

    # now its time to calculate the return on all our bids, at which point we're done.
    return_counter = 0
    for hand_rank in range(len(ordered_hands)):
        return_counter += (hand_rank + 1) * ordered_hands[hand_rank][1]

    return return_counter


def part2(file_name):
    # open file stream for input reading
    file = open(file_name, 'r', encoding="utf-8")

    # read in each hand and bid and store the hands and bids as tuples for later reference
    hands_bids_list = []
    for line in file:
        # the first segment is always the hand and the second segment is always the bid
        hands_bids_list.append((line.split()[0], int(line.split()[1])))

    # our algorithmic approach is actually very similar to part 1. The main difference is Jokers are now wild. We add
    # a handler switch for jokers in the hand calculation section to deal with this.

    # proceed as in part 1
    ranks_hands_bids_list = []
    for hand, bid in hands_bids_list:
        hand_set = list(set(list(hand)))
        card_counter = {}
        for card in hand_set:
            card_counter[card] = hand.count(card)

        # calculate hand values. Special combos can be done with joker, so we'll handle things a bit differently if a
        # joker is present
        if 'J' in card_counter.keys():
            j_less_card_counter = copy.deepcopy(card_counter)
            del j_less_card_counter['J']

            if len(j_less_card_counter) <= 1:
                ranks_hands_bids_list.append((hand_values.FIVE_OF_A_KIND, hand, bid))
            elif 3 in j_less_card_counter.values():
                ranks_hands_bids_list.append((hand_values.FOUR_OF_A_KIND, hand, bid))
            elif sum(count == 2 for count in j_less_card_counter.values()) == 2: # only way to build a Joker full house
                ranks_hands_bids_list.append((hand_values.FULL_HOUSE, hand, bid))
            elif 2 in j_less_card_counter.values():
                if card_counter['J'] < 2:
                    ranks_hands_bids_list.append((hand_values.THREE_OF_A_KIND, hand, bid))
                else:
                    ranks_hands_bids_list.append((hand_values.FOUR_OF_A_KIND, hand, bid))
            else:
                if card_counter['J'] < 2:
                    ranks_hands_bids_list.append((hand_values.ONE_PAIR, hand, bid)) # minimum joker hand
                elif card_counter['J'] < 3:
                    ranks_hands_bids_list.append((hand_values.THREE_OF_A_KIND, hand, bid))
                else:
                    ranks_hands_bids_list.append((hand_values.FOUR_OF_A_KIND, hand, bid))
        else: # logic is identical to part 1
            if 5 in card_counter.values():
                ranks_hands_bids_list.append((hand_values.FIVE_OF_A_KIND, hand, bid))
            elif 4 in card_counter.values():
                ranks_hands_bids_list.append((hand_values.FOUR_OF_A_KIND, hand, bid))
            elif 3 in card_counter.values():
                if 2 in card_counter.values():
                    ranks_hands_bids_list.append((hand_values.FULL_HOUSE, hand, bid,))
                else:
                    ranks_hands_bids_list.append((hand_values.THREE_OF_A_KIND, hand, bid))
            elif sum(count == 2 for count in card_counter.values()) == 2:
                ranks_hands_bids_list.append((hand_values.TWO_PAIR, hand, bid))
            elif 2 in card_counter.values():
                ranks_hands_bids_list.append((hand_values.ONE_PAIR, hand, bid))
            else:
                ranks_hands_bids_list.append((hand_values.HIGH_CARD, hand, bid))


    high_card_hands = []
    pair_hands = []
    two_pair_hands = []
    three_of_a_kind_hands = []
    full_house_hands = []
    four_of_a_kind_hands = []
    five_of_a_kind_hands = []

    for rank, hand, bid in ranks_hands_bids_list:
        # we need to replace all values of face cards T J Q K A with ascii characters that will resolve to proper
        # ordering for the purposes of sorting the hands. Once again identical to part 1 with the caveat that J
        # now resolves to 1
        sortable_hand = (hand.replace('A', 'Z')
                         .replace('K', 'Y')
                         .replace('Q', 'X')
                         .replace('J', '1')
                         .replace('T', 'W'))
        if rank == hand_values.HIGH_CARD:
            high_card_hands.append((sortable_hand, bid))
        elif rank == hand_values.ONE_PAIR:
            pair_hands.append((sortable_hand, bid))
        elif rank == hand_values.TWO_PAIR:
            two_pair_hands.append((sortable_hand, bid))
        elif rank == hand_values.THREE_OF_A_KIND:
            three_of_a_kind_hands.append((sortable_hand, bid))
        elif rank == hand_values.FULL_HOUSE:
            full_house_hands.append((sortable_hand, bid))
        elif rank == hand_values.FOUR_OF_A_KIND:
            four_of_a_kind_hands.append((sortable_hand, bid))
        else:
            five_of_a_kind_hands.append((sortable_hand, bid))

    # with the hands now partitioned, we can add our lists back together in sorted form to give us our final hand
    # ranking
    high_card_hands.sort()
    pair_hands.sort()
    two_pair_hands.sort()
    three_of_a_kind_hands.sort()
    full_house_hands.sort()
    four_of_a_kind_hands.sort()
    five_of_a_kind_hands.sort()
    ordered_hands = (high_card_hands + pair_hands + two_pair_hands + three_of_a_kind_hands + full_house_hands +
                     four_of_a_kind_hands + five_of_a_kind_hands)

    # now its time to calculate the return on all our bids, at which point we're done.
    return_counter = 0
    for hand_rank in range(len(ordered_hands)):
        return_counter += (hand_rank + 1) * ordered_hands[hand_rank][1]

    return return_counter


if __name__ == '__main__':
    print(part1('day7_input.txt'))
    print(part2('day7_input.txt'))