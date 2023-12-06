import itertools
import sys


def part1(file_name):
    # opent the filestream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # the input file format is a bit different this time compared to previous days. Instead of a raw file, it consists
    # of sections split by a blank line and section headers. As a result, compiling the input data is going to be a bit
    # more complex.
    # The first data we're going to read is the seed numbers. The numbers occur on the first line after the delimiter
    # ':'. So we're going to split the first line on this delimiter, then split the second line segment on whitespace,
    # and cast all the number strings to int to give us our list of seed numbers
    seed_numbers = [int(number) for number in file.readline().split(':')[1].split()]

    # the rest of the file consists of rules for number maps. Each map is seperated from the previous by a newline and
    # map title. The actual title of each map doesn't matter, but what's important is that each map maps the previous
    # step of the seed -> location calculation to the next step of the calculation. Transfer_maps list is our list of
    # sequential maps and curr_map is the currently constructing map
    transfer_maps = []
    curr_map = []

    for line in file:
        # split the line on whitespace and then determine if it's the title of a new map
        split_line = line.split()

        # we'll just ignore empty lines. We don't gain anything from considering them
        if split_line == []:
            continue

        # if we're at the title of a new map, close off the old map and start a new one, then continue to the next
        # line
        if '-' in split_line[0]:
            if curr_map != []:
                transfer_maps.append(curr_map)
                curr_map = []

            continue

        # if we're at a map entry, we'll add the throuple cast to int to the growing map
        curr_map.append([int(number) for number in split_line])

    # append the final map to the transfer_maps
    transfer_maps.append(curr_map)

    # with our seed numbers known and our maps now cached, we'll proceed seed by seed and record the minimum location
    # number in min_location
    min_location = sys.maxsize

    for seed in seed_numbers:
        curr_num = seed

        # proceed map by map and determine the current number
        for map in transfer_maps:
            for rule in map:
                if curr_num > rule[1] and curr_num < rule[1] + rule[2]:
                    curr_num = rule[0] + (curr_num - rule[1])
                    break
                # if we reach the end of the map without a match curr_num simply maps to itself and we proceed to the
                # next map

        # with our location number now known, we keep it if it's less than our last known minimum location
        min_location = curr_num if curr_num < min_location else min_location

    return min_location


