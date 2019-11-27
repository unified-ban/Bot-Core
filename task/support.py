#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils.helpers import h_message
from Utils import logger, sql

@permissions.is_operator('task_support_init')
def init(update, context, lang):
	try:
		bot = context.bot
		
		db = sql.Database(update)
		message = update.message
		chat_id = message.chat_id
		user = message.from_user
		'''
		validate support session
		'''
		if db.check_session():
			h_message.delete(context, update.message)
			bot.send_message(chat_id, lang.support_text % (message.text, user.name), parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)