from utility import Utility

class Crout:
    def crout_lr(self, matrix):
        n = len(matrix)

        # quadratische Matrix prüfen
        for row in matrix:
            if len(row) != n:
                raise ValueError("Matrix ist nicht quadratisch!")

        # L und R initialisieren
        L = [[0.0 for _ in range(n)] for _ in range(n)]
        R = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

        for j in range(n):
            # L berechnen
            for i in range(j, n):
                s = 0.0
                for k in range(j):
                    s += L[i][k] * R[k][j]
                L[i][j] = matrix[i][j] - s

            if L[j][j] == 0:
                raise ZeroDivisionError("Zero pivot encountered")

            # R berechnen
            for i in range(j + 1, n):
                s = 0.0
                for k in range(j):
                    s += L[j][k] * R[k][i]
                R[j][i] = (matrix[j][i] - s) / L[j][j]

        return L, R