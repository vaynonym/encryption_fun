import streamcipher as sc


def test():

    cipher_one = sc.VignereStreamCipher(
        "12345", 0, 5)

    cipher_two = sc.VignereStreamCipher(
        "12345", 0, 5)

    cipher_three = sc.VignereStreamCipher(
        "1234", 0, 20)

    cipher_four = sc.VignereStreamCipher(
        "1234", 0, 20)

    assert cipher_two.decrypt(
        cipher_one.encrypt("Super secret text don't share with anyone")) == "Super secret text don't share with anyone"

    assert cipher_two.decrypt(cipher_four.decrypt(cipher_three.encrypt(
        cipher_one.encrypt("Super secret text don't share with anyone")))) == "Super secret text don't share with anyone"


test()
