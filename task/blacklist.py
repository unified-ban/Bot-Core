#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger, sql


def init(update, context, group, lang):
	try:
		bot = context.bot
		
		if group[9] == 1:
			db = sql.Database(update)
			user = db.check_blacklist()
			message = update.message
			chat_id = message.chat_id
			user_obj = message.from_user
			
			if user is True:
				bot.kick_chat_member(chat_id, user_obj.id)
				bot.deleteMessage(chat_id, message.message_id)
				db = sql.Database(update); db.insert_blockedcontent("blacklist")
				return logger.report(update, context, lang.report_blacklist % (
						update.message.chat.title,
						'Blacklisted user',
						update.message.from_user.name,
						update.message.from_user.id
					)
				)
		else:
			return False
	except Exception as e:
		logger.exception(e)