import re
from math import gcd
from functools import reduce

def part1(file_name):
    # open file stream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # read instruction set from the first line of the file:
    line = file.readline()
    instruction_set = [instruction for instruction in line[:-1]]

    file.readline() # pop whitespace seperator

    # iterate through rest of file
    nodes = {}
    for line in file:
        # split along the = delimiter. The first element is the node id and the second element is a tuple containing
        # the left and right nodes connected to this node
        node = re.sub(r'\s+', '', line.split('=')[0])
        connections = re.sub(r'\s+', '', line.split('=')[1])
        left_connection = re.sub(r'\W', '', connections.split(',')[0])
        right_connection = re.sub(r'\W', '', connections.split(',')[1])

        # read node data into nodes dictionary
        nodes[node] = (left_connection, right_connection)

    # all we need to do now is iterate through our nodes dictionary, following each instruction. If we arrive at ZZZ,
    # we immediately return the number of steps taken. Otherwise, we try again until we reach ZZZ.
    curr_node = "AAA"
    instruction_count = 0
    while curr_node != "ZZZ":
        if instruction_set[instruction_count % len(instruction_set)] == 'L':
            curr_node = nodes[curr_node][0]
        else:
            curr_node = nodes[curr_node][1]

        instruction_count += 1

        if curr_node == "ZZZ":
            return instruction_count


def part2(file_name):
    # open file for input streaming
    file = open(file_name, 'r', encoding="utf-8")

    # read the instruction set from the first line
    line = file.readline()
    instruction_set = [instruction for instruction in line[:-1]]

    file.readline() # pop whitespace line

    # iterate through the file line by line, this time marking starting nodes that end in A
    nodes = {}
    start_nodes = []
    for line in file:
        node = re.sub(r'\s+', '', line.split('=')[0])
        connections = re.sub(r'\s+', '', line.split('=')[1])
        left_connection = re.sub(r'\W', '', connections.split(',')[0])
        right_connection = re.sub(r'\W', '', connections.split(',')[1])

        # read node data into nodes dictionary
        nodes[node] = (left_connection, right_connection)

        # add node id to start_nodes if it ends in A
        if node[-1] == 'A':
            start_nodes.append(node)

    # Our algorithm here is based on the observation that our input seems constructed in such a way to periodically
    # return to the same goal node it visits first every n instructions for a given start node.
    # As such, we can simply store the number of steps required to reach a goal by each start node then find the lowest
    # common multiple of these numbers. The paths should converge after that many instructions. If we try to brute
    # force, we'll be here all day because the size of the path periods are not conducive to this strategy.

    # iterate through our start nodes
    periods = []
    for node in start_nodes:
        period_size = 0
        curr_node = node

        while curr_node[-1] != 'Z':
            if instruction_set[period_size % len(instruction_set)] == 'L':
                curr_node = nodes[curr_node][0]
            else:
                curr_node = nodes[curr_node][1]

            period_size += 1

        # once we've determined the goal period for the current node, we append it to our periods list
        periods.append(period_size)

    # return our lowest common multiple from our list of periods
    return reduce((lambda a, b: int(a*b / gcd(a,b))), periods)


if __name__ == "__main__":
    print(part1("day8_input.txt"))
    print(part2("day8_input.txt"))