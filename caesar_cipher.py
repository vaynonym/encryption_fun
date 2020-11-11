def caesar_cipher_encrypt(text: str, shift_amount: int):
    return "".join([chr((ord(char) + shift_amount) % 256) if char != '\n' else "\n" for char in text])


def caesar_cipher_decrypt(text: str, shift_amount: int):
    return "".join([chr((ord(char) + 256 - shift_amount) % 256) if char != '\n' else "\n" for char in text])