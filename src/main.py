import os
import csv
import ast
import random
import copy

def main():
    question_count = 2

    # Get the absolute paths to the data files
    script_directory = os.path.dirname(os.path.realpath(__file__))
    member_table_path = os.path.join(script_directory, "..", "data", "member_table.csv")
    groups_path = os.path.join(script_directory, "..", "data", "group_assignment.csv")

    # Load member names and group assignments
    member_table = load_member_table(member_table_path)
    groups = load_groups(groups_path)

    # Generate a table assigning presenters to each questioner
    questioner_presenter_table = generate_questioner_presenter_table(question_count, groups)

    # Shuffle the questioner-presenter pairs to ensure diverse groupings
    shuffled_table = shuffle_questioner_presenter_table(question_count, groups, questioner_presenter_table)

    # Output the result in a human-readable format
    print(f"{format_questioner_presenters(member_table, shuffled_table)}\n")

    # Output the result in CSV format
    print(f"{generate_csv(member_table, shuffled_table)}\n")

    # aaa
    reversed_table = reverse_questioner_presenter_table(shuffled_table)

    # Output the result in a human-readable format
    print(f"{format_presenter_questioners(member_table, reversed_table)}\n")

    # Output the result in CSV format
    print(generate_csv(member_table, reversed_table))

# Load member IDs and names from CSV
def load_member_table(path):
    member_table = {}
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            member_id, name = row
            member_table[int(member_id)] = name

    return member_table

# Load group assignments from CSV
def load_groups(path):
    groups = []
    with open(path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            member_list = ast.literal_eval(row["member_list"])
            groups.append(member_list)

    return groups

# Get the next group's index, wrapping around at the end
def get_next_index(index, groups):
    if index != len(groups) - 1:
        return index + 1
    else:
        return 0

# Randomly generate presenter pairs from group members
def generate_presenter_pairs(group_members, pair_size):
    while True:
        presenters = group_members * pair_size
        random.shuffle(presenters)
        presenter_pairs = []

        while len(presenters) > 0:
            pair = presenters[:pair_size]
            presenters = presenters[pair_size:]

            # Ensure all elements in the pair are unique
            if len(set(pair)) == pair_size:
                presenter_pairs.append(pair)
            else:
                break

        # Ensure all members have valid presenter pairs
        if len(presenter_pairs) == len(group_members):
            break

    return presenter_pairs

# Assign presenters to each questioner across groups
def generate_questioner_presenter_table(question_count, groups):
    member_count = sum(len(group) for group in groups)
    questioner_presenter_table = {i: [] for i in range(member_count)}

    unpaired_presenters = []
    unpaired_questioner = 0
    swap_questioner = 0

    for i in range(len(groups)):
        next_i = get_next_index(i, groups)

        # Get presenter pairs from the next group
        presenter_pairs = generate_presenter_pairs(groups[next_i], question_count)

        # Handle group size mismatches
        if len(groups[i]) < len(groups[next_i]):
            unpaired_presenters = presenter_pairs[-1]

        if len(groups[i]) > len(groups[next_i]):
            unpaired_questioner = groups[i][-1]
            swap_questioner = random.choice(groups[next_i])
            presenter_pairs.append([0, 0])  # Temporary placeholder
        
        # Assign presenter pairs to questioners
        for j in range(len(groups[i])):
            questioner = groups[i][j]
            questioner_presenter_table[questioner] = presenter_pairs[j]

    # Swap presenters to balance group size differences
    if unpaired_questioner != 0:
        questioner_presenter_table[unpaired_questioner] = questioner_presenter_table[swap_questioner]
        questioner_presenter_table[swap_questioner] = unpaired_presenters

    return questioner_presenter_table

# Lookup member name by ID
def get_member_name(member_id, member_table):
    return member_table[member_id]

# Shuffle questioners across groups to diversify pairings
def shuffle_questioner_presenter_table(question_count, groups, questioner_presenter_table):
    table = copy.deepcopy(questioner_presenter_table)
    shuffled_groups = [random.sample(group, len(group)) for group in groups]
    swap_index = question_count // 2

    for i in range(len(groups) - 1):
        swap_count = min(len(groups[i]), len(groups[i + 1]))
        for j in range(swap_count):
            first_key = shuffled_groups[i][j]
            second_key = shuffled_groups[i + 1][j]

            first_tail = table[first_key][swap_index:]
            second_tail = table[second_key][swap_index:]

            table[first_key][swap_index:] = second_tail
            table[second_key][swap_index:] = first_tail

    return table

# 
def reverse_questioner_presenter_table(questioner_presenter_table):
    reversed_table = {}

    for key, values in questioner_presenter_table.items():
        for value in values:
            if value not in reversed_table:
                reversed_table[value] = []
            reversed_table[value].append(key)

    return reversed_table

# Format result into a readable string
def format_questioner_presenters(member_table, questioner_presenter_table):
    result = []

    for questioner, presenters in questioner_presenter_table.items():
        questioner_name = get_member_name(questioner, member_table)
        presenter_names = list(map(lambda presenter: f"'{get_member_name(presenter, member_table)}'", presenters))
        result.append(f"questioner: '{questioner_name}', presenters: [{", ".join(presenter_names)}]")

    return "\n".join(result)

# Format result into a readable string
def format_presenter_questioners(member_table, reversed_table):
    result = []

    for presenter, questioners in reversed_table.items():
        presenter_name = get_member_name(presenter, member_table)
        questioner_names = list(map(lambda questioner: f"'{get_member_name(questioner, member_table)}'", questioners))
        result.append(f"presenter: '{presenter_name}', questioners: [{", ".join(questioner_names)}]")

    return "\n".join(result)

# Format result into CSV-style string
def generate_csv(member_table, questioner_presenter_table):
    result = []

    for questioner, presenters in questioner_presenter_table.items():
        questioner_name = get_member_name(questioner, member_table)
        presenter_names = list(map(lambda presenter: get_member_name(presenter, member_table), presenters))
        result.append(f"{questioner_name},{",".join(presenter_names)}")

    return "\n".join(result)


if __name__ == "__main__":
    main()
