#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import InlineKeyboardButton, ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_keyboard, h_user
from Utils import logger, sql

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Add user to Blacklist
'''
@permissions.is_operator('operator_black_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		text = update.message.text
		
		if update.message.reply_to_message:
			'''
			Get User_ID from the quoted message
			'''
			user_id = update.message.reply_to_message.from_user.id
		else:
			'''
			Get User_ID inline
			'''
			user_id = text[7:]
			if user_id == "":
				return False
			
		'''
		Build the keyboard for motivation
		'''
		buttons = []
		buttons.append(InlineKeyboardButton('Spam', callback_data='BlackForSpam'))	
		buttons.append(InlineKeyboardButton('Scam', callback_data='BlackForScam'))	
		buttons.append(InlineKeyboardButton('Molestie', callback_data='BlackForHarassment'))	
		buttons.append(InlineKeyboardButton('Altro', callback_data='BlackForOther'))	
		markup = h_keyboard.build(buttons, n_cols=2)
		
		return bot.send_message(update.message.chat_id, lang.black_select_motivation % (
				update.message.from_user.id,
				user_id,
				h_user.get_user_name(update),
				user_id,
			), reply_markup=markup, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)

'''
Update motivation and add User_ID to the Blacklist
'''
def update(update, context):
	try:
		query = update.callback_query

		bot = context.bot

		db = sql.Database(query)
		
		if query.data.startswith("BlackFor"):
			chat_id = query.message.chat_id
			message = query.message
			operator_id = h_user.get_user_id(message.text)
			user_id = h_user.get_target_user_id(message.text)
			motivation = query.data[8:]
			
			if str(query.from_user.id) == str(operator_id):
				db.insert_blacklist(user_id, motivation)
				bot.edit_message_text(lang.black_done % (
					user_id,
					motivation
					), chat_id, query.message.message_id, parse_mode=ParseMode.HTML)
				try:
					bot.kick_chat_member(chat_id, user_id)
				except:
					pass
				return logger.report(query, context, lang.report_black % (
					operator_id,
					user_id,
					chat_id,
					motivation
				))
	except Exception as e:
		logger.exception(e)