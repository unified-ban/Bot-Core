#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message, chat
from Utils import logger, sql
from Utils.helpers import h_language, h_message
import html

@chat.only_groups
def init(update, context, group, lang):
	try:
		bot = context.bot

		if update.message is not None and update.message.chat_id is not None:
			message = update.message
			chat_id = message.chat_id
			
			if message.new_chat_members is not None or message.group_chat_created is not None:
				
				if message.new_chat_members is not None and len(message.new_chat_members) > 0:
					new_id = message.new_chat_members[0].id
				elif message.group_chat_created is not None:
					new_id = Params.telegram.Bot.id
				
				if new_id == Params.telegram.Bot.id:
					if group is False:
						
						# first time registration
						db = sql.Database(update)
						db.insert_groups()

						try:
							chat_title = message.chat.title
						except:
							chat_title = "Unknow"
						
						return logger.report(update, context, lang.report_registration % (
								chat_title,
								chat_id
							)
						)
					else:
						# already registered
						if group[3] == 0:
							# disabled group
							return bot.leaveChat(chat_id)
		return False
	except Exception as e:
		logger.exception(e)