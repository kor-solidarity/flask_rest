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
# from flask import *

APP_ROUTE = os.path.dirname(os.path.abspath(__file__))


# @app.before_request
# def check():
#     print('5555555555555555555555555555')


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
                   'WHERE player_unique_id = "{0}" '.format(player_unique_id))
                   # 'UNION '
                   # 'SELECT player_unique_id FROM `_friends_copy`'
                   # 'WHERE friend_unique_id = "{0}"'.format(player_unique_id))

    print(cursor.fetchall())
    # return 'a'

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

    # 다 끝내면 연결 바로바로 종료시킨다.
    cursor.close()
    conn.close()

    return hasher.hexdigest()


@app.route('/item/<item_type>/<item_num>')
def item_info(item_type, item_num):
    """
    템 정보 조회·수정·삭제기능
    :param type: 아이템의 유형. 저게 뭐냐에 따라 갈린다.
    :param item_num: 아이템 번호.
    :return:
    """

    # 아이템의 종류. 크루템, 시즌템, 개인템 세종류가 있으니 그에 맞춘다.
    type_list = ['crew', 'season', 'prsn']
    type_mismatch = True
    # 여기에 걸린다면 type 주소가 잘못됐단 소리. 오류 반환한다.
    # 추후에 이렇게 하지 말고 그냥 이전 페이지로 날려야함. 현재 그 페이지가 없는 상황.
    for ty in type_list:
        if ty == item_type:
            type_mismatch = False
            break
    if type_mismatch:
        return 'FAIL! NO SUCH type'

    # 테이블 이름
    table = None
    # 효과 테이블 이름
    table_effect = None
    # item_type에 따라 크루템인지 개인템인지 시즌템인지 등 확인.
    if item_type == 'crew':
        table = 'crew_item'
        table_effect = 'crew_item_effect'
    elif item_type == 'season':
        table = 'season_item'
        table_effect = 'season_item_effect'
    elif item_type == 'prsn':
        table = 'items'
        table_effect = 'items_effect'

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute('show FULL COLUMNS from {}'.format(table_effect))
    # 아이템 능력치 항목(칼럼)명들.
    item_effect_columns = cursor.fetchall()
    print("effect: {}".format(item_effect_columns))
    print('\n {}'.format(item_effect_columns[0]))

    # 해당 템의 아이디번호
    cursor.execute("select * from {} WHERE id_num = {}".format(table, item_num))
    item = cursor.fetchone()
    print("item: {}".format(item))

    cursor.execute("show FULL COLUMNS from {}".format(table))
    # 아이템 정보 관련
    item_info_columns = cursor.fetchall()
    print('item_info_columns: {}'.format(item_info_columns))

    cursor.execute("select * from {} WHERE id_num = {}".format(table_effect, item_num))
    item_info = cursor.fetchone()
    print('info: {}'.format(item_info))

    target = os.path.join(APP_ROUTE, 'pic\\items\\')
    print('target: {}'.format(target))
    # 이미지 저장된 위치. 현재 설정상 /src/pic/items 에 전부 위치
    item_pic_location = "pic/items/{}".format(item[3])

    item_effect_columns_len = len(item_effect_columns)

    # 다 끝내면 연결 바로바로 종료시킨다.
    cursor.close()
    conn.close()

    # item_reg 템 등록중인가? 이 항목은 템을 등록하는게 아니라 조회하는거니 해당사항 아니다.
    return render_template("admin_item_info.html", item=item, item_info_columns=item_info_columns
                           , item_effect_columns=item_effect_columns
                           , item_info=item_info
                           , item_edit=1, item_pic_location=item_pic_location
                           , item_effect_columns_len=item_effect_columns_len
                           , type=item_type)


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


# 플레이어 정보 불러오기
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
                   'INNER JOIN items b on a.item_num = b.id_num where a.player_num = {0} '.format(user_num))
                   # 'UNION '
                   # 'select * from _player_items a '
                   # 'INNER JOIN items_iap c on a.item_num = c.id_num where a.player_num = {0}'.format(user_num))
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


# 관리자 계정으로 로그인 절차. 당장은 그냥 되는걸로.
@app.route('/admin_login/')
def admin_login():
    return


@app.route('/admin_logout/')
def admin_logout():
    session.pop('logged_in', None)
    redirect(url_for())


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
@app.route('/inp/', methods=['POST', 'GET'])
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


