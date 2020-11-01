import math


def is_prime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n <= 1:
        return False

    sqr = int(math.sqrt(n)) + 1

    for divisor in range(3, sqr, 2):
        if n % divisor == 0:
            return False
    return True


def efficient_modulo_power(x, y, n):

    if (y == 0):
        return 1 % n

    result = x
    iteration = 1

    # Exponent of the closest power of 2 smaller than y
    number_of_iterations = int(math.log(y, 2))
    remainder_exponent = y - (1 << number_of_iterations)
    remainder = 1

    remainder_lookup_table = list()
    remainder_lookup_table.append(result)
    while iteration <= number_of_iterations:
        result = multiply_modulo(result, result, n)

        remainder_lookup_table.append(result)

        iteration += 1

    while not remainder_exponent == 0:
        lookup_index = int(math.log(remainder_exponent, 2))
        remainder = multiply_modulo(
            remainder, remainder_lookup_table[lookup_index], n)
        remainder_exponent -= 1 << lookup_index

    result = multiply_modulo(result, remainder, n)
    return result


def multiply_modulo(x, y, n):
    return (x * y) % n
