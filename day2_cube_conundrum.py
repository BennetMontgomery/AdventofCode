import re


def part1(file_name):
    # max_cubes dictionary records what the maximum number of cubes should be for valid games, sorted by colour.
    max_cubes = {"red": 12, "green": 13, "blue": 14}

    # open file stream for reading input
    file = open(file_name, 'r', encoding="utf-8")

    # because we want a sum of id totals, we can simply add to a counter every time we encounter a valid game ID
    id_total = 0

    for line in file:
        # split the game string into a leading game identifier and following game sequence. Because : occurs immediately
        # after the Game ID, we can reliably split on ':'
        game = line.split(':')

        # each bag withdrawal is delimited by the ';' character, so splitting on ';' gives us a list of cube showings
        # to iterate through for each game
        game_seq = game[1].split(';')

        valid_game = True

        for show in game_seq:
            # locate where and if red, green, and blue totals are given in each showing of the game
            red_index = show.find("red")
            green_index = show.find("green")
            blue_index = show.find("blue")

            # counts are always 1 or 2 digits, so we can just cast the three characters preceding each colour name
            # to int to get the total number of cubes shown in this showing
            red_count = int(show[red_index - 3 : red_index - 1]) if red_index != -1 else 0
            green_count = int(show[green_index - 3 : green_index - 1]) if green_index != -1 else 0
            blue_count = int(show[blue_index - 3 : blue_index - 1]) if blue_index != -1 else 0

            # as long as the cube count stays within constraints, we continue to view the subsequent showings
            if red_count > max_cubes["red"] or green_count > max_cubes["green"] or blue_count > max_cubes["blue"]:
                valid_game = False
                break # stop reviewing a showing if constraints are violated

        if valid_game:
            # the id is simply the first part of each line in the file stripped of alphabetic characters and whitespace
            # and then cast to int
            id_total += int(re.sub(r'[a-zA-Z \s]', '', game[0]))

    return id_total


def part2(file_name):
    # open filestream for input processing
    file = open(file_name, 'r', encoding="utf-8")

    # power_sum counter records the "power" of each game, i.e. the minimum count of each cube colour multiplied together
    power_sum = 0

    for line in file:
        # this time, we don't need to split on the game ID demarker ':'. Instead, we're just going to jump right to
        # splitting by cube showing.
        game_seq = line.split(';')

        # mins dictionary records the minimum number of cubes of each colour for all showings in the game sequence to
        # have been possible
        mins = {"red": 0, "green": 0, "blue": 0}

        for show in game_seq:
            # locate where and if each colour is mentioned in each showing, and then record these counts. The same
            # logic about indexing applies here as in part 1.
            red_index = show.find("red")
            green_index = show.find("green")
            blue_index = show.find("blue")

            red_count = int(show[red_index - 3: red_index - 1]) if red_index != -1 else 0
            green_count = int(show[green_index - 3: green_index - 1]) if green_index != -1 else 0
            blue_count = int(show[blue_index - 3: blue_index - 1]) if blue_index != -1 else 0

            # check each count against the current minimums. If any minimums are exceeded, replace them.
            mins["red"] = red_count if red_count > mins["red"] else mins["red"]
            mins["green"] = green_count if green_count > mins["green"] else mins["green"]
            mins["blue"] = blue_count if blue_count > mins["blue"] else mins["blue"]

        # with the minimum cube counts now known, add the power of this game to the counter and proceed to the next one
        power_sum += mins["red"] * mins["green"] * mins["blue"]

    return power_sum


if __name__ == "__main__":
    print(part1("day2_input.txt"))
    print(part2("day2_input.txt"))
