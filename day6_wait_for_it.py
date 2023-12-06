import math
import re

def part1(file_name):
    # open file stream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # read file contents into a matrix of time limits and target distances
    file_matrix = []
    for line in file:
        # The ':' delimiter seperates the line label from the integer entries
        numbers = line.split(':')[1]

        # we split again by whitespace on the number segment to give us our values and cast the resulting strings to
        # int
        file_matrix.append([int(number) for number in numbers.split()])

    # we can just brute force this problem. It's very simple. 0 and the maximum holding time are never going to be the
    # answer, so we iterate from 1 to the maximum holding time - 1 and check if that lets us hit the target time. If it
    # does, we increment the holding times counter and multiply the 3 holding times at the end to give us our answer.
    holding_times_matrix = []
    for race_index in range(len(file_matrix[0])):
        time_max = file_matrix[0][race_index]

        # holding_times counter records how many holding times give an acceptable distance
        holding_times = 0
        for time_candidate in range(1, time_max):
            if time_candidate*(time_max - time_candidate) >= file_matrix[1][race_index]:
                holding_times += 1

        # record the number of acceptable holding_times
        holding_times_matrix.append(holding_times)

    return math.prod(holding_times_matrix)


def part2(file_name):
    # open file stream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # this time we don't even need a file matrix. We just need two numbers.
    time_max = int(re.sub(r'\s+', '', file.readline().split(':')[1]))
    target_distance = int(re.sub(r'\s+', '', file.readline().split(':')[1]))

    # at first, this appears prohibitively harder to brute force than the first part, but that isn't true! Because we
    # have a maximum of 1 entry, our time complexity goes from O(n^2) to O(1*n) = O(n). We might as well just brute
    # force.
    holding_times = 0
    for time_candidate in range(1, time_max):
        if time_candidate*(time_max - time_candidate) >= target_distance:
            holding_times += 1

    return holding_times


if __name__ == '__main__':
    print(part1('day6_input.txt'))
    print(part2('day6_input.txt'))