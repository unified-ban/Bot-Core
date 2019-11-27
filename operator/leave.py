#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils import logger

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


'''
Remove bot from chat
'''
@permissions.is_operator('operator_leave_init')
@message.delete_input
def init(update, context):
	try:
		bot = context.bot

		bot.leaveChat(update.message.chat_id)
		return logger.report(update, context, lang.report_leave % (
				update.message.from_user.name,
				update.message.chat_id
			)
		)
	except Exception as e:
		logger.exception(e)