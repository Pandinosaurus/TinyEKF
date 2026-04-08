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

    print('\n            %s(' % name, end='')

def endclass():

    print('    };\n')


def declare_vector(n):

    beginclass('Vector')

    print('            float', end=' ')
    for i in range(n):
        print('_%d%s' % (i, ';\n' if i == n - 1 else ', '), end='')

    writedefault('Vector')

    for i in range(n):
        print('float _%d%s' % (i, ')\n' if i == n - 1 else ', '), end='')

    print('               : ', end='')

    for i in range(n):
        print('_%d(_%d)%s' % (i, i, ' {}\n' if i == n - 1 else ', '), end='')

    endclass()


def declare_matrix(n):

    beginclass('Matrix')

    print('            float')
    for i in range(n):
        print('              ', end='')
        for j in range(n):
            print('_%d%d' % (i, j), end=', ' if i*n+j < n*n-1 else ';')
        print()

    writedefault('Matrix')

    print()

    for i in range(n):
        print('              ', end='')
        for j in range(n):
            print('float _%d%d' % (i, j), end=', ' if i*n+j < n*n-1 else ')')
        print()

    print('            :')

    for i in range(n):
        print('              ', end='')
        for j in range(n):
            print('_%d%d(_%d%d)' % (i, j, i, j), end=', ' if i*n+j < n*n-1 else ' {}')
        print()


    endclass()


def declare_helper(n):

    beginclass('Helper')

    print('            Vector x;')
    print('            Matrix P;')

    writedefault('Helper')

    endclass()


def main():

    parser = argparse.ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('n', help='Stae vector dimensionality')
    args = parser.parse_args()

    n = int(args.n)

    print('#pragma once\n')

    print('namespace tinyekf {\n')

    declare_vector(n)

    declare_matrix(n)

    #declare_helper(n)

    print('}\n')


main()