# 템 목록
@app.route('/admin/item_list', methods=['GET', 'POST'])
def admin_item_list():
    # 관리자 창에서 템 목록을 만든다.
    # 여기서 쓰이는 변수는 세가지
    # 1. item_type == 템 종류(기본값은 일반템)
    # 2. sort == 정렬기준(기본값은 번호순)
    # 3. page_num == 페이지 번호(기본값은 당연 1)

    # get, post ambaŭ povas ekzisti.
    if request.method == 'POST':
        # POST params
        res = request.form
        print('res: ', res)
        item_type = res.getlist('item_type')[0]
        sort = res.getlist('sort')[0]
        try:
            page_num = res.getlist('page_num')[0]
        except IndexError:
            page_num = 1

    else:
        # 1. GET 변수들 확인.
        item_type = request.args.get('item_type')
        sort = request.args.get('sort')
        try:
            page_num = request.args.get('page_num')
        except IndexError:
            page_num = 1
    # 한 페이지에 띄울 게시물 수
    base_rows = 50

    # 테이블 기본값. 적혀있지 않거나 잘못 적혔거나 'prsn'일 경우
    table = 'items'
    # 정렬기준 기본값. 적혀있지 않거나 잘못 적혔거나 'id'일 경우
    table_sort = 'id_num'

    # 2. 각 타입을 확인하고 이에 맞춰서 테이블 빼온다. 또한 기입이 안돼있을 경우 기본값을 설정한다.
    # 테이블값
    if item_type == 'season':
        # 시즌템일 경우
        table = 'season_item'
    elif item_type == 'crew':
        # 크루템인 경우
        table = 'crew_item'
    else:
        item_type = 'prsn'
        table = 'items'

    # 정렬기준. 아래 기준중에 crew_num이 빠졌는데 이건 추후 조치필요.
    if sort == 'name':
        table_sort = 'item_name'
    elif sort == 'rank':
        table_sort = 'item_rank'
    elif sort == 'id':
        table_sort = 'id_num'
    else:
        sort = 'id'
        table_sort = 'id_num'

    try:
        # 페이지 번호. 근데 번호가 기입되지 않은 경우에는?? 1로 초기화한다.
        if int(page_num):
            if int(page_num) < 1:
                page_numbro = 1
            else:
                page_numbro = int(page_num)

        else:
            page_numbro = 1
    except:
        page_numbro = 1

    # 2. 테이블을 열고 자료를 가져온다.
    conn = mysql.connect()
    cursor = conn.cursor()

    # 먼져 위에 페이지 번호에 맞는지부터 확인을 해야함.
    cursor.execute('SELECT count(*) FROM {}'.format(table))
    totalnum = cursor.fetchone()[0]
    # print(totalnum)
    # 50개 이하면 페이지가 하나뿐이니 1로 값 초기화.
    if (totalnum / base_rows) < 1:
        page_numbro = 1

    # 여기서 나오는 최대 페이지 수.
    total_page = math.ceil(totalnum / base_rows)

    # 페이징 - 몇번글부터 읽어들이는가?
    starting_number = base_rows * (page_numbro - 1)

    # 3. 템 목록 빼오기. 일반템이면 위, 그외는 아래.
    if table == 'items':
        crew_check = False
        cursor.execute('SELECT i.id_num, i.item_name, i.item_image '
                       ', i.item_iap, i.item_rank FROM {} i LIMIT {}, 50'.format(table, starting_number))
    else:
        crew_check = True
        # 일반템이 아닌 경우에는 소속된 크루가 있기에 같이 빼와야 한다.
        cursor.execute(
            'select i.id_num, i.item_name, i.item_image'
            ', i.item_iap, i.item_rank, i.item_crew , c.crew_name '
            'from {} i left join crew c on c.crew_id = i.item_crew'.format(table))

    items = cursor.fetchall()

    print(items)
    print('crew_check: ', crew_check)

    return render_template('admin_item_list.html', item_list=items, crew_check=crew_check
                           , total_page=total_page, current_page=page_numbro
                           , item_type=item_type, sort_type=sort)


