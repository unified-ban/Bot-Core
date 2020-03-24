#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_scam, h_message, h_user
from Utils import logger, sql
from telegram import ChatPermissions


def init(update, context, group, lang):
	try:
		bot = context.bot
		if group[8] == 1:
			row = h_scam.is_phishing(update.message.text)
			
			message = update.message
			user = update.message.from_user
			
			if row == False:
				return False
			else:
				bot.restrict_chat_member(
					message.chat_id,
					user.id,
					ChatPermissions(
						can_send_messages=False, 
						can_send_media_messages=False, 
						can_send_polls=False,
						can_send_other_messages=False, 
						can_add_web_page_previews=False,
						can_invite_users=False
					),
					until_date=datetime.datetime.now() + datetime.timedelta(days=1)
				)
				bot.send_message(message.chat_id, lang.scam_block % 
						h_user.get_user_name(update.message.from_user)
				)
				db = sql.Database(update); db.insert_blockedcontent("scam")
				return logger.report(update, context, lang.report_scam % (
						update.message.chat.title,
						'Phishing attempt',
						row,
						h_user.get_user_name(update.message.from_user),
						update.message.from_user.id
					)
				)
		else:
			return False
	except Exception as e:
		logger.exception(e)