import re


def part1(file_name):
    # open filestream for reading input
    file = open(file_name, 'r', encoding="utf-8")

    # storage for calibration values (first and last digit concatenated)
    calibration_values = []

    for line in file:
        # regex resolves to all alphabetic and whitespace characters
        # stripped_line is line minus these characters
        stripped_line = re.sub(r'[a-zA-Z \s]', '', line)

        # store first and last digits. Store same digit twice if there is only one digit.
        # must be cast to int to allow proper resolution of sum method
        digits = int(stripped_line[0] + stripped_line[-1])
        calibration_values.append(digits)

    return sum(calibration_values)


def part2(file_name):
    # open filestream for reading input
    file = open(file_name, 'r', encoding="utf-8")

    # storage for calibration values (first and last digit concatenated)
    calibration_values = []

    # alphabetic substrings for recognized digits
    alpha_substrings = {"one": '1', "two": '2', "three": '3', "four": '4', "five": '5',
                        "six": '6', "seven": '7', "eight": '8', "nine": '9'}


    for line in file:
        # iterate through the string and place a digit at the first and last location of a digit substring. Note that
        # digit substrings may overlap, so we can't just outright replace them! We don't care about intermediate
        # locations.
        for alpha_code in alpha_substrings:
            first_alpha_index = line.find(alpha_code)
            second_alpha_index = line.rfind(alpha_code)

            if first_alpha_index != -1: # string not found if the result is -1
                line = line[:first_alpha_index+1] + alpha_substrings[alpha_code] + line[first_alpha_index+1:]

            if second_alpha_index != -1:
                line = line[:second_alpha_index+1] + alpha_substrings[alpha_code] + line[second_alpha_index+1:]

            # why index+1? Because inserting a number at the correct index can still cause overlapping numbers to break.
            # e.g., eightwo will resolve to eigh2two and not detect the 8 unless it instead resolves to eight2wo

        # strip lines as in part 1
        stripped_line = re.sub(r'[a-zA-Z \s]', '', line)

        # append first and last digit cast to int to calibration values
        digits = int(stripped_line[0] + stripped_line[-1])
        calibration_values.append(digits)

    print(calibration_values[36])

    return sum(calibration_values)


def main():
    print(part1("day1_input.txt"))
    print(part2("day1_input.txt"))


if __name__ == "__main__":
    main()