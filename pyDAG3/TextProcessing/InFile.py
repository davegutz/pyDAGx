#!/usr/bin/env python3
r""" Input file module, parse and manipulate input files

Tests:
>>> from pyDAG3.TextProcessing.InFile import InFile
>>> tf = open('temp', 'wt')
>>> text = "This is the first line.\n\nThis is the third line.\nThis is the fourth line.\nThis may be a line.\n"
>>> tf.write(text)
13
>>> tf.close()
>>> infile=InFile('temp','asTemp')
>>> infile.load()

>>> infile
asTemp (5 lines):
0:This is the first line.
1:
2:This is the third line.
3:This is the fourth line.
4:This may be a line.
<BLANKLINE>

Properties of the infile
>>> len(infile.lines)
5
>>> infile.num_lines
5
>>> infile.line(1600)
'This may be a line.\n'

Modify it
>>> infile.strip_blank_lines()
1
>>> infile.num_lines
4
>>> infile
asTemp (4 lines):
0:This is the first line.
1:This is the third line.
2:This is the fourth line.
3:This may a be line.
<BLANKLINE>
>>> infile.load_vars()
16
>>> infile.nVars
16
>>> infile.tokenize(";[]{}()!@#$%^&*-+_=`~/<>,.:'")
12
>>> infile.line_set(1600)
<000>|<001>This may be a third line|.<002>
|
>>> infile.line(int(infile.num_lines/3))
'This is the third line.\n'
>>> infile.line_set(int(infile.num_lines/3))
<000>|<001>This is the third line|.<002>
|
>>> firstThird = infile.find_string('third')
>>> infile.line(firstThird)
'This is the third line.\n'
>>> firstThird=infile.find_string('third', firstThird+1)
>>> infile.line(firstThird)
'This may be a line.\n'
>>> infile.token(firstThird, 1)
'This may be a line line'
>>> infile.max_line_length()
3
>>> infile.gsub('third', 'fourth', firstThird)
1
>>> infile
asTemp (4 lines):
0:<000>|<001>This is the first line|.<002>
|
1:<000>|<001>This is the third line|.<002>
|
2:<000>|<001>This is the fourth line|.<002>
|
3:<000>|<001>This may be a line|.<002>
|
<BLANKLINE>

>>> infile.reconstruct()
>>> infile
asTemp (4 lines):
0:This is the first line.
1:This is the third line.
2:This is the fourth line.
3:This may be a line.
<BLANKLINE>

>>> infile.upcase(0,3)
>>> infile
asTemp (4 lines):
0:THIS IS THE FIRST LINE.
1:THIS IS THE THIRD LINE.
2:THIS IS THE FOURTH LINE.
3:This may be a line.
<BLANKLINE>

>>> infile.gsub('This is also', '#This is also')
1
>>> infile.strip_comments('#')
1
>>> infile.tokenize(";[]{}()!@#$%^&*-+_=`~/<>,.:'")
9
>>> infile.add_line(1, 'This line was inserted, no line feed in input string')
>>> infile.add_line(1, 'This line was inserted, line feed in input string\n')
>>> infile.sort()
>>> infile
asTemp (6 lines):
0:1:THIS IS THE FIRST LINE.
2:THIS IS THE FOURTH LINE.
3:THIS IS THE THIRD LINE.
4:This line was inserted, line feed in input string
5:This line was inserted, no line feed in input string
<BLANKLINE>

>>> import os
>>> os.remove('temp')

"""
from pyDAG3.TextProcessing.StringSet import StringSet


# Exceptions
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return repr(self.expression)


