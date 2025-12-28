# -*- coding: utf-8 -*-
from utility import Utility

class Inverse:
    def gauss_jordan_inverse(self, matrix):
        """
        Berechnet die Inverse einer quadratischen Matrix mit dem Gau�-Jordan-Algorithmus.
        
        Args:
            matrix: Quadratische Matrix als Liste von Listen
            
        Returns:
            Die inverse Matrix als Liste von Listen
            
        Raises:
            ValueError: Wenn die Matrix nicht quadratisch ist
            ValueError: Wenn die Matrix singul�r ist (keine Inverse existiert)
        """
        n = len(matrix)
        
        # Quadratische Matrix pr�fen
        for row in matrix:
            if len(row) != n:
                raise ValueError("Matrix ist nicht quadratisch!")
        
        # Erweiterte Matrix erstellen: [A | I]
        # A ist die urspr�ngliche Matrix, I ist die Einheitsmatrix
        augmented = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(float(matrix[i][j]))
            # Einheitsmatrix anh�ngen
            for j in range(n):
                row.append(1.0 if i == j else 0.0)
            augmented.append(row)
        
        # Gau�-Jordan-Elimination durchf�hren
        for i in range(n):
            # Pivot-Element suchen (Zeile mit gr��tem Wert in Spalte i)
            max_row = i
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                    max_row = k
            
            # Zeilen tauschen
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            
            # Pr�fen ob Matrix singul�r ist
            if abs(augmented[i][i]) < 1e-10:
                raise ValueError("Matrix ist singul�r - keine Inverse existiert!")
            
            # Pivot-Zeile normalisieren (Diagonalelement auf 1 setzen)
            pivot = augmented[i][i]
            for j in range(2 * n):
                augmented[i][j] /= pivot
            
            # Alle anderen Zeilen eliminieren (auch oberhalb des Pivots)
            for k in range(n):
                if k != i:
                    factor = augmented[k][i]
                    for j in range(2 * n):
                        augmented[k][j] -= factor * augmented[i][j]
        
        # Inverse Matrix extrahieren (rechte H�lfte der erweiterten Matrix)
        inverse = []
        for i in range(n):
            row = []
            for j in range(n, 2 * n):
                row.append(augmented[i][j])
            inverse.append(row)
        
        return inverse
