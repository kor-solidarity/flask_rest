"""
이곳에서 플레이어 관련 작업을 다 전담한다.
"""

__author__ = 'KOR_Solidarity'

import hashlib
import json
import random
import os
import math

from flask_api import app, mysql
from .defs import pwd, verify
from .constants import *
from werkzeug.utils import secure_filename

from flask import request, jsonify, render_template, redirect, url_for, session


def error(err_msg):
    # 오류값 반환해주는 역할. 생값으로 보내면 타입오류 떠서 이리 분류.
    err = {'error': err_msg}
    return json.dumps(err)


# 로그인 시험
@app.route('/login/')
def trovi_ensaluti(user_id=None, pwd=None, reg=False):
    """
    :param user_id:
    :param pwd:
    :param reg:
    위 세 변수는 회원가입 됐을 시 한정으로만 작동한다.
    :return:
    """
    password = request.args.get('pass')
    identify = request.args.get('id')

    # 먼져 아이디가 있는지 확인한다.
    # 그 후 암호 확인. 아래 함수에서 별도 실행함. 다른 모든 기능들도 이래야함.
    result = verify.kontroli(identify, password)
    print("res", result)

    if not result:
        # 로그인 오류: 암호 또는 아이디이 불일치.
        return error(-4)

    # 여기서부터 본격적인 작업 실시.
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT user_num FROM `_users` WHERE user_id="{}"'.format(identify))
    # 유저번호 빼오기.
    user_num = cursor.fetchone()[0]
    print('user_num: {}'.format(user_num))
    # 확인이 끝나면 반환값들 찾아야함.
    # 여기(테이블)서 나와야 할 사안: id, 별명, 소속크루,
    cursor.execute('SELECT player_nick, player_unique_id, affiliated_crew_id '
                   'FROM `_players` WHERE user_num="{}"'.format(user_num))
    player_inf = cursor.fetchone()
    player_unique = player_inf[1]
    player_json = {PLAYER_NICK: player_inf[0], PLAYER_UNIQUE_ID: player_inf[1]
                   , CREW_ID: player_inf[2]}

    # progreso de kru-o. we need a full list of crew and their names and their
    cursor.execute('select crew_id, crew_name, crew_desc, crew_boundary '
                   'from crew where crew_exist = 1'.format(player_inf[2]))
    crew_inf = cursor.fetchall()
    # 안에 각종 크루 내용물 드가야 함.
    crew_json = {CREW_STATS: {}}
    # sample = {CREW_ID: {CREW_NAME: 0, CREW_DESC: 10, CREW_BOUNDARY: 3 }}
    for crew_ind_inf in crew_inf:
        print(crew_ind_inf)
        crew_ind_json = {crew_ind_inf[0]:
                             {CREW_NAME: crew_ind_inf[1], CREW_DESC: crew_ind_inf[2]
                              , CREW_BOUNDARY: crew_ind_inf[3]}}
        # CREW_STATS 안에다가 새로 값을 넣는다.
        crew_json[CREW_STATS].update(crew_ind_json)

    player_json.update(crew_json)

    # ero, mono.
    cursor.execute('SELECT * FROM `_players_cash` WHERE player_unique_id = {}'.format(player_unique))
    player_mono = cursor.fetchone()
    player_mono_inf = {CASH: {1: player_mono[1], 2: player_mono[2]
                              , 3: player_mono[3], 4: player_mono[4]}}

    player_json.update(player_mono_inf)
    """
    NOT NEEDED IN THIS PART.
    COMMENTED INSTEAD OF DELETED SINCE i'LL NEED IT LATER IN OTHER AREA.
    
    # amikoj
    cursor.execute('SELECT friend_unique_id FROM `_friends_copy` '
                   'WHERE player_unique_id = {0} AND friend_accepted = 1 '
                   'UNION '
                   'SELECT player_unique_id FROM `_friends_copy`'
                   'WHERE friend_unique_id = {0}'.format(player_inf[1]))
    amikoj = cursor.fetchall()
    print('amikoj: {}'.format(amikoj))
    friends_list = []

    # 친구가 없으면 돌리는 의미가 없다.
    if amikoj:
        print()
        # 각 친구들의 현황 추가해야함
        for amiko in amikoj:
            # 이름과 별명, 소속크루
            cursor.execute('SELECT player_unique_id, player_nick, affiliated_crew_id '
                           'from `_players` '
                           'WHERE player_unique_id = "{}"'.format(amiko[0]))
            friend_stat = cursor.fetchone()
            # 크루이름.
            cursor.execute('select crew_name '
                           'from crew where crew_id="{}"'.format(friend_stat[2]))
            friend_crew = cursor.fetchone()[0]
            # 친구목록 넣는다.
            friend_json = {PLAYER_UNIQUE_ID: friend_stat[0], PLAYER_NICK: friend_stat[1], CREW_NAME: friend_crew[0]}
            friends_list.append(friend_json)
    else:
        print('no friends')
    # 다 넣었으면 바로 추가작업 진행한다.
    player_json.update({FRIENDS: friends_list})
    print(player_json)
    """
    # todo 테이블을 쪼개되 종류별로 나눠야 함.
    # 테이블에서 프라이머리 키는 둘 이상 됨. 고로 아이템번호와 계정아이디를 엮는다.

    # json.dumps == dic를 JSON.stringify형태로 변환시켜준다.
    stringify = json.dumps(player_json, ensure_ascii=False)
    print('type: {} | {}'.format(type(stringify), stringify))
    # jsoned = json.loads(player_json)
    # print('type: {} | {}'.format(type(jsoned), jsoned))

    # 다 끝내면 연결 바로바로 종료시킨다.
    cursor.close()
    conn.close()

    return stringify


