import more_itertools as mit

notes = ["1","3","6","7"]
notes_and_rests = ["1","3","6","7","R","r"]

combination = []

# Utilities
# ==========
def compress_and_rest_strip_combination(combination):
    stripped = _strip_rests(combination)
    return _compress_combination(stripped)

def _compress_combination(combination):
    i = 0
    compressed = []
    while i < len(combination):
        compressed += combination[i]
        if combination[i] is "r":
            i += 1
        else:
            i += 2
    
    return compressed

def _strip_rests(combination):
    stripped_combination = []
    for note in combination:
        if note in notes:
            stripped_combination.append(note)

    return stripped_combination


def _is_consecutive(compressed_and_stripped_slice) -> bool:
    if len(compressed_and_stripped_slice) is 1:
        return False

    return compressed_and_stripped_slice[0] is compressed_and_stripped_slice[1]

def _note_has_more_than_four_separate_chains(compressed_and_stripped, note) -> bool:
    notes_minus_current = notes[:]
    notes_minus_current.remove(note)
    separated_by_non_current = list(mit.split_at(compressed_and_stripped, pred=lambda x: set(x) & set(notes_minus_current)))
    separated_by_non_current = [chain for chain in separated_by_non_current if chain != []]
    return len(separated_by_non_current) > 4
        

# Conditions
# ==========
def check_all(compressed_and_stripped) -> bool:
    return each_note_first_appearance_has_at_least_one_consecutive_repeat(compressed_and_stripped) and no_note_repeated_consecutively_more_than_eight_times(compressed_and_stripped)


def each_note_first_appearance_has_at_least_one_consecutive_repeat(compressed_and_stripped) -> bool:
    note_set = set(compressed_and_stripped)
    for note in note_set:
        first_index = compressed_and_stripped.index(note)
        if not _is_consecutive(compressed_and_stripped[first_index:]):
            return False
    
    return True

def no_note_repeated_consecutively_more_than_eight_times(compressed_and_stripped) -> bool:
    i = 0
    while i + 8 < len(compressed_and_stripped):
        nine_note_slice = compressed_and_stripped[i:i+9]
        if len(set(nine_note_slice)) == 1:
            return False
        i += 1
    
    return True

def no_note_can_have_four_separate_chains(compressed_and_stripped) -> bool:
    for note in notes:
        if _note_has_more_than_four_separate_chains(compressed_and_stripped, note):
            return False
    
    return True

# Main
# ====
def generate(combination):
    for note in notes:
        notes_to_add = []
        if note == "r":
            notes_to_add = ["r"]
        else:
            notes_to_add = [note, note]

        if len(combination) == 64:
            compressed_and_stripped = compress_and_rest_strip_combination(combination)
            if check_all(compressed_and_stripped):
                print(combination)
        elif len(combination) > 64:
            return combination
        else:
            new_combination = combination + notes_to_add
            generate(new_combination)

# Test (1,3,6,7)
# ====
def test_all():
    test_each_note_repeated_twice_consecutively()
    test_no_note_repeated_consecutively_more_than_eight_times()
    test_no_note_can_have_four_separate_chains()

def test_each_note_repeated_twice_consecutively():
    pass_case = _strip_rests(["1", "r", "1", "3", "3", "3", "1", "r", "1"])
    fail_case = _strip_rests(["1", "r", "1", "3", "3", "3", "1", "r", "6"])
    assert(each_note_first_appearance_has_at_least_one_consecutive_repeat(pass_case))
    assert(not each_note_first_appearance_has_at_least_one_consecutive_repeat(fail_case))

    print("Passed test_each_note_repeated_twice_consecutively!")

def test_no_note_repeated_consecutively_more_than_eight_times():
    pass_case = _strip_rests(["1", "R", "1", "R", "1", "1", "1", "1", "r", "1", "1"])
    fail_case = _strip_rests(["1", "R", "1", "R", "1", "1", "1", "1", "r", "1", "1", "R", "1"])
    assert(no_note_repeated_consecutively_more_than_eight_times(pass_case))
    assert(not no_note_repeated_consecutively_more_than_eight_times(fail_case))

    print("Passed test_no_note_repeated_consecutively_more_than_eight_times!")

def test_no_note_can_have_four_separate_chains():
    pass_case = _strip_rests(["1", "1", "r", "3", "3", "r", "1", "1", "1", "r", "6", "6", "6", "r", "7", "7", "7", "R", "1", "1", "1", "R", "3", "3", "3", "R", "1", "R", "1", "R", "7", "7", "6", "6"])
    fail_case = _strip_rests(["1", "1", "r", "3", "3", "r", "1", "1", "1", "r", "6", "6", "6", "r", "7", "7", "7", "R", "1", "1", "1", "R", "3", "3", "3", "R", "1", "R", "1", "R", "7", "7", "1", "1"])
    assert(no_note_can_have_four_separate_chains(pass_case))
    assert(not no_note_can_have_four_separate_chains(fail_case))

    print("Passed test_no_note_can_have_four_separate_chains!")

test_all()

# ["1", "1", "3", "3", "1", "1", "1", "6", "6", "6", "7", "7", "7", "1", "1", "1", "3", "3", "3", "1", "1", "7", "7", "6", "6"]