#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import Params
from Utils.helpers import h_group
from Utils.decorators import permissions

'''
Load language from settings.
Choose your preferred language in Params.settings.
'''
lang = Params.settings.language


@permissions.is_admin('test_message_init')
def init(update, context):
	bot = context.bot
	
	# get group language from config
	lang = h_group.get_language(update)
	return update.message.reply_text(lang.test)