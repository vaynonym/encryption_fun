import random

import encryptionmath as em


def get_random_n(number_of_digits_for_n):
    n = random.randint(10**(number_of_digits_for_n-1), 10 **
                       (number_of_digits_for_n) - 1)
    assert len(str(n)) == number_of_digits_for_n
    return n


def get_secret_number(n):
    a = random.randint(1, n)
    return a


def diffie_hellman_syn(g: int, n: int, a: int) -> int:

    assert em.is_prime(g), "g has to be prime"

    result: int = em.efficient_modulo_power(g, a, n)
    return result


def diffie_hellman_syn_ack(gb: int, n: int, a: int) -> int:
    result: int = em.efficient_modulo_power(gb, a, n)
    return result


