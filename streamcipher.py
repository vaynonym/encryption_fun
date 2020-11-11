
class StreamCipher:

    def __init__(self, key: str, initial_index: int, number_of_digits: int):
        while len(key) < number_of_digits:
            key = "0" + key
        self.key = key
        self.index = initial_index
        self.number_of_digits = number_of_digits

    def encrypt(self, text):
        encrypted_text = self._encryption_algorithm(
            text, self.__get_shifted_key())
        self.__adjust_index(len(text))
        return encrypted_text

    def decrypt(self, text):
        decrypted_text = self._decryption_algorithm(
            text, self.__get_shifted_key())
        self.__adjust_index(len(text))
        return decrypted_text

    def __get_shifted_key(self):
        return self.key[self.index:] + self.key[:self.index]

    def __adjust_index(self, shift: int):
        self.index = (self.index + self.number_of_digits +
                      shift) % self.number_of_digits

    def _encryption_algorithm(self, text, shifted_key):
        raise Exception("No encryption algorithm implemented")
        """This is the pure algorithm to encrypt the text using a key.
        The algorithm should be a block-cipher and will get the key
        shifted by the appropriate index."""

    def _decryption_algorithm(self, text, shifted_key):
        raise Exception("No decryption algorithm implemented")
        """This is the pure algorithm to decrypt the text using a key.
        The algorithm should be a block-cipher and will get the key
        shifted by the appropriate index."""


class VignereStreamCipher(StreamCipher):

    def __init__(self, key: str, index: int, number_of_digits: int):
        super().__init__(key, index, number_of_digits)

    def _encryption_algorithm(self, text, key):

        sequence_of_shifts = [key[i:i+2]
                              for i in range(0, len(key), 2)]

        shifted_text = ""

        # make key long enough for the text by repetition
        self.__repeat_list_until_length(sequence_of_shifts, len(text))

        for i in range(len(text)):
            shifted_text += chr((ord(text[i]) +
                                 int(sequence_of_shifts[i])) % 256)

        return shifted_text

    def _decryption_algorithm(self, text, key):

        sequence_of_shifts = [key[i:i+2]
                              for i in range(0, len(key), 2)]
        shifted_text = ""

        # make key long enough for the text by repetition
        self.__repeat_list_until_length(sequence_of_shifts, len(text))

        for i in range(len(text)):
            shifted_text += chr((ord(text[i]) + 256 -
                                 int(sequence_of_shifts[i])) % 256)

        return shifted_text

    def __repeat_list_until_length(self, list_arg: list, length: int) -> list:
        size_difference = length - len(list_arg)

        if size_difference > len(list_arg):
            factor: int = int(size_difference / len(list_arg))
            size_difference -= factor * len(list_arg)
            list_arg += factor * list_arg

        list_arg += list_arg[0:size_difference]
        return list_arg
