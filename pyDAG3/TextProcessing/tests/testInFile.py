#!/usr/bin/env python3
""" Input file module, parse and manipulate input files"""
import sys
from pyDAG3.TextProcessing.InFile import InFile


def main():
    infile = InFile('testy.txt', 'asTested')
    infile.load()
    print('\nInfile=\n', infile)
    print('\nnum_lines=', infile.num_lines)
    infile.strip_blank_lines()
    print('num_lines after strip=', infile.num_lines)
    print('num vars=', infile.load_vars(), 'infile.nVars=', infile.nVars)
    print('return of tokenize=', infile.tokenize(";[]{}()!@#$%^&*-+_=`~/<>,.:'"))
    print('line at 1/3=', infile.line(int(infile.num_lines / 3)))
    print('string-set at that place=', infile.line_set(int(infile.num_lines / 3)))
    print('first_third =', infile.line(infile.find_string('third')))
    first_third = infile.find_string('third')
    print('token at place #1 of that line=', infile.token(first_third, 1))
    print('max_line_length=', infile.max_line_length())
    print('number of substitutions of "third" to "fourth"=', infile.gsub('third', 'fourth', first_third))
    print('\nTokenized infile with substitution=\n', infile)
    infile.reconstruct()
    print('\nReconstructed infile=\n', infile)
    print('return of re-tokenize=', infile.tokenize(";[]{}()!@#$%^&*-+_=`~/<>,.:'"))
    print('\nRe-tokenized infile=\n', infile)
    infile.reconstruct()
    print('\nRe-reconstructed infile=\n', infile)
    infile.upcase(0, 3)
    print('\nPartially upcased infile=\n', infile)
    # >>> infile.gsub('This is also', '#This is also')
    # >>> infile.strip_comments('#')
    # >> infile.tokenize(";[]{}()!@#$%^&*-+_=`~/<>,.:'")
    # 9
    infile.add_line(1, 'This line was inserted, no line feed in input string')
    infile.add_line(1, 'This line was inserted, line feed in input string\n')
    infile.sort()
    print('\nSorted infile=\n', infile)


if __name__ == '__main__':
    # sys.exit(cProfile.run("main(sys.argv[1:])"))
    sys.exit(main())
