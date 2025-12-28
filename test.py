# -*- coding: utf-8 -*-
from utility import Utility
from gauss import Gauss
from crout import Crout
from inverse import Inverse

def test_gauss_lr():
    A = [
        [4, 2, 0],
        [4, 4, 2],
        [2, 2, 3]
    ]

    print("\n=== Gauss LR ===")

    gauss = Gauss()
    L, R = gauss.gauss_lr(A)

    print("L Matrix:")
    for row in L:
        print(row)

    print("\nR Matrix:")
    for row in R:
        print(row)

    util = Utility()
    A_product = util.get_products(L, R)

    print("\nAusgabe A (L * R):")
    for row in A_product:
        print(row)

def test_crout_lr():
    A = [
        [4, 2, 0],
        [4, 4, 2],
        [2, 2, 3]
    ]

    print("\n=== Crout LR ===")

    crout = Crout()
    L, R = crout.crout_lr(A)

    print("L Matrix:")
    for row in L:
        print(row)

    print("\nR Matrix:")
    for row in R:
        print(row)

    util = Utility()
    A_product = util.get_products(L, R)

    print("\nAusgabe A (L * R):")
    for row in A_product:
        print(row)

def test_inverse():
    print("\n=== Matrix-Inverse (Gauss-Jordan-Algorithmus) ===")
    
    # Test 1: Einfache 2x2 Matrix
    A1 = [
        [4, 7],
        [2, 6]
    ]
    
    print("\nTest 1: 2x2 Matrix")
    print("Original Matrix A:")
    for row in A1:
        print(row)
    
    inverse = Inverse()
    util = Utility()
    
    try:
        A1_inv = inverse.gauss_jordan_inverse(A1)
        
        print("\nInverse Matrix A^(-1):")
        for row in A1_inv:
            print(row)
        
        # Verifikation: A * A^(-1) sollte Einheitsmatrix ergeben
        identity = util.get_products(A1, A1_inv)
        print("\nVerifikation A * A^(-1) (sollte Einheitsmatrix sein):")
        for row in identity:
            print(row)
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 2: 3x3 Matrix
    A2 = [
        [4, 2, 0],
        [4, 4, 2],
        [2, 2, 3]
    ]
    
    print("\n\nTest 2: 3x3 Matrix")
    print("Original Matrix A:")
    for row in A2:
        print(row)
    
    try:
        A2_inv = inverse.gauss_jordan_inverse(A2)
        
        print("\nInverse Matrix A^(-1):")
        for row in A2_inv:
            print(row)
        
        # Verifikation
        identity = util.get_products(A2, A2_inv)
        print("\nVerifikation A * A^(-1) (sollte Einheitsmatrix sein):")
        for row in identity:
            print(row)
    except Exception as e:
        print(f"Fehler: {e}")
    
    # Test 3: Singuläre Matrix (sollte Fehler werfen)
    A3 = [
        [1, 2],
        [2, 4]
    ]
    
    print("\n\nTest 3: Singuläre Matrix (sollte Fehler werfen)")
    print("Matrix A:")
    for row in A3:
        print(row)
    
    try:
        A3_inv = inverse.gauss_jordan_inverse(A3)
        print("\nInverse Matrix:")
        for row in A3_inv:
            print(row)
    except ValueError as e:
        print(f"\nErwarteter Fehler: {e}")

if __name__ == "__main__":
    test_gauss_lr()
    test_crout_lr()
    test_inverse()