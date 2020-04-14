#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import InlineKeyboardButton, ParseMode, ChatPermissions
from Utils.decorators import permissions, message
from telegram.ext.dispatcher import run_async
from Utils import logger, sql
from Utils.helpers import h_user, h_variables, h_keyboard, h_message
import datetime

def init(update, context, group, lang):
	try:
		bot = context.bot

		# ConfUserRTL
		if group[23] == 1 and update.message.new_chat_members:
			user = update.message.new_chat_members[0]
			if h_user.is_rtl(user):
				return bot.restrict_chat_member(
					update.message.chat_id,
					user.id,
					ChatPermissions(
						can_send_messages=False, 
						can_send_media_messages=False, 
						can_send_polls=False,
						can_send_other_messages=False, 
						can_add_web_page_previews=False,
						can_invite_users=False
					),
					until_date=datetime.datetime.now() + datetime.timedelta(years=1)
				)
		
		# ConfWelcome
		if group[16] == 1 and update.message.new_chat_members:
			user = update.message.new_chat_members[0]
			message = update.message
			message_id = message.message_id
			
			if user.id == Params.telegram.Bot.id:
				return False
			
			welcome_message = group[17]
			
			variables = [
				["{username}", h_user.get_user_name(update)],
				["{first_name}", user.first_name if user.first_name is not None else ""],
				["{last_name}", user.last_name if user.last_name is not None else ""],
				["{chat_name}", update.message.chat.title]
			]
			
			welcome_message = h_variables.define(welcome_message, variables) 
			
			db = sql.Database(update);buttons = db.get_buttons("!welcome")
			buttons_list = []
			
			if len(buttons) > 0 or group[22] == 1:
				if len(buttons) > 0:
					for b in buttons:
						buttons_list.append(InlineKeyboardButton(b[0], url=b[1]))
					
				if group[22] == 1:
					# captcha enabled
					bot.restrict_chat_member(
						message.chat_id,
						user.id,
						ChatPermissions(
							can_send_messages=False, 
							can_send_media_messages=False, 
							can_send_polls=False,
							can_send_other_messages=False, 
							can_add_web_page_previews=False,
							can_invite_users=False
						),
						until_date=datetime.datetime.now() + datetime.timedelta(days=256)
					)
					buttons_list.append(InlineKeyboardButton(lang.w_captcha, callback_data="Captcha"+str(user.id)))
					welcome_message = welcome_message + lang.welcome_captcha
				
				markup = h_keyboard.build(buttons_list, n_cols=2)
				for new in update.message.new_chat_members:
					bot.send_message(update.message.chat_id, welcome_message, reply_markup=markup, parse_mode=ParseMode.HTML)
			else:
				for new in update.message.new_chat_members:
					bot.send_message(update.message.chat_id, welcome_message, parse_mode=ParseMode.HTML)
			return True
		else:
			return False
	except Exception as e:
		logger.exception(e)

'''
Update captcha
'''
def update(update, context):
	try:
		bot = context.bot

		query = update.callback_query
		message = query.message
		
		if query.data.startswith('Captcha'):
			user_id = query.data[7:]
			if str(query.from_user.id) == user_id:
				bot.restrict_chat_member(
					message.chat_id,
					user_id,
					ChatPermissions(
						can_send_messages=True, 
						can_send_media_messages=True, 
						can_send_polls=True,
						can_send_other_messages=True, 
						can_add_web_page_previews=True,
						can_invite_users=True
					),
					until_date=datetime.datetime.now() + datetime.timedelta(seconds=30)
				)
				return h_message.delete(query, context)
	except Exception as e:
		logger.exception(e)