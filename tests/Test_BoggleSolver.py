#!/usr/bin/env python

"""
Test_BoggleSolver runs unit tests on BoggleSolver.py.

Python 2.7.13

"""


import os
import re
import sys
import unittest
# edit sys.path for module import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from BoggleSolver import BoggleBoard, check_input_args

CUR_DIR = os.path.abspath(os.getcwd())
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
DICT_FILE = os.path.join(DATA_DIR, "dictionary.txt")
BOARD_1_FILE = os.path.join(DATA_DIR, "board_1.txt")
BOARD_2_FILE = os.path.join(DATA_DIR, "board_2.txt")
BOARD_1_SOL_FILE = os.path.join(DATA_DIR, "board_1_solution.txt")
BOARD_2_SOL_FILE = os.path.join(DATA_DIR, "board_2_solution.txt")


def read_file_to_string(text_file):
    """Read text file and return data as string."""
    output_string = ""
    with open(text_file, 'rU') as text_file_open:
        output_string = text_file_open.read()
    return output_string


def read_lines_to_list(text_file):
    """Read text file lines and return data as word list."""
    output_list = []
    with open(text_file, 'rU') as text_file_open:
        for line in text_file_open.readlines():
            output_list.append(line)
    return output_list


class TestSampleBoards(unittest.TestCase):
    """Test various Boggle Boards."""

    def tearDown(self):
        """Cleanup temp output files based on *_test_output.txt format."""
        pattern = ".+_test_output.txt"
        for f in os.listdir(CUR_DIR):
            if re.search(pattern, f):
                os.remove(os.path.join(CUR_DIR, f))

    def test_board_1(self):
        """Validate board_1.txt output equals provided board_1_solution.txt."""
        output_file = "board_1_test_output.txt"
        BoggleBoard(DICT_FILE, BOARD_1_FILE, output_file)
        board_1_output = read_file_to_string(output_file)
        board_1_solution = read_file_to_string(BOARD_1_SOL_FILE)
        self.assertEqual(board_1_output, board_1_solution)

    def test_board_2(self):
        """Validate board_2.txt output equals provided board_2_solution.txt."""
        output_file = "board_2_test_output.txt"
        BoggleBoard(DICT_FILE, BOARD_2_FILE, output_file)
        board_2_output = read_file_to_string(output_file)
        board_2_solution = read_file_to_string(BOARD_2_SOL_FILE)
        self.assertEqual(board_2_output, board_2_solution)

    def test_no_words(self):
        """Validate board with no words returns nothing."""
        all_x_board = "X" * 16
        output_file = "no_words_test_output.txt"
        BoggleBoard(DICT_FILE, all_x_board, output_file)
        no_words_output = read_file_to_string(output_file)
        self.assertEqual(no_words_output, "")

    def test_1_word(self):
        """Validate that a board where only 1 word(via) is found."""
        one_word_board = "VVVVVVIAVVVVVVVV"
        output_file = "one_word_test_output.txt"
        BoggleBoard(DICT_FILE, one_word_board, output_file)
        one_word_output = read_file_to_string(output_file)
        self.assertEqual(one_word_output, "via" + "\n")

    def test_long_word(self):
        """Validate that a board where word "misunderstanding" is found."""
        long_word_board = "misurednstangnid"
        output_file = "long_word_test_output.txt"
        BoggleBoard(DICT_FILE, long_word_board, output_file)
        long_word_output = read_lines_to_list(output_file)
        self.assertTrue("misunderstanding\n" in long_word_output)

    def test_whitespace(self):
        """Validate boards with excessive whitespace."""
        whitespace = "C  U R T\nB A\t N  D\nA T\n M Z\r\nM X   F\r\n O\n"
        ws_output_file = "whitespace_test_output.txt"
        BoggleBoard(DICT_FILE, whitespace, ws_output_file)
        whitespace_output = read_file_to_string(ws_output_file)

        fixed_spacing = "C U R T\nB A N D\nA T M Z\nM X F O\n"
        fs_output_file = "fixed_spacing_test_output.txt"
        BoggleBoard(DICT_FILE, fixed_spacing, fs_output_file)
        fixed_spacing_output = read_file_to_string(fs_output_file)

        self.assertEqual(whitespace_output, fixed_spacing_output)

    def test_capitalization(self):
        """Validate boards with different capitalization."""
        uppercase = "B A R N\nD O O R\nH A T S\nS H I N\n"
        uc_output_file = "uppercase_test_output.txt"
        BoggleBoard(DICT_FILE, uppercase, uc_output_file)
        uppercase_output = read_file_to_string(uc_output_file)

        lowercase = "b a r n\nd o o r\nh a t s\ns h i n\n"
        lc_output_file = "lowercase_test_output.txt"
        BoggleBoard(DICT_FILE, lowercase, lc_output_file)
        lowercase_output = read_file_to_string(lc_output_file)

        mixedcase = "b A r N\nD O o r\nh a T s\nS h i N\n"
        mc_output_file = "mixedcase_test_output.txt"
        BoggleBoard(DICT_FILE, mixedcase, mc_output_file)
        mixedcase_output = read_file_to_string(mc_output_file)

        self.assertEqual(lowercase_output, uppercase_output)
        self.assertEqual(lowercase_output, mixedcase_output)
        self.assertEqual(uppercase_output, mixedcase_output)


class TestOutputFiles(unittest.TestCase):
    """Test output files are written correctly."""

    def tearDown(self):
        """Cleanup temp output files."""
        pattern = ".+_test_output.txt"
        for f in os.listdir(CUR_DIR):
            if re.search(pattern, f):
                os.remove(os.path.join(CUR_DIR, f))

    def test_alphabetical(self):
        """Validate output answers are alphabetical."""
        output_file = "board_1_test_output.txt"
        BoggleBoard(DICT_FILE, BOARD_1_FILE, output_file)
        board_1_solution_words = read_lines_to_list(output_file)
        self.assertEqual(board_1_solution_words, sorted(board_1_solution_words))

    def test_lowercase(self):
        """Validate output answers are lowercase."""
        output_file = "board_1_test_output.txt"
        BoggleBoard(DICT_FILE, BOARD_1_FILE, output_file)
        board_1_output = read_file_to_string(output_file)
        self.assertEqual(board_1_output, board_1_output.lower())


class TestInputFiles(unittest.TestCase):
    """Test invalid input files throw errors."""

    def test_bad_dict(self):
        """Validate error is thrown for bad dict file."""
        self.assertRaises(IOError, check_input_args, "bad_dict_file.txt",
                          BOARD_1_FILE)

    def test_bad_board(self):
        """Validate error is thrown for bad board file."""
        self.assertRaises(IOError, check_input_args, DICT_FILE,
                          "bad_board_file.txt")


if __name__ == "__main__":
    unittest.main()
