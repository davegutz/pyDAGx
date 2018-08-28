#!/usr/bin/env python3
r"""StringSet:  string tokenizer class

Tests:

>>> from pyDAG3.TextProcessing.StringSet import StringSet

>>> testStrSet = StringSet("Mary had a little lamb; it's was white as snow.")
>>> otherStrSet = StringSet("Mary had a little lamb; it's was white as snow.")

Basic attributes:
>>> len(testStrSet)
47
>>> otherStrSet == testStrSet
True
>>> testStrSet.tokenize(",;.'")
>>> len(testStrSet)
4
>>> len(otherStrSet)
47
>>> otherStrSet==testStrSet
False
>>> for field in testStrSet:
...     print(field)
Mary had a little lamb
 it
s was white as snow
<BLANKLINE>

replacing:
>>> numRepl = testStrSet.gsub('white', 'black')
>>> print(numRepl)
1
>>> print(testStrSet)
<000>Mary had a little lamb|;<001> it|'<002>s was black as snow|.<003>|
>>> otherStrSet.tokenize(".")
>>> otherStrSet.glob_sub_delims(".", "!")
1
>>> print(otherStrSet)
<000>Mary had a little lamb; it's was white as snow|!<001>|

Token details:
>>> ss =StringSet('class Error(Exception):\n', ';[]{}()!@#$%^&*-+_=`~/<>,.:\'')
>>> ss.str
'class Error(Exception):\n'
>>> ss
<000>class Error|(<001>Exception|):<002>
|
>>> ss.size_tokens
3
>>> ss.size_delimiters
3
>>> ss.tokens
['class Error', 'Exception', '\n']
>>> ss.delims
['(', '):', '']
>>> ss.reconstruct()
'class Error(Exception):\n'
>>> ss =StringSet('[class Error(Exception):\n', ';[]{}()!@#$%^&*-+_=`~/<>,.:\'')
>>> ss.str
'[class Error(Exception):\n'
>>> ss
<000>|[<001>class Error|(<002>Exception|):<003>
|
>>> ss.size_tokens
4
>>> ss.size_delimiters
4
>>> ss.tokens
['', 'class Error', 'Exception', '\n']
>>> ss.delims
['[', '(', '):', '']
>>> ss.reconstruct()
'[class Error(Exception):\n'
>>> ss = StringSet('./rdg100Small.txt', "./")
>>> ss.str
'./rdg100Small.txt'
>>> ss
<000>|./<001>rdg100Small|.<002>txt|
>>> ss.size_tokens
3
>>> ss.size_delimiters
3
>>> ss.tokens
['', 'rdg100Small', 'txt']
>>> ss.tokens
['', 'rdg100Small', 'txt']
>>> ss.reconstruct()
'./rdg100Small.txt'
"""

import re


