import diffie_hellman as dh
import json
from streamcipher import VignereStreamCipher

JSON_G = "prime_number_g"
JSON_NUMBER_OF_DIGITS = "number_of_digits"
JSON_N = "n"
JSON_SECRET_NUMBER = "secret_number"
JSON_PARTNER_PUBLIC_NUMBER = "partner_public_number"
JSON_OWN_PUBLIC_NUMBER = "own_public_number"
JSON_KEY = "key"
JSON_KEY_FIRST_INDEX = "key_first_index"
JSON_KEY_SECOND_INDEX = "key_second_index"
JSON_FST_INDEX_HISTORY = "first_key_index_history"
JSON_SND_INDEX_HISTORY = "second_key_index_history"


def dh_double_vignere_enc():

    try:
        with open("crypto_parameters.json", 'r') as crypto_parameters_file:
            crypto_parameters = json.load(crypto_parameters_file)
    except:
        crypto_parameters = {}

    try:
        key_string, number_of_digits, first_key_index, second_key_index = load_or_create_crypto_parameters(
            crypto_parameters)
    except Exception as e:
        print(e)
        return
    finally:
        save_json(crypto_parameters, "crypto_parameters.json")

    first_vigner_stream_cipher = VignereStreamCipher(
        key_string, first_key_index, number_of_digits)

    second_vigner_stream_cipher = VignereStreamCipher(
        key_string[:-2], second_key_index, number_of_digits - 2)

    with open("message.txt", 'r') as message_file:
        text = message_file.read()

    encrypted_text = first_vigner_stream_cipher.encrypt(text)

    double_encrypted_text = second_vigner_stream_cipher.encrypt(encrypted_text)

    save_indices(crypto_parameters, first_key_index, second_key_index,
                 first_vigner_stream_cipher.index, second_vigner_stream_cipher.index)

    with open("encrypted_message.txt", 'w') as output_file:
        output_file.write(double_encrypted_text)

    save_json(crypto_parameters, "crypto_parameters.json")

    return


def dh_double_vignere_dec():

    with open("crypto_parameters.json", 'r') as crypto_parameters_file:
        try:
            crypto_parameters = json.load(crypto_parameters_file)
        except:
            crypto_parameters = {}

    try:
        key_string, number_of_digits, first_key_index, second_key_index = load_or_create_crypto_parameters(
            crypto_parameters)
    except Exception as e:
        save_json(crypto_parameters, "crypto_parameters.json")
        print(e)
        return

    save_json(crypto_parameters, "crypto_parameters.json")

    first_vigner_stream_cipher = VignereStreamCipher(
        key_string, first_key_index, number_of_digits)

    second_vigner_stream_cipher = VignereStreamCipher(
        key_string[:-2], second_key_index, number_of_digits - 2)

    with open("encrypted_message.txt", 'r') as message_file:
        double_encrypted_text = message_file.read()

    encrypted_text = second_vigner_stream_cipher.decrypt(
        double_encrypted_text)
    text = first_vigner_stream_cipher.decrypt(encrypted_text)

    save_indices(crypto_parameters, first_key_index, second_key_index,
                 first_vigner_stream_cipher.index, second_vigner_stream_cipher.index)

    with open("message.txt", 'w') as output_file:
        output_file.write(text)

    save_json(crypto_parameters, "crypto_parameters.json")
    return


def load_or_create_crypto_parameters(crypto_parameters):
    g = load_field_or_create_default(JSON_G, 7, crypto_parameters)

    number_of_digits = int(load_field_or_create_default(
        JSON_NUMBER_OF_DIGITS, 2500, crypto_parameters))

    n = int(load_field_or_calculate_and_create(
        JSON_N, lambda: dh.get_random_n(number_of_digits), crypto_parameters))

    secret_number = int(load_field_or_calculate_and_create(
        JSON_SECRET_NUMBER, lambda: dh.get_secret_number(n), crypto_parameters))

    own_public_number = int(load_field_or_calculate_and_create(
        JSON_OWN_PUBLIC_NUMBER, lambda: dh.diffie_hellman_syn(g, n, secret_number), crypto_parameters))

    if not JSON_PARTNER_PUBLIC_NUMBER in crypto_parameters:
        raise Exception(
            "Continuing requires the public number of your partner")

    partner_public_number = int(crypto_parameters[JSON_PARTNER_PUBLIC_NUMBER])

    key_string = load_field_or_calculate_and_create(JSON_KEY, lambda: dh.diffie_hellman_syn_ack(
        partner_public_number, n, secret_number), crypto_parameters)

    first_key_index = load_field_or_create_default(
        JSON_KEY_FIRST_INDEX, 0, crypto_parameters)
    second_key_index = load_field_or_create_default(
        JSON_KEY_SECOND_INDEX, 0, crypto_parameters)

    return key_string, number_of_digits, first_key_index, second_key_index


def save_indices(crypto_parameters, first_key_index_old, second_key_index_old, first_key_index_new, second_key_index_new):
    if not JSON_FST_INDEX_HISTORY in crypto_parameters:
        crypto_parameters[JSON_FST_INDEX_HISTORY] = list()
    if not JSON_SND_INDEX_HISTORY in crypto_parameters:
        crypto_parameters[JSON_SND_INDEX_HISTORY] = list()
    crypto_parameters[JSON_FST_INDEX_HISTORY].append(first_key_index_old)
    crypto_parameters[JSON_SND_INDEX_HISTORY].append(second_key_index_old)
    crypto_parameters[JSON_KEY_FIRST_INDEX] = first_key_index_new
    crypto_parameters[JSON_KEY_SECOND_INDEX] = second_key_index_new


def load_field_or_create_default(field_name, default_value, crypto_parameters):
    if not field_name in crypto_parameters:
        field = default_value
        crypto_parameters[field_name] = field
        return field
    else:
        return crypto_parameters[field_name]


def load_field_or_calculate_and_create(field_name, calculating_function, crypto_parameters):
    if not field_name in crypto_parameters:
        field = str(calculating_function())
        crypto_parameters[field_name] = field
        return field
    else:
        return crypto_parameters[field_name]


def save_json(json_obj, file_name):
    with open(file_name, 'w') as file:
        json.dump(json_obj, file)
