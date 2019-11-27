#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from telegram import ParseMode
from Utils.decorators import permissions, message, chat
from Utils.helpers import h_chat, h_group
from Utils import logger

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language

'''
Check bot permissions in group
'''
@permissions.is_admin('admin_delete_init')
@message.delete_input
@chat.only_groups
def init(update, context):
	try:
		# get group language from config
		
		bot = context.bot
		
		chat_id = update.message.chat_id
		bot_user = bot.getChatMember(chat_id, Params.telegram.Bot.id)
		
		can_delete = bot_user.can_delete_messages
		can_ban = bot_user.can_restrict_members
		
		if False in [can_delete, can_ban]:
			bot_status = lang.check_false
		else:
			bot_status = lang.check_true
		
		output_text = lang.check % (str(can_delete), str(can_ban), bot_status)
		return bot.send_message(chat_id, output_text, parse_mode=ParseMode.HTML)
	except Exception as e:
		logger.exception(e)