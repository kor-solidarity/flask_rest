from passlib.hash import sha256_crypt
import pymysql

# from defs import mysql
from . import mysql

def kontroli(identify, chifro):
    """

    :param identify: 아이디
    :param chifro: 암호
    :return: 결과값들. 아직 정확히 안정함.
    """

    print('ID: ', identify)
    print('PASS:', chifro)

    # 암호확인작업.
    conn = mysql.connect()
    cursor = conn.cursor()

    # 아이디가 존재하는지 확인한다.
    cursor.execute('SELECT user_num FROM `_users` WHERE user_id = "{}"'.format(identify))
    user_num = cursor.fetchone()[0]
    print('user_num', user_num)
    print('type:', type(user_num))
    print(bool(user_num))
    # ne user_num signifas tie ne estas tiel ID.
    if not user_num:
        # return 'FAIL - no such ID'
        return False
    else:
        # 확인이 됐으면 해당 아이디에 저장된 암호화된 암호 빼간다.
        cursor.execute('SELECT pwd FROM `_pass` WHERE user_num = "{}"'.format(user_num))
        password = cursor.fetchone()[0]

    print('password:', password)
    # 실질적인 확인작업
    kontrolado = sha256_crypt.verify(chifro, password)
    print(kontrolado)
    # kontrolado = sha256_crypt.verify(identify, chifro)
    # True or False
    return kontrolado
