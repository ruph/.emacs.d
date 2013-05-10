#!/usr/bin/env python
'''
For python's flymake:
- $ cp pyflakespep8.py /usr/local/bin/
- $ chmod a+x /usr/local/bin/pyflakespep8.py
- $ sudo pip install pyflakes pep8
'''

import commands
import re
import sys


def make_re(*msgs):
    return re.compile('(%s)' % '|'.join(msgs))

pyflakes_ignore = make_re('unable to detect undefined names')
pyflakes_warning = make_re(
    'imported but unused',
    'is assigned to but never used',
    'redefinition of unused',
)
'''
Ignoring:
E501 line too long
E128 continuation line under-indented
E121 continuation line indentation is not a multiple of four
E122 continuation line missing indentation
W191 indentation contains tabs
'''
pep8_ignore = ['E501', 'E128', 'E121', 'E122', 'W191']
pep8_warning = make_re('.')


def run(cmd, ignore_re, warning_re):
    output = commands.getoutput(cmd)
    for line in output.splitlines():
        if ignore_re and ignore_re.search(line):
            continue
        elif ': ' in line and warning_re.search(line):
            line = '%s: WARNING %s' % tuple(line.split(': ', 1))
        print line

run('pyflakes %s' % sys.argv[1], pyflakes_ignore, pyflakes_warning)
print '## pyflakes above, pep8 below ##'
pep8_ignore = '--ignore=' + ','.join(i for i in pep8_ignore)
run('pep8 %s --repeat %s' % (pep8_ignore, sys.argv[1]), None, pep8_warning)
