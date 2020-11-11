# What this program is for

Encrypting a continuous stream of E-mails in a (somewhat) secure manner

# How does it work?

Obviously, both end-to-end partners will need a version of the program. 
The encryption works by establishing a symmetric key securely through a diffie hellman key exchange (each partner will have to agree on common parameters n, g and number_of_digits for this exchange and afterward send the public key to each other). The methods `dh_double_vignere_enc` and `dh_double_vignere_dec` will do all the work for you - they'll calculate any value that can be calculated based on the values stored in a `crypto_parameters.json` file or use the values already inside that file when possible. If there are no values to work with, the functions will use reasonable defaults. The only parameter that can't be calculated or substituted by a default is your partner's public key - you won't be able to encrypt or decrypt anything without that. After the shared key has been calculated, these same methods will encrypt a message in a `message.txt` file or decrypt a message in `encrypted_message.txt` respectively, and write their output in the opposite file. The actual cipher is a two-fold vignere-cipher, first using the shared key, and then the shared key with two digits cut off, in order to allow for much longer texts (a length of n², where n is the length of the key divided by 2) to be (somewhat) securely encrypted and decrypted. The cipher is a stream-cipher, so it's important that whenever one partner encrypts messages, the other partner has to decrypt the same messages in the same order so that their programs do not desync (meaning disaligned indices of the two ciphers). Should you accidentally make a mistake and threaten to desync your indices, don't worry! The program saves a history of every index position. You'll just have to look into your `crypto_parameters.json` and manually adjust the indices.

I think that's about it? If you have any questions, feel free to ask me!

# Why?

Read the title.

# No seriously, why?

We're doing a pen and paper over e-mail where eavesdropping/ intercepting messages is an actual thing, so this is a bit of a defense against that. Also read the title.
