#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils import logger, sql
from Utils.helpers import h_group, h_user
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		
		group = db.get_groups()
		
		report_channel = group[19]
		message = update.message
		base_link = "https://t.me/{group}/{id}"
		
		report_text = message.text.split(" ")
		if len(report_text) > 1:
			report_text = report_text[1]
		else:
			report_text = "No message"
		
		if message.chat.username == None:
			message_link = "Private group"
		else:
			message_link = base_link.format(
				group = message.chat.username,
				id = message.message_id
			)
		user = h_user.get_user_name(update)
		
		report = lang.user_report % (
			message.chat.title,
			h_user.get_user_name(update),
			report_text,
			message_link
		)
		bot.send_message(report_channel, report, parse_mode=ParseMode.HTML)
		return bot.send_message(message.chat.id, lang.user_report_sent)
	except Exception as e:
		logger.exception(e)