import re


def main():
    # open filestream for reading input
    file = open('day1_input.txt', 'r', encoding="utf-8")

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

    print(sum(calibration_values))


if __name__ == "__main__":
    main()