#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import Params
from telegram import InlineKeyboardButton, ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_scam, h_message, h_user, h_keyboard, h_group
from Utils import logger, sql
import time

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

def init(update, context, group, lang):
	try:
		bot = context.bot
		if group[21] == 1:
			db = sql.Database(update)
			
			message = update.message
			user = update.message.from_user
			
			if update.message.media_group_id is not None:
				return False
			
			check_flood = db.check_flood()
			
			if check_flood == 3:
				bot.restrict_chat_member(
					message.chat_id, 
					user.id,
					datetime.datetime.now() + datetime.timedelta(minutes=10)
				)
				
				buttons = []
				buttons.append(InlineKeyboardButton(lang.f_unlimit, callback_data='FloodUnlimit'))
				markup = h_keyboard.build(buttons, n_cols=2)

				bot.send_message(message.chat_id, lang.flood_block % user.id, reply_markup=markup)
				db = sql.Database(update); db.insert_blockedcontent("flood")
				time.sleep(4)
				return logger.report(update, context, lang.report_flood % (
						update.message.chat.title,
						'Flood',
						user.id
					)
				)
			else:
				db = sql.Database(update)
				db.insert_flood()
		else:
			return False
	except Exception as e:
		logger.exception(e)

'''
Update user limitations
'''
def update(update, context):
	try:
		bot = context.bot
		db = sql.Database(update)
		
		query = update.callback_query
		
		if query.data == 'FloodUnlimit':
			user_id = h_user.get_user_id(query.message.text)
			if bot.get_chat_member(query.message.chat_id, query.message.from_user.id).status in ["creator", "administrator"] or query.message.from_user.id in Params.operators.users:
				bot.restrict_chat_member(
					query.message.chat_id, 
					user_id, 
					can_send_messages=True, 
					can_send_media_messages=True, 
					can_send_other_messages=True, 
					can_add_web_page_previews=True
				)
				output = bot.edit_message_text(lang.flood_unlimited, query.message.chat_id, query.message.message_id)
				return h_message.delete(output, context, 5)
	except Exception as e:
		logger.exception(e)