# 아이템 수정창 띄운다. 템 관리목록에서 템 누르면 뜨는부분.
@app.route('/item_edit/<item_type>/<item_num>', methods=['POST', 'GET'])
def item_edit(item_type, item_num):
    """
    :param item_type:
    :param item_num:
    :return:
    """

    # phase 1. 우선 리퀘스트를 싹 다 가져온다.

    # 아이템 소개 부분.
    item_name = request.form.getlist('item_name')[0]
    item_desc = request.form.getlist('item_desc')[0]
    item_rank = request.form.getlist('item_rank')[0]

    try:
        page_num = request.form.getlist('page_num')[0]
    except IndexError:
        page_num = 1

    # effects 부분
    itm_atk = request.form.getlist('itm_atk')[0]
    itm_timer = request.form.getlist('itm_timer')[0]
    itm_max_pause = request.form.getlist('itm_max_pause')[0]
    itm_min_pause = request.form.getlist('itm_min_pause')[0]
    itm_collider_size = request.form.getlist('itm_collider_size')[0]
    itm_max_speed = request.form.getlist('itm_max_speed')[0]
    itm_accel = request.form.getlist('itm_accel')[0]
    itm_boost_time = request.form.getlist('itm_boost_time')[0]
    itm_boost_spd = request.form.getlist('itm_boost_spd')[0]
    itm_fever_gauge = request.form.getlist('itm_fever_gauge')[0]
    itm_fever_time = request.form.getlist('itm_fever_time')[0]
    itm_fever_bonus = request.form.getlist('itm_fever_bonus')[0]
    itm_train_hp = request.form.getlist('itm_train_hp')[0]
    itm_spw_chance = request.form.getlist('itm_spw_chance')[0]
    itm_obstacle_power = request.form.getlist('itm_obstacle_power')[0]

    print('checking types...')
    # phase 2. 개인|크루|시즌 템타입 확인여부
    # item_type = int(request.form.getlist('is_item_type')[0])
    print("item_type: {}".format(item_type))
    print('connecting to sql...')

    table = ''
    table_effect = ''
    # item_type에 따라 크루템인지 개인템인지 시즌템인지 등 확인.
    if item_type == 'crew':
        table = 'crew_item'
        table_effect = 'crew_item_effect'
    elif item_type == 'season':
        table = 'season_item'
        table_effect = 'season_item_effect'
    elif item_type == 'prsn':
        table = 'items'
        table_effect = 'items_effect'

    # 이 시점부터 서버 연결.
    conn = mysql.connect()
    cursor = conn.cursor()

    # phase 3. 이미지 확인.

    print('saving file')
    # 이게 파일임. bool 적용이 되니 그걸로 판단한다.
    try:
        img = request.files['image']
    # 여기 걸린다는건 업로드한 사진이 없다는거임.
    except Exception as e:
        img = False

    # 사진이 있을 경우 원래의 파일명으로 덮어씌운다. 없으면 넘기는거.
    if img:
        cursor.execute('SELECT item_image FROM {} WHERE id_num={}'.format(table, item_num))
        img_name = cursor.fetchone()[0]
        try:
            # 기존 사진 삭제
            os.remove(os.path.join(app.config['UPLOAD_FOLDER']+'/pic/items', img_name))
        # se ne povas serĉi la bildon, ĵus pasu.
        except FileNotFoundError:
            pass
        extension = img.filename.split('.')[-1]
        img_name = img_name.split('.')[0] + '.{}'.format(extension)
        # 새로 저장
        img.save(os.path.join(app.config['UPLOAD_FOLDER']+'/pic/items', img_name))
        # update.
        cursor.execute('UPDATE {} SET item_image="{}" WHERE id_num={}'.format(table, img_name, item_num))

    # phase 4. 유료템 여부 확인.
    if request.form.getlist('iap'):
        cursor.execute('UPDATE {} SET item_iap=1 WHERE id_num = {}'.format(table, item_num))
    else:
        cursor.execute('UPDATE {} SET item_iap=0 WHERE id_num = {}'.format(table, item_num))

    # phase 5. 수정 실시.
    # effects
    cursor.execute('UPDATE {} SET itm_atk={}'
                   ', itm_timer={}, itm_max_pause={}, itm_min_pause={}'
                   ', itm_collider_size={}, itm_max_speed={}, itm_accel={}'
                   ', itm_boost_time={}, itm_boost_spd={}, itm_fever_gauge={}'
                   ', itm_fever_time={}, itm_fever_bonus={}, itm_train_hp={}'
                   ', itm_spw_chance={}, itm_obstacle_power={} WHERE id_num={}'
                   .format(table_effect, itm_atk, itm_timer, itm_max_pause, itm_min_pause
                           , itm_collider_size, itm_max_speed, itm_accel
                           , itm_boost_time, itm_boost_spd, itm_fever_gauge
                           , itm_fever_time, itm_fever_bonus, itm_train_hp
                           , itm_spw_chance, itm_obstacle_power, item_num))
    # names and ranks, etc.
    cursor.execute('UPDATE {} SET item_name = "{}"'
                   ', item_rank = {}, item_desc = "{}" WHERE id_num = {}'
                   .format(table, item_name, item_rank, item_desc, item_num))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_item_list', item_type=item_type, page_num=page_num))


