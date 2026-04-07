#!/usr/bin/python3

'''
Copyright (C) 2026 Simon D. Levy

MIT License
'''

import argparse
from argparse import ArgumentDefaultsHelpFormatter


def beginclass(name):

    print('    class %s {\n' % name)
    print('        public:\n')


def writedefault(name):

    print('\n            %s() = default;' % name)

def endclass():

    print('    };\n')

def main():

    parser = argparse.ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('n', help='Stae vector dimensionality')
    args = parser.parse_args()

    n = int(args.n)

    print('#pragma once\n')

    print('namespace tinyekf {\n')

    beginclass('Vector')

    print('            float', end=' ')
    for i in range(n):
        print('_%d%s' % (i, ';\n' if i == n - 1 else ', '), end='')

    writedefault('Vector')

    endclass()

    beginclass('Matrix')

    for i in range(n):
        print('            ', end='')
        for j in range(n):
            print('_%d%d' % (i, j), end=', ' if i*n+j < n*n-1 else ';')
        print()

    writedefault('Matrix')

    endclass()

    beginclass('Helper')

    print('            Vector x;')
    print('            Matrix P;')

    writedefault('Helper')

    endclass()

    print('}\n')


main()
