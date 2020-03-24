#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import InlineKeyboardButton, ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_chat, h_keyboard, h_user, h_group, h_sql
from Utils import logger, sql
from datetime import datetime

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Show feedback menu
'''
@permissions.is_admin('admin_feedback_init')
def init(update, context, edit=False):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		text = update.message.text
		
		if update.message.reply_to_message:
			'''
			Set the text of the feedback from the message 
			that user has mentioned
			'''
			feedback_text = update.message.reply_to_message.text
		else:
			feedback_text = update.message.text[10:]
			
		if feedback_text:
			'''
			Build the feedback buttons for selecting the type
			'''
			buttons = []
			buttons.append(InlineKeyboardButton(lang.f_suggestion, callback_data='FeedbackTypeSuggestion'))	
			buttons.append(InlineKeyboardButton(lang.f_bug, callback_data='FeedbackTypeBug'))	
			buttons.append(InlineKeyboardButton(lang.f_report, callback_data='FeedbackTypeReport'))	
			markup = h_keyboard.build(buttons, n_cols=2)
			
			return bot.send_message(update.message.chat_id, lang.feedback_selection % (
					update.message.from_user.id,
					feedback_text
				), reply_markup=markup, parse_mode=ParseMode.HTML)
		else:
			'''
			The text of the feedback was not provided
			output an error message.
			'''
			return bot.send_message(update.message.chat_id, lang.feedback_no_text)
	except Exception as e:
		logger.exception(e)

'''
Update feedback
'''
def update(update, context):
	try:
		query = update.callback_query
		
		# get group language from config
		lang = h_group.get_language(query)

		bot = context.bot
		
		if query.data.startswith("FeedbackType"):
			chat_id = query.message.chat_id
			feedback_type = query.data.replace("FeedbackType", "")
			text = query.message.text
			text = text.replace(lang.report_feedback_choose, "")
			
			logger.report_operators(query, context, lang.report_feedback % (
				feedback_type,
				h_user.get_user_name(query),
				text
			))
			return bot.edit_message_text(lang.feedback_sent, chat_id, query.message.message_id, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)