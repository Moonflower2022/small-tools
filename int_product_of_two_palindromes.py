from sympy import factorint

def is_palindrome(n):
    return str(n) == str(n)[::-1]

def reduce_factorization(factorization):
    factors = []
    for factor, count in factorization.items():
        factors += [factor] * count
    return factors

def get_product_of_two_palindromes(n):
    factors = reduce_factorization(factorint(n))
    for factor in factors:
        if is_palindrome(factor) and is_palindrome(n // factor):
            return True
    return False

if __name__ == "__main__":
    limit = 1000000
    num_good_ints = 0
    for i in range(1, limit + 1):
        if get_product_of_two_palindromes(i):
            num_good_ints += 1
    print(num_good_ints)
