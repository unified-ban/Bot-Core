#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import InlineKeyboardButton, ParseMode, ChatPermissions
from Utils.decorators import permissions, message, chat
from Utils.helpers import h_chat, h_keyboard, h_user, h_group, h_sql
from Utils import logger, sql
from datetime import datetime

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Show bot settings menu for group
'''
@permissions.is_admin('admin_configure_init')
@chat.only_groups
def init(update, context, edit=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)
		
		bot = context.bot
		
		buttons = []
		chat_id = update.message.chat_id
		user_id = update.message.from_user.id
		db = sql.Database(update)
		group = db.get_groups()
		
		'''
		Prepare the configuration menu buttons for the first construction
		'''
		buttons.append(InlineKeyboardButton(lang.c_instructions, url='https://unifiedban.solutions/?p=faq#FAQ_configure_instructions'))
		buttons.append(InlineKeyboardButton(lang.c_dashboard, url='https://unifiedban.solutions/'))
		buttons.append(InlineKeyboardButton(lang.c_offensive % ('✅' if group[5] == 1 else '❌'), callback_data='ConfOffensive'))
		buttons.append(InlineKeyboardButton(lang.c_spam % ('✅' if group[12] == 1 else '❌'), callback_data='ConfSpam'))
		buttons.append(InlineKeyboardButton(lang.c_flood % ('✅' if group[21] == 1 else '❌'), callback_data='ConfFlood'))
		buttons.append(InlineKeyboardButton(lang.c_captcha % ('✅' if group[22] == 1 else '❌'), callback_data='ConfCaptcha'))
		buttons.append(InlineKeyboardButton(lang.c_nonwest % ('✅' if group[11] == 1 else '❌'), callback_data='ConfNonWest'))
		buttons.append(InlineKeyboardButton(lang.c_telegram_link % ('✅' if group[6] == 1 else '❌'), callback_data='ConfTelegram'))
		buttons.append(InlineKeyboardButton(lang.c_username % ('✅' if group[7] == 1 else '❌'), callback_data='ConfName'))
		buttons.append(InlineKeyboardButton(lang.c_scam % ('✅' if group[8] == 1 else '❌'), callback_data='ConfAntiscam'))
		buttons.append(InlineKeyboardButton(lang.c_blacklist % ('✅' if group[9] == 1 else '❌'), callback_data='ConfBlacklist'))
		buttons.append(InlineKeyboardButton(lang.c_welcome % ('✅' if group[16] == 1 else '❌'), callback_data='ConfWelcome'))
		buttons.append(InlineKeyboardButton(lang.c_user_rtl % ('✅' if group[23] == 1 else '❌'), callback_data='ConfUserRTL'))
		buttons.append(InlineKeyboardButton(lang.c_language % (group[18]), callback_data='ConfLang'))
		buttons.append(InlineKeyboardButton(lang.c_report_channel, callback_data='ConfReportChannel'))
		buttons.append(InlineKeyboardButton(lang.c_open_group if group[10] == 1 else lang.c_close_group, callback_data='ConfHammer0' if group[10] == 1 else 'ConfHammer1'))
		db = sql.Database(update)
		if db.check_permissions():
			buttons.append(InlineKeyboardButton(lang.c_sign, callback_data='Sign'))
		if h_chat.is_private(update) == False and h_chat.is_private_group(update) == False:
			buttons.append(InlineKeyboardButton(lang.c_call_operator, callback_data='CallOperator'))
		else:
			buttons.append(InlineKeyboardButton(lang.c_community_support, url='https://t.me/unifiedban_group'))
		buttons.append(InlineKeyboardButton(lang.c_faq, url='https://unifiedban.solutions/?p=faq'))
		buttons.append(InlineKeyboardButton(lang.c_news, url='https://t.me/unifiedban_news'))
		buttons.append(InlineKeyboardButton(lang.c_close, callback_data='CloseMenu'))
		
		markup = h_keyboard.build(buttons, n_cols=2)
		
		if edit == False:
			'''
			Build configuration menu buttons
			for the first time
			'''
			return bot.send_message(chat_id, lang.configure % user_id, reply_markup=markup, parse_mode=ParseMode.HTML)
		else:
			user_id = h_user.get_user_id(update.message.text)
			
		if edit == 'ConfLang':
			'''
			Rebuild configuration menu buttons
			for language selection
			'''
			lang_buttons = []
			lang_buttons.append(InlineKeyboardButton('it_IT', callback_data='SetLang_it_IT'))
			lang_buttons.append(InlineKeyboardButton('en_US', callback_data='SetLang_en_US'))
			lang_buttons.append(InlineKeyboardButton('pr_PR', callback_data='SetLang_pr_PR'))

			lang_markup = h_keyboard.build(lang_buttons, n_cols=2)
			return bot.edit_message_text(lang.configure_lang % user_id, chat_id, update.message.message_id, reply_markup=lang_markup, parse_mode=ParseMode.HTML)
		elif edit == 'ConfReportChannel':
			'''
			Rebuild configuration menu buttons
			for channel selection
			'''
			report_buttons = []
			report_buttons.append(InlineKeyboardButton(lang.c_go_dashboard, url='https://unifiedban.solutions/'))
			report_buttons.append(InlineKeyboardButton(lang.c_back, callback_data='Back'))
			report_buttons.append(InlineKeyboardButton(lang.c_close, callback_data='CloseMenu'))
			report_markup = h_keyboard.build(report_buttons, n_cols=2)
			return bot.edit_message_text(lang.configure_report % user_id, chat_id, update.message.message_id, reply_markup=report_markup, parse_mode=ParseMode.HTML)
		elif edit == 'CallOperator':
			'''
			Rebuild configuration menu buttons
			for call an operator
			'''
			call_buttons = []
			call_buttons.append(InlineKeyboardButton(lang.c_faq, url='https://unifiedban.solutions/?p=faq'))
			call_buttons.append(InlineKeyboardButton(lang.c_back, callback_data='Back'))
			call_buttons.append(InlineKeyboardButton(lang.c_close, callback_data='CloseMenu'))
			call_markup = h_keyboard.build(call_buttons, n_cols=2)
			logger.report_operators(update, context, lang.report_call_operator % (
				h_user.get_user_name(update),
				update.message.chat.title,
				update.message.chat.username
			))
			return bot.edit_message_text(lang.configure_call % user_id, chat_id, update.message.message_id, reply_markup=call_markup, parse_mode=ParseMode.HTML)
		elif edit == 'Sign':
			'''
			Rebuild configuration menu buttons
			for enabling the dashboard
			'''
			db = sql.Database(update); db.insert_permissions();
			report_buttons = []
			report_buttons.append(InlineKeyboardButton(lang.c_go_dashboard, url='https://unifiedban.solutions/'))
			report_buttons.append(InlineKeyboardButton(lang.c_back, callback_data='Back'))
			report_buttons.append(InlineKeyboardButton(lang.c_close, callback_data='CloseMenu'))
			report_markup = h_keyboard.build(report_buttons, n_cols=2)
			return bot.edit_message_text(lang.configure_sign % user_id, chat_id, update.message.message_id, reply_markup=report_markup, parse_mode=ParseMode.HTML)
		else:
			'''
			Rebuild configuration menu buttons
			with user modifications
			'''
			text = lang.configure % user_id
			text = text+lang.configure_update % datetime.now().strftime("%B-%d-%Y--%I:%M%p")
			return bot.edit_message_text(text, chat_id, update.message.message_id, reply_markup=markup, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)

'''
Update bot settings for group
'''
def update(update, context):
	try:
		query = update.callback_query

		# get group language from config
		lang = h_group.get_language(query)
		
		bot = context.bot
		
		if query.data.startswith("Conf") or query.data.startswith("Close") or query.data.startswith("Set") or query.data.startswith("Back") or query.data.startswith("Call") or query.data.startswith("Sign"):
			if h_chat.is_private(query):
				return False
			else:
				chat_id = query.message.chat_id
				user_id = h_user.get_user_id(query.message.text)
				if str(query.from_user.id) == str(user_id):
					db = sql.Database(query); db.insert_chatoperationslog(query.data)
					# Close menu
					if query.data == 'CloseMenu':
						return bot.edit_message_text(lang.configure_close, chat_id, query.message.message_id)
					# Open group
					elif query.data == 'ConfOpen':
						return bot.edit_message_text(lang.configure_hammer_open, chat_id, query.message.message_id)
					# Back to the menu
					elif query.data == 'Back':
						return init(query, context, True)
					# Back to the menu
					elif query.data == 'CallOperator':
						return init(query, context, 'CallOperator')
					# Change user report channel
					elif query.data == 'ConfReportChannel':
						return init(query, context, 'ConfReportChannel')
					# Change bot language
					elif query.data == 'ConfLang':
						return init(query, context, 'ConfLang')
					# Enable dashboard
					elif query.data == 'Sign':
						return init(query, context, 'Sign')
					# Set bot language
					elif query.data.startswith('SetLang_'):
						db = sql.Database(query); db.update_groups('ConfLang', query.data[8:])
						return init(query, context, True)
					# Other settings
					else:
						# Hammer
						if query.data.startswith('ConfHammer'):
							bot.set_chat_permissions(
								chat_id,
								ChatPermissions(
									can_send_messages=True, 
									can_send_media_messages=False, 
									can_send_polls=False,
									can_send_other_messages=False, 
									can_add_web_page_previews=False,
									can_invite_users=False
								)
							)
							if query.data == 'ConfHammer0':
								# open group
								bot.set_chat_permissions(
									chat_id,
									ChatPermissions(
										can_send_messages=True, 
										can_send_media_messages=True, 
										can_send_polls=True,
										can_send_other_messages=True, 
										can_add_web_page_previews=True,
										can_invite_users=True
									)
								)
								db = sql.Database(query); hammer = db.get_hammer(chat_id)
								db = sql.Database(query); report_channel = db.get_groups()[19]
								if len(hammer) > 0:
									hammer_list = ""
									for h in hammer:
										hammer_list = hammer_list + "- " + h[0] + "\n"
									try:
										bot.send_message(report_channel, lang.report_hammer % hammer_list, parse_mode=ParseMode.HTML)
									except:
										bot.send_message(Params.telegram.ReportChannel.id, lang.report_hammer % hammer_list, parse_mode=ParseMode.HTML)
								else:
									try:
										bot.send_message(report_channel, lang.report_hammer_empty, parse_mode=ParseMode.HTML)
									except:
										bot.send_message(Params.telegram.ReportChannel.id, lang.report_hammer_empty, parse_mode=ParseMode.HTML)
								db = sql.Database(query); db.delete_hammer(chat_id)
							query.data = query.data[:-1]
							db = sql.Database(query); db.update_groups('ConfWelcome', 'IF(ConfWelcome = 0, 1, 0)', switch=True)
							
						db = sql.Database(query); db.update_groups(query.data, 'IF(' + query.data + ' = 0, 1, 0)', switch=True)
						return init(query, context, True)
				else:
					logger.log.error("Lose query")
					return False
	except Exception as e:
		logger.exception(e)