class StringSet:
    """Create string sets from lines for easy file text manipulation"""

    def __eq__(self, other):
        """== special class method"""
        if isinstance(other, StringSet):
            if other.str == self.str and \
                    other.size_tokens == self.size_tokens and \
                    other.size_delimiters == self.size_delimiters and \
                    other.tokenized == self.tokenized and \
                    other.delims == self.delims and \
                    other.tokens == self.tokens:
                result = True
            else:
                result = False
        else:
            result = False
        return result

    def __init__(self, source_str=None, delimiters=None):
        self.str = source_str
        self.tokens = []
        self.size_tokens = 0
        self.delims = []
        self.size_delimiters = 0
        self.tokenized = 0
        self.delimiters = ''
        if delimiters:
            self.delimiters = delimiters
            self.tokenize(delimiters)
            self.tokenized = 1
        self.n_iter = 0

    def __len__(self):
        """String length if not tokenized, otherwise number tokens."""
        if self.tokenized:
            return self.size_tokens
        else:
            return len(self.str)

    def __ne__(self, other):
        """!= special class method"""
        if isinstance(other, StringSet):
            if other.str != self.str or \
                    other.size_tokens != self.size_tokens or \
                    other.size_delimiters != self.size_delimiters or \
                    other.tokenized != self.tokenized or \
                    other.delims != self.delims or \
                    other.tokens != self.tokens:
                result = True
            else:
                result = False
        else:
            result = True
        return result

    def __iter__(self):
        self.n_iter = 0
        return self

    def __next__(self):
        """Enable iteration"""
        if self.n_iter < self.size_tokens:
            if self.tokenized:
                result = self.tokens[self.n_iter]
            else:
                result = self.str
            self.n_iter += 1
            return result
        else:
            raise StopIteration

    def __repr__(self):
        """Print the class"""
        if self.tokenized:
            if self.size_delimiters:
                if not self.size_tokens:
                    cout = '<000> %(d0)s' % {'d0': self.delims[0]}
                else:
                    cout = ''
                slist = ['<%(i)03d>%(ti)s|%(di)s'
                         % {'i': i, 'di': self.delims[i], 'ti': self.tokens[i]} for i in range(self.size_delimiters)]
                cout = cout.join(slist)
                if self.size_tokens and self.size_delimiters > self.size_tokens:
                    cout = cout.join('<%(ss1)03d>%(dss1)s'
                                     % {'ss1': self.size_delimiters - 1, 'dss1': self.delims[self.size_delimiters - 1]})
            else:
                slist = ['<%(i)03d>%(ti)s'
                         % {'i': i, 'ti': self.tokens[i]} for i in range(self.size_tokens)]
                cout = ''.join(slist)
        else:
            cout = self.str
        return cout

    def gsub(self, target, replacement):
        """Global token replace, return number of replacements"""
        changed = 0
        if target != replacement:
            for i in range(self.size_tokens):
                changed += self.tokens[i].count(target)
                self.tokens[i] = self.tokens[i].replace(target, replacement)
                changed -= self.tokens[i].count(target)
        return changed

    def glob_sub_delims(self, target, replacement):
        """Global delimiter replace, return number of replacements"""
        changed = 0
        if target != replacement:
            for i in range(self.size_delimiters):
                changed += self.delims[i].count(target)
                self.delims[i] = self.delims[i].replace(target, replacement)
                changed -= self.delims[i].count(target)
        return changed

    def reconstruct(self):
        """Reconstruct the tokenized version and return it"""
        if self.size_delimiters:
            if not self.size_tokens:
                cout = '%(d0)s' % {'d0': self.delims[0]}
            else:
                cout = ''
            slist = ['%(ti)s%(di)s' % {'di': self.delims[i], 'ti': self.tokens[i]} for i in range(self.size_delimiters)]
            cout = cout.join(slist)
            if self.size_tokens and self.size_delimiters > self.size_tokens:
                cout = cout.join('%(dlast)s' % {'dlast': self.delims[self.size_delimiters - 1]})
        else:
            slist = ['%(ti)s ' % {'ti': self.tokens[i]}
                     for i in range(self.size_tokens)]
            cout = "".join(slist)
        return cout

    def shorten_delim(self, i):
        """Shorten delimiter by one character at end"""
        self.delims[i] = self.delims[i][:len(self.delims[i]) - 1]

    def token(self, i, verbose=True):
        """Use __getitem__ instead"""
        if verbose:
            print("(", __name__, "):  token() deprecated.   Use ''[]'' instead")
        return self.tokens[i]

    def __getitem__(self, i):
        """Return an element"""
        return self.tokens[i]

    def tokenize(self, delimiters, save_delims=True):
        """Find tokens of self.str separated by one or more delimiters;
        save tokens and delimiters"""
        # Initialize
        self.delimiters = delimiters
        if self.tokenized:
            self.tokens = []
            self.size_tokens = 0
            self.delims = []
            self.size_delimiters = 0
            self.tokenized = 0
        if not self.str:
            return
        reg_exp = re.compile("[" + re.escape(delimiters) + "]+")
        self.tokens = reg_exp.split(self.str)
        self.tokenized = 1
        if save_delims:
            self.delims = []
            raw_delims = reg_exp.findall(self.str)
            for strg in raw_delims:
                if strg:
                    self.delims.append(strg)
        self.size_tokens = len(self.tokens)
        while len(self.delims) < self.size_tokens:
            self.delims.append('')
        self.size_delimiters = len(self.delims)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
