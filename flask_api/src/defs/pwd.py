from passlib.hash import sha256_crypt


def crpyt_pass(password):
    """
    암호화 작업
    :param password:
    :return:
    """
    return sha256_crypt.encrypt(password)