@app.route('/reg_player/')
def reg_player():
    """
    플레이어 등록.
    :user_num
    :return:
    """
    # 플레이어 이름(계정아이디)
    user_num = request.args.get('user_num')
    # 게임닉
    nick = request.args.get('nick')
    crew_id = request.args.get('crew_id')
    # test = request
    print('user_num: {}, nick: {}, crew_id: {}'.format(user_num, nick, crew_id))
    conn = mysql.connect()
    cursor = conn.cursor()
    print('chk2')
    # 0. 이게 걸릴일은 없긴 한데... 이미 플레이어 등록된 계정에 새로 시도할 경우 중복아이디 오류
    cursor.execute('SELECT player_unique_id from `_players` WHERE user_num = "{}"'.format(user_num))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return ERR_SAME_ID

    print('chk3')
    # 1. 닉이 중복되는지 확인한다.
    # 2. 크루가 존재하는지 확인한다.
    # 2. 등록완료.
    cursor.execute('SELECT player_nick FROM `_players` WHERE player_nick = "{}"'.format(nick))
    # 여기 걸리면 닉이 있는거임.
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return error(ERR_SAME_NICK)
    print('chk4')
    # 크루 확인. 존재하는 크루인지 확인한다. 사실 인위적으로 뭘 잘못 건드리지 않는 한 문제는 안생길거라고 예상함.
    # what_the = cursor.execute('select crew_id from crew where crew_id = "{}" AND crew_exist = "{}"'.format(crew_id, str(1)))
    # print('crew? {}'.format(what_the))
    # if not what_the:
    if not cursor.execute('select crew_id from crew where crew_id = "{}" AND crew_exist = "{}"'.format(crew_id, str(1))):
        print('checkin')
        cursor.close()
        conn.close()
        return error(ERR_NO_CREW)
    # print("huh", cursor.fetchall())

    # 고유 식별번호.
    unique_number = random.randint(1, 999000)
    # 중복확인
    cursor.execute('SELECT player_unique_id FROM `_players` WHERE player_unique_id = "{}"'.format(unique_number))
    sama = cursor.fetchone()  # 여기서 None 반환 안하면 중복임.
    print('sama: {}, unique_number: {}'.format(sama, unique_number))
    # 식별번호가 중복? 그럼 중복 안될때까지 1더한다. Facile, ĉu ne?
    while sama:
        unique_number += 1
        cursor.execute('SELECT player_unique_id FROM `_players` WHERE player_unique_id = "{}"'.format(unique_number))
        sama = cursor.fetchone()

    cursor.execute('INSERT INTO `_players`(player_unique_id, user_num, affiliated_crew_id, player_nick) '
                   'VALUES ("{}", "{}", "{}", "{}")'.format(unique_number, user_num, crew_id, nick))
    conn.commit()
    cursor.close()
    conn.close()

    return 'OK'

