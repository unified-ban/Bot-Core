#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils import logger, sql
from Utils.helpers import h_group
from Utils.decorators import chat, message
from telegram import ParseMode

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

@message.delete_input
@chat.only_groups
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		db = sql.Database(update)
		
		group = db.get_groups()
		rules_text = group[20]
		
		chat_id = update.message.chat.id
		
		if rules_text is None:
			# rules message is not defined
			return bot.send_message(chat_id, lang.rules, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
		else:
			# rules message defined
			return bot.send_message(chat_id, rules_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
	except Exception as e:
		logger.exception(e)