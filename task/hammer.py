#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger, sql
from Utils.helpers import h_user
import datetime

def init(update, context, group, lang):
	try:
		bot = context.bot
		
		if group[10] == 1 and  0 < len(update.message.new_chat_members):
			# group is closed
			user = update.message.new_chat_members[0]
			db = sql.Database(update); db.insert_hammer()
			chat_id = update.message.chat.id
			message_id = update.message.message_id
			
			bot.deleteMessage(chat_id, message_id)
			return bot.kick_chat_member(chat_id, user.id)
	except Exception as e:
		logger.exception(e)