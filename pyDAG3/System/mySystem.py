#!/usr/bin/env python3
""""Various system utilities

>>> import mySystem as mS
>>> import time
>>> import os

Copy file
>>> mS.copy('mySystem.dic', 'tests/.temp')

Time stamp
>>> mS.get_stamp('mySystem.dic') == os.path.getmtime('mySystem.dic')
True

Touch
>>> mS.touch('tests/MANIFEST.in')
>>> time.sleep(0.1)
>>> mS.touch('tests/pyDAG.dic')
>>> time.sleep(0.1)
>>> mS.touch('tests/mySystem.dic')
>>> time.sleep(0.1)
>>> mS.touch('tests/.temp')

Sorted reverse time
>>> mS.lslrt('tests')
['MANIFEST.in', 'pyDAG.dic', 'mySystem.dic', '.temp']

Sorted alphabetically
>>> mS.lsl('tests')
['.temp', 'MANIFEST.in', 'mySystem.dic', 'pyDAG.dic']

>>> mS.replace_in_file('lslrt', 'lslrt_replaced', 'tests/.temp')
1

>>> mS.cat('tests/.temp', 'tests/.temp', 'tests/.temp1')
2

>>> os.remove('tests/.temp')

>>> os.remove('tests/.temp1')

"""

# import cProfile
import sys
import os
import shutil


# Exceptions
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.
    Attributes:
    message -- explanation of the error
    """

    def __init__(self, message, usage_=0):
        Error.__init__(self)
        self.message = message
        self.usage = usage_

    def __str__(self):
        if self.usage:
            return repr(self.message) + '\n\n%(doc)s' % {'doc': __doc__}
        else:
            return repr(self.message)


def usage(code, msg=''):
    """Usage description"""
    print(sys.stderr, __doc__)
    if msg:
        print(sys.stderr, msg)
    sys.exit(code)


def find_executable(executable, path=None):
    """Try to find 'executable' in the directories listed in 'path' (a
    string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH']).  Returns the complete filename or None if not
    found
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    ext_list = ['']

    if os.name == 'os2':
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + ".exe"
    elif sys.platform == 'win32':
        path_ext = os.environ['PATHEXT'].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in path_ext:
            ext_list = path_ext
        print('path_ext=', path_ext, ', base=', base, ', ext=', ext,
              'ext_list=', ext_list)
    for ext in ext_list:
        exec_name = executable + ext
        if os.path.isfile(exec_name):
            return exec_name
        else:
            for p in paths:
                f = os.path.join(p, exec_name)
                if os.path.isfile(f):
                    return f
    else:
        return None


def copy(file1, output_file):
    """Copy file to destination, return total lines copied"""
    shutil.copy(file1, output_file)
    # inf1  = open(file1)
    # output  = open(output_file, 'w')
    # count = 0
    # for s in inf1.readline():
    #    count += 1
    #    output.write(s)
    # inf1.close()
    # output.close()
    # return count


def get_stamp(my_file):
    """Time stamp of file"""
    is_file = os.path.isfile(my_file)
    if is_file:
        date_file = os.path.getmtime(my_file)
    else:
        date_file = 0
    return date_file


def lslrt(path):
    """Directory listing sorted by time, latest last"""
    file_list = []
    for x in os.listdir(path):
        x_full = path+'/'+x
        if not os.path.isdir(x_full):
            file_list.append((os.stat(x_full).st_mtime, x))
    file_list.sort()
    dir_list = [x[1] for x in file_list]
    return dir_list


def lsl(path):
    """Directory listing sorted alphabetically"""
    file_list = []
    for x in os.listdir(path):
        x_full = path+'/'+x
        if not os.path.isdir(x_full):
            file_list.append(x)
    file_list.sort()
    return file_list


def replace_in_file(s_text, r_text, input_file_name):
    """Replace string in file"""
    input_file = open(input_file_name)
    output = open('.r_temp', 'w')
    count = 0
    for s in input_file.readlines():
        count += s.count(s_text)
        output.write(s.replace(s_text, r_text))
    input_file.close()
    output.close()
    if count > 0:
        shutil.move('.r_temp', input_file_name)
    else:
        os.remove('.r_temp')
    return count


def cat(file1, file2, output_file):
    """Cat two files to destination, return total lines catted"""
    input1 = open(file1)
    input2 = open(file2)
    output = open(output_file, 'w')
    count = 0
    for s in input1.readlines():
        count += 1
        output.write(s)
    for s in input2.readlines():
        count += 1
        output.write(s)
    input1.close()
    input2.close()
    output.close()
    return count


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
