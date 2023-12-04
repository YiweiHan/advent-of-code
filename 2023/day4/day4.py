import re
from collections import deque

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

matches_by_card_id = {}

for line in lines:
    parts = re.split(r":\s+", line)
    card_id = int(re.split(r"\s+", parts[0])[1])
    winning, have = re.split(r"\s+\|\s+", parts[1])
    winning = {int(x) for x in re.split(r"\s+", winning)}
    have = {int(x) for x in re.split(r"\s+", have)}
    matches = len(winning.intersection(have))
    matches_by_card_id[card_id] = matches

# part 1
score = 0
for card_id, matches in matches_by_card_id.items():
    if matches > 0:
        score = score + 2 ** (matches - 1)
print(score)

# part 2
cards = deque(matches_by_card_id.keys())
total_card_count = 0
while len(cards) > 0:
    card_id = cards.popleft()
    matches = matches_by_card_id[card_id]
    next_card_ids = list(filter(lambda x: x in matches_by_card_id, range(card_id + 1, card_id + matches + 1)))
    cards.extend(next_card_ids)
    total_card_count = total_card_count + 1

print(total_card_count)
