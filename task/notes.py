#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message
from Utils import logger, sql
from Utils.helpers import h_notes

def init(update, context):
	try:
		bot = context.bot
		
		note = h_notes.is_set(update)
		if note:
			db = sql.Database(update)
			note = db.get_notes(note.lower())
			if note is not None:
				return bot.send_message(update.message.chat_id, note[0], parse_mode=ParseMode.HTML)
		return False
	except Exception as e:
		logger.exception(e)