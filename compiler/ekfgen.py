#!/usr/bin/python3

'''
Copyright (C) 2026 Simon D. Levy

MIT License
'''

import argparse
from argparse import ArgumentDefaultsHelpFormatter


def write(s):
    print(s, end='')

def beginclass(name):
    print('    class %s {\n' % name)
    print('        public:\n')


def writedefault(name):
    print('\n            %s() = default;' % name)
    write('\n            %s(' % name)


def beginmethod():
    print('            {')


def endmethod():
    print('            }\n')

def endclass():
    print('    };\n')

def split(i, n, s1, s2):
    return s2 if i == n-1 else s1

def commasplit(i, n, s):
    return split(i, n, ', ', s)

def declare_vector(n):

    beginclass('Vector')

    write('            float ')
    for i in range(n):
        write('_%d%s' % (i, commasplit(i, n, ';\n')))

    writedefault('Vector')

    for i in range(n):
        write('float _%d%s' % (i, split(i, n, ', ', ')\n')))

    write('               : ')

    for i in range(n):
        write('_%d(_%d)%s' % (i, i, commasplit(i, n, ' {}\n')))

    endclass()


def declare_matrix(n):

    beginclass('Matrix')

    print('            float')
    for i in range(n):
        write('              ')
        for j in range(n):
            print(' _%d%d' % (i, j), end=commasplit(i*n+j, n*n, ';'))
        print()

    writedefault('Matrix')

    print()

    for i in range(n):
        write('              ')
        for j in range(n):
            print('float _%d%d' % (i, j), end=commasplit(i*n+j, n*n, ')'))
        print()

    print('            :')

    for i in range(n):
        write('              ')
        for j in range(n):
            print('_%d%d(_%d%d)' %
                  (i, j, i, j), end=commasplit(i*n+j, n*n, ' {}'))
        print()

    endclass()


def declare_predict():

    print('            // P_k = F_{k-1} P_{k-1} F^T_{k-1} -------------------')
    print('            auto predict(const Matrix & F) -> Matrix')
    beginmethod()
    print('                Matrix FP;')
    print('                dot(F, P, FP);\n')
    print('                Matrix Ft;')
    print('                trans(F, Ft);\n')
    print('                dot(FP, Ft, P);')
    endmethod()


def declare_add_covariance_noise(n):
    print('            void addCovarianceNoise(const Vector & noise)')
    beginmethod()
    for i in range(n):
        print('                P._%d%d += noise._%d;' % (i, i, i))
    endmethod()

def declare_get_pval():
    print('            static auto get_pval(const int i, const int j, ')
    print('              const float pval, const float minval,')
    print('              const float maxval) -> float')
    beginmethod()
    print('              return')
    print('                isnan(pval) || pval > maxval ? maxval : ')
    print('                i==j && pval < minval ? minval : ')
    print('                pval; ')
    endmethod()

def declare_enforce_symmetry(n):
    print('            void enforceSymmetry(const float minval, '
          'const float maxval)')
    beginmethod()
    for i in range(n):
        for j in range(n):
            if i == j:
                print('                P._%d%d = get_pval(%d,% d, '
                      '0.5*P._%d%d + 0.5*P._%d%d, minval, maxval);' %
                      (i, j, i, j, i, j, j, i))
            else:
                print('                P._%d%d = P._%d%d = get_pval(%d,% d, '
                      '0.5*P._%d%d + 0.5*P._%d%d, minval, maxval);' %
                      (i, j, j, i, i, j, i, j, j, i))
    endmethod()


def declare_predict():
     print('            // P_k = F_{k-1} P_{k-1} F^T_{k-1} --------------------')
     print('            void predict(const Matrix &F)')
     beginmethod()
     print('                Matrix FP;')
     print('                dot(F, P, FP);')
     print('                Matrix Ft;')
     print('                trans(F, Ft);')
     print('                dot(FP, Ft, P);')
     endmethod()
 

def declare_update_with_scalar(n):
    print('            void updateWithScalar(const Vector & h,')
    print('                    const float error,') 
    print('                    const float stdMeasNoise,')
    print('                    const float minCovariance,')
    print('                    const float maxCovariance)')
    beginmethod()
    print('                const auto R = stdMeasNoise * stdMeasNoise;\n')
    print('                Vector PHt;')
    print('                dot(P, h, PHt); // PH\n')
    write('                const auto HPHR = R') 
    for i in range(n):
        write(' + h._%d*PHt._%d' % (i, i))
    print(';\n')
    print('                // kalman gain = (PH\' (HPH\' + R )^-1)')
    write('                const auto G = Vector(')
    for i in range(n):
        write('PHt._%d/HPHR%s' % (i, commasplit(i, n, ');\n\n')))
    print('                Matrix GH;')
    print('                outer(G, h, GH);\n')
    write('                ')
    for i in range(n):
        write('GH._%d%d-=1; ' % (i, i))
    print()
    endmethod()


def declare_dot_ax(n):

    print('            // y = A * x')
    print('            static void dot(const Matrix & A, const Vector &x, '
          'Vector &y)')
    beginmethod()
    for i in range(n):
        write('                y._%d = ' % i)
        for j in range(n):
            write('A._%d%d%s ' % (i, j, split(j, n, ' + ', ';\n')))
    endmethod()


def declare_dot_ab(n):

    print('            // C = A * B')
    print('            static void dot(const Matrix & A, ' +
          'const Matrix &B, Matrix &C)')
    beginmethod()
    for i in range(n):
        for j in range(n):
            write('                C._%d%d = ' % (i, j))
            for k in range(n):
                write('A._%d%d*B._%d%d%s' %
                      (i, k, k, j, split(k, n, ' + ', ';\n')))
    endmethod()


def declare_outer(n):

    print('            // A = x * y')
    print('            static void outer(const Vector & x, ' +
          'const Vector &y, Matrix &A)')
    beginmethod()
    for i in range(n):
        write('                ')
        for j in range(n):
            write('A._%d%d = x._%d*y._%d; ' % (i, j, i, j))
        print()
    endmethod()


def declare_trans(n):

    print('            // At = A^T')
    print('            static void trans(const Matrix & A, Matrix & At)')
    beginmethod()
    for i in range(n):
        write('              ')
        for j in range(n):
            write('At._%d%d=A._%d%d;' % (i, j, j, i))
        print()
    endmethod()


def declare_core(n):

    beginclass('Core')

    print('            Vector x;')
    print('            Matrix P;')

    writedefault('Core')

    print('Vector & x, Matrix & P) : x(x), P(P) {}\n')

    declare_predict()
    declare_update_with_scalar(n)
    declare_add_covariance_noise(n)
    declare_enforce_symmetry(n)

    print('\n        private:\n')

    declare_get_pval()
    declare_dot_ax(n)
    declare_dot_ab(n)
    declare_outer(n)
    declare_trans(n)
    endclass()


def main():

    parser = argparse.ArgumentParser(
            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('n', help='Stae vector dimensionality')
    args = parser.parse_args()

    n = int(args.n)

    print('// AUTO-GENERATED CODE; DO NOT EDIT\n')
    print('#pragma once\n')
    print('#include <math.h>\n')
    print('namespace tinyekf {\n')

    declare_vector(n)

    declare_matrix(n)

    declare_core(n)

    print('}\n')


main()