# 아이템 신규등록창. 여기서 등록 진행하는거 아님.
@app.route('/item_add/')
def item_add():
    # 여기서 필요한거? 딱히 없는듯......;;
    # 목록에서 추가되는거 설정유지 해야하나?
    # 뒤로 돌아가는거 대비?

    conn = mysql.connect()
    cursor = conn.cursor()

    # 아이템 목록 설명부분을 넣어야함.
    # 아이템 효과는 시즌템이나 아니나 무조건 동일함.
    # 고로 어떤걸로 하던 한쪽만 가져와도 추방함.

    # 템 항목 설명
    cursor.execute("show FULL COLUMNS from items")

    item_info_columns = cursor.fetchall()
    print('item_info_columns: {}'.format(item_info_columns))

    # 템 능력치별 항목 설명ㅊ
    cursor.execute("show FULL COLUMNS from items_effect")
    item_effect_columns = cursor.fetchall()
    item_effect_columns_len = len(item_effect_columns)

    # 다 끝내면 연결 바로바로 종료시킨다.
    cursor.close()
    conn.close()

    return render_template('admin_item_info.html'
                           , item_edit=0, item_info_columns=item_info_columns
                           , item_effect_columns_len=item_effect_columns_len
                           , item_effect_columns=item_effect_columns)


