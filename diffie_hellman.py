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


def vignere_cipher_encrypt(text: str, key: int, number_of_digits_for_n: int) -> str:
    string_key = str(key)

    while len(string_key) < number_of_digits_for_n:
        string_key = "0" + string_key

    sequence_of_shifts: list(int) = [int(string_key[i:i+2])
                                     for i in range(0, len(string_key), 2)]

    # make key long enough for the text by repetition
    repeat_list_until_length(sequence_of_shifts, len(text))

    shifted_text = ""
    for i in range(len(text)):
        shifted_text += chr(ord(text[i]) + sequence_of_shifts[i])

    return shifted_text


def vignere_cipher_decrypt(text: str, key: int, number_of_digits_for_n: int):
    string_key = str(key)

    while len(string_key) < number_of_digits_for_n:
        string_key = "0" + string_key

    sequence_of_shifts = [string_key[i:i+2]
                          for i in range(0, len(string_key), 2)]
    shifted_text = ""

    # make key long enough for the text by repetition
    repeat_list_until_length(sequence_of_shifts, len(text))

    for i in range(len(text)):
        shifted_text += chr(ord(text[i]) - int(sequence_of_shifts[i]))

    return shifted_text


def repeat_list_until_length(list_arg: list, length: int) -> list:
    size_difference = length - len(list_arg)

    if size_difference > len(list_arg):
        factor: int = size_difference / len(list_arg)
        size_difference -= factor * len(list_arg)
        list_arg += factor * list_arg

    list_arg += list_arg[0:size_difference]
    return list_arg


def caesar_cipher_encrypt(text: str, shift_amount: int):
    return "".join([chr((ord(char) + shift_amount) % 256) if char != '\n' else "\n" for char in text])


def caesar_cipher_decrypt(text: str, shift_amount: int):
    return "".join([chr((ord(char) + 256 - shift_amount) % 256) if char != '\n' else "\n" for char in text])


number_of_digits = 2500
g = 7
