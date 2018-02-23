# 각종 반환값 모음.

# 정상실행됨
OK = 0

ERR_SAME_NICK = -1  # 중복별명
ERR_SAME_ID = -2  # 중복아이디
ERR_EMAIL_EXIST = -3  # 이메일 중복
ERR_PWD_INCORRECT = -4  # 암호틀림
ERR_ID_INCORRECT = -4  # 아이디가 틀림. 굳이 위와 따로 분류할 필요는 없을듯.
ERR_NO_CREW = -5  # 선택한 크루는 존재하지 않음.
TOO_LONG = -6  # 뭔진 모르겠지만 입력한게 너무 길다.

###############################
# 자료반환에 쓰일 각종 플레이어 칼럼명.
PLAYER_UNIQUE_ID = 'player_unique_id'
PLAYER_NICK = 'player_nick'
CREW_BOUNDARY = 'crew_boundary'
CREW_DESC = 'crew_desc'
CREW_ID = 'crew_id'
CREW_NAME = 'crew_name'
CREW_STATS = 'crew_stats'
FRIENDS = 'friends'
CASH = 'cash'