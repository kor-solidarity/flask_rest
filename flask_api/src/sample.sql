-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.1.22-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- lifgames_railroad 데이터베이스 구조 내보내기
DROP DATABASE IF EXISTS `lifgames_railroad`;
CREATE DATABASE IF NOT EXISTS `lifgames_railroad` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
USE `lifgames_railroad`;

-- 테이블 lifgames_railroad.crew 구조 내보내기
DROP TABLE IF EXISTS `crew`;
CREATE TABLE IF NOT EXISTS `crew` (
  `crew_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '기초적인 관리번호',
  `crew_name` int(11) NOT NULL COMMENT '크루 이름(번호)...',
  `crew_desc` int(11) NOT NULL COMMENT '해당 클랜의 설명',
  `crew_boundary` float NOT NULL DEFAULT '0' COMMENT '시즌별에 필요한건데... 클랜간의 영역 점유율. 무조건 시즌별 클랜들 이 레이트 값이 100에 맞춰져야 한다. ',
  `crew_exist` int(11) NOT NULL DEFAULT '1' COMMENT '(현 운영중인 시즌에)존재하는 크루인가? 0이면 아님.',
  `crew_name_txt` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'nomo de crew. 클라이언트로 굳이 보내진 않지만 이쪽 자료를 위해.',
  PRIMARY KEY (`crew_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='클랜같은거. NPC 콥.\r\n세부적인 내용이 여기에서 저장되는 일은 없다. 모두 번호로 분류되며 클라이언트 내에서 번호에 맞춰서 불려진다. \r\n*추가사항: 아에템?';

-- 테이블 데이터 lifgames_railroad.crew:~2 rows (대략적) 내보내기
DELETE FROM `crew`;
/*!40000 ALTER TABLE `crew` DISABLE KEYS */;
INSERT INTO `crew` (`crew_id`, `crew_name`, `crew_desc`, `crew_boundary`, `crew_exist`, `crew_name_txt`) VALUES
	(1, 0, 1, 33.3, 1, ''),
	(3, 22223, 32, 222, 1, '');
/*!40000 ALTER TABLE `crew` ENABLE KEYS */;

-- 테이블 lifgames_railroad.deal_rec 구조 내보내기
DROP TABLE IF EXISTS `deal_rec`;
CREATE TABLE IF NOT EXISTS `deal_rec` (
  `deal_num` int(11) NOT NULL AUTO_INCREMENT COMMENT '거래순번',
  `deal_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '거래시각',
  `user_num` int(11) NOT NULL COMMENT '플레이어(유저 id)',
  `열 4` int(11) NOT NULL COMMENT '이하 추후 추가.',
  `열 5` int(11) NOT NULL,
  `열 6` int(11) NOT NULL,
  `열 7` int(11) NOT NULL,
  PRIMARY KEY (`deal_num`),
  KEY `FK_deal_rec__users` (`user_num`),
  CONSTRAINT `FK_deal_rec__users` FOREIGN KEY (`user_num`) REFERENCES `_users` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='모든 거래내역';

-- 테이블 데이터 lifgames_railroad.deal_rec:~0 rows (대략적) 내보내기
DELETE FROM `deal_rec`;
/*!40000 ALTER TABLE `deal_rec` DISABLE KEYS */;
/*!40000 ALTER TABLE `deal_rec` ENABLE KEYS */;

-- 테이블 lifgames_railroad.items 구조 내보내기
DROP TABLE IF EXISTS `items`;
CREATE TABLE IF NOT EXISTS `items` (
  `id_num` int(11) NOT NULL AUTO_INCREMENT COMMENT 'numbro de item-o. Ĉu mi devas klarigi ĉi tio?',
  `item_nomo` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '이름',
  `item_klarigo` varchar(500) COLLATE utf8_bin NOT NULL COMMENT '설명',
  `item_image` varchar(50) COLLATE utf8_bin NOT NULL COMMENT 'image name',
  `item_iap` int(11) NOT NULL DEFAULT '0' COMMENT '유료템인가? 0이면 아님',
  `item_rank` int(11) NOT NULL DEFAULT '0' COMMENT '랭크제한.',
  PRIMARY KEY (`id_num`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='listo de iuj en la ludo.\r\nĉiuj itemoj ne bezonas havi tekstojn en la DB.\r\n모든 아이템은 id를 같은대로 공유한다. 관리 편의성 용도.';

-- 테이블 데이터 lifgames_railroad.items:~2 rows (대략적) 내보내기
DELETE FROM `items`;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` (`id_num`, `item_nomo`, `item_klarigo`, `item_image`, `item_iap`, `item_rank`) VALUES
	(1, 'goddamnit', '템 설명서', '1.png', 0, 0),
	(2, 'second time', '두번째 템임', 'aaaa', 0, 0);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;

-- 테이블 lifgames_railroad.items_effect 구조 내보내기
DROP TABLE IF EXISTS `items_effect`;
CREATE TABLE IF NOT EXISTS `items_effect` (
  `id_num` int(11) NOT NULL COMMENT '아이템명. items 테이블 번호와 호환되야함. ',
  `itm_atk` int(11) NOT NULL COMMENT '공격력 효과',
  `itm_timer` int(11) NOT NULL COMMENT '제한시간 증감효과',
  `itm_max_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최대값. (상세수치는 일정 범위 안에서 랜덤.)',
  `itm_min_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최소값.',
  `itm_collider_size` int(11) NOT NULL COMMENT '판정 구간 넓이 증감',
  `itm_max_speed` int(11) NOT NULL COMMENT '최고 속도 증감',
  `itm_accel` int(11) NOT NULL COMMENT '가속도 증감',
  `itm_boost_time` int(11) NOT NULL COMMENT '부스트 유지시간 증감',
  `itm_boost_spd` int(11) NOT NULL COMMENT '부스트 속도 증감',
  `itm_fever_gauge` int(11) NOT NULL COMMENT '피버 게이지 충전량 증감',
  `itm_fever_time` int(11) NOT NULL COMMENT '피버 타임 유지시간 증가/감소',
  `itm_fever_bonus` int(11) NOT NULL COMMENT '피버 타임시 점수 보너스 증가/감소',
  `itm_train_hp` int(11) NOT NULL COMMENT '열차 체력 수치 증감',
  `itm_spw_chance` int(11) NOT NULL COMMENT '상위 아이템 등장 확률',
  `itm_obstacle_power` int(11) NOT NULL COMMENT '파괴해야하는 장애물에 대한 공격 횟수 ( ex: 1회 클릭 당 공격횟수에 영향. 공격횟수가 2일때 더블어택, 3일때 트리플어택 )',
  PRIMARY KEY (`id_num`),
  CONSTRAINT `FK__items` FOREIGN KEY (`id_num`) REFERENCES `items` (`id_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='템별 효과.\r\n단순 증감효과인건 굳이 + - 따로 두지 않았음. 필요시 쪼개겠음.\r\n';

-- 테이블 데이터 lifgames_railroad.items_effect:~1 rows (대략적) 내보내기
DELETE FROM `items_effect`;
/*!40000 ALTER TABLE `items_effect` DISABLE KEYS */;
INSERT INTO `items_effect` (`id_num`, `itm_atk`, `itm_timer`, `itm_max_pause`, `itm_min_pause`, `itm_collider_size`, `itm_max_speed`, `itm_accel`, `itm_boost_time`, `itm_boost_spd`, `itm_fever_gauge`, `itm_fever_time`, `itm_fever_bonus`, `itm_train_hp`, `itm_spw_chance`, `itm_obstacle_power`) VALUES
	(1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15);
/*!40000 ALTER TABLE `items_effect` ENABLE KEYS */;

-- 테이블 lifgames_railroad.items_iap 구조 내보내기
DROP TABLE IF EXISTS `items_iap`;
CREATE TABLE IF NOT EXISTS `items_iap` (
  `id_num` int(11) NOT NULL AUTO_INCREMENT COMMENT '템번호',
  `item_nomo` int(11) NOT NULL COMMENT '이름',
  `item_klarigo` int(11) NOT NULL COMMENT '설명',
  `item_image` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '사진이름',
  PRIMARY KEY (`id_num`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='유료템(in_app_purchase). 로그관리 용이성을 위해 분류.\r\nNULLIFIED';

-- 테이블 데이터 lifgames_railroad.items_iap:~1 rows (대략적) 내보내기
DELETE FROM `items_iap`;
/*!40000 ALTER TABLE `items_iap` DISABLE KEYS */;
INSERT INTO `items_iap` (`id_num`, `item_nomo`, `item_klarigo`, `item_image`) VALUES
	(101, 5, 222, 'aaa');
/*!40000 ALTER TABLE `items_iap` ENABLE KEYS */;

-- 테이블 lifgames_railroad.items_iap_effect 구조 내보내기
DROP TABLE IF EXISTS `items_iap_effect`;
CREATE TABLE IF NOT EXISTS `items_iap_effect` (
  `id_num` int(11) NOT NULL COMMENT '기본 관리번호. items_iap의 번호와 맞아야한다. ',
  `iap_atk` int(11) NOT NULL COMMENT '공격력 효과',
  `iap_timer` int(11) NOT NULL COMMENT '제한시간 증감효과',
  `iap_max_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최대값. (상세수치는 일정 범위 안에서 랜덤.)',
  `iap_min_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최소값.',
  `iap_collider_size` int(11) NOT NULL COMMENT '판정 구간 넓이 증감',
  `iap_max_speed` int(11) NOT NULL COMMENT '최고 속도 증감',
  `iap_accel` int(11) NOT NULL COMMENT '가속도 증감',
  `iap_boost_time` int(11) NOT NULL COMMENT '부스트 유지시간 증감',
  `iap_boost_spd` int(11) NOT NULL COMMENT '부스트 속도 증감',
  `iap_fever_gauge` int(11) NOT NULL COMMENT '피버 게이지 충전량 증감',
  `iap_fever_time` int(11) NOT NULL COMMENT '피버 타임 유지시간 증가/감소',
  `iap_fever_bonus` int(11) NOT NULL COMMENT '피버 타임시 점수 보너스 증가/감소',
  `iap_train_hp` int(11) NOT NULL COMMENT '열차 체력 수치 증감',
  `iap_spw_chance` int(11) NOT NULL COMMENT '상위 아이템 등장 확률',
  `iap_obstacle_power` int(11) NOT NULL COMMENT '파괴해야하는 장애물에 대한 공격 횟수 ( ex: 1회 클릭 당 공격횟수에 영향. 공격횟수가 2일때 더블어택, 3일때 트리플어택 )',
  PRIMARY KEY (`id_num`),
  CONSTRAINT `FK__items_iap` FOREIGN KEY (`id_num`) REFERENCES `items_iap` (`id_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='캐시템 효과. 기본적으로 일반템과 수치 자체는 전부 동일하다.\r\nNULLIFIED';

-- 테이블 데이터 lifgames_railroad.items_iap_effect:~0 rows (대략적) 내보내기
DELETE FROM `items_iap_effect`;
/*!40000 ALTER TABLE `items_iap_effect` DISABLE KEYS */;
/*!40000 ALTER TABLE `items_iap_effect` ENABLE KEYS */;

-- 테이블 lifgames_railroad.season 구조 내보내기
DROP TABLE IF EXISTS `season`;
CREATE TABLE IF NOT EXISTS `season` (
  `season_num` int(11) NOT NULL AUTO_INCREMENT COMMENT '관리번호',
  `season_descr` varchar(500) COLLATE utf8_bin NOT NULL COMMENT '시즌 이야기',
  `season_name` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '시즌 명칭',
  `start_date` datetime NOT NULL COMMENT '시작일자.',
  `end_date` datetime NOT NULL COMMENT '시즌 종료일자. ',
  `crew_num` int(11) NOT NULL DEFAULT '0' COMMENT '쓸 수 있는 크루.',
  PRIMARY KEY (`season_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='각 시즌별 기록기재 용도? 우선은 이래 놓기만.\r\n이 항목은 UI상에서 띄울 자료만 넣는다. ';

-- 테이블 데이터 lifgames_railroad.season:~0 rows (대략적) 내보내기
DELETE FROM `season`;
/*!40000 ALTER TABLE `season` DISABLE KEYS */;
/*!40000 ALTER TABLE `season` ENABLE KEYS */;

-- 테이블 lifgames_railroad.season_item 구조 내보내기
DROP TABLE IF EXISTS `season_item`;
CREATE TABLE IF NOT EXISTS `season_item` (
  `season_item_num` int(11) NOT NULL AUTO_INCREMENT,
  `season_item_name` int(11) NOT NULL COMMENT '이름',
  `season_item_descr` int(11) NOT NULL COMMENT '설명',
  `season_item_image` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '이미지이름',
  `season_item_crew` int(11) NOT NULL COMMENT '소속된 크루 번호. 한 템은 무조건 한 크루에게만 주어진다',
  PRIMARY KEY (`season_item_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='시즌아이템. 크루전용.';

-- 테이블 데이터 lifgames_railroad.season_item:~0 rows (대략적) 내보내기
DELETE FROM `season_item`;
/*!40000 ALTER TABLE `season_item` DISABLE KEYS */;
/*!40000 ALTER TABLE `season_item` ENABLE KEYS */;

-- 테이블 lifgames_railroad.season_item_effect 구조 내보내기
DROP TABLE IF EXISTS `season_item_effect`;
CREATE TABLE IF NOT EXISTS `season_item_effect` (
  `season_item_num` int(11) NOT NULL,
  `itm_atk` int(11) NOT NULL COMMENT '공격력 효과',
  `itm_timer` int(11) NOT NULL COMMENT '제한시간 증감효과',
  `itm_max_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최대값. (상세수치는 일정 범위 안에서 랜덤.)',
  `itm_min_pause` int(11) NOT NULL COMMENT '일정시간동안 제한시간 정지. 랜덤 범위 최소값.',
  `itm_collider_size` int(11) NOT NULL COMMENT '판정 구간 넓이 증감',
  `itm_max_speed` int(11) NOT NULL COMMENT '최고 속도 증감',
  `itm_accel` int(11) NOT NULL COMMENT '가속도 증감',
  `itm_boost_time` int(11) NOT NULL COMMENT '부스트 유지시간 증감',
  `itm_boost_spd` int(11) NOT NULL COMMENT '부스트 속도 증감',
  `itm_fever_gauge` int(11) NOT NULL COMMENT '피버 게이지 충전량 증감',
  `itm_fever_time` int(11) NOT NULL COMMENT '피버 타임 유지시간 증가/감소',
  `itm_fever_bonus` int(11) NOT NULL COMMENT '피버 타임시 점수 보너스 증가/감소',
  `itm_train_hp` int(11) NOT NULL COMMENT '열차 체력 수치 증감',
  `itm_spw_chance` int(11) NOT NULL COMMENT '상위 아이템 등장 확률',
  `itm_obstacle_power` int(11) NOT NULL COMMENT '파괴해야하는 장애물에 대한 공격 횟수 ( ex: 1회 클릭 당 공격횟수에 영향. 공격횟수가 2일때 더블어택, 3일때 트리플어택 )',
  PRIMARY KEY (`season_item_num`),
  CONSTRAINT `FK_season_item_effect_season_item` FOREIGN KEY (`season_item_num`) REFERENCES `season_item` (`season_item_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='시즌아이템 능력치';

-- 테이블 데이터 lifgames_railroad.season_item_effect:~0 rows (대략적) 내보내기
DELETE FROM `season_item_effect`;
/*!40000 ALTER TABLE `season_item_effect` DISABLE KEYS */;
/*!40000 ALTER TABLE `season_item_effect` ENABLE KEYS */;

-- 테이블 lifgames_railroad._best_record 구조 내보내기
DROP TABLE IF EXISTS `_best_record`;
CREATE TABLE IF NOT EXISTS `_best_record` (
  `player_num` int(11) NOT NULL COMMENT '플레이어 이름. ',
  `record_num` int(11) NOT NULL COMMENT '기록정보. 어차피 기록중에 가장 점수 잘나온거만 빼오는거니 여기에 굳이 별도의 자료가 필요하진 않음.',
  PRIMARY KEY (`player_num`),
  CONSTRAINT `FK__players_` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='각 플레이어별 최고기록 저장되는거. ';

-- 테이블 데이터 lifgames_railroad._best_record:~0 rows (대략적) 내보내기
DELETE FROM `_best_record`;
/*!40000 ALTER TABLE `_best_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `_best_record` ENABLE KEYS */;

-- 테이블 lifgames_railroad._blocked_player 구조 내보내기
DROP TABLE IF EXISTS `_blocked_player`;
CREATE TABLE IF NOT EXISTS `_blocked_player` (
  `user_num` int(11) NOT NULL COMMENT '차단시도하는 당사자',
  `blocked_num` int(11) NOT NULL COMMENT '차단대상',
  PRIMARY KEY (`user_num`,`blocked_num`),
  CONSTRAINT `FK__blokigxi_players` FOREIGN KEY (`user_num`) REFERENCES `_players` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='차단상대. 필요 없을듯. ';

-- 테이블 데이터 lifgames_railroad._blocked_player:~0 rows (대략적) 내보내기
DELETE FROM `_blocked_player`;
/*!40000 ALTER TABLE `_blocked_player` DISABLE KEYS */;
/*!40000 ALTER TABLE `_blocked_player` ENABLE KEYS */;

-- 테이블 lifgames_railroad._friends 구조 내보내기
DROP TABLE IF EXISTS `_friends`;
CREATE TABLE IF NOT EXISTS `_friends` (
  `player_unique_id` int(11) NOT NULL COMMENT '친구추가 당사자',
  `friend_unique_id` int(11) NOT NULL COMMENT '추가할 친구',
  `relation` int(11) NOT NULL COMMENT '세부내용 테이블코멘트',
  PRIMARY KEY (`player_unique_id`,`friend_unique_id`),
  KEY `FK___players_2` (`friend_unique_id`,`player_unique_id`),
  CONSTRAINT `FK___players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`),
  CONSTRAINT `FK___players_2` FOREIGN KEY (`friend_unique_id`) REFERENCES `_players` (`player_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='친구추가. \r\nrelation 테이블 구분:\r\n0 - 친구추가 승인대기(friend_unique_id가 승인해야함)\r\n1 - 친구\r\n2 - 차단상태. player_unique_id가 friend_unique_id를 차단한거.\r\n';

-- 테이블 데이터 lifgames_railroad._friends:~0 rows (대략적) 내보내기
DELETE FROM `_friends`;
/*!40000 ALTER TABLE `_friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `_friends` ENABLE KEYS */;

-- 테이블 lifgames_railroad._friends_copy 구조 내보내기
DROP TABLE IF EXISTS `_friends_copy`;
CREATE TABLE IF NOT EXISTS `_friends_copy` (
  `player_unique_id` int(11) NOT NULL COMMENT '친구추가 당사자',
  `friend_unique_id` int(11) NOT NULL COMMENT '추가할 친구',
  `friend_accepted` int(11) DEFAULT '0' COMMENT '0이면 추가 확인 띄워야함.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT COMMENT='친구추가. \r\nrelation 테이블 구분:\r\n0 - 친구추가 승인대기(friend_unique_id가 승인해야함)\r\n1 - 친구\r\n2 - 차단상태. player\r\n';

-- 테이블 데이터 lifgames_railroad._friends_copy:~4 rows (대략적) 내보내기
DELETE FROM `_friends_copy`;
/*!40000 ALTER TABLE `_friends_copy` DISABLE KEYS */;
INSERT INTO `_friends_copy` (`player_unique_id`, `friend_unique_id`, `friend_accepted`) VALUES
	(1, 3, 1),
	(1, 2, 1),
	(2, 3, 0),
	(1, 4, 0);
/*!40000 ALTER TABLE `_friends_copy` ENABLE KEYS */;

-- 테이블 lifgames_railroad._pass 구조 내보내기
DROP TABLE IF EXISTS `_pass`;
CREATE TABLE IF NOT EXISTS `_pass` (
  `user_num` int(11) NOT NULL,
  `pwd` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`user_num`),
  CONSTRAINT `user_num` FOREIGN KEY (`user_num`) REFERENCES `_users` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='암호';

-- 테이블 데이터 lifgames_railroad._pass:~1 rows (대략적) 내보내기
DELETE FROM `_pass`;
/*!40000 ALTER TABLE `_pass` DISABLE KEYS */;
INSERT INTO `_pass` (`user_num`, `pwd`) VALUES
	(10, '$5$rounds=535000$diRlKQeywQVq7hSP$2L/S6nnKV3RFViiYnqYhg4d316nRkqsvWRXURG9UG06');
/*!40000 ALTER TABLE `_pass` ENABLE KEYS */;

-- 테이블 lifgames_railroad._players 구조 내보내기
DROP TABLE IF EXISTS `_players`;
CREATE TABLE IF NOT EXISTS `_players` (
  `player_num` int(11) NOT NULL AUTO_INCREMENT COMMENT '플레이어 관리용 고유번호. ',
  `player_unique_id` int(11) NOT NULL COMMENT '플레이어 식별번호? 개인적으로 왜필요한진 잘 모르겠음.',
  `user_num` int(11) NOT NULL COMMENT 'user_num과 동일. 고유 관리번호.',
  `affiliated_crew_id` int(11) NOT NULL COMMENT '소속된 크루 번호. crew 테이블의 crew_id',
  `player_nick` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '케릭명',
  `player_highscore` int(200) NOT NULL DEFAULT '0' COMMENT '플레이어의 최고점수(지도 통틀어서)',
  `reg_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`player_num`),
  UNIQUE KEY `player_nick` (`player_nick`),
  UNIQUE KEY `player_unique_id` (`player_unique_id`),
  KEY `FK_players_crew` (`affiliated_crew_id`),
  KEY `player_num` (`user_num`),
  CONSTRAINT `FK_players_crew` FOREIGN KEY (`affiliated_crew_id`) REFERENCES `crew` (`crew_id`),
  CONSTRAINT `player_num` FOREIGN KEY (`user_num`) REFERENCES `_users` (`user_num`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='플레이어들과 관련된 기본 사항. ';

-- 테이블 데이터 lifgames_railroad._players:~1 rows (대략적) 내보내기
DELETE FROM `_players`;
/*!40000 ALTER TABLE `_players` DISABLE KEYS */;
INSERT INTO `_players` (`player_num`, `player_unique_id`, `user_num`, `affiliated_crew_id`, `player_nick`, `player_highscore`, `reg_time`) VALUES
	(2, 277793, 10, 1, '알아서뭐하게', 0, '2017-12-04 17:35:44');
/*!40000 ALTER TABLE `_players` ENABLE KEYS */;

-- 테이블 lifgames_railroad._players_cash 구조 내보내기
DROP TABLE IF EXISTS `_players_cash`;
CREATE TABLE IF NOT EXISTS `_players_cash` (
  `player_unique_id` int(11) NOT NULL,
  `player_cash_1` int(11) NOT NULL DEFAULT '0' COMMENT '재화. 임의로 이름둚. 아직 확정되지 않음. ',
  `player_cash_2` int(11) NOT NULL DEFAULT '0',
  `player_cash_3` int(11) NOT NULL DEFAULT '0',
  `player_cash_4` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`player_unique_id`),
  CONSTRAINT `FK__players_cash__players` FOREIGN KEY (`player_unique_id`) REFERENCES `_players` (`player_unique_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임 내 재화';

-- 테이블 데이터 lifgames_railroad._players_cash:~1 rows (대략적) 내보내기
DELETE FROM `_players_cash`;
/*!40000 ALTER TABLE `_players_cash` DISABLE KEYS */;
INSERT INTO `_players_cash` (`player_unique_id`, `player_cash_1`, `player_cash_2`, `player_cash_3`, `player_cash_4`) VALUES
	(277793, 11111, 222222, 3333, 4);
/*!40000 ALTER TABLE `_players_cash` ENABLE KEYS */;

-- 테이블 lifgames_railroad._player_challenge_list 구조 내보내기
DROP TABLE IF EXISTS `_player_challenge_list`;
CREATE TABLE IF NOT EXISTS `_player_challenge_list` (
  `player_num` int(11) NOT NULL COMMENT '플레이어 번호. players 테이블의 프라이머리키',
  `열 2` int(11) NOT NULL DEFAULT '0' COMMENT '각 목록 달성여부: 1이 달성',
  KEY `FK_challenge_list_players` (`player_num`),
  CONSTRAINT `FK_challenge_list_players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='도전과제 목록.\r\n내용물은 아직 들어가있지 않음.';

-- 테이블 데이터 lifgames_railroad._player_challenge_list:~0 rows (대략적) 내보내기
DELETE FROM `_player_challenge_list`;
/*!40000 ALTER TABLE `_player_challenge_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `_player_challenge_list` ENABLE KEYS */;

-- 테이블 lifgames_railroad._player_items 구조 내보내기
DROP TABLE IF EXISTS `_player_items`;
CREATE TABLE IF NOT EXISTS `_player_items` (
  `player_num` int(11) NOT NULL,
  `item_num` int(11) NOT NULL,
  `item_quantity` int(11) NOT NULL,
  KEY `item_num` (`item_num`),
  KEY `player_num` (`player_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='플레이어가 가지고 있는 아이템 목록.';

-- 테이블 데이터 lifgames_railroad._player_items:~2 rows (대략적) 내보내기
DELETE FROM `_player_items`;
/*!40000 ALTER TABLE `_player_items` DISABLE KEYS */;
INSERT INTO `_player_items` (`player_num`, `item_num`, `item_quantity`) VALUES
	(10, 1, 1),
	(10, 101, 2);
/*!40000 ALTER TABLE `_player_items` ENABLE KEYS */;

-- 테이블 lifgames_railroad._player_items_iap_locked 구조 내보내기
DROP TABLE IF EXISTS `_player_items_iap_locked`;
CREATE TABLE IF NOT EXISTS `_player_items_iap_locked` (
  `player_num` int(11) NOT NULL,
  `item_num` int(11) NOT NULL,
  `item_quantity` int(11) NOT NULL,
  PRIMARY KEY (`player_num`),
  CONSTRAINT `FK__player_items_iap_locked__players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='해금된 캐시템 목록. 이 목록에 없으면 해금이 안된거임.';

-- 테이블 데이터 lifgames_railroad._player_items_iap_locked:~0 rows (대략적) 내보내기
DELETE FROM `_player_items_iap_locked`;
/*!40000 ALTER TABLE `_player_items_iap_locked` DISABLE KEYS */;
/*!40000 ALTER TABLE `_player_items_iap_locked` ENABLE KEYS */;

-- 테이블 lifgames_railroad._player_items_locked 구조 내보내기
DROP TABLE IF EXISTS `_player_items_locked`;
CREATE TABLE IF NOT EXISTS `_player_items_locked` (
  `player_num` int(11) NOT NULL COMMENT '플레이어 번호',
  `unlocked_item_num` int(11) NOT NULL COMMENT '해금된 아이템 번호. 이 목록에 없으면 해금 안된거.',
  PRIMARY KEY (`player_num`),
  KEY `FK__player_items_locked_items` (`unlocked_item_num`),
  CONSTRAINT `FK__player_items_locked__players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_num`),
  CONSTRAINT `FK__player_items_locked_items` FOREIGN KEY (`unlocked_item_num`) REFERENCES `items` (`id_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='해금된 아이템 목록. 이 목록에 없으면 해금이 안된거임.';

-- 테이블 데이터 lifgames_railroad._player_items_locked:~0 rows (대략적) 내보내기
DELETE FROM `_player_items_locked`;
/*!40000 ALTER TABLE `_player_items_locked` DISABLE KEYS */;
/*!40000 ALTER TABLE `_player_items_locked` ENABLE KEYS */;

-- 테이블 lifgames_railroad._records 구조 내보내기
DROP TABLE IF EXISTS `_records`;
CREATE TABLE IF NOT EXISTS `_records` (
  `record_num` int(11) NOT NULL AUTO_INCREMENT,
  `player_num` int(11) NOT NULL,
  `map_info` longblob NOT NULL COMMENT '맵정보. 자료를 통째로 넣는걸 가정하고 넣음.',
  `victory` int(11) NOT NULL COMMENT 'if 1, win, elif 0, lose',
  `elapsed_time` float NOT NULL COMMENT 'elapsed time in seconds',
  `recorded_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '등록된 시간.',
  `item_used` text COLLATE utf8_bin NOT NULL COMMENT '해당 판에 쓰인 아이템 목록. JSON 형태로 저장해야 할듯?',
  PRIMARY KEY (`record_num`),
  KEY `player_num` (`player_num`),
  CONSTRAINT `FK__players` FOREIGN KEY (`player_num`) REFERENCES `_players` (`user_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='게임기록들. ';

-- 테이블 데이터 lifgames_railroad._records:~0 rows (대략적) 내보내기
DELETE FROM `_records`;
/*!40000 ALTER TABLE `_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `_records` ENABLE KEYS */;

-- 테이블 lifgames_railroad._users 구조 내보내기
DROP TABLE IF EXISTS `_users`;
CREATE TABLE IF NOT EXISTS `_users` (
  `user_num` int(11) NOT NULL AUTO_INCREMENT COMMENT '고유 관리번호',
  `user_id` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '아이디',
  `user_email` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '이메일주소',
  `user_bd` date DEFAULT NULL COMMENT '생년월일. 필요하긴 할라나?',
  `user_reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '회원가입시간.',
  `last_login` date DEFAULT NULL COMMENT '최종 로그인 일자',
  `pass` varchar(50) COLLATE utf8_bin DEFAULT NULL COMMENT '임시로 시험차 추가한거. 필요없음.',
  PRIMARY KEY (`user_num`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='기본정보. 계정아이디, 이메일, 별명, 등등. ';

-- 테이블 데이터 lifgames_railroad._users:~3 rows (대략적) 내보내기
DELETE FROM `_users`;
/*!40000 ALTER TABLE `_users` DISABLE KEYS */;
INSERT INTO `_users` (`user_num`, `user_id`, `user_email`, `user_bd`, `user_reg_date`, `last_login`, `pass`) VALUES
	(1, 'yolo', 'aa@aa.com', '2017-11-07', '2017-11-07 17:07:34', NULL, 'liveonce'),
	(2, 'haha', 'aa@aaa.com', NULL, '2017-11-16 13:18:13', NULL, NULL),
	(10, 'someoneyouknow', 'yy@aaaa.com', NULL, '2017-11-16 14:22:50', NULL, NULL);
/*!40000 ALTER TABLE `_users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
