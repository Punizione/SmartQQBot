# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

import requests
import six
from smart_qq_bot.logger import logger
from smart_qq_bot.signals import on_group_message
from bs4 import BeautifulSoup

# 类型
SHIP_TYPE_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-of-type(3) > td:nth-of-type(2)"

#星级
SHIP_LEVEL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-of-type(3) > td:nth-of-type(4)"

#建造时间
SHIP_BUILDTIME_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-of-type(4) > td:nth-of-type(4)"

#普通掉落点
SHIP_DROP_NORMAL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-of-type(5) > td:nth-of-type(2)"

#特殊掉落点
SHIP_DROP_SPECIAL_SELECTOR = "table.wikitable.sv-general > tbody > tr:nth-of-type(6) > td:nth-of-type(2)"

#耐久
SHIP_ATTR_DURABLE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(4) > td:nth-of-type(2)"

#炮击
SHIP_ATTR_CANNONRY_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(5) > td:nth-of-type(2)"

#防空
SHIP_ATTR_AIR_DEFENSE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(6) > td:nth-of-type(2)"

#反潜
SHIP_ATTR_ANTISUBMARINE_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(7) > td:nth-of-type(2)"

#装甲
SHIP_ATTR_AMMR_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(4) > td:nth-of-type(4)"

#装填
SHIP_ATTR_RELOAD_SELECTOR = " table.wikitable.sv-performance > tbody > tr:nth-of-type(4) > td:nth-of-type(6)"

#雷击
SHIP_ATTR_LIGHTNING_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(5) > td:nth-of-type(4)"

#机动
SHIP_ATTR_MOTOR_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(5) > td:nth-of-type(6)"

#航空
SHIP_ATTR_AVIATION_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(6) > td:nth-of-type(4)"

#油耗
SHIP_ATTR_OIL_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(6) > td:nth-of-type(6)"

#航速
SHIP_ATTR_SPEED_SELECTOR = "table.wikitable.sv-performance > tbody > tr:nth-of-type(8) > td:nth-of-type(2)"

#推荐PVE配装
SHIP_EQUIPMENT_SELECTOR = "div.pverecommend1 .REt > span > a:nth-of-type(2)"

# 别称/花名
nickname_dict = {
	"克爹": "克利夫兰",
	"爹": "克利夫兰",
	"三叔": "蒙彼利埃",
	"二叔": "哥伦比亚",
	"金坷垃": "圣地亚哥",
	"彩坷垃": "圣地亚哥",
	"圣爹": "圣地亚哥",
	"小姨子": "萨拉托加"
}
@on_group_message
def ship(msg, bot):
	match1 = re.match(
		six.text_type('^(船|老婆|舰娘) (.*)'),
		msg.content
	)
	# match2 = re.match(
	# 	six.text_type("^(=)")
	# )
	if match1:
		logger.info("RUNTIMELOG 查询舰娘...")
		command = match1.group(1)
		ship = match1.group(2)
		ship = nickname_dict.get(ship, ship)
		logger.info("RUNTIMELOG 查询舰娘语句: "+msg.content)
		if command == six.text_type("船") or command == six.text_type("老婆") or command == six.text_type("舰娘"):
			str_data = ""
			str_data = exctrace_ship(ship)
			bot.reply_msg(msg, str_data)


@on_group_message
def picture_stream(msg, bot):
	match1 = re.match(
		six.text_type("^(装备|装备一图流)\s?(井号|#)?"),
		msg.content
	)
	match2 = re.match(
		six.text_type("^(天梯|舰娘排行)\s?(兔老师)?"),
		msg.content
	)





def exctrace_ship(ship=None):
	url = "http://wiki.joyme.com/blhx/{ship}".format(
		ship=ship
	)
	reply_str = "类型:{ship_type}"+ \
		"稀有度:{ship_level}"+ \
		"建造时间:{ship_buildtime}"+ \
		"普通掉落:{ship_drop_normal}"+ \
		"特殊掉落:{ship_drop_special}"+ \
		"耐久:{ship_attr_durable}"+ \
		"炮击:{ship_attr_cannonry}"+ \
		"防空:{ship_attr_air_defense}"+ \
		"反潜:{ship_attr_antisubmarine}"+ \
		"装甲:{ship_attr_ammr}"+ \
		"装填:{ship_attr_reload}"+ \
		"雷击:{ship_attr_lighting}"+ \
		"机动:{ship_attr_motor}"+ \
		"航空:{ship_attr_aviation}"+ \
		"油耗:{ship_attr_oil}"+ \
		"航速:{ship_attr_speed}"+ \
		"配装:{ship_equip}"

	try:
		response = requests.request("GET", url)
		soup = BeautifulSoup(response.text, "html5lib")
	except Exception as ex:
		logger.error(ex)
		str_data = "请求失败 :("
		return str_data
	match = re.match(
		six.text_type("本页面目前没有内容"),
		response.text
	)
	if match:
		return "emmm这可能是颗卫星 :("
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
	ship_attr_reload = extract_first_match(SHIP_ATTR_RELOAD_SELECTOR, soup)
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
		ship_attr_reload=ship_attr_reload,
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
			if not attr:
				for element in match_elements:
					str_list.append(element.get_text())
			else:
				for element in match_elements:
					str_list.append(element[attr])
			return splitor.join(str_list)
	return ''