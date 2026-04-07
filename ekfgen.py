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

    print('namespace tinyekf {\n')

    print('    class Vector {\n')

    print('        public:\n')

    print('            float', end=' ')
    for i in range(n):
        print('_%d%s' % (i, ';\n' if i == n - 1 else ', '), end='')

    print('    };\n')

    print('    class EkfCore {\n')

    print('        public:\n')

    print('            float', end=' ')
    for i in range(n):
        print('x%d%s' % (i, ';\n' if i == n - 1 else ', '), end='')

    print('\n            float')
    for i in range(n):
        print('            ', end='')
        for j in range(n):
            print('p%d%d' % (i, j), end=', ' if i*n+j < n*n-1 else ';')
        print()

    print('\n            EkfCore() = default;')

    print('    };')

    print('}\n')


main()
