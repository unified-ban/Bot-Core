#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.decorators import permissions, message
from Utils.helpers import h_spam
from Utils import logger, sql

'''
Current methods:
- telegram links in post
- telegram links in user name
- spam recogniser from models
'''
def init(update, context, group, lang):
	try:
		bot = context.bot

		domains = h_spam.get_telegram_domains(update, bool(group[7]))
		update = h_spam.set_correct_user(update)
		actions = [group[13], group[14], group[15]]
		
		'''
		Spam recogniser
		'''
		if group[12] == 1:
			db = sql.Database(update)
			logics = db.get_spamlogics()
			for l in logics:
				if l[2] == "containsWords":
					if h_spam.logic_containsWords(update, l[3]):
						logger.log.info("aa")
						h_spam.perform_group_spam_action(update, context, actions)
						db = sql.Database(update); db.insert_blockedcontent("spamlogic:%s" % l[1])
						return logger.report(update, context, lang.report_spam_logic % (
								update.message.chat.title,
								'Spamlogic detected',
								l[1],
								update.message.from_user.name,
								update.message.from_user.id
							)
						)
				if l[2] == "imageComparison":
					if h_spam.logic_imageComparison(update, context, l[3]):
						logger.log.info("imagecomparison")
						h_spam.perform_group_spam_action(update, context, actions)
						db = sql.Database(update); db.insert_blockedcontent("spamlogic:%s" % l[1])
						return logger.report(update, context, lang.report_spam_logic % (
								update.message.chat.title,
								'Spamlogic detected',
								l[1],
								update.message.from_user.name,
								update.message.from_user.id
							)
						)
			pass
			
		'''
		Telegram links
		'''
		if group[6] == 1:
			db = sql.Database(update)
			for row in domains:
				if h_spam.is_telegram_domain(row):
					if db.check_safe(row[12:]) == False:
						h_spam.perform_group_spam_action(update, context, actions)
						db = sql.Database(update); db.insert_blockedcontent("telegramlink")
						return logger.report(update, context, lang.report_spam % (
								update.message.chat.title,
								'Unsafe Telegram domain',
								row,
								update.message.from_user.name,
								update.message.from_user.id
							)
						)
			
		'''
		Spam username
		'''
		if group[7] == 1:
			'''
			The user name check is already present at the beginning of this 
			file, in the future this function will include other control methods
			'''
			#bot.send_message(update.message.chat_id, 'Antispam (username) ON')
			pass
		
		return False
	except Exception as e:
		logger.exception(e)