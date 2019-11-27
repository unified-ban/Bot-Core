#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_message, h_sql, h_group
from Utils import logger, sql

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Update welcome message
'''
@permissions.is_admin('admin_setwelcome_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		welcome_text = update.message.text[12:]
		
		if welcome_text != "":
			'''
			The text of the welcome message has been passed
			save it in the database
			'''
			output = bot.send_message(chat_id, lang.welcome_set, parse_mode=ParseMode.HTML)
			db.update_groups('WelcomeText', welcome_text)
			db = sql.Database(update); db.insert_chatoperationslog("SetWelcome")
			return h_message.delete(output, context, 5)
		else:
			'''
			The text of the welcome message was not passed
			output an error message
			'''
			bot.send_message(chat_id, lang.welcome_help, parse_mode=ParseMode.HTML)
			return False
	except Exception as e:
		logger.exception(e)

@permissions.is_admin('admin_addwelcomebutton_init')
@message.delete_input
def addwelcomebutton(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot

		chat_id = update.message.chat_id
		text = update.message.text
		
		params = text.split(" ")
		
		if len(params) >= 3:
			if len(params) > 3:
				logger.log.info(params)
				tmp_params = []
				tmp_params = tmp_params+params
				del tmp_params[0]
				del tmp_params[-1]
				name = ""
				for t in tmp_params:
					name = name+t+" "
				name = name[:-1]
				link = params[-1]
			else:
				name = params[1]
				link = params[2]
			
			db = sql.Database(update);db.insert_buttons(name, link, "!welcome")
			output = bot.send_message(chat_id, lang.welcome_buttons_add % name)
			return h_message.delete(output, context, 5)
		else:
			return bot.send_message(chat_id, lang.welcome_buttons_format_error)
	except Exception as e:
		logger.exception(e)

@permissions.is_admin('admin_removewelcomebutton_init')
@message.delete_input
def removewelcomebutton(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		chat_id = update.message.chat_id
		text = update.message.text
		
		params = text[21:]
		
		if params != " ":
			name = params
			
			db = sql.Database(update);db.delete_buttons(name, "!welcome")
			output = bot.send_message(chat_id, lang.welcome_buttons_remove % name)
			return h_message.delete(output, context, 5)
		else:
			return bot.send_message(chat_id, lang.welcome_buttons_format_error)
	except Exception as e:
		logger.exception(e)

@permissions.is_admin('admin_welcomebuttons_init')
def welcomebuttons(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot

		db = sql.Database(update)
		chat_id = update.message.chat_id
		text = update.message.text
		buttons = db.get_buttons("!welcome")
		buttons_list = ""
		
		if len(buttons) > 0:
			for b in buttons:
				buttons_list = buttons_list + "<b>{name}</b> ({url})\n\n".format(
					name = b[0],
					url = b[1]
				)
		else:
			buttons_list = lang.welcome_buttons_empty
			
		return bot.send_message(chat_id, buttons_list, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
	except Exception as e:
		logger.exception(e)
