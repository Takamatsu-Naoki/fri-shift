import pytest
import os
from collections import Counter
from main import load_member_table, load_groups, get_next_index, generate_presenter_pairs, generate_questioner_presenter_table, get_member_name

@pytest.fixture
def member_table():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    member_table_path = os.path.join(script_directory, "data", "test_member_table.csv")

    return load_member_table(member_table_path)

@pytest.fixture
def groups():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    groups_path = os.path.join(script_directory, "data", "test_group_assignment.csv")

    return load_groups(groups_path)

def test_load_member_table(member_table):
    assert member_table == {0: "John Smith", 1: "Jane Doe", 2: "Emily Johnson", 3: "Michael Brown", 4: "Sarah Davis", 5: "David Martinez", 6: "Laura Wilson", 7: "Chris Lee", 8: "Jessica Taylor", 9: "James Anderson", 10: "Mary Thomas", 11: "Robert Clark", 12: "Linda Harris", 13: "William Lewis", 14: "Anna White"}

def test_load_groups(groups):
    assert groups == [[11, 7, 1], [9, 12, 8, 2], [14, 0, 13, 6], [5, 10, 3, 4]]

def test_get_next_index(groups):
    assert get_next_index(1, groups) == 2
    assert get_next_index(3, groups) == 0

def test_generate_presenter_pairs(groups):
    presenter_pairs = generate_presenter_pairs(groups[1], 3)

    assert len(presenter_pairs) == 4
    assert all(len(pair) == 3 for pair in presenter_pairs)

    flat_list = [item for sublist in presenter_pairs for item in sublist]
    count = Counter(flat_list)

    assert all(value == 3 for value in count.values())

def test_generate_questioner_presenter_table(groups):
    questioner_presenter_table = generate_questioner_presenter_table(3, groups)
    
    flat_list = []
    for key, value in questioner_presenter_table.items():
        flat_list.extend(value)

    count = Counter(flat_list)

    assert all(value == 3 for value in count.values())

def test_get_member_name(member_table):
    assert get_member_name(14, member_table) == "Anna White"
