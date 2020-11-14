
class StreamCipher:

    def __init__(self, key: str, initial_index: int, number_of_digits: int):
        self.key = key.zfill(number_of_digits)
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

    CHARACTER_SPACE_START = 33
    CHARACTER_SPACE_END = 126
    CHARACTER_SPACE_SIZE = CHARACTER_SPACE_END - CHARACTER_SPACE_START

    def __init__(self, key: str, index: int, number_of_digits: int):
        super().__init__(key, index, number_of_digits)

    def _keep_in_character_space(self, number: int):
        return ((number + self.CHARACTER_SPACE_SIZE - self.CHARACTER_SPACE_START) % self.CHARACTER_SPACE_SIZE) + self.CHARACTER_SPACE_START

    def _encryption_algorithm(self, text, key):

        sequence_of_shifts = [int(key[i:i+2]) % self.CHARACTER_SPACE_SIZE
                              for i in range(0, len(key), 2)]

        shifted_text = ""

        # make key long enough for the text by repetition
        self.__repeat_list_until_length(sequence_of_shifts, len(text))

        for i in range(len(text)):
            shifted_text += chr(self._keep_in_character_space((ord(text[i]) + sequence_of_shifts[i]))) if ord(
                text[i]) >= self.CHARACTER_SPACE_START and ord(text[i]) < self.CHARACTER_SPACE_END else text[i]

        return shifted_text

    def _decryption_algorithm(self, text, key):

        sequence_of_shifts = [int(key[i:i+2]) % self.CHARACTER_SPACE_SIZE
                              for i in range(0, len(key), 2)]
        shifted_text = ""

        # make key long enough for the text by repetition
        self.__repeat_list_until_length(sequence_of_shifts, len(text))

        for i in range(len(text)):
            shifted_text += chr(self._keep_in_character_space(ord(text[i]) + self.CHARACTER_SPACE_SIZE - sequence_of_shifts[i])) if ord(
                text[i]) >= self.CHARACTER_SPACE_START and ord(text[i]) < self.CHARACTER_SPACE_END else text[i]

        return shifted_text

    def __repeat_list_until_length(self, list_arg: list, length: int) -> list:
        size_difference=length - len(list_arg)

        if size_difference > len(list_arg):
            factor: int=int(size_difference / len(list_arg))
            size_difference -= factor * len(list_arg)
            list_arg += factor * list_arg

        list_arg += list_arg[0:size_difference]
