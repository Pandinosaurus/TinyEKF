#!/usr/bin/python3

'''
Copyright (C) 2026 Simon D. Levy

MIT License
'''

import argparse
from argparse import ArgumentDefaultsHelpFormatter


def main():

    parser = argparse.ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('n', help='Stae vector dimensionality')
    args = parser.parse_args()

    n = int(args.n)

    print('#pragma once\n')
    print('class EkfCore {\n')
    print('    public:\n')

    print('        float', end=' ')

    print(', '.join([('x%d%c' %
                              (i, ';' if i == n - 1 else ' '))
                             for i in range(n)]))

    print('\n        EkfCore(', end='\n          ')

    print('        , '.join([('const float x%d%c' %
                              (i, ')' if i == n - 1 else '\n'))
                             for i in range(n)]))
    print('    {}')

    print('};')


main()
