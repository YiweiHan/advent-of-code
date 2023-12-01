import re

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# part 1
reg = re.compile(r"[0-9]")
total = 0
for line in lines:
    numbers = reg.findall(line)
    conc = numbers[0] + numbers[-1]
    total = total + int(conc)
print(total)


# part 2
reg = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|[0-9]))")
word2char = {
    "one": '1',
    "two": '2',
    "three": '3',
    "four": '4',
    "five": '5',
    "six": '6',
    "seven": '7',
    "eight": '8',
    "nine": '9',
}


def get_char(num):
    if num in word2char:
        return word2char[num]
    return num


total = 0
for line in lines:
    numbers = reg.findall(line)
    conc = get_char(numbers[0]) + get_char(numbers[-1])
    total = total + int(conc)

print(total)
