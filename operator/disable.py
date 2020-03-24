#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_user
from Utils import logger, sql
from telegram import ParseMode
import psutil, subprocess

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Disable chat and leave bot
'''
@permissions.is_privileged_operator('operator_disable_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		chat_id = update.message.text[9:]
		chat_title = "n/a"
		chat_username = "n/a"
		
		if chat_id == "":
			chat_id = update.message.chat.id
			chat_title = update.message.chat.title
			chat_username = update.message.chat.username if update.message.chat.username else "private"
		
		bot.leaveChat(chat_id)
		
		return logger.report(update, context, lang.report_disable % (
			h_user.get_user_name(update),
			chat_username,
			chat_title,
			chat_id
		))
	except Exception as e:
		logger.exception(e)