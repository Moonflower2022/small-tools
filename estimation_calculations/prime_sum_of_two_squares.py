from math import isqrt

def is_prime(n):
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    limit = isqrt(n)
    for i in range(5, limit+1, 6):
        if n % i == 0 or n % (i+2) == 0:
            return False
    return True

def is_sum_of_two_squares(n):
    return n % 4 != 3

if __name__ == "__main__":
    limit = 1000000
    num_good_primes = 0
    for n in range(1, limit + 1):
        if is_prime(n) and is_sum_of_two_squares(n):
            num_good_primes += 1
    print(f"Number of good primes up to {limit}: {num_good_primes}")