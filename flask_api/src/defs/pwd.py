from passlib.hash import sha256_crypt


def crpyt_pass(password):
    return sha256_crypt.encrypt(password)
