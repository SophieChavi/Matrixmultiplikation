from utility import Utility
from gauss import Gauss
from crout import Crout

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



if __name__ == "__main__":
    test_gauss_lr()
    test_crout_lr()