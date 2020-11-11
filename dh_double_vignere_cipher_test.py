from dh_double_vignere_cipher import dh_double_vignere_enc
from dh_double_vignere_cipher import dh_double_vignere_dec
import dh_double_vignere_cipher as dvc
import diffie_hellman as dh
import json


def test():
    with open("message.txt", 'w') as message_file:
        message_file.write("Super secret text\n don't share with anyone\n")

    with open("crypto_parameters.json", 'w') as crypto_file:
        json.dump({}, crypto_file)

    # act 1
    dh_double_vignere_enc()

    # assert 1
    with open("crypto_parameters.json", 'r') as crypto_parameters_file:
        crypto_parameters = json.load(crypto_parameters_file)
        assert crypto_parameters[dvc.JSON_G] == 7
        assert crypto_parameters[dvc.JSON_NUMBER_OF_DIGITS] == 2500
        assert len(crypto_parameters[dvc.JSON_N]
                   ) == crypto_parameters[dvc.JSON_NUMBER_OF_DIGITS]
        assert dvc.JSON_SECRET_NUMBER in crypto_parameters
        assert dvc.JSON_OWN_PUBLIC_NUMBER in crypto_parameters
        assert dvc.JSON_KEY not in crypto_parameters
        assert dvc.JSON_PARTNER_PUBLIC_NUMBER not in crypto_parameters

        crypto_parameters[dvc.JSON_PARTNER_PUBLIC_NUMBER] = str(dh.diffie_hellman_syn(
            int(crypto_parameters[dvc.JSON_G]), int(crypto_parameters[dvc.JSON_N]), dh.get_secret_number(int(crypto_parameters[dvc.JSON_N]))))

    with open("crypto_parameters.json", 'w') as crypto_parameters_file:
        json.dump(crypto_parameters, crypto_parameters_file)

    # act 2
    dh_double_vignere_enc()

    with open("crypto_parameters.json", 'r') as crypto_parameters_file:
        crypto_parameters = json.load(crypto_parameters_file)
        assert crypto_parameters[dvc.JSON_G] == 7
        assert crypto_parameters[dvc.JSON_NUMBER_OF_DIGITS] == 2500
        assert len(crypto_parameters[dvc.JSON_N]
                   ) == crypto_parameters[dvc.JSON_NUMBER_OF_DIGITS]
        assert dvc.JSON_SECRET_NUMBER in crypto_parameters
        assert dvc.JSON_OWN_PUBLIC_NUMBER in crypto_parameters
        assert dvc.JSON_PARTNER_PUBLIC_NUMBER in crypto_parameters
        assert dvc.JSON_KEY in crypto_parameters

    with open("crypto_parameters.json", 'w') as crypto_parameters_file:
        crypto_parameters.pop(dvc.JSON_KEY_FIRST_INDEX)
        crypto_parameters.pop(dvc.JSON_KEY_SECOND_INDEX)
        json.dump(crypto_parameters, crypto_parameters_file)

    # act 3

    dh_double_vignere_dec()

    with open("message.txt", 'r') as message_file:
        assert message_file.read() == "Super secret text\n don't share with anyone\n"


test()