# 아이템 신규등록.
@app.route('/item_adding/', methods=['POST', 'GET'])
def item_adding():

    # 통상 여기서
    print('????????')
    # 포스트 방식으로 name 태그 붙은 인풋들. 다 잘 받아지긴 함.
    res = request.form

    # 여기서 값을 가져올 시
    # request.form.getlist('항목')[0]
    # 위 처럼 쓴다.
    # 없으면 아예 오류가 떠버림.

    # phase 1. 값을 받아온다.
    # 그리고 이건 sql 테이블명을 직접 뜯어오는 거기 때문에
    # 테이블을 수정하면 이거 꼭!! 바꿔야 한다.

    print(res)

    print('getting requests')

    # try:

    # 아이템 소개 부분.
    item_name = request.form.getlist('item_name')[0]
    item_desc = request.form.getlist('item_desc')[0]
    item_rank = request.form.getlist('item_rank')[0]

    # effects 부분
    itm_atk = request.form.getlist('itm_atk')[0]
    itm_timer = request.form.getlist('itm_timer')[0]
    itm_max_pause = request.form.getlist('itm_max_pause')[0]
    itm_min_pause = request.form.getlist('itm_min_pause')[0]
    itm_collider_size = request.form.getlist('itm_collider_size')[0]
    itm_max_speed = request.form.getlist('itm_max_speed')[0]
    itm_accel = request.form.getlist('itm_accel')[0]
    itm_boost_time = request.form.getlist('itm_boost_time')[0]
    itm_boost_spd = request.form.getlist('itm_boost_spd')[0]
    itm_fever_gauge = request.form.getlist('itm_fever_gauge')[0]
    itm_fever_time = request.form.getlist('itm_fever_time')[0]
    itm_fever_bonus = request.form.getlist('itm_fever_bonus')[0]
    itm_train_hp = request.form.getlist('itm_train_hp')[0]
    itm_spw_chance = request.form.getlist('itm_spw_chance')[0]
    itm_obstacle_power = request.form.getlist('itm_obstacle_power')[0]

    # # 여기에 걸리면 뭔가 기입이 빠졌다는거. 보통 빠질리가 없음.
    # except IndexError as a:
    #     print(a)

    print('checking types...')
    # phase 2. 개인|크루|시즌 템 확인여부
    item_type = int(request.form.getlist('is_item_type')[0])
    print("item_type: {}".format(item_type))
    print('connecting to sql...')
    # 이 시점부터 서버 연결.
    conn = mysql.connect()
    cursor = conn.cursor()

    # phase 3. 유료템 여부 확인. 다만 개인템만 유료템일 가능성이 있음
    # 아이템타입이 0이면 개인템임
    # phase 4병행: 템의 종류에 따라 필요한 테이블을 찾는다.
    table_name = None
    effect_table_name = None
    item_iap = 0
    if item_type == 0:
        print('0')
        # iap 가 존재하는가? 존재하면 유료
        if request.form.getlist('iap'):
            item_iap = 1
        table_name = 'items'
        effect_table_name = 'items_effect'
    # 1 == season_item
    elif item_type == 1:
        print(1)
        table_name = 'season_item'
        effect_table_name = 'season_item_effect'
    # 2 == crew_item
    elif item_type == 2:
        print(2)
        table_name = 'crew_item'
        effect_table_name = 'crew_item_effect'

    print('grabbing table number, table_name == {}'.format(table_name))
    # phase 5. 테이블의 마지막 번호 추출한 후 이미지 저장한다.
    # id_num 맨 끝번호 추출
    cursor.execute('SELECT id_num from {} ORDER BY id_num DESC LIMIT 1'.format(table_name))
    id_res = cursor.fetchone()
    if id_res:
        # 'items 12' 같은 식...
        id_num = table_name + " " + str(int(id_res[0]) + 1)
    else:
        id_num = table_name + " 1"

    print('saving file')
    # 이게 파일임. bool 적용이 되니 그걸로 판단한다.
    img = request.files['image']

    # try:
    #     img = request.files['image']
    # # 여기 걸린다는건 업로드한 사진이 없다는거임. 여기서 걸리면 이상한거임!!!
    # except Exception as e:
    #     img = False
    # # print(bool(img))

    # 이거 기능: 파일명을 더 안정적인 버전으로 변환.
    file_name = secure_filename(id_num)
    print('file_name: {}'.format(file_name))
    print(img)
    img.save(os.path.join(app.config['UPLOAD_FOLDER']+'/pic/items'
                          , file_name + '.{}'.format(img.filename.split('.')[-1])))

    print('inserting. FINALLY.')
    # phase 6. 본격적으로 테이블에 인서트.
    cursor.execute('INSERT INTO {}'
                   '(item_name, item_desc, item_image, item_rank) '
                   'VALUES ("{}", "{}", "{}", "{}")'
                   .format(table_name, item_name, item_desc, file_name, item_rank))
    # 인서트할때 등록된 item_name
    cursor.execute('SELECT LAST_INSERT_ID()')
    current_id = cursor.fetchone()[0]

    # 개인템인 경우 유료템인지 확인한다. 유료면 처리!
    if item_iap == 1:
        print('IAP!!')
        cursor.execute('UPDATE items SET item_iap="{}" WHERE id_num="{}"'
                       .format(item_iap, current_id))

    # items_effect 인서트
    cursor.execute('INSERT INTO {}'
                   '(id_num, itm_atk, itm_timer, itm_max_pause, itm_min_pause, '
                   'itm_collider_size, itm_max_speed, itm_accel, itm_boost_time, '
                   'itm_boost_spd, itm_fever_gauge, itm_fever_time, itm_fever_bonus, '
                   'itm_train_hp, itm_spw_chance, itm_obstacle_power) '
                   'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", '
                   '"{}", "{}", "{}", "{}","{}", "{}", "{}", "{}")'
                   .format(effect_table_name, current_id, itm_atk, itm_timer, itm_max_pause, itm_min_pause,
                           itm_collider_size, itm_max_speed, itm_accel, itm_boost_time,
                           itm_boost_spd, itm_fever_gauge, itm_fever_time, itm_fever_bonus,
                           itm_train_hp, itm_spw_chance, itm_obstacle_power))

    conn.commit()
    cursor.close()
    conn.close()
    print('all finished')

    return 'done'

# 아이템 목록으로 리다렉트 시켜줌.
def redirect_to_item_list():
    return


# 아이템 목록·효과를 JSON 형태로 싹 다 보낸다.
@app.route('/tot_item_list/')
def total_item_list():
    # connect to the sql server
    conn = mysql.connect()
    cursor = conn.cursor()

    # 안에 들어가야 하는 값들.
    json_dic = {}

    # 모든 템 관련 머시기들을 빼와야 하기 때문.
    table_list = ['items', 'crew_item', 'season_item']
    dic_total = {}
    for tl in table_list:
        cursor.execute('SELECT * FROM {}'.format(tl))
        # 테이블 칼럼명
        # table_desc = cursor.description
        # 셀렉트문 결과값
        table_val = cursor.fetchall()

        # print(table_desc)
        print(table_val)

        dic_item = {tl: []}

        for i in range(len(table_val)):
            _table = []
            # 낱개
            for j in range(len(table_val[i])):
                print('table_val[i][j]', table_val[i][j])
                _table.append(table_val[i][j])

            dic_item[tl].append(_table)

        dic_total.update(dic_item)

    print(dic_total)

    # print(json.dumps(dic_total, ensure_ascii=False))

    cursor.close()
    conn.close()

    return json.dumps(dic_total, ensure_ascii=False)
