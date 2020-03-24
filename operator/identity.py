#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_group, h_user
from Utils import logger

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Show operator identity
'''
@permissions.is_operator('operator_identity_init')
@message.delete_input
def init(update, context):
	try:
		# get group language from config
		lang = h_group.get_language(update)

		bot = context.bot
		
		message = update.message
		chat_id = message.chat.id
		user = h_user.get_user_name(update)
		
		bot.send_message(chat_id, lang.identity % user)
	except Exception as e:
		logger.exception(e)