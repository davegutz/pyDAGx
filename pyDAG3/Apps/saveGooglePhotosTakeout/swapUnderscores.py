#!/usr/bin/env python
"""
swapUnderscores.py
Move photo filename trailing underscore numbers before date so saveGooglePhotosTakeout.py works properly
 swapUnderscores.py -f "D:\Pictures\Saved Pictures\KPGUTZ_2014_raw"
"""
# import cProfile
import sys
import os
import shutil
import getopt


def usage(msg=''):
    """Usage description"""
    code = sys.stderr
    print(code, __doc__)
    if msg:
        print(code, msg)
    sys.exit(code)


def main(argv):
    """desc here"""

    # Initialize
    folder = ''

    # Options
    options = ""
    try:
        options, remainder = getopt.getopt(argv, 'f:', ['folder='])
    except getopt.GetoptError:
        usage('ERR')
    for opt, arg in options:
        if opt in ('-f', '--folder'):
            top_folder = arg
        else:
            print("error:  i or o inputs only")
            exit(-1)

    # Check inputs
    print("folder=", top_folder)

    # Get information about output:  only input files of same date will be copied
    folders = os.listdir(top_folder)
    print(folders)
    for folder in folders:
        if folder[-2] == '_':
            root, found, num = folder.partition('_')
            ending = root[-4:]
            beginning = root[:-4]
            new_name = beginning + str(num) + '_' + ending
            folder_path = top_folder + "\\" + folder
            new_path = top_folder + "\\" + new_name
            print("old=", folder_path, "----->", new_path)
            shutil.move(folder_path, new_path)


if __name__ == '__main__':
    # sys.exit(cProfile.run("main(sys.argv[1:])"))
    sys.exit(main(sys.argv[1:]))
