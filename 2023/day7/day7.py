import re
from functools import cmp_to_key
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

hands = []
for line in lines:
    cards, bid = re.split(r"\s+", line)
    bid = int(bid)
    hands.append((cards, bid))

card_rankings = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


def get_type_level(cards):
    m = defaultdict(int)

    for c in cards:
        m[c] = m[c] + 1

    counts = list(m.values())
    if 5 in counts:
        type_level = 7
    elif 4 in counts:
        type_level = 6
    elif 3 in counts and 2 in counts:
        type_level = 5
    elif 3 in counts:
        type_level = 4
    elif len(list(filter(lambda x: x == 2, counts))) == 2:
        type_level = 3
    elif 2 in counts:
        type_level = 2
    else:
        type_level = 1
    return type_level


card_rankings_joker = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


def get_type_level_joker(cards):
    non_j = {c for c in cards if c != "J"}
    possible_new_cards = [cards] + [re.sub(r"J", char, cards) for char in non_j]
    new_type_levels = [get_type_level(new_cards) for new_cards in possible_new_cards]
    return max(new_type_levels)


def add_type_level(hands, joker=False):
    processed_hands = []
    for h in hands:
        if joker and "J" in h[0]:
            processed_hands.append((h[0], get_type_level_joker(h[0]), h[1]))
        else:
            processed_hands.append((h[0], get_type_level(h[0]), h[1]))
    return processed_hands


def cmp_hands_with_rankings(h1, h2, rankings_map):
    if h1[1] != h2[1]:
        return h1[1] - h2[1]
    for c1, c2 in zip(h1[0], h2[0]):
        if c1 != c2:
            return rankings_map[c1] - rankings_map[c2]
    return 0


def cmp_hands(h1, h2):
    return cmp_hands_with_rankings(h1, h2, rankings_map=card_rankings)


def cmp_hands_joker(h1, h2):
    return cmp_hands_with_rankings(h1, h2, rankings_map=card_rankings_joker)


def winnings(sorted_hands):
    total = 0
    for i, h in enumerate(sorted_hands):
        total = total + (i + 1) * h[2]
    return total


# part 1
processed_hands = add_type_level(hands)
sorted_hands = sorted(processed_hands, key=cmp_to_key(cmp_hands))
print(winnings(sorted_hands))

# part 2
processed_hands = add_type_level(hands, joker=True)
sorted_hands = sorted(processed_hands, key=cmp_to_key(cmp_hands_joker))
print(winnings(sorted_hands))
