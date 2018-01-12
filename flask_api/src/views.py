__author__ = 'KOR_Solidarity'

import hashlib
import json
import random
import os

from flask_api import app, mysql
from .defs import pwd, verify
from .constants import *
from werkzeug.utils import secure_filename

from flask import request, jsonify, render_template

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))


# 여기서 해야하는 사안:
@app.route('/')  # ~.com/api/
def hello():
    return 'hi'


def error(err_msg):
    # 오류값 반환해주는 역할. 생값으로 보내면 타입오류 떠서 이리 분류.
    err = {'error': err_msg}
    return json.dumps(err)


# test. delete it.
@app.route('/auth')
def auth():
    username = request.args.get('user')
    password = request.args.get('pass')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM users WHERE user_id='" + username + "' AND pass='" + password + "'")
    # cursor.execute("")
    data = cursor.fetchone()
    print(data)
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"


@app.route('/get/')  # hope this works.
def get_method():
    jsons = request.args
    jsoned = json.JSONEncoder().encode(jsons)

    return jsoned


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
    test = request
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


# 친구추가
@app.route('/add_friend/')
def aldoni_amikon():
    # 의문사항. 플레이어를 연결해야 하는가? 계정을 연결해야 하는가? - 플레이어(캐릭터).
    # 우선은 플레이어를 연결해야 한다고 가정함.
    friend_id = request.args.get('friend_id')
    player_id = request.args.get('player_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('insert into `_friends` VALUES ("{}", "{}")'.format(player_id, friend_id))

    conn.commit()
    cursor.close()
    conn.close()

    return OK


@app.route('/get_friend/')
def get_friend():
    # 친구목록 불러오기.
    # 플레이어 고유번호
    player_unique_id = request.args.get('player_id')

    conn = mysql.connect()
    cursor = conn.cursor()
    # cursor.execute('select * from INNER JOIN `_friends` on `_players`.player_unique_id = `_friends`.friend_unique_id '
    #                'WHERE `_friends`.friend_unique_id = "{}"'.format(user_id))
    # redonas numero de rezultoj
    cursor.execute('SELECT friend_unique_id FROM `_friends_copy` '
                   'WHERE player_unique_id = "{0}" '
                   'UNION '
                   'SELECT player_unique_id FROM `_friends_copy`'
                   'WHERE friend_unique_id = "{0}"'.format(player_unique_id))

    friend_ids = cursor.fetchall()

    loads = []

    content = {}

    for f in friend_ids:
        cursor.execute('select a.player_unique_id, a.player_nick  from `_players` AS a WHERE player_unique_id')
        content = {PLAYER_UNIQUE_ID: f[1], 'email': f[2]}

    cursor.close()
    conn.close()
    # 미완성. 자료가 유니티로 어떻게 넘겨지는지에 대해 좀 알아봐야함.
    # 이름, 크루, 랭크, 고유 식별번호
    # MUST BE IN JSON
    return jsonify(loads)


@app.route('/block_user/')
def block_user():
    """
    상대방 차단. 아이디로 확인한다.
    :return:
    """


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
    # 여기(테이블)서 나와야 할 사안: 별명, 소속크루,
    cursor.execute('SELECT player_nick, player_unique_id, affiliated_crew_id '
                   'FROM `_players` WHERE user_num="{}"'.format(user_num))
    player_inf = cursor.fetchone()
    player_json = {PLAYER_NICK: player_inf[0], PLAYER_UNIQUE_ID: player_inf[1]
                   , CREW_ID: player_inf[2]}

    # progreso.
    cursor.execute('select crew_name, crew_boundary '
                   'from crew where crew_id="{}"'.format(player_inf[2]))
    crew_inf = cursor.fetchone()
    player_json.update({CREW_NAME: crew_inf[0], CREW_BOUNDARY: crew_inf[1]})

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

    # 여기까지 왔으면 이제남은건 아이템 목록과 재화현황.
    # todo 테이블을 쪼개되 종류별로 나눠야 함.
    # 테이블에서 프라이머리 키는 둘 이상 됨. 고로 아이템번호와 계정아이디를 엮는다.



    # json.dumps == dic를 JSON.stringify형태로 변환시켜준다.
    stringify = json.dumps(player_json)
    print('type: {} | {}'.format(type(stringify), stringify))
    # jsoned = json.loads(player_json)
    # print('type: {} | {}'.format(type(jsoned), jsoned))

    return stringify


# ONLY FOR TEST. BETTER NOT HAVE IT WHEN RELEASED
@app.route('/debug/')
def debug():

    # return "10"
    player_unique_id = request.args.get('player_id')
    conn = mysql.connect()
    cursor = conn.cursor()
    userid = 10

    cursor.execute('SELECT * FROM `_users` WHERE user_num = "{}"'.format(userid))
    # 친구목록 불러오기.
    # 해당 execute 자체는 목록의 수를 반환함.
    cursor.execute('SELECT friend_unique_id FROM `_friends_copy` '
                   'WHERE player_unique_id = "{0}" '
                   'UNION '
                   'SELECT player_unique_id FROM `_friends_copy`'
                   'WHERE friend_unique_id = "{0}"'.format(player_unique_id))

    print(cursor.fetchall())
    return 'a'

    # print('res {}, type {}'.format(res, type(res)))

    # 이 방식으로 jSON화.

    smth = cursor.fetchall()
    loads = []
    content = {}

    for s in smth:
        print(s)
        content = {'user_id': s[1], 'email': s[2]}
        loads.append(content)

    print('sss')
    # dumps = json.dumps()
    print('loads : {}, type: {}'.format(loads, type(loads)))
    # print(bool)
    # stringify = ''
    jsonified = jsonify(loads)
    stringify = json.dumps(loads)

    print('type: {}'.format(type(jsonified)))
    print('stringify: {}, type: {}'.format(stringify, type(stringify)))
    stringify = stringify.encode('utf-8')
    hasher = hashlib.md5()
    hasher.update(stringify)

    return hasher.hexdigest()


@app.route('/item/<item_num>')
def item_info(item_num):
    """
    템 정보 조회·수정·삭제기능
    :param item_num: 아이템 번호.
    :return:
    """

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('show FULL COLUMNS from items_effect')
    # 아이템 항목(칼럼)명들.
    item_effect_columns = cursor.fetchall()
    print("effect: {}".format(item_effect_columns))
    print('\n {}'.format(item_effect_columns[0]))

    cursor.execute("select * from items WHERE id_num = {}".format(item_num))
    item = cursor.fetchone()
    print("item: {}".format(item))

    cursor.execute("show FULL COLUMNS from items")

    item_info_columns = cursor.fetchall()
    print('item_info_columns: {}'.format(item_info_columns))

    cursor.execute("select * from items_effect WHERE id_num = {}".format(item_num))
    item_info = cursor.fetchone()
    print('info: {}'.format(item_info))

    target = os.path.join(APP_ROUTE, 'pic\\items\\')
    print('target: {}'.format(target))
    # 이미지 저장된 위치. 현재 설정상 /src/pic/items 에 전부 위치
    item_pic_location = "pic/items/{}".format(item[3])

    item_effect_columns_len = len(item_effect_columns)

    # item_reg 템 등록중인가? 이 항목은 템을 등록하는게 아니라 조회하는거니 해당사항 아니다.
    return render_template("admin_item_info.html", item=item, item_info_columns=item_info_columns
                           , item_effect_columns=item_effect_columns
                           , item_info=item_info
                           , item_reg=1, item_pic_location=item_pic_location
                           , item_effect_columns_len=item_effect_columns_len
                           , season_item=0)


@app.route('/a/')
def aaa():
    # sample.
    topic = '플레이어 명단'
    conn = mysql.connect()
    cursor = conn.cursor()
    print('A?')
    cursor.execute('select a.user_num, a.user_id, a.user_email,  b.player_unique_id, b.player_nick , b.player_highscore, c.crew_name '
                   'from _users as a  JOIN `_players` as b  JOIN crew as c on a.user_num = b.user_num and b.affiliated_crew_id = c.crew_id')
    # select
    # a.user_num, a.user_id, a.user_email, b.player_unique_id, b.player_nick, b.player_highscore, c.crew_name
    # from
    # `_users` as a
    # JOIN
    # `_players` as b
    # JOIN
    # crew as c
    # on
    # a.user_num = b.user_num and b.affiliated_crew_id = c.crew_id;

    p = cursor.fetchall()
    print(p)
    print(p[0][1])
    print('******')
    for a in p:
        print(a)
    print('진입')
    return render_template('admin_player_list.html', a='1', player_list=p, topic=topic)


# 관리자 페이지.
@app.route('/admin/player_list/<page_num>')
def admin_player_list(page_num=1):

    # 관리자한테 필요한거?
    # 계정확인.
    #
    conn = mysql.connect()
    cursor = conn.cursor()
    print('A?')
    cursor.execute('select a.user_num, a.user_id, a.user_email,  b.player_unique_id, b.player_nick, '
                   'b.player_highscore, c.crew_name '
                   'from `_users` as a  JOIN `_players` as b  JOIN crew as c '
                   'on a.user_num = b.user_num and b.affiliated_crew_id = c.crew_id')
    # select
    # a.user_num, a.user_id, a.user_email, b.player_unique_id, b.player_nick, b.player_highscore, c.crew_name
    # from
    # `_users` as a
    # JOIN
    # `_players` as b
    # JOIN
    # crew as c
    # on
    # a.user_num = b.user_num and b.affiliated_crew_id = c.crew_id;

    player_list = cursor.fetchall()
    print(player_list)
    print(player_list[0][1])
    for a in player_list:
        print(a)

    cursor.close()
    conn.close()

    return render_template('admin_player_list.html', a='1', player_list=player_list, page_num=page_num)


@app.route('/admin/player/<player_id>')
def admin_player_info(player_id):
    """

    :param player_id: 플레이어 고유번호 (유니크 아이디)
    :return:
    """

    # 여러번에 걸쳐서 테이블을 부른다. 한번에 다 하려고 했는데 졸라 머리아픔.

    conn = mysql.connect()
    cursor = conn.cursor()

    # 플레이어 별명, 고유번호, 유저번호, 랭크, 소속크루 번호.
    cursor.execute('select player_nick, player_unique_id, user_num, player_highscore, affiliated_crew_id '
                   'from _players WHERE player_unique_id = {}'.format(player_id))
    # 하나만 떠야 정상임.
    _player = cursor.fetchone()

    print("_player: {}".format(_player))

    # 이메일, 가입일자, 최종 로그인 일자, 등등이 필요. 현재는 미구현.

    # 소속크루
    crew_num = _player[4]
    print("crew_num: {}".format(crew_num))
    # 관리번호. 추후 고유번호로 바꿔야함.
    user_num = _player[2]
    print("user_num: {}".format(user_num))

    # 유저의 아이디.
    cursor.execute('select user_id from _users WHERE _users.user_num = {}'.format(user_num))
    user_id = cursor.fetchone()[0]
    print('user_id: {}'.format(user_id))
    # 소속 크루 관련 정보. 소속 크루 번호에 따른 이름.
    cursor.execute('SELECT crew_id, crew_name from crew WHERE crew_id = {}'.format(crew_num))

    _crew = cursor.fetchone()
    print("_crew: {}".format(_crew))
    # 현존하는 전체 크루 목록.
    cursor.execute('SELECT crew_id, crew_name from crew WHERE crew_exist = 1')
    # 모든 크루 목록.
    crew_list = cursor.fetchall()
    print("crew_list: {}".format(crew_list))

    # 보유 아이템 목록
    cursor.execute('select * from _player_items a '
                   'INNER JOIN items b on a.item_num = b.id_num where a.player_num = {0} '
                   'UNION '
                   'select * from _player_items a '
                   'INNER JOIN items_iap c on a.item_num = c.id_num where a.player_num = {0}'.format(user_num))
    lists = cursor.fetchall()
    print("lists: {}".format(lists))

    # 가진 돈 목록:
    cursor.execute('select * from _players_cash WHERE _players_cash.player_unique_id = {}'.format(player_id))

    money = cursor.fetchone()
    print('money: {}'.format(money))

    cursor.close()
    conn.close()

    return render_template('admin_user_profile.html', _player=_player, _crew=_crew, crew_list=crew_list, lists=lists
                           , user_id=user_id, money=money)


@app.route('/admin_login/')
def admin_login():
    # 관리자 계정으로 로그인 절차. 당장은 그냥 되는걸로.
    return


# 회원가입
@app.route('/register/')
def register():
    # 여기서 기초적인 회원가입을 실시한다.
    # 회원가입에 쓰일 테이블은 _users, _pass 두가지다.
    userid = request.args.get("id")
    passwd = request.args.get("pwd")
    email = request.args.get('email')

    hashed_pwd = pwd.crpyt_pass(passwd)
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        print("INSERT INTO `_users`(user_id, user_email) VALUES ({}, {})".format(userid, email))
        cursor.execute("INSERT INTO `_users`(user_id, user_email) VALUES (\"{}\", \"{}\")".format(userid, email))
        print('chkpt')
        cursor.execute("SELECT user_num FROM `_users` WHERE user_id = \"{}\"".format(userid))
        user_num = cursor.fetchone()
        print(user_num[0])
        # conn.close()
        cursor.execute("INSERT into `_pass`(user_num, pwd) VALUES (\"{}\", \"{}\")".format(user_num[0], hashed_pwd))
        print(conn.commit())
    except Exception as e:
        # 리턴값 따로 만들어야함. 이대로 나가면 안됨.
        print(e.args)
        print(e.__class__)
        return "Eraro ozakis. {}".format(e)

    cursor.close()
    conn.close()

    return 'done probably'


# post 방식으로 자료받기 테스트
@app.route('/inp', methods=['POST', 'GET'])
def inp():
    # 포스트 방식으로 name 태그 붙은 인풋들 다 잘 받아지긴 함.
    res = request.form
    for r in res:
        print(res[r])
        # print(r.value)
    print(res)
    # 이게 파일임. bool 적용이 되니 그걸로 판단한다.
    try:
        img = request.files['image']
    # 여기 걸린다는건 업로드한 사진이 없다는거임.
    except Exception as e:
        img = False
    # print(bool(img))
    if img:
        # 이거 기능: 파일명을 더 안정적인 버전으로 변환.
        name = secure_filename(img.filename)
        print('name: {}'.format(name))
        print(img)
        img.save(os.path.join(app.config['UPLOAD_FOLDER']+'/pic/items', name))
    return 'um??'


# 아이템 수정
@app.route('/item_edit/<item_num>')
def item_edit(item_num):
    return