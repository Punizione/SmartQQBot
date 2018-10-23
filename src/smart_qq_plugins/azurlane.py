import re

import requests
import six
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_group_message
from bs4 import BeautifulSoup

# 类型
SHIP_TYPE_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-child(3) > td:nth-child(2)"

#星级
SHIP_LEVEL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-child(3) > td:nth-child(4)"

#建造时间
SHIP_BUILDTIME_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-child(4) > td:nth-child(4)"

#普通掉落点
SHIP_DROP_NORMAL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-child(5) > td:nth-child(2)"

#特殊掉落点
SHIP_DROP_SPECIAL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-child(6) > td:nth-child(2)"

#耐久
SHIP_ATTR_DURABLE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(4) > td:nth-child(2)"

#炮击
SHIP_ATTR_CANNONRY_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(5) > td:nth-child(2)"

#防空
SHIP_ATTR_AIR_DEFENSE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(6) > td:nth-child(2)"

#反潜
SHIP_ATTR_ANTISUBMARINE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(7) > td:nth-child(2)"

#装甲
SHIP_ATTR_AMMR_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(4) > td:nth-child(4)"

#装填
SHIP_ATTR_RELOAD_SELECTOR = " table.wikitable.sv-performance > tbody > tr:nth-child(4) > td:nth-child(6)"

#雷击
SHIP_ATTR_LIGHTNING_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(5) > td:nth-child(4)"

#机动
SHIP_ATTR_MOTOR_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(5) > td:nth-child(6)"

#航空
SHIP_ATTR_AVIATION_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(6) > td:nth-child(4)"

#油耗
SHIP_ATTR_OIL_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(6) > td:nth-child(6)"

#航速
SHIP_ATTR_SPEED_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-child(8) > td:nth-child(2)"

#推荐PVE配装
SHIP_EQUIPMENT_SELECTOR = "div.pverecommend1 .REt > span > a~a"

@on_group_message
def ship(msg, bot):
	match1 = re.match(
		six.text_type('^(船|老婆|舰娘) (.*)'),
		msg.content
	)
	match2 = re.match(
		six.text_type("^()")
	)
	if match1:
		logger.info("RUNTIMELOG 查询舰娘...")
		command = match.group(1)
		ship = match.group(2)
		logger.info("RUNTIMELOG 查询舰娘语句: "+msg.content)
		if command == six.text_type("船") or command == six.text_type("老婆") or command == six.text_type("舰娘"):
			str_data = ""
			str_data = exctrace_ship(ship)
			bot.reply_msg(msg, str_data)


@on_group_message
def picture_stream(msg, bot):
	match1 = re.match(
		six.text_type("^(装备|装备一图流)\s?(井号|#)"),
		msg.content
	)
	match2 = re.match(
		six.text_type("^(天梯|舰娘排行)\s?(兔老师)"),
		msg.content
	)





def exctrace_ship(ship=None):
	url = "http://wiki.joyme.com/blhx/{ship}".format(
		ship=ship
	)
	reply_str = "类型:{ship_type}\n"+
		"稀有度:{ship_level}\n"+
		"建造时间:{ship_buildtime}\n"+
		"普通掉落:{ship_drop_normal}\n"+
		"特殊掉落:{ship_drop_special}\n"+
		"耐久:{ship_attr_durable}\n"+
		"炮击:{ship_attr_cannonry}\n"+
		"防空:{ship_attr_air_defense}\n"+
		"反潜:{ship_attr_antisubmarine}\n"+
		"装甲:{ship_attr_ammr}\n"+
		"装填:{ship_attr_reload}\n"+
		"雷击:{ship_attr_lighting}\n"+
		"机动:{ship_attr_motor}\n"+
		"航空:{ship_attr_aviation}\n"+
		"油耗:{ship_attr_oil}\n"+
		"航速:{ship_attr_speed}\n"+
		"配装:{ship_equip}\n"

	try:
		response = requests.request("GET", url)
		soup = BeautifulSoup(response.text, "html5lib")
	except Exception as ex:
		logger.error(ex)
		str_data = "请求失败 :("
		return str_data
	ship_type = extract_first_match(SHIP_TYPE_SELECTOR, soup)
	ship_level = extract_first_match(SHIP_LEVEL_SELECTOR, soup)
	ship_buildtime = extract_first_match(SHIP_BUILDTIME_SELECTOR, soup)
	ship_drop_normal = extract_first_match(SHIP_DROP_NORMAL_SELECTOR, soup)
	ship_drop_special = extract_first_match(SHIP_DROP_NORMAL_SELECTOR, soup)
	ship_attr_durable = extract_first_match(SHIP_ATTR_DURABLE_SELECTOR, soup)
	ship_attr_cannonry = extract_first_match(SHIP_ATTR_CANNONRY_SELECTOR, soup)
	ship_attr_air_defense = extract_first_match(SHIP_ATTR_AIR_DEFENSE_SELECTOR, soup)
	ship_attr_antisubmarine = extract_first_match(SHIP_ATTR_ANTISUBMARINE_SELECTOR, soup)
	ship_attr_ammr = extract_first_match(SHIP_ATTR_AMMR_SELECTOR, soup)
	ship_atrr_reload = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
	ship_attr_lighting = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
	ship_attr_motor = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
	ship_attr_aviation = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
	ship_attr_oil = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
	ship_attr_speed = extract_first_match(SHIP_ATTR_SPEED_SELECTOR, soup)
	ship_equip = extract_all_with_splitor(SHIP_EQUIPMENT_SELECTOR, soup)

	str_data = reply_str.format(
		ship_type=ship_type,
		ship_level=ship_level,
		ship_buildtime=ship_buildtime,
		ship_drop_normal=ship_drop_normal,
		ship_drop_special=ship_drop_special,
		ship_attr_durable=ship_attr_durable,
		ship_attr_cannonry=ship_attr_cannonry,
		ship_attr_air_defense=ship_attr_air_defense,
		ship_attr_antisubmarine=ship_attr_antisubmarine,
		ship_attr_ammr=ship_attr_ammr,
		ship_atrr_reload=ship_atrr_reload,
		ship_attr_lighting=ship_attr_lighting,
		ship_attr_motor=ship_attr_motor,
		ship_attr_aviation=ship_attr_aviation,
		ship_attr_oil=ship_attr_oil,
		ship_attr_speed=ship_attr_speed,
		ship_equip=ship_equip
	)
	return str_data







def extract_first_match(selector, soup, attr=None):
	if selector and soup:
		match_elements = soup.select(selector)
		if match_elements:
			if not attr:
				return match_elements[0].get_text()
			else:
				return match_elements[0][attr]
	return ''

def extract_all_with_splitor(selector, soup, splitor=",", attr=None):
	if selector and soup:
		str_list = list()
		match_elements = soup.select(selector)
		if match_elements:
			if attr:
				for element in match_elements:
					str_list.append(element.get_text())
			else:
				for element in match_elements:
					str_list.append(element[attr])
			return splitor.join(str_list)
	return ''