with open("input.txt", "r") as f:
    lines = f.read().splitlines()


# part 1
def line_score_part1(line):
    if line == "C X" or line == "A Y" or line == "B Z":
        outcome_score = 6
    elif ord(line[2]) - (ord("X") - ord("A")) == ord(line[0]):
        outcome_score = 3
    else:
        outcome_score = 0

    return outcome_score + ord(line[2]) - ord("X") + 1


print(sum(map(line_score_part1, lines)))


# part 2 - attempted golfing
def line_score_part2(line):
    shift = 0 if line[2] == "Y" else 1 if line[2] == "Z" else 2
    return line_score_part1(line[0:2] + chr((ord(line[0]) - ord("A") + shift) % 3 + ord("X")))


print(sum(map(line_score_part2, lines)))
