#!/usr/bin/env python

"""
BoggleSolver solves Boggle boards.

Python 2.7.13

Command line arguments:
 python BoggleSolver.py <dictionary_filename> <board_filename> <output_filename>

"""

import os
import sys

# path to data directory for argument path handling
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def check_input_args(dict_arg, board_arg):
    """Check for input files in data folder if path not explicitly passed."""
    # if dict_arg is only the file name, try looking in data folder
    if not os.path.isfile(dict_arg):
        try:
            dict_arg = os.path.join(DATA_DIR, dict_arg)
            assert os.path.isfile(dict_arg)
        except AssertionError:
            raise IOError("Dictionary file not found.")
    # if board_arg is only the file name, try looking in data folder
    if not os.path.isfile(board_arg):
        try:
            board_arg = os.path.join(DATA_DIR, board_arg)
            assert os.path.isfile(board_arg)
        except AssertionError:
            raise IOError("Board file not found.")

    return dict_arg, board_arg


class BoggleBoard:
    """
    BoggleBoard class loads and solves a Boggle game, creating an output file.

    Args:
        dict_file:
            An ASCII text file that lists alphabetized acceptable words.
            Each word is new line separated.
            All lowercase, utilizing only letters 'a' to 'z'.

        board_arg:
            This arg will accept an ASCII text file or a 16 letter string for
            simple testing.

            These represent the game board, a 4x4 matrix of characters.
            These may be mixed case.
            Whitespace is optional and should be ignored.
            Only letters 'a' to 'z' or 'A' to 'Z' are used.

        out_file:
            Output file to be create with alphabetized words found on the board.

    """

    possible_index_moves = {}

    def __init__(self, dict_file, board_arg, out_file):
        """Initialize the board data and run solve functions."""
        self.board = ""
        self.valid_words = {}
        self.found_words = set()
        self.dict_file = dict_file
        self.board_arg = board_arg
        self.out_file = out_file

        self._build_possible_index_moves()
        self._load_board()
        self._load_dictionary()
        self._solve_board()

    def _build_possible_index_moves(self):
        """Build the class dict storing base moves for each board index."""
        for i in range(0, 16):
            self.possible_index_moves[i] = self._get_possible_index_moves(i)

    def _get_possible_index_moves(self, index):
        """Return list of moves for a given Boggle Board index."""
        # list of all possible movement paths on a boggle board
        # based on the layout of the 4x4 matrix board in a 1 dimensional string
        possible_moves = (-5, -4, -3, -1, 1, 3, 4, 5)
        index_moves = set()
        for move in possible_moves:
            # if value is within board range, add to available moves
            if index + move >= 0 and index + move <= 15:
                index_moves.add(move)

        # if in the left column no leftward moves
        if index % 4 == 0:
            index_moves.difference_update((-5, -1, 3))
        # if in the right column no rightward moves
        elif index % 4 == 3:
            index_moves.difference_update((-3, 1, 5))
        # if in the top row no upward moves
        if index < 4 == 0:
            index_moves.difference_update((-5, -4, -3))
        # if in the bottom row no downward moves
        elif index > 11 == 3:
            index_moves.difference_update((3, 4, 5))

        return index_moves

    def _load_board(self):
        """Load board file to memory and sterilize data."""
        if os.path.isfile(self.board_arg):
            with open(self.board_arg, 'r') as b:
                    self.board = b.read()
        else:
            self.board = self.board_arg

        self.board = self.board.lower()
        self.board = "".join(self.board.split())

        # validate that board input is a 16 letter string
        assert (len(self.board) == 16 and isinstance(self.board, str) and
                self.board.isalpha())

    def _load_dictionary(self):
        """Load dictionary file to memory and remove all invalid words."""
        assert os.path.isfile(self.dict_file)
        dict_words = []
        with open(self.dict_file, 'r') as dictionary:
            for line in dictionary:
                word = line.strip()
                # exclude words < 3 letters and words > 17 letters
                if len(word) > 2 and len(word) < 18:
                    dict_words.append(word)

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        # find missing letters not present on board
        missing_letters = [letter for letter in alphabet
                           if letter not in self.board]
        # add special case for 'qu' words
        if 'q' not in missing_letters and 'u' in missing_letters:
            missing_letters.remove('u')
        # create dict structure based on present letters only
        present_letters = [letter for letter in alphabet
                           if letter not in missing_letters]
        # remove words containing any missing letters
        remove_words = set()
        for word in dict_words:
            has_missing_letters = False
            for letter in missing_letters:
                if has_missing_letters:
                    continue
                if letter in word:
                    has_missing_letters = True
                    remove_words.add(word)
        unsorted_valid_words = [word for word in dict_words
                                if word not in remove_words]

        # build a nested dict for valid words with their first 2 letters as keys
        # ex. self.valid_words['a']['b'] returns ["abbey", about", "absent"]
        for first_word_letter in present_letters:
            self.valid_words[first_word_letter] = {}
            for second_word_letter in present_letters:
                self.valid_words[first_word_letter][second_word_letter] = []

        for word in unsorted_valid_words:
            self.valid_words[word[0]][word[1]].append(word)

    def _solve_board(self):
        """Solve the board and write sorted solution words to output file."""
        # for each board index, find words starting at that index
        # all letters start recursive _find_words function unused
        used_letter = [False] * 16
        for i in range(0, 16):
            self._find_words(i, used_letter, [])

        # convert found word set to list and sort
        out_words = sorted(list(self.found_words))
        # write solution words to output file
        with open(self.out_file, 'w') as output:
            for word in out_words:
                output.write(word + '\n')

    def _find_words(self, index, used_letter_arg, cur_path_arg):
        """Find valid words on Boggle Board recursively."""
        used_letter = [val for val in used_letter_arg]
        # set current letter as used on board
        used_letter[index] = True

        cur_path = [val for val in cur_path_arg]
        # add the current index to the path thus far
        cur_path.append(index)

        # test the current index's possible moves against the available letters
        available_moves = [move for move in self.possible_index_moves[index]
                           if not used_letter[index + move]]

        is_word_start = False
        if len(cur_path) == 1:
            # all individual letters can start words
            is_word_start = True
        else:
            cur_word = ""
            for pos in cur_path:
                cur_word += self.board[pos]
                if self.board[pos] == 'q':
                    cur_word += 'u'

            for word in self.valid_words[cur_word[0]][cur_word[1]]:
                if word.startswith(cur_word):
                    is_word_start = True
                    break

            # add > 2 letter, valid words to found words
            if len(cur_word) > 2:
                if cur_word in self.valid_words[cur_word[0]][cur_word[1]]:
                    self.found_words.add(cur_word)
        # recursively call _find_words function on available moves from index
        if is_word_start and available_moves:
            for move in available_moves:
                self._find_words(index + move, used_letter, cur_path)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: BoggleSolver " + \
              "<dictionary_filename> <board_filename> <output_filename>"
        sys.exit(1)

    dict_arg, board_arg, output_arg = sys.argv[1:]
    dict_arg, board_arg = check_input_args(dict_arg, board_arg)
    b = BoggleBoard(dict_arg, board_arg, output_arg)

    sys.exit(0)
