# -*- coding: utf-8 -*-
import ast
from numbers import Number


class Utility:
    # Dimensionen bestimmen und dann prüfen
    def get_products(self, matrix_a, matrix_b):
        rows_a = len(matrix_a)
        cols_a = len(matrix_a[0])
        rows_b = len(matrix_b)
        cols_b = len(matrix_b[0])

        if cols_a != rows_b:
            message = "Matrizen können nicht multipliziert werden. Inkorrekte Dimensionen."
            return message

        result_matrix = [[0 for row in range(cols_b)] for col in range(rows_a)]

        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]
        return result_matrix

    # Matrix ausgeben
    def pretty_print_matrix(self, matrix: list[list[float]]):
        for i in matrix:
            print(f"{i}")

    # Matrix als String formatieren: Matrix Liste in lesbaren String
    def format_matrix_list_to_str(self, matrix: list[list[float]]):
        """changes a list-type matrix into a str-matrix with new-lines added"""
        # Round values to avoid floating point precision issues
        rounded_matrix = [[round(val, 10) for val in row] for row in matrix]
        matrix_str = str(rounded_matrix).split('],')
        result = ""

        for i in range(len(matrix_str)-1):
            result += matrix_str[i] + "],\n"
        result += matrix_str[len(matrix_str)-1]

        return result

    # Matrix aus String einlesen: Wandelt vom Benutzer eingegebene Matrix um, String -> Liste von Listen
    def format_matrix_str_to_list(self, matrix: str):
        """formats a matrix from string for list and casts all numbers to floats"""
        try:
            result = ast.literal_eval(matrix)
            if isinstance(result[0], Number):
                for i in range(len(result)):
                    result[i] = [result[i]]
            result = [[float(j) for j in i] for i in result]

            return result
        except:
            return (
                "Der eingegebene Matrix-String konnte nicht in eine Liste konvertiert werden. Bitte die Eingabe in das Format: [[1, 2], [3, 4]] ändern.")

    # L,R-Matrix kombinieren für Darstellung, dient zur Visualisierung von L & R
    def add_matrices(self, matrix1, matrix2):
        result = [[0]*len(matrix1) for i in range(len(matrix1))]
        for row in range(len(matrix1)):
            for col in range(len(matrix1)):
                if row == col:
                    result[row][col] = matrix2[row][col]
                else:
                    result[row][col] = matrix1[row][col] + matrix2[row][col]
        return result