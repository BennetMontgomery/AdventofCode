import re
import copy


def part1(file_name):
    # open file stream for input reading
    file = open(file_name, 'r', encoding="utf-8")

    file_matrix = []

    # begin processing through the file line by line
    for line in file:
        # read lines into file_matrix for rapid reference later
        file_matrix.append(line)

    parts_counter = 0

    # proceed line by line
    for line_index in range(1, len(file_matrix)):
        # the logic of our algorithm is: there is never a special character in the first or last line nor in the first
        # or last 3 indices of a line. There is also never a case where a number borders more than one special character
        # This may just be random chance for our specific input, but it is a useful pattern for our solution.
        # Regardless, we can scan for special characters and safely peek at all neighbouring characters in a 2D
        # character matrix representing the file without risking an index error where "neighbouring" implies the
        # following spatial relationship:
        # [[[.].].].[.[.[.]]]
        # [[[.].].]*[.[.[.]]]
        # [[[.].].].[.[.[.]]]
        # where a . character is a potential neighbour if the character in the level of square bracket notation
        # above is a digit and so,

        # proceed character by character
        for char_index in range(3, len(file_matrix[line_index]) - 4):
            # evaluate if current character is a special symbol
            if re.match(r'\W', file_matrix[line_index][char_index]) and file_matrix[line_index][char_index] != '.':
                # call our neighbour calculator
                neighbours = calculate_neighbours(file_matrix, line_index, char_index)

                # now we begin parsing our neighbour indices into integers. We do this by identifying which indices
                # on each line are consecutive, concatenating the digit characters in consecutive indices, and casting
                # the results to int.
                numbers = []

                for line in range(len(neighbours)):
                    if len(neighbours[line]) == 0:
                        # if we don't skip empty lines, strange behaviours will result due to indexing defaults
                        continue

                    # we add the first digit character on each line as the initial character of the first number string
                    numbers.append(file_matrix[line_index + (line - 1)][neighbours[line][0]])
                    for digit_index in range(1, len(neighbours[line])):
                        # proceeding digit by digit, if the next digit is consecutive to the previous digit, append
                        # it to the building number string
                        if neighbours[line][digit_index] == neighbours[line][digit_index-1] + 1:
                            numbers[-1] += file_matrix[line_index + (line - 1)][neighbours[line][digit_index]]
                        # otherwise, we cast the newly built number to int and start the next number string
                        elif (line == 0 and digit_index != 0) or line > 0:
                            numbers[-1] = int(numbers[-1])
                            numbers.append(file_matrix[line_index + (line - 1)][neighbours[line][digit_index]])

                    # when each line sweep terminates, we need to cast the final number generated in the previous line
                    # to int to prevent merging numbers between lines
                    numbers[-1] = int(numbers[-1])

                # with the neighbouring numbers now generated, we add their sums to the building parts counter
                parts_counter += sum(numbers)

    return parts_counter


def part2(file_name):
    # open filestream for input reading
    file = open(file_name, 'r', encoding="utf-8")

    file_matrix = []

    # read lines into file matrix for rapid reference
    for line in file:
        file_matrix.append(line)

    gear_ratio = 0

    # proceed line by line. What lines and characters we review uses the exact same logic as shown in part1().
    for line_index in range(1, len(file_matrix)):
        for char_index in range(3, len(file_matrix[line_index]) - 4):
            # our pattern matching this time is actually much simpler, as we only care about the special character *
            # and therefore don't need to simplify with a regular expression
            if file_matrix[line_index][char_index] == '*':
                # call our neighbour calculator
                neighbours = calculate_neighbours(file_matrix, line_index, char_index)

                # now, we'll do the same casting to int of our neighbour digit characters as we did in part 1. I simply
                # don't feel like making a dedicated function for this task so I'm just pasting the same code here.
                numbers = []

                for line in range(len(neighbours)):
                    if len(neighbours[line]) == 0:
                        continue

                    # we add the first digit character on each line as the initial character of the first number string
                    numbers.append(file_matrix[line_index + (line - 1)][neighbours[line][0]])
                    for digit_index in range(1, len(neighbours[line])):
                        # proceeding digit by digit
                        if neighbours[line][digit_index] == neighbours[line][digit_index - 1] + 1:
                            numbers[-1] += file_matrix[line_index + (line - 1)][neighbours[line][digit_index]]
                        elif (line == 0 and digit_index != 0) or line > 0:
                            numbers[-1] = int(numbers[-1])
                            # start the next number string
                            numbers.append(file_matrix[line_index + (line - 1)][neighbours[line][digit_index]])

                    # cast the final number generated per line to int
                    numbers[-1] = int(numbers[-1])

                # with our integer neighbours now cast, we need to check if we have exactly two neighbours. If we do,
                # we have a gear!
                if len(numbers) == 2:
                    gear_ratio += numbers[0] * numbers[1]

    return gear_ratio


def calculate_neighbours(file_matrix, line_index, char_index):
    # utility function used by both parts to calculate what numbers neighbour a special character. The logic of
    # what is meant by a "neighbour" is further explained in part1().

    # evaluate neighbouring characters and store digits
    prev_line_indices = []
    same_line_indices = []
    next_line_indices = []
    for neighbour_index in range(char_index - 3, char_index + 4):
        if file_matrix[line_index - 1][neighbour_index].isdigit():
            prev_line_indices.append(neighbour_index)

        if file_matrix[line_index][neighbour_index].isdigit():
            same_line_indices.append(neighbour_index)

        if file_matrix[line_index + 1][neighbour_index].isdigit():
            next_line_indices.append(neighbour_index)

    neighbours = [prev_line_indices, same_line_indices, next_line_indices]
    true_neighbours = copy.deepcopy(neighbours)  # deep copying necessary to prevent for loop funny business!

    # pop digits that are false neighbours. For example, the first digit stored on each line is only a true
    # neighbour if it forms a contiguous number with the next two characters
    for line in range(len(neighbours)):
        for index in neighbours[line]:
            # remove false neighbours from the left side
            if index < char_index - 2 and index + 2 not in neighbours[line]:
                true_neighbours[line].remove(index)
            elif index < char_index - 1 and index + 1 not in neighbours[line]:
                true_neighbours[line].remove(index)

            # remove false neighbours from the right side
            if index > char_index + 1 and index - 1 not in neighbours[line]:
                true_neighbours[line].remove(index)
            elif index > char_index + 2 and index - 2 not in neighbours[line]:
                true_neighbours[line].remove(index)

    # true neighbours are now established. We just need to cast these digit sequences to int and add them
    # to our parts counter. We start by constructing these digit sequences in our numbers array.
    return true_neighbours


if __name__ == "__main__":
    print(part1("day3_input.txt"))
    print(part2("day3_input.txt"))