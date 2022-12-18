with open("input.txt", "r") as f:
    lines = f.read().splitlines()

stream = lines[0]
rocks = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 2), (0, 1), (1, 1), (2, 1), (1, 0)},
    {(2, 2), (2, 1), (0, 0), (1, 0), (2, 0)},
    {(0, 3), (0, 2), (0, 1), (0, 0)},
    {(0, 1), (1, 1), (0, 0), (1, 0)},
]


def sim(max_rested):
    rested_coords = set()

    def collision(coords):
        return any([p[0] >= 7 or p[0] < 0 or p[1] < 0 or p in rested_coords for p in coords])

    rested_count = 0
    rock_index = 0
    jet_index = 0
    height = 0
    height_skip = None
    seen_cycle_states = {}

    while rested_count < max_rested:
        rock_coords = {(p[0] + 2, p[1] + height + 3) for p in rocks[rock_index]}

        while True:
            after_jet_coords = {(p[0] + (1 if stream[jet_index] == ">" else -1), p[1]) for p in rock_coords}
            curr_jet_index = jet_index
            jet_index = (jet_index + 1) % len(stream)

            if collision(after_jet_coords):
                after_jet_coords = rock_coords

            after_fall_coords = {(p[0], p[1] - 1) for p in after_jet_coords}

            if collision(after_fall_coords):
                rested_coords.update(after_jet_coords)
                height = max(set.union({height}, {p[1] + 1 for p in after_jet_coords}))
                rested_count += 1

                if not height_skip:
                    state = (rock_index, curr_jet_index, frozenset({(x, y - height) for x, y in rested_coords if y > (height - 15)}))
                    if state in seen_cycle_states:
                        last_state_rested_count, last_state_height = seen_cycle_states[state]
                        remaining_count = max_rested - rested_count
                        remaining_cycles = remaining_count // (rested_count - last_state_rested_count)
                        height_skip = remaining_cycles * (height - last_state_height)
                        rested_count += remaining_cycles * (rested_count - last_state_rested_count)
                    seen_cycle_states[state] = (rested_count, height)
                break
            else:
                rock_coords = after_fall_coords
        rock_index = (rock_index + 1) % len(rocks)
    return height + (height_skip or 0)


print(sim(2022))
print(sim(1000000000000))
