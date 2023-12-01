import re
from math import prod
import concurrent.futures


def max_possible_geode(args):
    minutes_remaining, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = args

    def can_get_higher_max_geode(max_geode, minutes_remaining, geode_robots, geode):
        return (geode + sum(range(geode_robots, geode_robots + minutes_remaining))) > max_geode

    minutes_remaining -= 2
    ore_robots = 1
    clay_robots = obsidian_robots = geode_robots = 0
    ore = 2
    clay = obsidian = geode = 0

    start_state = (ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode, minutes_remaining)

    seen_states = set()
    s = [start_state]
    max_geode = 0

    while s:
        state = s.pop()
        ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode, minutes_remaining = state

        if minutes_remaining <= 0:
            max_geode = max(max_geode, geode)
            continue

        if not can_get_higher_max_geode(max_geode, minutes_remaining, geode_robots, geode):
            continue

        if state in seen_states:
            continue
        seen_states.add(state)

        new_ore = ore + ore_robots
        new_clay = clay + clay_robots
        new_obsidian = obsidian + obsidian_robots
        new_geode = geode + geode_robots

        if ore >= ore_robot_ore_cost:
            s.append((ore_robots + 1, clay_robots, obsidian_robots, geode_robots, new_ore - ore_robot_ore_cost, new_clay, new_obsidian, new_geode, minutes_remaining - 1))
        if ore >= clay_robot_ore_cost:
            s.append((ore_robots, clay_robots + 1, obsidian_robots, geode_robots, new_ore - clay_robot_ore_cost, new_clay, new_obsidian, new_geode, minutes_remaining - 1))
        if ore >= obsidian_robot_ore_cost and clay >= obsidian_robot_clay_cost:
            s.append((ore_robots, clay_robots, obsidian_robots + 1, geode_robots, new_ore - obsidian_robot_ore_cost, new_clay - obsidian_robot_clay_cost, new_obsidian, new_geode, minutes_remaining - 1))
        if ore >= geode_robot_ore_cost and obsidian >= geode_robot_obsidian_cost:
            s.append((ore_robots, clay_robots, obsidian_robots, geode_robots + 1, new_ore - geode_robot_ore_cost, new_clay, new_obsidian - geode_robot_obsidian_cost, new_geode, minutes_remaining - 1))
            continue

        s.append((ore_robots, clay_robots, obsidian_robots, geode_robots, new_ore, new_clay, new_obsidian, new_geode, minutes_remaining - 1))

    return max_geode


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.read().splitlines()

    bps = {}
    for line in lines:
        bp_id, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = map(int, filter(bool, re.split("[a-zA-Z :.]+", line)))
        bps[bp_id] = (ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost)

    # part 1
    args = [(24, *props) for _, props in bps.items()]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print(sum([bp_id * geode for bp_id, geode in zip(bps.keys(), executor.map(max_possible_geode, args, chunksize=1))]))

    # part 2
    args = [(32, *props) for _, props in bps.items()][:3]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print(prod(executor.map(max_possible_geode, args, chunksize=1)))
