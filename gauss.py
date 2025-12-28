# -*- coding: utf-8 -*-
from utility import Utility

class Gauss:
    def gauss_lr(self, matrix):
        n = len(matrix)

    # quadratische Matrix prüfen
        for row in matrix:
            if len(row) != n:
                raise ValueError("Matrix ist nicht quadratisch!")

    # L und R initialisieren
        L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        R = [[float(matrix[i][j]) for j in range(n)] for i in range(n)]

        for k in range(n - 1):
            if R[k][k] == 0:
                raise ZeroDivisionError("Zero pivot encountered")

            for i in range(k + 1, n):
                factor = R[i][k] / R[k][k]
                L[i][k] = factor

                for j in range(k, n):
                    R[i][j] -= factor * R[k][j]      
        return L, R 