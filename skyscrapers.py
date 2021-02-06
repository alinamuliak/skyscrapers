"""
This module help to play skyscrappers game.
"""


def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']
    """
    list_of_lines = []
    with open(path, 'r') as f:
        for line in f.readlines():
            list_of_lines.append(line.strip())
    return list_of_lines


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    max_building = max(list(input_line[1:pivot]))
    if max_building < input_line[pivot]:
        return True
    return False


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*',\
 '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*',\
 '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
 '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board[1:-1]:
        if len(line[1:-1]) != len(set(line[1:-1])):
            return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    board = board[1:-1]
    for line in board:
        if not line[0].isdigit():
            continue
        able_to_see = 1    # one because the first building is always visible
        for pivot in range(2, len(line[1:-1]) + 1):
            if left_to_right_check(line, pivot):
                able_to_see += 1
        if able_to_see != int(line[0]):
            print(line, able_to_see)
            return False

    for line in board:
        reversed_line = line[::-1]
        if not reversed_line[0].isdigit():
            continue
        able_to_see = 1    # one because the first building is always visible
        for pivot in range(2, len(reversed_line[1:-1]) + 1):
            if left_to_right_check(reversed_line, pivot):
                able_to_see += 1
        if able_to_see != int(reversed_line[0]):
            return False
    return True


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness (buildings of unique height)
    and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215',\
 '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215',\
 '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215',\
 '*35214*', '*41532*', '*2*1***'])
    False
    """
    # making an inverted board to use horisontal functions
    vice_versa_board = ['' for _ in range(len(board))]

    current_sumbol = 0
    while current_sumbol < len(board[0]):
        for line in board:
            vice_versa_board[current_sumbol] += line[current_sumbol]
        current_sumbol += 1
    if not check_uniqueness_in_rows(vice_versa_board):
        return False

    if not check_horizontal_visibility(vice_versa_board):
        return False

    # reversing lines so we can check top-bottom and vice versa visibility
    vice_versa_board_copy = vice_versa_board.copy()
    for i in range(len(vice_versa_board_copy)):
        vice_versa_board_copy[i] = vice_versa_board_copy[i][::-1]

    if not check_horizontal_visibility(vice_versa_board_copy):
        return False

    return True


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    """
    board = read_input(input_path)
    # checking all conditions
    if not check_not_finished_board(board):
        return False
    if not check_uniqueness_in_rows(board):
        return False
    if not check_horizontal_visibility(board):
        return False
    if not check_columns(board):
        return False
    return True


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