def part2(file_name):
    # open filestream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # we're going to have to take a different approach this time. The time complexity of our part1 solution is O(nml)
    # where n = seed count, m = map count, l = rule count which is basically O(n^3). Not good! This time, we have
    # billions or trillions of numbers to check! Luckily, we don't even need to reduce the time complexity if we can
    # shave down the value of n to something more manageable...

    # read in the file data as in part1
    seed_numbers = [int(number) for number in file.readline().split(':')[1].split()]

    transfer_maps = []
    curr_map = []

    for line in file:
        split_line = line.split()

        if split_line == []:
            continue

        if '-' in split_line[0]:
            if curr_map != []:
                transfer_maps.append(curr_map)
                curr_map = []

            continue

        curr_map.append([int(number) for number in split_line])

    transfer_maps.append(curr_map)

    # with our data now read, we proceed to the meat of our solution. The general idea here is to work exclusively with
    # number ranges instead of individual numbers. Instead of curr_num as in part1(), we're going to treat each pair of
    # numbers as a start point and end point in a number range. We're then going to compare this to each map rule source
    # range. There are 5 cases:
    # 1. [ current ]                Overlap from below
    #       [ map rule source ]
    # 2.                [ current ]     Overlap from above
    #   [ map rule source ]
    # 3.    [ current ]                 Current range within map
    #   [ map rule source ]
    # 4. [          current         ]   Map within current range
    #       [ map rule source ]
    # 5. [ current ]                            No overlap
    #                   [ map rule source ]
    # In all cases except 3 and 5, we split the current range into mapped and unmapped portions. We then use the map
    # rule to find new current seed ranges and proceed until we terminate at the location map. The minimum location for
    # a given seed range is the lowest start point of all final sub-ranges.

    min_location = sys.maxsize

    # iterate through every pair of numbers in our seed array. The first number is the initial lower bound of the range
    # and the second number is the size of our range.
    cases_hit = []
    for start_index in range(0, len(seed_numbers), 2):
        ranges = [[seed_numbers[start_index], seed_numbers[start_index] + seed_numbers[start_index + 1] - 1]]

        # now, proceed through the map sequence rule by rule and check against the five possible overlap cases. Generate
        # a new list of ranges from this each time.
        map_counter = 0
        for map_ in transfer_maps:
            map_counter += 1
            # trimmed_ranges tracks ranges not relevant to different rules.
            trimmed_ranges = []
            new_ranges = []

            for start, end in ranges:
                for rule in map_:
                    # case 1
                    if start < rule[1] and end > rule[1] and end < rule[1] + rule[2]:
                        # note the first portion of the range being cut out and thrown to our trimmed ranges
                        trimmed_ranges.append([start, rule[1] - 1])
                        # now, resolve the outcome of the mapping rule. Rule[1] always resolves to rule[0] as per the
                        # mapping rules and the difference between the start and end point added to rule[0] is the new
                        # end point.
                        new_ranges.append([rule[0], rule[0] + (end - start)])
                    # case 2
                    if start >= rule[1] and start < rule[1] + rule[2] and end >= rule[1] + rule[2]:
                        # we do the inverse of case 1 for case 2
                        trimmed_ranges.append([rule[1] + rule[2] + 1, end])
                        new_ranges.append([rule[0] + (start - rule[1]), rule[0] + rule[2]])
                    # case 3
                    if start >= rule[1] and start < rule[1] + rule[2] and end < rule[1] + rule[2]:
                        # in this case, no range is trimmed because there is nothing outside of the map rule
                        new_ranges.append([rule[0] + (start - rule[1]), rule[0] + (end - rule[1])])
                    # case 4
                    if start < rule[1] and end >= rule[1] + rule[2]:
                        # this time we trim both ends of the range and then add the target sequence to our new
                        # ranges
                        trimmed_ranges.append([start, rule[1] - 1])
                        trimmed_ranges.append([rule[1] + rule[2] + 1, end])
                        new_ranges.append([rule[1], rule[1] + rule[2]])
                    # case 5: no coincidence
                    if (start < rule[1] and end < rule[1]) or (start >= rule[1] + rule[2]):
                        # this range doesn't follow this rule. We'll dump it in our trimmed ranges for now.
                        trimmed_ranges.append([start, end])

            # dump duplicates in the trimmed ranges
            trimmed_ranges = list(range_ for range_, _ in itertools.groupby(trimmed_ranges))

            # now, we need to make sure we ONLY add the appropriate seed number ranges. What we don't want to happen
            # is for trimmed_ranges to contain a range that should be caught by our map rules in this step.
            true_ranges = []
            for trim_index in range(len(trimmed_ranges)):
                # adjusted boolean tells us whether or not to append this range to the true_ranges at the end
                adjusted = False
                for rule in map_:
                    # case 2
                    if trimmed_ranges[trim_index][0] >= rule[1] and trimmed_ranges[trim_index][0] < rule[1] + rule[2]:
                        if trimmed_ranges[trim_index][0] < rule[1]: # case 1
                            true_ranges.append([trimmed_ranges[trim_index][0], rule[1] - 1])
                        elif trimmed_ranges[trim_index][1] >= rule[1] + rule[2]: # not case 3
                            true_ranges.append([rule[1] + rule[2] - 1, trimmed_ranges[trim_index][1]])
                        # in any case, mark this range as falling under a case that isn't 5
                        adjusted = True
                    # case 4
                    elif trimmed_ranges[trim_index][0] < rule[1] and trimmed_ranges[trim_index][1] >= rule[1] + rule[2]:
                        true_ranges.append([rule[1] + rule[2], trimmed_ranges[trim_index][1]])
                        true_ranges.append([trimmed_ranges[trim_index][0], rule[1] - 1])
                        # mark range as adjusted
                        adjusted = True
                    # case 5

                true_ranges = true_ranges + [trimmed_ranges[trim_index]] if not adjusted else true_ranges


            # combine our range sets and dump out any duplicates
            merged_ranges = [list(range_) for range_ in set(map(tuple, true_ranges + new_ranges))]
            # now we need to merge overlapping ranges. If we don't do this the number of ranges being tracked will
            # explode exponentially
            merged_ranges.sort()
            ranges = []
            while len(merged_ranges) > 1:
                if merged_ranges[0][1] >= merged_ranges[1][0] and merged_ranges[0][1] <= merged_ranges[1][1]:
                    merged_ranges[0][1] = merged_ranges[1][1] # merge overlapping ranges
                    merged_ranges.pop(1) # pop second range, as it is now accounted for in first range
                elif merged_ranges [0][1] < merged_ranges[1][0]:
                    ranges.append(merged_ranges[0]) # pop the first element if not overlapping with the 2nd
                    merged_ranges.pop(0)
                elif merged_ranges[0][1] >= merged_ranges[1][1]:
                    merged_ranges.pop(1)  # pop second element if it's in the first one but don't add it to ranges

            ranges = ranges + merged_ranges # add last range

        # check if our final ranges' lowest location is lower than the current found minimum
        ranges.sort()
        min_location = ranges[0][0] if ranges[0][0] < min_location else min_location

    return min_location


if __name__ == "__main__":
    print(part1("day5_input.txt"))
    print(part2("day5_input.txt"))
