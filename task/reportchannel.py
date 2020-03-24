#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger
from Utils.helpers import h_chat
from telegram import ParseMode

def init(update, context, lang):
	try:
		bot = context.bot

		if h_chat.is_private(update):
			if update.message.forward_from_chat is not None:
				chat_id = update.message.chat.id
				channel_id = update.message.forward_from_chat.id
				return bot.send_message(chat_id, lang.reportchannel_setup % channel_id, parse_mode=ParseMode.HTML)
			else: 
				return False
		else:
			return False
	except Exception as e:
		logger.exception(e)