class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
    previous -- state at beginning of transition
    next_state -- attempted new state
    message -- explanation of why the specific transition is not allowed
    """
    def __init__(self, previous, next_state, message):
        self.previous = previous
        self.next_state = next_state
        self.message = message


class InFile:
    """Load, parse, and manipulate input files.  Supports gzip automatically

    Test of throughput exercising StringSet and InFile:
    time python testInfile.py       time extrag rdg100Large
    real   11    1.7
    user   8.6   1.5
    sys    2.0   0.03
    """
    def __init__(self, src_file="user input", pname=""):
        # Check the inputs
        if __debug__:
            if not src_file:
                raise InputError("", "no source file specified")
        # Process the inputs
        self.v_set = None         # list of StringSet
        self.inFile = src_file  # the source file
        self.f = None          # filename pointer
        self.lines = None      # list of line strings
        self.num_lines = 0      # Number of lines in the file
        self.token_delims = None  # string of token delimiters for tokenization
        self.file_extension = None  # part of filename after last "."
        self.file_root = None   # part of filename before first "."
        self.programName = pname  # the name of this object, usually file name
        self.Vars = None  # list of variables found in file by load_vars
        self.nVars = 0  # the number of variables found in file by load_vars
        self.reconstructed = 0  # whether tokenized then reconstructed
        self.tokenized = 0  # whether tokenized
        self.max_line_tokens = 0  # stored value of maximum line length, in tokens
        self.counted = 0  # whether maximum line length is counted
        self.loaded = 0   # whether readlines already run on self.f

    def __repr__(self):
        """Print the class"""
        cout = '%(name)s (%(num_lines)d lines):\n' \
            % {'name': self.programName, 'num_lines': self.num_lines}
        if self.tokenized:
            slist = ['%(i)d:%(line)s\n'
                     % {'i': i, 'line': self.v_set[i]}
                     for i in range(self.num_lines)]
        else:
            slist = ['%(i)d:%(line)s'
                     % {'i': i, 'line': self.lines[i]}
                     for i in range(self.num_lines)]
        cout += "".join(slist)
        return cout

    def line(self, i):
        """Return the line string demanded but always in-range"""
        limited_index = max(min(i, len(self.lines)-1), 0)
        return '%(line)s' % {'line': self.lines[limited_index]}

    def line_set(self, i):
        """Return the tokenized representation of line i, always in range"""
        # Check input
        if __debug__:
            if not self.tokenized:
                raise InputError("", "must run InFile.tokenize before look in InFile.line_set")
        limited_index = max(min(i, len(self.v_set)-1), 0)
        return self.v_set[limited_index]

    def add_line(self, after_line, new_line_str):
        """Insert line of string new_line_str after line after_line"""
        if not new_line_str[len(new_line_str)-1] == '\n':
            new_line_str += '\n'
        self.lines[(after_line+1):(after_line+1)] = [new_line_str]
        if self.tokenized:
            vs = StringSet(new_line_str, self.token_delims)
            self.v_set[(after_line+1):(after_line+1)] = [vs]
        self.num_lines = len(self.lines)

    def close_file(self):
        self.f.close()

    def delete_line(self, line_index):
        """Delete line and readjust internal arrays"""
        del self.v_set[line_index]
        self.num_lines = len(self.lines)

    def downcase(self, start_line=0, end_line=None):
        """Downcase all the text lines in specified line range"""
        if end_line:
            end_line = max(min(end_line, self.num_lines-1), 0)
        start_line = max(min(start_line, end_line), 0)
        for i in range(start_line, end_line):
            self.lines[i] = self.lines[i].lower()
        self.reconstructed = 0

    def find_string(self, target, start_line=0):
        """Number of line containing first 'target' in lines after 'start_line'"""
        offset = -1
        for line in self.lines[max(min(start_line, self.num_lines), 0):]:
            offset += 1
            if line.count(target):
                break
        return start_line + offset

    def get_line(self, f):
        """Get a line at a time from the unloaded file and return it's string"""
        if __debug__:
            if self.loaded:
                raise InputError("", "do not run load() before get_line()")
        new_line = f.readline()
        if not new_line:
            return ""
        if not self.lines:
            self.lines = [new_line]
        else:
            self.lines += [new_line]
        self.num_lines = len(self.lines)
        return new_line

    def gsub(self, target, replace, start_line=0, end_line=None):
        """Global substitution in lines or StringSets(if tokenized); return total number of replacements"""
        if end_line:
            end_line = max(min(end_line, self.num_lines), 0)
        else:
            end_line = self.num_lines
        start_line = max(min(start_line, end_line), 0)
        count = 0
        if not self.tokenized:
            if not target == replace:
                for i in range(start_line, end_line):
                    count += self.lines[i].count(target)
                    self.lines[i] = self.lines[i].replace(target, replace)
        else:
            if not target == replace:
                for i in range(start_line, end_line):
                    count += self.v_set[i].gsub(target, replace)
        return count

    def glob_sub_delims(self, target, replace, start_line=0, end_line=None):
        """Globally substitute target with replace in the specified range of tokenized file memory;
         return total number of replacements"""
        if __debug__:
            if not self.tokenized:
                raise InputError("", "must be tokenized")
        if end_line:
            end_line = max(min(end_line, self.num_lines), 0)
        else:
            end_line = self.num_lines
        count = 0
        if not target == replace:
            for i in range(start_line, end_line):
                count += self.v_set[i].glob_sub_delims(target, replace)
        return count

    def load(self, quiet=True):
        """Load the file"""
        in_file_set = StringSet(self.inFile, "/.")
        if len(in_file_set) > 2:
            self.file_extension = in_file_set[len(in_file_set)-1]
        self.file_root = in_file_set[1]
        if self.file_extension == 'gz':
            import gzip
            self.f = gzip.open(self.inFile)
        else:
            self.f = open(self.inFile, 'r')
        self.lines = self.f.readlines()
        self.num_lines = len(self.lines)
        self.loaded = 1
        if not quiet:
            print('loaded', self.inFile, 'root=', self.file_root,
                  'num_lines=', self.num_lines, ' extension=', self.file_extension)

    def load_vars(self):
        """Load variable vector data, using text (isnum) as delimiter.
        Useful for reading general input data files"""
        if __debug__:
            if self.tokenized:
                raise InputError("", "must not be tokenized yet")
        self.tokenize(" =!\t\n\a\b\r\f\v;%<>/,&^?#|$@*():{}\\\'[]\"")
        loading_var = 0
        # Strip out the data vectors
        loc_vars = []            # local storage of data coordinates
        self.Vars = []
        name = ""
        n = self.num_lines
        for i in range(n):
            m = len(self.v_set[i])
            for j in range(m):
                token = self.v_set[i][j]
                # skip if haven't found a new alphanumeric variable name
                if not loading_var and not token.isalnum():
                    continue
                if not token.isalnum():
                    loc_vars.append([i, j])
                # flag last token
                last_token = (n == i+1) and (m == j+1)
                # new data is available, or end
                if token.isalnum() or last_token:
                    # save previous data
                    self.Vars.append([[name], [len(loc_vars)], [loc_vars]])
                    # Start processing new data
                    loading_var = 0
                    if not last_token:     # found a new one
                        self.nVars += 1
                        name = token    # new data vector name
                        loading_var = 1  # flag to process
                        loc_vars = []       # make room for new data
        return self.nVars

    def max_line_length(self):
        """Determine length of longest line, in tokens"""
        if self.counted:
            print('WARNING(InFile):  max_line_length : already counted.  Returning stored value')
            return self.max_line_tokens
        elif not self.tokenized:
            return 1
        else:
            self.counted = 1
            for v_set in self.v_set:
                self.max_line_tokens = max(self.max_line_tokens, len(v_set))
        return self.max_line_tokens

    def reconstruct(self):
        """Reconstruct the tokenized memory back into the lines"""
        if __debug__:
            if not self.tokenized:
                raise InputError("", "must be tokenized")
            if self.reconstructed:
                raise InputError("", "reconstructed already")
        for i in range(self.num_lines):
            # Dangling initial delimiter
            if self.v_set[i].sized and not self.v_set[i].size:
                self.lines[i] = self.v_set[i].delim(0)
            else:
                self.lines[i] = ""
            # Some tokens exist
            # print 'i=', i, 'v_set=', self.v_set[i], 'size=', self.v_set[i].size, 'sized=', self.v_set[i].sized
            # print 'tokens=', self.v_set[i].tokens, '\ndelims=', self.v_set[i].delims, '\nstr=', self.v_set[i].str,
            #  '\n delimiters', self.v_set[i].delimiters
            self.lines[i] += self.v_set[i].reconstruct()
        self.reconstructed = 1
        self.tokenized = 0

    def shorten_delimiter(self, line_index, i):
        """Delete last char of i'th delimiter in tokenized line line_index"""
        if __debug__:
            if not self.tokenized:
                raise InputError("", "must be tokenized")
            if line_index >= self.num_lines:
                raise InputError("", "line number out of range")
        self.v_set[line_index].shorten_delimiter(i)
        self.reconstructed = 0

    def sort(self):
        """Sort"""
        self.lines.sort()
        self.v_set = []
        # whether tokenized then reconstructed
        self.reconstructed = 0
        self.tokenized = 0    # whether tokenized
        # stored value of maximum line length, in tokens
        self.max_line_tokens = 0
        self.counted = 0   # whether maximum line length is counted
        self.loaded = 0    # whether readlines already run on self.f

    def sout(self):
        """Stream the class"""
        if self.tokenized:
            slist = ['%(line)s\n' % {'line': self.v_set[i].reconstruct()} for i in range(self.num_lines)]
            cout = "".join(slist)
        else:
            slist = ['%(line)s\n' % {'line': self.lines[i]} for i in range(self.num_lines)]
            cout = "".join(slist)
        return cout

    def strip_blank_lines(self, end_line=None):
        """Strip lines containing only white, in specified line range; return number of lines remaining"""
        # Check input
        if __debug__:
            if self.tokenized:
                raise InputError("", "run before tokenizing")
        if end_line:
            end_line = max(min(end_line, self.num_lines), 0)
        else:
            end_line = self.num_lines
        num_blank_lines = 0
        i = 0
        while i < end_line:
            if not len(self.lines[i].strip()):
                self.lines.pop(i)
                num_blank_lines += 1
                i = i - 1
                self.num_lines -= 1
                end_line = max(min(end_line, self.num_lines), 0)
            i += 1
        if self.num_lines == 0:
            print('WARNING(InFile):  strip_blank_lines : ', self.inFile, 'is empty after stripping white space')
        return num_blank_lines

    def strip_comments(self, comment_delim):
        """Strip comments from delimiter to end of line, in specified line range; return number of comments stripped"""
        num_comment_str = 0
        for i in range(self.num_lines):
            if self.lines[i].find(comment_delim) > -1:
                num_comment_str += 1
                self.lines[i] = self.lines[i].split(comment_delim)[0]
        return num_comment_str

    def token(self, i, j):
        """Return token at specified location"""
        if 0 > i or 0 > j:
            return ""
        else:
            return self.line_set(i)[j]

    def tokenize(self, delimiters):
        """Tokenize each line of file into a StringSet.  Return total number of tokens"""
        self.v_set = []
        num_tokens = 0
        self.token_delims = delimiters
        if self.num_lines:
            self.reconstructed = 0
        for i in range(self.num_lines):
            self.v_set.append(StringSet(self.lines[i], delimiters))
            num_tokens += len(self.v_set[len(self.v_set)-1])
        self.tokenized = 1
        self.reconstructed = 0
        return num_tokens

    def upcase(self, start_line=0, end_line=None):
        """Upcase all the text lines in specified line range"""
        if end_line:
            end_line = max(min(end_line, self.num_lines-1), 0)
        else:
            end_line = self.num_lines
        start_line = max(min(start_line, end_line), 0)
        for i in range(start_line, end_line):
            self.lines[i] = self.lines[i].upper()
        self.reconstructed = 0


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
